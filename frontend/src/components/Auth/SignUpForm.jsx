function SignUpForm({ showLogin }) {
    return (
      <div id="sign-up-form" className="form-container bg-white text-center">
        <h2 className="primary-color mb-4 auth-title">Sign Up</h2>
        <form>
          <div className="mb-3 input-icon-container input-group">
            <label htmlFor="username_reg" className="input-group-text w-40px">
              <i className="fa-solid fa-user"></i>
            </label>
            <input
              type="text"
              id="username_reg"
              className="form-control"
              placeholder="Username"
            />
          </div>
          <div className="mb-3 input-icon-container input-group">
            <label htmlFor="password_reg" className="input-group-text w-40px">
              <i className="fa-solid fa-lock"></i>
            </label>
            <input
              type="password"
              id="password_reg"
              className="form-control"
              placeholder="Password"
            />
          </div>
          <div className="mb-3 input-icon-container input-group">
            <label htmlFor="email_reg" className="input-group-text w-40px">
              <i className="fa-regular fa-envelope"></i>
            </label>
            <input
              type="text"
              id="email_reg"
              className="form-control"
              placeholder="Email"
            />
          </div>
          <div className="mb-3 input-icon-container input-group">
            <label htmlFor="phone_reg" className="input-group-text w-40px">
              <i className="fa-solid fa-phone"></i>
            </label>
            <input
              type="text"
              id="phone_reg"
              className="form-control"
              placeholder="Phone Number"
            />
          </div>
          <div className="mb-3 input-icon-container input-group">
            <label htmlFor="address_reg" className="input-group-text w-40px">
              <i className="fa-solid fa-location-dot"></i>
            </label>
            <input
              type="text"
              id="address_reg"
              className="form-control"
              placeholder="Address"
            />
          </div>
          <button type="submit" className="btn-login w-100 mb-4">
            Sign Up
          </button>
          <a href="#" className="text-decoration-none toggle-auth text-primary" onClick={showLogin}>
            Login
          </a>
        </form>
      </div>
    );
  }
  
  export default SignUpForm;