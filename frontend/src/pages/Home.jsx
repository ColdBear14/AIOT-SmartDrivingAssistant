import React, { useState, useEffect } from 'react';
import styles from '../components/Home/Home.module.css'

const Home = () => {

  return (
    <>

      <div className='row'>
        {/* Distance Sensor Panel */}
        <div className="col-md mb-3">
          <div className="p-4 shadow bg-white rounded">
            <h4 className="mb-2">Air conditioning</h4>
            <div className='mb-2'>
              <p className='mb-1 small text-body-tertiary'>Temperature</p>
              {/* variable temperature */}
              <p className="fw-bold fs-2 mb-1">25.3°C</p>
            </div>
            <div className='mb-2'>
              <p className='mb-1 small text-body-tertiary'>Humidity</p>
              {/* variable humidity */}
              <p className="fw-bold fs-2 mb-1">53.2%</p>
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
          <div className="p-4 shadow bg-white rounded">
            <h4 className="mb-2">Driver monitoring</h4>
            <div className='mb-2 d-flex align-items-center'>
              <div className="rounded-circle me-2 bg-success" style={{width: '16px', height:'16px'}}></div>
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
                onChange={() => {}}
                className='mx-2 flex-grow-1' 
                />
                <span className='ms-2 small'>High</span>
              </div>
            </div>
            <div className='mb-2 bg-light rounded small'>
              <p className='fw-medium mb-1 mt-3'>Recent announcements:</p>
                  <ul className="ms-3 list-unstyled mb-0">
                    <li className="text-success mb-1">✓ Người lái tỉnh táo</li>
                    <li className="text-muted mb-1">14:30 - Phát hiện dấu hiệu mệt mỏi</li>
                    <li className="text-muted">12:15 - Phát hiện mất tập trung</li>
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
                <p className="fw-bold fs-2 mb-1">103 cm</p>
                {/* variable warning */}
                <button disabled className={`rounded btn text-white bg-success px-3 py-1`}>An toàn</button>
              </div>
              <div className={`${styles.distanceSensorIcon} rounded-5`}>
                <i className="fa-solid fa-bolt"></i>
              </div>
            </div>
          </div>
          <div className="p-4 mb-3 shadow bg-white rounded">
            <h4 className="mb-1">Slope Detection</h4>
            {/* variable Slope */}
            <p className="fw-bold fs-2 mb-1">-0.4°</p>
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
                  style={{ width: '80%' }}
                  aria-valuemin="0"
                  aria-valuemax="100"></div>
              </div>
              <p className="mt-1 mb-0 text-end small">80%</p>
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