import { useNavigate } from 'react-router-dom';
import { useContext } from 'react';

import axios from 'axios';
import Cookies from 'js-cookie';

import { UserContext } from '../../hooks/UserContext.jsx';

function LoginForm({ showSignUp }) {
  const navigate = useNavigate();
  const { setSessionId } = useContext(UserContext);

  const handleLogin = (e) => {
    e.preventDefault();

    const username = document.getElementById('username_log').value;
    const password = document.getElementById('password_log').value;
    
    if (username && password) {
    } else {
      alert('Please enter username and password');
    }

    const request = {
      username: username,
      password: password
    }
    
    axios.patch(`${process.env.REACT_APP_SERVER_URL}/auth/login`, request, 
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    )
      .then(response => {
        if (response.status === 200) {
          const session_id = Cookies.get('session_id');
          if (session_id) {
            setSessionId(session_id);
          }
          console.log(`Login successful with response: ${response} and session_id: ${session_id}`);
          navigate('/home');
        } else {
          alert('Login failed');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during login');
      });
  };

  return (
    <div id="login-form" className="form-container bg-white text-center">
      <h2 className="primary-color mb-4 auth-title">Login</h2>
      <form onSubmit={handleLogin}>
        <div className="mb-3 input-icon-container input-group">
          <label htmlFor="username_log" className="input-group-text w-40px">
            <i className="fa-solid fa-user"></i>
          </label>
          <input
            type="text"
            id="username_log"
            className="form-control"
            placeholder="Username"
          />
        </div>
        <div className="mb-3 input-icon-container input-group">
          <label htmlFor="password_log" className="input-group-text w-40px">
            <i className="fa-solid fa-lock"></i>
          </label>
          <input
            type="password"
            id="password_log"
            className="form-control"
            placeholder="Password"
          />
        </div>
        <button type="submit" className="btn-login w-100 mb-4">
          Login
        </button>
        <a href="#" className="text-decoration-none toggle-auth text-primary" onClick={showSignUp}>
          Don't have an account? Sign up
        </a>
      </form>
    </div>
  );
}

export default LoginForm;