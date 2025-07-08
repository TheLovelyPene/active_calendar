import { collection, getDocs, query, where, orderBy, limit } from "firebase/firestore";
import { db } from "../firebase";

// Service to fetch events from Firestore
export const eventService = {
  // Get all events
  async getAllEvents() {
    try {
      const eventsRef = collection(db, "events");
      const q = query(eventsRef, orderBy("date", "asc"));
      const querySnapshot = await getDocs(q);
      
      const events = [];
      querySnapshot.forEach((doc) => {
        events.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return events;
    } catch (error) {
      console.error("Error fetching events:", error);
      return [];
    }
  },

  // Get events by borough
  async getEventsByBorough(borough) {
    try {
      const eventsRef = collection(db, "events");
      const q = query(
        eventsRef, 
        where("borough", "==", borough),
        orderBy("date", "asc")
      );
      const querySnapshot = await getDocs(q);
      
      const events = [];
      querySnapshot.forEach((doc) => {
        events.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return events;
    } catch (error) {
      console.error("Error fetching events by borough:", error);
      return [];
    }
  },

  // Get events by date range
  async getEventsByDateRange(startDate, endDate) {
    try {
      const eventsRef = collection(db, "events");
      const q = query(
        eventsRef,
        where("date", ">=", startDate),
        where("date", "<=", endDate),
        orderBy("date", "asc")
      );
      const querySnapshot = await getDocs(q);
      
      const events = [];
      querySnapshot.forEach((doc) => {
        events.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return events;
    } catch (error) {
      console.error("Error fetching events by date range:", error);
      return [];
    }
  },

  // Get recent events (last 10)
  async getRecentEvents() {
    try {
      const eventsRef = collection(db, "events");
      const q = query(
        eventsRef,
        orderBy("scraped_at", "desc"),
        limit(10)
      );
      const querySnapshot = await getDocs(q);
      
      const events = [];
      querySnapshot.forEach((doc) => {
        events.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return events;
    } catch (error) {
      console.error("Error fetching recent events:", error);
      return [];
    }
  },

  // Get free events only
  async getFreeEvents() {
    try {
      const eventsRef = collection(db, "events");
      const q = query(
        eventsRef,
        where("is_free", "==", true),
        orderBy("date", "asc")
      );
      const querySnapshot = await getDocs(q);
      
      const events = [];
      querySnapshot.forEach((doc) => {
        events.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return events;
    } catch (error) {
      console.error("Error fetching free events:", error);
      return [];
    }
  }
}; 