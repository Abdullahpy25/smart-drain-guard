import json
import urllib.request
from risk_score import calculate_risk


FIREBASE_URL = (
    "https://smart-drain-guard-default-rtdb."
    "asia-southeast1.firebasedatabase.app"
)

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=12.9716"
    "&longitude=77.5946"
    "&hourly=precipitation_probability"
    "&forecast_hours=1"
    "&timezone=Asia%2FKolkata"
)


def get_firebase_data():
    url = f"{FIREBASE_URL}/drains.json"

    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode())


def get_rain_score():
    with urllib.request.urlopen(OPEN_METEO_URL, timeout=10) as response:
        data = json.loads(response.read().decode())

    rain_probability = data["hourly"]["precipitation_probability"][0]

    return rain_probability


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


def main():
    print("Reading Firebase...")
    drains = get_firebase_data()

    print("Fetching Bengaluru rain forecast...")
    rain_score = get_rain_score()

    print(f"Rain score: {rain_score}")

    for drain_id, drain_data in drains.items():

        blockage = drain_data.get("blockage", 0)

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

    print("Firebase update complete.")


if __name__ == "__main__":
    main()