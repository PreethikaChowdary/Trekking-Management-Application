<template>
  <div class="container-fluid py-4 px-4">
    <h4 class="fw-bold mb-4" style="color:#E9E4DC;">Welcome, {{ user.name }} 🏔️</h4>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3" v-for="card in cards" :key="card.label">
        <div class="card text-center border-0 shadow-sm" style="background:#E9E4DC;">
          <div class="card-body py-3">
            <div style="font-size:2rem;">{{ card.icon }}</div>
            <div class="fs-3 fw-bold" style="color:#585D27;">{{ card.value }}</div>
            <div class="small" style="color:#775B45;">{{ card.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Treks Section -->
    <div class="card border-0 shadow-sm mb-4" style="background:#E9E4DC;">
      <div class="card-header fw-semibold d-flex justify-content-between align-items-center"
           style="background:#BCA890;color:#2B2414;">
        <span>🟢 Available Treks</span>
        <router-link to="/user/treks" class="btn btn-sm fw-semibold"
                     style="background:#585D27;border:none;color:#E9E4DC;">View All</router-link>
      </div>
      <div class="card-body p-0">
        <div v-if="loadingTreks" class="text-center py-4">
          <div class="spinner-border" style="color:#585D27;"></div>
        </div>
        <table v-else class="table mb-0" style="background:#E9E4DC;">
          <thead style="background:#BCA890;color:#2B2414;">
            <tr><th>#</th><th>Trek</th><th>Location</th><th>Difficulty</th><th>Slots</th><th>Start Date</th></tr>
          </thead>
          <tbody>
            <tr v-for="(trek, index) in activeTreks" :key="trek.id">
              <td style="color:#2B2414;">{{ index + 1 }}</td>
              <td class="fw-semibold" style="color:#2B2414;">{{ trek.name }}</td>
              <td style="color:#775B45;">{{ trek.location }}</td>
              <td>
                <span class="badge" :style="diffStyle(trek.difficulty)">{{ trek.difficulty }}</span>
              </td>
              <td style="color:#2B2414;">{{ trek.available_slots }} left</td>
              <td style="color:#2B2414;">{{ trek.start_date || '—' }}</td>
            </tr>
            <tr v-if="!activeTreks.length">
              <td colspan="6" class="text-center py-4" style="color:#775B45;">
                No open treks available.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Recent Bookings Section -->
    <div class="card border-0 shadow-sm" style="background:#E9E4DC;">
      <div class="card-header fw-semibold d-flex justify-content-between align-items-center"
           style="background:#BCA890;color:#2B2414;">
        <span>Recent Bookings</span>
        <router-link to="/user/bookings" class="btn btn-sm fw-semibold"
                     style="background:#585D27;border:none;color:#E9E4DC;">View All</router-link>
      </div>
      <div class="card-body p-0">
        <div v-if="loadingBookings" class="text-center py-4">
          <div class="spinner-border" style="color:#585D27;"></div>
        </div>
        <table v-else class="table mb-0" style="background:#E9E4DC;">
          <thead style="background:#BCA890;color:#2B2414;">
            <tr><th>#</th><th>Trek</th><th>Location</th><th>Booked On</th><th>Status</th></tr>
          </thead>
          <tbody>
            <tr v-for="(b, index) in recentBookings" :key="b.booking_id">
              <td style="color:#2B2414;">{{ index + 1 }}</td>
              <td class="fw-semibold" style="color:#2B2414;">{{ b.trek_name }}</td>
              <td style="color:#775B45;">{{ b.location }}</td>
              <td style="color:#2B2414;">{{ b.booking_date }}</td>
              <td>
                <span class="badge"
                      :style="b.status === 'Booked' || b.status === 'Completed'
                        ? 'background:#585D27;'
                        : b.status === 'Cancelled'
                        ? 'background:#775B45;'
                        : 'background:#BCA890;color:#2B2414;'">
                  {{ b.status }}
                </span>
              </td>
            </tr>
            <tr v-if="!recentBookings.length">
              <td colspan="5" class="text-center py-4" style="color:#775B45;">
                No bookings yet.
                <router-link to="/user/treks" style="color:#585D27;">Browse treks!</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
const bookings = ref([])
const activeTreks = ref([])
const loadingBookings = ref(true)
const loadingTreks = ref(true)

const recentBookings = computed(() => bookings.value.slice(0, 5))

const cards = computed(() => [
  { label: 'Total Bookings', value: bookings.value.length, icon: '📋' },
  { label: 'Active', value: bookings.value.filter(b => b.status === 'Booked').length, icon: '🟢' },
  { label: 'Completed', value: bookings.value.filter(b => b.status === 'Completed').length, icon: '✅' },
  { label: 'Cancelled', value: bookings.value.filter(b => b.status === 'Cancelled').length, icon: '❌' },
])

onMounted(async () => {
  // Load bookings
  const { data: bookingData } = await api.get('/user/bookings')
  bookings.value = bookingData
  loadingBookings.value = false

  // Load active treks
  const { data: trekData } = await api.get('/user/treks')
  activeTreks.value = trekData
  loadingTreks.value = false
})

const diffStyle = d => {
  if (d === 'Easy') return 'background:#585D27;'
  if (d === 'Moderate') return 'background:#BCA890;color:#2B2414;'
  return 'background:#775B45;'
}
</script>