<template>
  <div style="min-height:100vh;background:#775B45;">
    <nav v-if="user" class="navbar navbar-expand-lg navbar-dark" style="background:#585D27;">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">🏔️ TrekApp</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navMenu">
          <ul v-if="user.role === 'admin'" class="navbar-nav me-auto">
            <li class="nav-item"><router-link class="nav-link" to="/admin">Dashboard</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/treks">Treks</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/staff">Staff</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/users">Users</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/bookings">Bookings</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/stats">Stats</router-link></li>
          </ul>
          <ul v-else-if="user.role === 'staff'" class="navbar-nav me-auto">
            <li class="nav-item"><router-link class="nav-link" to="/staff">Dashboard</router-link></li>
          </ul>
          <ul v-else-if="user.role === 'trekker'" class="navbar-nav me-auto">
            <li class="nav-item"><router-link class="nav-link" to="/user">Dashboard</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/user/treks">Browse Treks</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/user/bookings">My Bookings</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/user/profile">Profile</router-link></li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <span class="nav-link" style="color:#BCA890;">👤 {{ user.name }}</span>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-light btn-sm mt-1" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view />
    <Toast ref="toastRef" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, provide } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Toast from './components/Toast.vue'

const router = useRouter()
const route = useRoute()
const user = ref(null)
const toastRef = ref(null)

function loadUser() {
  const stored = localStorage.getItem('user')
  user.value = stored ? JSON.parse(stored) : null
}

onMounted(loadUser)
watch(route, loadUser)

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  user.value = null
  router.push('/login')
}

// Provide toast globally so any component can use it
provide('toast', {
  success: (msg) => toastRef.value?.show(msg, 'success'),
  error: (msg) => toastRef.value?.show(msg, 'error')
})
</script>

<style>
* { box-sizing: border-box; }
body {
  background: #775B45 !important;
  min-height: 100vh;
  margin: 0;
}
</style>