import styles from "./Sidebar.module.css"
import { NavLink } from "react-router-dom"
import clsx from "clsx"
import Robot from '../../../assets/robot.svg'

const SideBar = () => {
  return (
    <nav className={styles.wrapper}>
      <div className={styles.logo}>
        <img className={styles.logoImg} src={Robot} alt=""></img>
        <div className={styles.SDA}>SDA</div>
      </div>
      <ul className={styles.list}>
        <li><NavLink to="/home" className={({ isActive }) => clsx(
          styles.sidebarLink,
          isActive ? styles.active : '')}>
          <div className={styles.icon}>
            <i className="fa-solid fa-house"></i>
          </div>
          Home
        </NavLink></li>
        <li><NavLink to="/services" className={({ isActive }) => clsx(
          styles.sidebarLink,
          isActive ? styles.active : '')}>
          <div className={styles.icon}>
            <i className="fa-solid fa-gears"></i>
          </div>
          Devices
        </NavLink></li>
        <li><NavLink to="/profile" className={({ isActive }) => clsx(
          styles.sidebarLink,
          isActive ? styles.active : '')}>
          <div className={styles.icon}>
            <i class="fa-solid fa-user"></i>
          </div>
          Profile
        </NavLink></li>
        <li>
          <NavLink to="/" className={styles.sidebarLink}>
            <div className={styles.icon}>
              <i className="fa-solid fa-right-from-bracket"></i>
            </div>
            Logout
          </NavLink>
        </li>
      </ul>
    </nav>
  )
}

export default SideBar