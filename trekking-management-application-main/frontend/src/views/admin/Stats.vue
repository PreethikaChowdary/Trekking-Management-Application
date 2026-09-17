<template>
  <div class="container-fluid py-4 px-4">
    <h4 class="fw-bold mb-4" style="color:#E9E4DC;">Trekking Statistics</h4>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else class="row g-4">

      <!-- Summary Cards -->
      <div class="col-6 col-md-3" v-for="card in summaryCards" :key="card.label">
        <div class="card text-center border-0 shadow-sm" style="background:#E9E4DC;">
          <div class="card-body py-3">
            <div style="font-size:1.8rem;">{{ card.icon }}</div>
            <div class="fw-bold" style="font-size:1.8rem;color:#585D27;">{{ card.value }}</div>
            <div class="fw-semibold" style="font-size:0.85rem;color:#2B2414;">{{ card.label }}</div>
          </div>
        </div>
      </div>

      <!-- Popular Treks Table -->
      <div class="col-12 col-lg-6">
        <div class="card border-0 shadow-sm" style="background:#E9E4DC;">
          <div class="card-header fw-bold" style="background:#BCA890;color:#2B2414;">
            🏆 Popular Treks
          </div>
          <div class="card-body p-0">
            <table class="table mb-0" style="background:#E9E4DC;">
              <thead style="background:#BCA890;color:#2B2414;">
                <tr><th>#</th><th>Trek</th><th>Location</th><th>Difficulty</th><th>Bookings</th></tr>
              </thead>
              <tbody>
                <tr v-for="(t, index) in stats.popular_treks" :key="t.name">
                  <td style="color:#2B2414;">{{ index + 1 }}</td>
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
                <tr v-if="!stats.popular_treks?.length">
                  <td colspan="5" class="text-center py-3" style="color:#775B45;">No data yet.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Difficulty Chart -->
      <div class="col-12 col-sm-6 col-lg-3">
        <div class="card border-0 shadow-sm h-100" style="background:#E9E4DC;">
          <div class="card-header fw-bold" style="background:#BCA890;color:#2B2414;">
            Difficulty Split
          </div>
          <div class="card-body d-flex align-items-center justify-content-center">
            <canvas ref="diffChart" height="200"></canvas>
          </div>
        </div>
      </div>

      <!-- Status Chart -->
      <div class="col-12 col-sm-6 col-lg-3">
        <div class="card border-0 shadow-sm h-100" style="background:#E9E4DC;">
          <div class="card-header fw-bold" style="background:#BCA890;color:#2B2414;">
            Trek Status
          </div>
          <div class="card-body d-flex align-items-center justify-content-center">
            <canvas ref="statusChart" height="200"></canvas>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '../../api'

Chart.register(...registerables)

const stats = ref({})
const loading = ref(true)
const diffChart = ref(null)
const statusChart = ref(null)

const summaryCards = computed(() => [
  { label: 'Total Bookings', value: stats.value.total_bookings ?? 0, icon: '📋' },
  { label: 'Completed', value: stats.value.total_completed ?? 0, icon: '✅' },
  { label: 'Cancelled', value: stats.value.total_cancelled ?? 0, icon: '❌' },
  { label: 'Open Treks', value: stats.value.status_distribution?.Open ?? 0, icon: '🟢' },
])

onMounted(async () => {
  const { data } = await api.get('/admin/stats')
  stats.value = data
  loading.value = false

  await nextTick()

  const dd = data.difficulty_distribution || {}
  new Chart(diffChart.value, {
    type: 'doughnut',
    data: {
      labels: Object.keys(dd),
      datasets: [{
        data: Object.values(dd),
        backgroundColor: ['#585D27', '#BCA890', '#775B45']
      }]
    },
    options: {
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  })

  const sd = data.status_distribution || {}
  new Chart(statusChart.value, {
    type: 'bar',
    data: {
      labels: Object.keys(sd),
      datasets: [{
        label: 'Treks',
        data: Object.values(sd),
        backgroundColor: '#585D27'
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 }
        }
      }
    }
  })
})
</script>