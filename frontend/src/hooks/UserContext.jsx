import { createContext, useState } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [sensorData, setSensorData] = useState(null);

  return (
    <UserContext.Provider value={{ user, setUser, sessionId, setSessionId, sensorData, setSensorData }}>
      {children}
    </UserContext.Provider>
  );
};