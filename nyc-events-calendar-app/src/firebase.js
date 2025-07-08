// Firebase configuration for NYC Events Calendar
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAvjLXZfsqP_lQZ1wMiJTgOVqfnW8rA_CU",
  authDomain: "nyc-events-calendar.firebaseapp.com",
  projectId: "nyc-events-calendar",
  storageBucket: "nyc-events-calendar.firebasestorage.app",
  messagingSenderId: "871281441124",
  appId: "1:871281441124:web:19825764a586bc6ae02271"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
const db = getFirestore(app);

export { db }; 