import React from 'react';
import styles from '../components/Home/Services.module.css';
import { useContext } from 'react';
import { UserContext } from '../hooks/UserContext.jsx';
import axios from 'axios';

function Services() {
  const { servicesState, setServicesState } = useContext(UserContext);

  const handleToggleChange = async (service, value) => {
    const newState = { ...servicesState, [service]: value };
    setServicesState(newState);

    // Gửi trạng thái mới về backend
    try {
      await axios.post(`${import.meta.env.VITE_SERVER_URL}/services/update`, newState, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Services state updated on backend:', newState);
    } catch (error) {
      console.error('Error updating services state:', error);
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
            checked={servicesState.distance}
            onChange={() => handleToggleChange('distance', !servicesState.distance)}
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
            checked={servicesState.temperature}
            onChange={() => handleToggleChange('temperature', !servicesState.temperature)}
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
            checked={servicesState.driver}
            onChange={() => handleToggleChange('driver', !servicesState.driver)}
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
            checked={servicesState.slope}
            onChange={() => handleToggleChange('slope', !servicesState.slope)}
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
            checked={servicesState.headlight}
            onChange={() => handleToggleChange('headlight', !servicesState.headlight)}
          />
        </div>
      </div>
    </div>
  );
}

export default Services;