import React, { useState } from "react";
import styles from "../components/Home/Profile.module.css"; // Import CSS module
import defaultAvatar from "../assets/images/Avatar.png";
import { FaPencilAlt } from "react-icons/fa";
import "bootstrap/dist/css/bootstrap.min.css";

function Profile() {
  const [formData, setFormData] = useState({
    name: "Charlene Reed",
    email: "charlenereed@gmail.com",
    dob: "1990-01-25",
    permanentAddress: "San Jose, California, USA",
    userName: "Charlene Reed",
    password: "********",
    presentAddress: "San Jose, California, USA",
    country: "USA",
  });

  const [avatar, setAvatar] = useState(defaultAvatar);

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "dob") {
      const selectedDate = new Date(value);
      const minDate = new Date("1900-01-01");
      const maxDate = new Date();

      if (selectedDate < minDate || selectedDate > maxDate) {
        alert("Ngày sinh phải từ năm 1900 đến hiện tại!");
        return;
      }
    }
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => setAvatar(event.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Data sent to backend:", formData);
    alert("Profile saved successfully! (Check console)");
  };

  return (
    <div className={`container mt-4 ${styles.container}`}>
      <div className="row">
        {/* Avatar Section */}
        <div className="col-md-2 text-center">
          <div className={styles.avatarContainer}>
            <img src={avatar} alt="Avatar" className={styles.avatar} />
            <label htmlFor="avatarUpload" className={styles.editIcon}>
              <FaPencilAlt size={14} />
            </label>
            <input type="file" id="avatarUpload" className="d-none" accept="image/*" onChange={handleAvatarChange} />
          </div>
        </div>

        {/* Left Form Section */}
        <div className="col-md-5">
          <form>
            <div className="mb-3">
              <label htmlFor="name" className={styles.formLabel}>Your Name</label>
              <input type="text" className={`form-control ${styles.formControl}`} id="name" name="name" value={formData.name} onChange={handleChange} />
            </div>

            <div className="mb-3">
              <label htmlFor="email" className={styles.formLabel}>Email</label>
              <input type="email" className={`form-control ${styles.formControl}`} id="email" name="email" value={formData.email} onChange={handleChange} />
            </div>

            <div className="mb-3">
              <label htmlFor="dob" className={styles.formLabel}>Date of Birth</label>
              <input
                type="date"
                className={`form-control ${styles.formControl}`}
                id="dob"
                name="dob"
                value={formData.dob}
                onChange={handleChange}
                pattern="\d{4}-\d{2}-\d{2}" /* Hỗ trợ nhập tay theo định dạng YYYY-MM-DD */
                placeholder="YYYY-MM-DD"
              />
            </div>

            <div className="mb-3">
              <label htmlFor="permanentAddress" className={styles.formLabel}>Permanent Address</label>
              <input type="text" className={`form-control ${styles.formControl}`} id="permanentAddress" name="permanentAddress" value={formData.permanentAddress} onChange={handleChange} />
            </div>
          </form>
        </div>

        {/* Right Form Section */}
        <div className="col-md-5">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="userName" className={styles.formLabel}>User Name</label>
              <input type="text" className={`form-control ${styles.formControl}`} id="userName" name="userName" value={formData.userName} onChange={handleChange} />
            </div>

            <div className="mb-3">
              <label htmlFor="password" className={styles.formLabel}>Password</label>
              <input type="password" className={`form-control ${styles.formControl}`} id="password" name="password" value={formData.password} onChange={handleChange} />
            </div>

            <div className="mb-3">
              <label htmlFor="presentAddress" className={styles.formLabel}>Present Address</label>
              <input type="text" className={`form-control ${styles.formControl}`} id="presentAddress" name="presentAddress" value={formData.presentAddress} onChange={handleChange} />
            </div>

            <div className="mb-3">
              <label htmlFor="country" className={styles.formLabel}>Country</label>
              <input type="text" className={`form-control ${styles.formControl}`} id="country" name="country" value={formData.country} onChange={handleChange} />
            </div>

            <div className={styles.saveButtonContainer}>
              <button type="submit" className={styles.submitButton}>
                Save
              </button>
            </div>

          </form>
        </div>
      </div>
    </div>
  );
}

export default Profile;
