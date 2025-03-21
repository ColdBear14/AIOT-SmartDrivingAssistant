import React from 'react'
import styles from '../components/Home/Services.module.css'
import { useState } from 'react'

function Services() {
  const [allServicesChecked, setAllServicesChecked] = useState(true)

  // Danh sách các dịch vụ
  const services = [
    { header: "Distance", text: "Distance between objects" },
    { header: "Air Conditioning", text: "Automatic air conditioning" },
    { header: "Driver monitoring", text: "Check the driver's status" },
    { header: "Slope Detection", text: "Detect the slope of the road" },
    { header: "Smart Headlights", text: "Adjust Light when it's dark" }
  ]

  return (
    <div className="row">
      <div className="col-md-12">
        {/* Nút toggle tổng */}
        <div className={[styles.servicesToggle, 'form-check form-switch mb-3'].join(' ')}>
          <label className={[styles.servicesToggleLabel, "form-check-label"].join(' ')} role='switch' htmlFor="allServicesToggle">
            <h4 className={styles.servicesToggleHeader}>All Services</h4>
            <div className={styles.servicesToggleText}>Toggle all services on/off</div>
          </label>
          <input 
            type="checkbox" 
            className="form-check-input" 
            id="allServicesToggle" 
            checked={allServicesChecked} 
            onChange={() => setAllServicesChecked(!allServicesChecked)}
          />
        </div>

        {/* Hiển thị danh sách dịch vụ */}
        {services.map((service, index) => (
          <div key={index} className={[styles.servicesToggle, 'mb-3'].join(' ')}>
            <div className={styles.servicesToggleLabel}>
              <h4 className={styles.servicesToggleHeader}>{service.header}</h4>
              <div className={styles.servicesToggleText}>{service.text}</div>
            </div>
            {/* Hiển thị trạng thái mà không có nút toggle riêng */}
            <span className="badge bg-primary">{allServicesChecked ? "ON" : "OFF"}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Services