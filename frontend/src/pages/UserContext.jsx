import { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [sessionId, setSessionId] = useState(null);
  const [sensorData, setSensorData] = useState([]);
  const [servicesState, setServicesState] = useState({
    distance: true,
    temperature: true,
    driver: true,
    slope: true,
    headlight: true,
  });

  useEffect(() => {
    const fetchServicesState = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_SERVER_URL}/services/state`, {
          withCredentials: true,
          headers: { 'Content-Type': 'application/json' },
        });
        setServicesState(response.data);
      } catch (error) {
        console.error('Error fetching services state:', error);
      }
    };
    fetchServicesState();
  }, []);

  return (
    <UserContext.Provider value={{ sessionId, setSessionId, sensorData, setSensorData, servicesState, setServicesState }}>
      {children}
    </UserContext.Provider>
  );
};