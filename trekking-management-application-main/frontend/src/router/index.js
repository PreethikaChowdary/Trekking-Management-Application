import { createRouter, createWebHistory } from 'vue-router'

import Landing from '../views/Landing.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/admin/Dashboard.vue'
import AdminTreks from '../views/admin/Treks.vue'
import AdminStaff from '../views/admin/Staff.vue'
import AdminUsers from '../views/admin/Users.vue'
import AdminBookings from '../views/admin/Bookings.vue'
import AdminStats from '../views/admin/Stats.vue'
import StaffDashboard from '../views/staff/Dashboard.vue'
import StaffTrek from '../views/staff/TrekDetail.vue'
import UserDashboard from '../views/user/Dashboard.vue'
import UserTreks from '../views/user/Treks.vue'
import UserBookings from '../views/user/Bookings.vue'
import UserProfile from '../views/user/Profile.vue'

const routes = [
  { path: '/', component: Landing },
  { path: '/login', component: Login },
  { path: '/register', component: Register },

  { path: '/admin', component: AdminDashboard, meta: { role: 'admin' } },
  { path: '/admin/treks', component: AdminTreks, meta: { role: 'admin' } },
  { path: '/admin/staff', component: AdminStaff, meta: { role: 'admin' } },
  { path: '/admin/users', component: AdminUsers, meta: { role: 'admin' } },
  { path: '/admin/bookings', component: AdminBookings, meta: { role: 'admin' } },
  { path: '/admin/stats', component: AdminStats, meta: { role: 'admin' } },

  { path: '/staff', component: StaffDashboard, meta: { role: 'staff' } },
  { path: '/staff/trek/:id', component: StaffTrek, meta: { role: 'staff' } },

  { path: '/user', component: UserDashboard, meta: { role: 'trekker' } },
  { path: '/user/treks', component: UserTreks, meta: { role: 'trekker' } },
  { path: '/user/bookings', component: UserBookings, meta: { role: 'trekker' } },
  { path: '/user/profile', component: UserProfile, meta: { role: 'trekker' } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  if (to.meta.role) {
    if (!token) return next('/login')
    if (to.meta.role !== user.role) {
      const dashMap = { admin: '/admin', staff: '/staff', trekker: '/user' }
      return next(dashMap[user.role] || '/login')
    }
  }
  next()
})

export default router