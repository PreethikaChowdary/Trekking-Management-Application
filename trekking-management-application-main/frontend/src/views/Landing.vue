<template>
  <div style="min-height:100vh;background:#775B45;">
    <!-- Hero Section -->
    <div class="text-center py-5 px-4">
      <h1 class="fw-bold mb-2" style="color:#E9E4DC;font-size:3rem;">🏔️ TrekApp</h1>
      <p class="mb-4" style="color:#BCA890;font-size:1.2rem;">
        Discover, Book and Manage Trekking Adventures
      </p>
      <div class="d-flex gap-3 justify-content-center">
        <router-link to="/login" class="btn fw-semibold px-4 py-2"
                     style="background:#585D27;color:#E9E4DC;border:none;">
          Login
        </router-link>
        <router-link to="/register" class="btn fw-semibold px-4 py-2"
                     style="background:#E9E4DC;color:#585D27;border:none;">
          Register
        </router-link>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="container pb-4">
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border" style="color:#E9E4DC;"></div>
      </div>
      <div v-else class="row g-3 mb-4">
        <div class="col-6 col-md-3" v-for="card in statCards" :key="card.label">
          <div class="card text-center border-0 shadow-sm" style="background:#E9E4DC;">
            <div class="card-body py-3">
              <div style="font-size:2rem;">{{ card.icon }}</div>
              <div class="fs-3 fw-bold" style="color:#585D27;">{{ card.value }}</div>
              <div class="small" style="color:#775B45;">{{ card.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Popular Treks -->
      <div class="card border-0 shadow-sm mb-4" style="background:#E9E4DC;">
        <div class="card-header fw-semibold" style="background:#BCA890;color:#2B2414;">
          🏆 Popular Treks
        </div>
        <div class="card-body p-0">
          <table class="table mb-0" style="background:#E9E4DC;">
            <thead style="background:#BCA890;color:#2B2414;">
              <tr><th>Trek</th><th>Location</th><th>Difficulty</th><th>Bookings</th></tr>
            </thead>
            <tbody>
              <tr v-for="t in popularTreks" :key="t.name">
                <td class="fw-semibold" style="color:#2B2414;">{{ t.name }}</td>
                <td style="color:#775B45;">{{ t.location }}</td>
                <td>
                  <span class="badge"
                        :style="t.difficulty === 'Easy' ? 'background:#585D27;' :
                                t.difficulty === 'Moderate' ? 'background:#BCA890;color:#2B2414;' :
                                'background:#775B45;'">
                    {{ t.difficulty }}
                  </span>
                </td>
                <td class="fw-bold" style="color:#585D27;">{{ t.bookings }}</td>
              </tr>
              <tr v-if="!popularTreks.length">
                <td colspan="4" class="text-center py-3" style="color:#775B45;">No data yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Charts -->
      <div class="row g-3">
        <div class="col-12 col-md-6">
          <div class="card border-0 shadow-sm" style="background:#E9E4DC;">
            <div class="card-header fw-semibold" style="background:#BCA890;color:#2B2414;">
              Trek Difficulty Distribution
            </div>
            <div class="card-body d-flex justify-content-center">
              <canvas ref="diffChart" height="200"></canvas>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="card border-0 shadow-sm" style="background:#E9E4DC;">
            <div class="card-header fw-semibold" style="background:#BCA890;color:#2B2414;">
              Trek Status Overview
            </div>
            <div class="card-body d-flex justify-content-center">
              <canvas ref="statusChart" height="200"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '../api'

Chart.register(...registerables)

const stats = ref({})
const loading = ref(true)
const diffChart = ref(null)
const statusChart = ref(null)

const popularTreks = computed(() => stats.value.popular_treks || [])

const statCards = computed(() => [
  { label: 'Total Treks', value: stats.value.total_treks ?? 0, icon: '🗺️' },
  { label: 'Open Treks', value: stats.value.open_treks ?? 0, icon: '🟢' },
  { label: 'Total Bookings', value: stats.value.total_bookings ?? 0, icon: '📋' },
  { label: 'Completed Treks', value: stats.value.completed_treks ?? 0, icon: '✅' },
])

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/public/stats')
    stats.value = data
  } catch (e) {
    console.log('Stats not available')
  } finally {
    loading.value = false
  }

  await nextTick()

  if (diffChart.value && stats.value.difficulty_distribution) {
    const dd = stats.value.difficulty_distribution
    new Chart(diffChart.value, {
      type: 'doughnut',
      data: {
        labels: Object.keys(dd),
        datasets: [{ data: Object.values(dd), backgroundColor: ['#585D27', '#BCA890', '#775B45'] }]
      },
      options: { plugins: { legend: { position: 'bottom' } } }
    })
  }

  if (statusChart.value && stats.value.status_distribution) {
    const sd = stats.value.status_distribution
    new Chart(statusChart.value, {
      type: 'bar',
      data: {
        labels: Object.keys(sd),
        datasets: [{ label: 'Treks', data: Object.values(sd), backgroundColor: '#585D27' }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
      }
    })
  }
})
</script>