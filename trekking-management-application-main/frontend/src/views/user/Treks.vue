<template>
  <div class="container-fluid py-4 px-4">
    <h4 class="fw-bold mb-4" style="color:#E9E4DC;">Browse Treks</h4>

    <div class="card border-0 shadow-sm mb-4" style="background:#E9E4DC;">
      <div class="card-body">
        <div class="row g-2">
          <div class="col-12 col-md-4">
            <input v-model="filters.q" class="form-control" placeholder="🔍 Search by name…"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" @input="loadTreks" />
          </div>
          <div class="col-6 col-md-2">
            <select v-model="filters.difficulty" class="form-select"
                    style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" @change="loadTreks">
              <option value="">All Difficulties</option>
              <option>Easy</option><option>Moderate</option><option>Hard</option>
            </select>
          </div>
          <div class="col-6 col-md-2">
            <input v-model="filters.location" class="form-control" placeholder="📍 Location"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" @input="loadTreks" />
          </div>
          <div class="col-6 col-md-2">
            <input v-model.number="filters.duration" type="number" min="1" class="form-control"
                   placeholder="⏱ Days" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" @input="loadTreks" />
          </div>
          <div class="col-6 col-md-2">
            <button class="btn w-100" style="border-color:#BCA890;color:#2B2414;background:#BCA890;" @click="resetFilters">Reset</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else-if="!treks.length" class="text-center py-5" style="color:#E9E4DC;">
      No open treks found matching your filters.
    </div>

    <div v-else class="row g-3">
      <div class="col-12 col-md-6 col-lg-4" v-for="trek in treks" :key="trek.id">
        <div class="card border-0 shadow-sm h-100" style="background:#E9E4DC;">
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between mb-2">
              <h6 class="fw-bold mb-0" style="color:#2B2414;">{{ trek.name }}</h6>
              <span class="badge" :style="diffStyle(trek.difficulty)">{{ trek.difficulty }}</span>
            </div>
            <p class="small mb-1" style="color:#775B45;">📍 {{ trek.location }}</p>
            <p class="small mb-1" style="color:#2B2414;">⏱ {{ trek.duration }} days</p>
            <p class="small mb-1" style="color:#2B2414;">🎟 Slots: <strong>{{ trek.available_slots }}</strong> left</p>
            <p v-if="trek.start_date" class="small mb-3" style="color:#775B45;">📅 {{ trek.start_date }}</p>
            <button class="btn btn-sm fw-semibold mt-auto"
                    style="background:#585D27;border:none;color:#E9E4DC;"
                    @click="bookTrek(trek.id)"
                    :disabled="trek.available_slots === 0 || booking === trek.id">
              {{ booking === trek.id ? 'Booking…' : trek.available_slots === 0 ? 'Full' : 'Book Now' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import api from '../../api'

const toast = inject('toast')
const treks = ref([])
const loading = ref(true)
const booking = ref(null)
const filters = ref({ q: '', difficulty: '', location: '', duration: '' })

onMounted(loadTreks)

async function loadTreks() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.difficulty) params.difficulty = filters.value.difficulty
    if (filters.value.location) params.location = filters.value.location
    if (filters.value.duration) params.duration = filters.value.duration
    if (filters.value.q) {
      const { data } = await api.get('/user/treks/search', { params: { q: filters.value.q } })
      treks.value = data
    } else {
      const { data } = await api.get('/user/treks', { params })
      treks.value = data
    }
  } finally {
    loading.value = false
  }
}

async function bookTrek(trekId) {
  booking.value = trekId
  try {
    await api.post('/user/bookings', { trek_id: trekId })
    toast.success('Trek booked successfully! 🎉')
    await loadTreks()
  } catch (e) {
    toast.error(e.response?.data?.message || 'Booking failed')
  } finally {
    booking.value = null
  }
}

function resetFilters() {
  filters.value = { q: '', difficulty: '', location: '', duration: '' }
  loadTreks()
}

const diffStyle = d => {
  if (d === 'Easy') return 'background:#585D27;'
  if (d === 'Moderate') return 'background:#BCA890;color:#2B2414;'
  return 'background:#775B45;'
}
</script>