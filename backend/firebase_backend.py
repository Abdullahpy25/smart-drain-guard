import json
import time
import urllib.request
import urllib.error

from risk_score import calculate_risk
from telegram_alert import send_telegram_alert


FIREBASE_URL = (
    "https://smart-drain-guard-default-rtdb."
    "asia-southeast1.firebasedatabase.app"
)

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=12.9716"
    "&longitude=77.5946"
    "&hourly=precipitation_probability"
    "&forecast_hours=6"
    "&timezone=Asia%2FKolkata"
)

CHECK_INTERVAL = 10 # 10 seconds


def get_firebase_data():
    url = f"{FIREBASE_URL}/drains.json"

    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode())


def get_rain_score():
    with urllib.request.urlopen(OPEN_METEO_URL, timeout=10) as response:
        data = json.loads(response.read().decode())

    rain_probabilities = data["hourly"]["precipitation_probability"]

    return max(rain_probabilities)


def update_firebase(drain_id, risk_score, status):
    url = f"{FIREBASE_URL}/drains/{drain_id}.json"

    data = {
        "risk_score": risk_score,
        "status": status
    }

    payload = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="PATCH"
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode())


def update_alert_status(drain_id, status):
    url = f"{FIREBASE_URL}/drains/{drain_id}.json"

    data = {
        "last_alert_status": status
    }

    payload = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="PATCH"
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode())


def process_once(last_rain_score):
    print("\n--- New monitoring cycle ---")

    try:
        print("Reading Firebase...")
        drains = get_firebase_data()
    except Exception as error:
        print(f"Firebase error: {error}")
        return last_rain_score

    try:
        print("Fetching Bengaluru rain forecast...")
        rain_score = get_rain_score()
        print(f"Rain score: {rain_score}")

    except Exception as error:
        print(f"Weather API error: {error}")

        if last_rain_score is not None:
            print(
                f"Using last known rain score: "
                f"{last_rain_score}"
            )
            rain_score = last_rain_score
        else:
            print("No previous rain score available.")
            return last_rain_score

    for drain_id, drain_data in drains.items():

        try:
            blockage = drain_data.get("blockage", 0)

            previous_status = drain_data.get(
                "last_alert_status",
                "GREEN"
            )

            risk_score, status = calculate_risk(
                blockage,
                rain_score
            )

            print(
                f"{drain_id}: "
                f"blockage={blockage}, "
                f"risk={risk_score}, "
                f"status={status}"
            )

            update_firebase(
                drain_id,
                risk_score,
                status
            )

            if status == "RED" and previous_status != "RED":
                print(
                    "RED status detected. "
                    "Sending Telegram alert..."
                )

                try:
                    send_telegram_alert(
                        drain_id,
                        blockage,
                        risk_score
                    )
                    print("Telegram alert sent.")

                except Exception as error:
                    print(
                        f"Telegram error: {error}"
                    )

            update_alert_status(
                drain_id,
                status
            )

        except Exception as error:
            print(
                f"Error processing {drain_id}: "
                f"{error}"
            )

    print("Monitoring cycle complete.")

    return rain_score


def main():
    print("===================================")
    print(" SMART DRAIN GUARD BACKEND")
    print(" Automatic monitoring started")
    print(" Check interval: 2 minutes")
    print("===================================")

    last_rain_score = None

    while True:

        try:
            last_rain_score = process_once(
                last_rain_score
            )

        except KeyboardInterrupt:
            print("\nBackend stopped by user.")
            break

        except Exception as error:
            print(
                f"Unexpected error: {error}"
            )

        print(
            f"\nWaiting {CHECK_INTERVAL} seconds..."
        )

        try:
            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\nBackend stopped by user.")
            break


if __name__ == "__main__":
    main()
