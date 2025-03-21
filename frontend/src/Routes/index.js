import Home from '../pages/Home'
import Services from '../pages/Services'
import Profile from '../pages/Profile'
import Auth from '../pages/Auth'

const publicRoutes = [
  {path: '/', component: Auth},
  {path: '/home', component: Home},
  {path: '/services', component: Services},
  {path: '/profile', component: Profile},
]

export {publicRoutes}