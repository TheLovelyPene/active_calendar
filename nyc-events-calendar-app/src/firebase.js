// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAvjLXZfsqP_lQZ1wMiJTgOVqfnW8rA_CU",
  authDomain: "nyc-events-calendar.firebaseapp.com",
  projectId: "nyc-events-calendar",
  storageBucket: "nyc-events-calendar.appspot.com",
  messagingSenderId: "871281441124",
  appId: "1:871281441124:web:19825764a586bc6ae02271"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);