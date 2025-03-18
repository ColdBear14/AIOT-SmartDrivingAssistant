import React from 'react'
import styles from '../components/Home/Services.module.css'

function Services() {
  return (
    <div className="row">
      <div className="col-md-4">
        <div className={[styles.servicesToggle, 'form-check form-switch'].join(' ')}>
          <label className="form-check-label" role='switch' htmlFor="distanceToggle">
            <h4 className={styles.servicesToggleHeader}>Distance</h4>
            <p className={styles.servicesToggleText}>Distance between objects</p>
          </label>
          <input type="checkbox" className="form-check-input" id="distanceToggle" />
        </div>
      </div>
      <div className="col-md-4">
        <div className="services-toggle"></div>
      </div>
      <div className="col-md-4">
        <div className="services-toggle"></div>
      </div>
    </div>
  )
}

export default Services