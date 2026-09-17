<template>
  <div class="container-fluid py-4 px-4">
    <h4 class="fw-bold mb-4" style="color:#E9E4DC;">All Bookings</h4>

    <div class="mb-3">
      <input v-model="search" class="form-control" placeholder="🔍 Filter by user or trek name…"
             style="max-width:400px;border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
    </div>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else class="table-responsive">
      <table class="table table-hover align-middle rounded shadow-sm" style="background:#E9E4DC;">
        <thead style="background:#BCA890;color:#2B2414;">
          <tr>
            <th>#</th>
            <th>User</th>
            <th>Trek</th>
            <th>Booked On</th>
            <th>Status</th>
            <th>Payment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(b, index) in filtered" :key="b.id">
            <td style="color:#2B2414;">{{ index + 1 }}</td>
            <td class="fw-semibold" style="color:#2B2414;">{{ b.user_name }}</td>
            <td style="color:#2B2414;">{{ b.trek_name }}</td>
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
            <td style="color:#775B45;">{{ b.payment_status || '—' }}</td>
          </tr>
          <tr v-if="!filtered.length">
            <td colspan="6" class="text-center py-4" style="color:#775B45;">No bookings found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const bookings = ref([])
const loading = ref(true)
const search = ref('')

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return bookings.value.filter(b =>
    b.user_name.toLowerCase().includes(q) || b.trek_name.toLowerCase().includes(q)
  )
})

onMounted(async () => {
  const { data } = await api.get('/admin/bookings')
  bookings.value = data
  loading.value = false
})
</script>