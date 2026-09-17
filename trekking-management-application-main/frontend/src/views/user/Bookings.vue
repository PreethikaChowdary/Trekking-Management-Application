<template>
  <div class="container-fluid py-4 px-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="fw-bold mb-0" style="color:#E9E4DC;">My Bookings</h4>
      <button class="btn fw-semibold" style="background:#585D27;border:none;color:#E9E4DC;"
              @click="exportCSV" :disabled="exporting">
        {{ exporting ? 'Exporting…' : '⬇ Export CSV' }}
      </button>
    </div>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else class="table-responsive">
      <table class="table table-hover align-middle rounded shadow-sm" style="background:#E9E4DC;">
        <thead style="background:#BCA890;color:#2B2414;">
          <tr><th>#</th><th>Trek</th><th>Location</th><th>Difficulty</th><th>Start Date</th><th>Booked On</th><th>Status</th><th>Action</th></tr>
        </thead>
        <tbody>
          <tr v-for="(b, index) in bookings" :key="b.booking_id">
            <td style="color:#2B2414;">{{ index + 1 }}</td>
            <td class="fw-semibold" style="color:#2B2414;">{{ b.trek_name }}</td>
            <td style="color:#775B45;">{{ b.location }}</td>
            <td><span class="badge" :style="diffStyle(b.difficulty)">{{ b.difficulty }}</span></td>
            <td style="color:#2B2414;">{{ b.start_date || '—' }}</td>
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
            <td>
              <button v-if="b.status === 'Booked'" class="btn btn-sm fw-semibold"
                      style="background:#775B45;border:none;color:#E9E4DC;"
                      @click="cancel(b.booking_id)">Cancel</button>
            </td>
          </tr>
          <tr v-if="!bookings.length">
            <td colspan="8" class="text-center py-4" style="color:#775B45;">
              No bookings yet.
              <router-link to="/user/treks" style="color:#585D27;">Browse treks!</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import api from '../../api'

const toast = inject('toast')
const bookings = ref([])
const loading = ref(true)
const exporting = ref(false)

onMounted(loadBookings)

async function loadBookings() {
  const { data } = await api.get('/user/bookings')
  bookings.value = data
  loading.value = false
}

async function cancel(id) {
  if (!confirm('Cancel this booking?')) return
  try {
    await api.put(`/user/bookings/${id}/cancel`)
    toast.success('Booking cancelled successfully!')
    await loadBookings()
  } catch (e) {
    toast.error(e.response?.data?.message || 'Cancellation failed')
  }
}

async function exportCSV() {
  exporting.value = true
  try {
    await api.post('/user/export-history')
    toast.success('Export started! You will receive an email shortly.')
  } catch (e) {
    toast.error(e.response?.data?.message || 'Export failed')
  } finally {
    exporting.value = false
  }
}

const diffStyle = d => {
  if (d === 'Easy') return 'background:#585D27;'
  if (d === 'Moderate') return 'background:#BCA890;color:#2B2414;'
  return 'background:#775B45;'
}
</script>