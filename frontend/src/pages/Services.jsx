import React from 'react';

import axios from 'axios';

import styles from '../components/Home/Services.module.css';
import { useContext } from 'react';
import { UserContext } from '../hooks/UserContext.jsx';
import { IOTServices } from '../utils/IOTServices.jsx';

function Services() {
  const { servicesState, setServicesState } = useContext(UserContext);

  const serviceStates = {
    auto: "auto",
    manual: "manual",
    on: "on",
    off: "off"
  }

  const safeServicesState = servicesState || Object.fromEntries(
    Object.keys(IOTServices).map(key => [key, true])
  );

  const handleToggleChange = (service, value) => {
    const newState = { ...safeServicesState, [service]: value };
    setServicesState(newState);
  };

  const handleSaveChanges = async (e) => {
    e.preventDefault();
    
    try {
      const response = await axios.patch(`${import.meta.env.VITE_SERVER_URL}/iot/config`, servicesState, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response) {
        console.log('Services updated successfully: ', response);

        // TODO: handle store services
      }
    } catch (error) {
      if (error.response.status === 401) {
        // TODO: handle unauthorized error

      } else {
        // TODO: handle internal server error

      }
    }
  };

  return (
    <div className="row">
      <div className="col-md-4">
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="distanceToggle">
            <h4 className={styles.servicesToggleHeader}>Distance</h4>
            <div className={styles.servicesToggleText}>Distance between objects</div>
          </label>
          <input
            type="checkbox"
            className="form-check-input"
            id="distanceToggle"
            checked={safeServicesState.distance}
            onChange={() => handleToggleChange('distance', !safeServicesState.dist_service)}
          />
        </div>
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="temperatureToggle">
            <h4 className={styles.servicesToggleHeader}>Air Conditioning</h4>
            <div className={styles.servicesToggleText}>Automatic air conditioning</div>
          </label>
          <input
            type="checkbox"
            className="form-check-input"
            id="temperatureToggle"
            checked={safeServicesState.temperature}
            onChange={() => handleToggleChange('temperature', !safeServicesState.temp_service)}
          />
        </div>
      </div>
      <div className="col-md-4">
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="driverToggle">
            <h4 className={styles.servicesToggleHeader}>Driver monitoring</h4>
            <div className={styles.servicesToggleText}>Check the driver's status</div>
          </label>
          <input
            type="checkbox"
            className="form-check-input"
            id="driverToggle"
            checked={safeServicesState.driver}
            onChange={() => handleToggleChange('driver', !safeServicesState.driver)}
          />
        </div>
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="slopeToggle">
            <h4 className={styles.servicesToggleHeader}>Slope Detection</h4>
            <div className={styles.servicesToggleText}>Detect the slope of the road</div>
          </label>
          <input
            type="checkbox"
            className="form-check-input"
            id="slopeToggle"
            checked={safeServicesState.slope}
            onChange={() => handleToggleChange('slope', !safeServicesState.slope)}
          />
        </div>
      </div>
      <div className="col-md-4">
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="headlightToggle">
            <h4 className={styles.servicesToggleHeader}>Smart Headlights</h4>
            <div className={styles.servicesToggleText}>Adjust Light when it's dark</div>
          </label>
          <input
            type="checkbox"
            className="form-check-input"
            id="headlightToggle"
            checked={safeServicesState.headlight}
            onChange={() => handleToggleChange('headlight', !safeServicesState.lux_service)}
          />
        </div>
      </div>
    </div>
  );
}

export default Services;