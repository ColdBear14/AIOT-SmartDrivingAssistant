import { useNavigate } from 'react-router-dom';

function LoginForm({ showSignUp }) {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault(); // Ngăn form submit mặc định
    navigate('/home'); // Chuyển hướng sang Home
    // Giả lập logic đăng nhập (bạn có thể thêm gọi API ở đây)
    // const username = document.getElementById('username_log').value;
    // const password = document.getElementById('password_log').value;
    
    if (username && password) {
    } else {
      alert('Please enter username and password');
    }
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