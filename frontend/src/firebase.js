// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD91HKGsO4xGrbNDBFDBS9lhM6fTfL44nM",
  authDomain: "smart-drain-guard.firebaseapp.com",
  databaseURL: "https://smart-drain-guard-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "smart-drain-guard",
  storageBucket: "smart-drain-guard.firebasestorage.app",
  messagingSenderId: "1001033813892",
  appId: "1:1001033813892:web:2f8a71a22112dc479957d1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const database = getDatabase(app);