import React from 'react'
import styles from '../components/Home/Services.module.css'
import { useState } from 'react'

function Services() {
  const [distanceChecked, setDistanceChecked] = useState(true)
  const [temperatureChecked, setTemperatureChecked] = useState(true)
  const [driverChecked, setDriverChecked] = useState(true)
  const [slopeChecked, setSlopeChecked] = useState(true)
  const [headlightChecked, setHeadlightChecked] = useState(true)


  return (
    <div className="row">
      <div className="col-md-4">
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="distanceToggle">
            <h4 className={styles.servicesToggleHeader}>Distance</h4>
            <div className={styles.servicesToggleText}>Distance between objects</div>
          </label>
          <input type="checkbox" className="form-check-input" id="distanceToggle" checked={distanceChecked} onChange={() => setDistanceChecked(!distanceChecked)}/>
        </div>
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="temperatureToggle">
            <h4 className={styles.servicesToggleHeader}>Temperature</h4>
            <div className={styles.servicesToggleText}>Auto Adjust temperature</div>
          </label>
          <input type="checkbox" className="form-check-input" id="temperatureToggle" checked={temperatureChecked} onChange={() => setTemperatureChecked(!temperatureChecked)}/>
        </div>
      </div>
      <div className="col-md-4">
      <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="driverToggle">
            <h4 className={styles.servicesToggleHeader}>Driver</h4>
            <div className={styles.servicesToggleText}>Check the driver's status</div>
          </label>
          <input type="checkbox" className="form-check-input" id="driverToggle" checked={driverChecked} onChange={() => setDriverChecked(!driverChecked)}/>
        </div>
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="slopeToggle">
              <h4 className={styles.servicesToggleHeader}>Slope Detection</h4>
            <div className={styles.servicesToggleText}>Detect the slope of the road</div>
          </label>
          <input type="checkbox" className="form-check-input" id="slopeToggle" checked={slopeChecked} onChange={() => setSlopeChecked(!slopeChecked)}/>
        </div>
      </div>
      <div className="col-md-4">
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="headlightToggle">
            <h4 className={styles.servicesToggleHeader}>Smart Headlights</h4>
            <div className={styles.servicesToggleText}>Adjust Light when it's dark</div>
          </label>
          <input type="checkbox" className="form-check-input" id="headlightToggle" checked={headlightChecked} onChange={() => setHeadlightChecked(!headlightChecked)}/>
        </div>
      </div>
    </div>
  )
}

export default Services