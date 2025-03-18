import React from 'react'
import styles from '../components/Home/Services.module.css'
import { useState } from 'react'

function Services() {
  const [checked, setChecked] = useState(true)
  return (
    <div className="row">
      <div className="col-md-4">
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <input type="checkbox" className="form-check-input" id="distanceToggle" checked={checked} onChange={() => setChecked(!checked)}/>
          <label className="form-check-label" role='switch' htmlFor="distanceToggle">
            <h4 className={styles.servicesToggleHeader}>Distance</h4>
            <div className={styles.servicesToggleText}>Distance between objects</div>
          </label>
        </div>
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <input type="checkbox" className="form-check-input" id="temperatureToggle" checked={checked} onChange={() => setChecked(!checked)}/>
          <label className="form-check-label" role='switch' htmlFor="temperatureToggle">
            <h4 className={styles.servicesToggleHeader}>Temperature</h4>
            <div className={styles.servicesToggleText}>Auto Adjust temperature</div>
          </label>
        </div>
      </div>
      <div className="col-md-4">
      <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <input type="checkbox" className="form-check-input" id="driverToggle" checked={checked} onChange={() => setChecked(!checked)}/>
          <label className="form-check-label" role='switch' htmlFor="driverToggle">
            <h4 className={styles.servicesToggleHeader}>Driver</h4>
            <div className={styles.servicesToggleText}>Check the driver's status</div>
          </label>
        </div>
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <input type="checkbox" className="form-check-input" id="slopeToggle" checked={checked} onChange={() => setChecked(!checked)}/>
          <label className="form-check-label" role='switch' htmlFor="slopeToggle">
            <h4 className={styles.servicesToggleHeader}>Slope Detection</h4>
            <div className={styles.servicesToggleText}>Detect the slope of the road</div>
          </label>
        </div>
      </div>
      <div className="col-md-4">
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <input type="checkbox" className="form-check-input" id="headlightToggle" checked={checked} onChange={() => setChecked(!checked)}/>
          <label className="form-check-label" role='switch' htmlFor="headlightToggle">
            <h4 className={styles.servicesToggleHeader}>Smart Headlights</h4>
            <div className={styles.servicesToggleText}>Adjust Light when it's dark</div>
          </label>
        </div>
      </div>
    </div>
  )
}

export default Services