import React, { useState, useEffect } from 'react';
import styles from '../components/Home/Home.module.css'

import axios from 'axios';
import { useContext } from 'react';
import { UserContext } from '../hooks/UserContext.jsx';

const Home = () => {
  const [data, setData] = useState({
    distance: 120, // cm
    temperature: 28, // Celsius
    humidity: 65, // Percentage
    lightLevel: 75, // Percentage
    incline: 2, // Degrees
    headlightsMode: "Auto", // Auto, Manual, Off
    headlightsBrightness: 2, // 1-4 (Dim, Low, Medium, High)
    driverStatus: "Alert", // Alert, Tired, Distracted
    airConditioner: {
      status: "Auto",
      temperature: 22,
    }
  });
  // Tích hợp APT
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const { sessionId, sensorData, setSensorData } = useContext(UserContext);

  const handleGetData = async () => {
    setLoading(true);
    setError(null);
    try {
      const requestPayload = {
        sensor_type: 'temp',
        amt: 2
      };

      const response = await axios.get('http://127.0.0.1:8000/iot/all_data', 
        {
          withCredentials: true
        }
      );

      setSensorData(response.data);
      console.log("Dữ liệu tải về:", response.data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  // simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      handleGetData();

      setData(prevData => ({
        ...prevData,
        distance: Math.max(20, prevData.distance + Math.floor(Math.random() * 11) - 5),
        temperature: Math.max(0, Math.min(40, prevData.temperature + (Math.random() - 0.5))),
        humidity: Math.max(30, Math.min(90, prevData.humidity + (Math.random() - 0.5) * 2)),
        headlightsBrightness: Math.max(0, Math.min(100, prevData.lightLevel + (Math.random() - 0.5) * 5)),
        incline: Math.max(-10, Math.min(10, prevData.incline + (Math.random() - 0.5))),
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  // Distance warning indicator
  const getDistanceWarning = () => {
    if (data.distance < 50) return { class: "bg-danger", message: "Danger" };
    if (data.distance < 100) return { class: "bg-warning", message: "Warning" };
    return { class: "bg-success", message: "Safe" };
  };

  const distanceWarning = getDistanceWarning();


  return (
    <>

      <div className='row'>
        {/* Distance Sensor Panel */}
        <div className="col-md mb-3">
          <div className={[styles.panel, `p-4 shadow bg-white rounded`].join(" ")}>
            <h4 className="mb-2">Air conditioning</h4>
            <div className='mb-2'>
              <p className='mb-1 small text-body-tertiary'>Temperature</p>
              {/* variable temperature */}
              <p className="fw-bold fs-2 mb-1">{data.temperature.toFixed(1)}°C</p>
            </div>
            <div className='mb-2'>
              <p className='mb-1 small text-body-tertiary'>Humidity</p>
              {/* variable humidity */}
              <p className="fw-bold fs-2 mb-1">{data.humidity.toFixed(1)}</p>
            </div>
            <div className='mb-2'>
              <p className='mb-2 small text-body-tertiary'>Air conditioning</p>
              {/* variable air conditioning */}
              <div className='d-flex flex-wrap'>
                {/* variable warning */}
                <button className={`rounded btn text-white bg-primary me-2 mb-2 px-3 py-1`}>Auto</button>
                <button className={`rounded btn text-white bg-secondary me-2 mb-2 px-3 py-1`}>Manual</button>
                <button className={`rounded btn mb-2 text-white bg-secondary px-3 py-1`}>Off</button>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md mb-3">
          <div className={[styles.panel, `p-4 shadow bg-white rounded`].join(" ")}>
            <h4 className="mb-2">Driver monitoring</h4>
            <div className='mb-2 d-flex align-items-center'>
              <div className="rounded-circle me-2 bg-success" style={{ width: '16px', height: '16px' }}></div>
              <p className='mb-0 fw-bold fs-4'>Conscious</p>
            </div>
            <div className='mb-2'>
              <p className='mb-1 small text-body-tertiary'>Sleepiness detection sensitivity</p>
              {/* variable humidity */}
              <div className='d-flex align-items-center'>
                <span className='me-2 small'>Low</span>
                <input
                  type='range'
                  min='0'
                  max='10'
                  value='3'
                  onChange={() => { }}
                  className='mx-2 flex-grow-1'
                />
                <span className='ms-2 small'>High</span>
              </div>
            </div>
            <div className='mb-2 bg-light rounded small'>
              <p className='fw-medium mb-1 mt-3'>Recent announcements:</p>
              <ul className="ms-3 list-unstyled mb-0">
                <li className="text-success mb-1">✓ Sober driver</li>
                <li className="text-muted mb-1">14:30 - Detect signs of fatigue</li>
                <li className="text-muted">12:15 - Distraction Detection</li>
              </ul>
            </div>
          </div>
        </div>
        <div className="col-md col-md-4 mb-3">
          <div className="p-4 mb-3 shadow bg-white rounded">
            <h4 className="mb-1">Distance Sensor</h4>
            <div className="d-flex justify-content-between align-items-center">
              <div>
                {/* variable distance */}
                <p className="fw-bold fs-2 mb-1">{data.distance} cm</p>
                {/* variable warning */}
                <button disabled className={`rounded btn text-white bg-success px-3 py-1 ${distanceWarning.class}`}>{distanceWarning.message}</button>
              </div>
              <div className={`${styles.distanceSensorIcon} rounded-5`}>
                <i className="fa-solid fa-bolt"></i>
              </div>
            </div>
          </div>
          <div className="p-4 mb-3 shadow bg-white rounded">
            <h4 className="mb-1">Slope Detection</h4>
            {/* variable Slope */}
            <p className="fw-bold fs-2 mb-1">{data.incline.toFixed(1)}°</p>
            <p className='mb-0 small text-body-tertiary'>Flat terrain</p>
          </div>
        </div>
      </div>
      <div className='row'>
        <div className='col-md col-md-6 mb-3'>
          <div className="p-4 shadow bg-white rounded">
            <h4 className="mb-2">Smart Headlights</h4>
            <div>
              <p className='mb-2 small text-body-tertiary'>Ambient light intensity</p>
              <div className="progress">
                <div className="progress-bar bg-primary"
                  role="progressbar"
                  // variable ambient light intensity
                  style={{ width: `${data.lightLevel}%` }}
                  aria-valuemin="0"
                  aria-valuemax="100"></div>
              </div>
              <p className="mt-1 mb-0 text-end small">{data.lightLevel}%</p>
              <div className='mt-1'>
                <p className='mb-2 small text-body-tertiary'>Headlight mode</p>
                {/* variable air conditioning */}
                <div className='d-flex flex-wrap'>
                  {/* variable warning */}
                  <button className={`rounded btn text-white bg-primary me-2 mb-2 px-3 py-1`}>Auto</button>
                  <button className={`rounded btn text-white bg-secondary me-2 mb-2 px-3 py-1`}>Manual</button>
                  <button className={`rounded btn mb-2 text-white bg-secondary px-3 py-1`}>Off</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;