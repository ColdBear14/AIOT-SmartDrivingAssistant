import React, { useState, useEffect } from 'react';
import styles from '../components/Home/Home.module.css';
import axios from 'axios';
import { useContext } from 'react';
import { UserContext } from '../hooks/UserContext.jsx';

const Home = () => {
  const { sensorData, setSensorData, servicesState } = useContext(UserContext);
  const [data, setData] = useState({
    distance: 0,
    temperature: 0,
    humidity: 0,
    lightLevel: 0,
    incline: 0,
    headlightsMode: "Auto",
    headlightsBrightness: 0,
    driverStatus: "Alert",
    airConditioner: { status: "Auto", temperature: 0 },
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Kiểm tra an toàn để tránh lỗi undefined
  const safeServicesState = servicesState || {
    distance: true,
    temperature: true,
    driver: true,
    slope: true,
    headlight: true,
  };

  const handleGetData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${import.meta.env.VITE_SERVER_URL}/iot/all_data`, {
        withCredentials: true,
        headers: { 'Content-Type': 'application/json' },
      });
      const sensorList = response.data.slice(0, 10);
      sensorList.forEach(sensor => {
        const value = parseFloat(sensor.value);
        let type = sensor.sensor_type.toString().toLowerCase().replace(/\s+|\W+/g, '');
        switch (type) {
          case 'temp':
            setData((prev) => ({ ...prev, temperature: value }));
            break;
          case 'humid':
            setData((prev) => ({ ...prev, humidity: value }));
            break;
          case 'dis':
            setData((prev) => ({ ...prev, distance: value }));
            break;
          case 'lux':
            setData((prev) => ({ ...prev, lightLevel: value }));
            break;
          default:
            break;
        }
      });
      setSensorData(sensorList);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleGetData();
    const interval = setInterval(handleGetData, 2000);
    return () => clearInterval(interval);
  }, []);

  const getDistanceWarning = (distance) => {
    if (distance < 50) return { class: "bg-danger", message: "Danger" };
    if (distance < 100) return { class: "bg-warning", message: "Warning" };
    return { class: "bg-success", message: "Safe" };
  };

  const distanceWarning = getDistanceWarning(data.distance);

  return (
    <>
      <div className='row'>
        {safeServicesState.temperature && (
          <div className="col-md mb-3">
            <div className={[styles.panel, `p-4 shadow bg-white rounded`].join(" ")}>
              <h4 className="mb-2">Air conditioning</h4>
              <div className='mb-2'>
                <p className='mb-1 small text-body-tertiary'>Temperature</p>
                <p className="fw-bold fs-2 mb-1">{data.temperature?.toFixed(1)}°C</p>
              </div>
              <div className='mb-2'>
                <p className='mb-1 small text-body-tertiary'>Humidity</p>
                <p className="fw-bold fs-2 mb-1">{data.humidity?.toFixed(1)}%</p>
              </div>
              <div className='mb-2'>
                <p className='mb-2 small text-body-tertiary'>Air conditioning</p>
                <div className='d-flex flex-wrap'>
                  <button className={`rounded btn text-white ${data.airConditioner?.status === 'Auto' ? 'bg-primary' : 'bg-secondary'} me-2 mb-2 px-3 py-1`}>Auto</button>
                  <button className={`rounded btn text-white ${data.airConditioner?.status === 'Manual' ? 'bg-primary' : 'bg-secondary'} me-2 mb-2 px-3 py-1`}>Manual</button>
                  <button className={`rounded btn text-white ${data.airConditioner?.status === 'Off' ? 'bg-primary' : 'bg-secondary'} mb-2 px-3 py-1`}>Off</button>
                </div>
              </div>
            </div>
          </div>
        )}

        {safeServicesState.driver && (
          <div className="col-md mb-3">
            <div className={[styles.panel, `p-4 shadow bg-white rounded`].join(" ")}>
              <h4 className="mb-2">Driver monitoring</h4>
              <div className='mb-2 d-flex align-items-center'>
                <div className="rounded-circle me-2 bg-success" style={{ width: '16px', height: '16px' }}></div>
                <p className='mb-0 fw-bold fs-4'>{data.driverStatus}</p>
              </div>
              <div className='mb-2'>
                <p className='mb-1 small text-body-tertiary'>Sleepiness detection sensitivity</p>
                <div className='d-flex align-items-center'>
                  <span className='me-2 small'>Low</span>
                  <input type='range' min='0' max='10' value='3' onChange={() => {}} className='mx-2 flex-grow-1' />
                  <span className='ms-2 small'>High</span>
                </div>
              </div>
              <div className='mb-2 bg-light rounded small'>
                <p className='fw-medium mb-1 mt-3'>Recent announcements:</p>
                <ul className="ms-3 list-unstyled mb-0">
                  {sensorData && sensorData.slice(0, 3).map((sensor, index) => (
                    <li key={index} className="text-muted mb-1">
                      {new Date(sensor.timestamp).toLocaleTimeString()} - {sensor.sensor_type}: {sensor.value}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {(safeServicesState.distance || safeServicesState.slope) && (
          <div className="col-md col-md-4 mb-3">
            {safeServicesState.distance && (
              <div className="p-4 mb-3 shadow bg-white rounded">
                <h4 className="mb-1">Distance Sensor</h4>
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <p className="fw-bold fs-2 mb-1">{data.distance} cm</p>
                    <button disabled className={`rounded btn text-white ${distanceWarning.class} px-3 py-1`}>
                      {distanceWarning.message}
                    </button>
                  </div>
                  <div className={`${styles.distanceSensorIcon} rounded-5`}>
                    <i className="fa-solid fa-bolt"></i>
                  </div>
                </div>
              </div>
            )}
            {safeServicesState.slope && (
              <div className="p-4 mb-3 shadow bg-white rounded">
                <h4 className="mb-1">Slope Detection</h4>
                <p className="fw-bold fs-2 mb-1">{data.incline?.toFixed(1)}°</p>
                <p className='mb-0 small text-body-tertiary'>Flat terrain</p>
              </div>
            )}
          </div>
        )}
      </div>

      {safeServicesState.headlight && (
        <div className='row'>
          <div className='col-md col-md-6 mb-3'>
            <div className="p-4 shadow bg-white rounded">
              <h4 className="mb-2">Smart Headlights</h4>
              <div>
                <p className='mb-2 small text-body-tertiary'>Ambient light intensity</p>
                <div className="progress">
                  <div
                    className="progress-bar bg-primary"
                    role="progressbar"
                    style={{ width: `${data.lightLevel}%` }}
                    aria-valuemin="0"
                    aria-valuemax="100"
                  ></div>
                </div>
                <p className="mt-1 mb-0 text-end small">{data.lightLevel}%</p>
                <div className='mt-1'>
                  <p className='mb-2 small text-body-tertiary'>Headlight mode</p>
                  <div className='d-flex flex-wrap'>
                    <button className={`rounded btn text-white ${data.headlightsMode === 'Auto' ? 'bg-primary' : 'bg-secondary'} me-2 mb-2 px-3 py-1`}>Auto</button>
                    <button className={`rounded btn text-white ${data.headlightsMode === 'Manual' ? 'bg-primary' : 'bg-secondary'} me-2 mb-2 px-3 py-1`}>Manual</button>
                    <button className={`rounded btn text-white ${data.headlightsMode === 'Off' ? 'bg-primary' : 'bg-secondary'} mb-2 px-3 py-1`}>Off</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Home;