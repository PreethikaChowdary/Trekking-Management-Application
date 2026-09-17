<template>
  <div class="container py-4">
    <router-link to="/staff" class="btn btn-sm mb-3"
                 style="border-color:#BCA890;color:#E9E4DC;">← Back</router-link>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else>
      <div class="card border-0 shadow-sm mb-4" style="background:#E9E4DC;">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h5 class="fw-bold" style="color:#2B2414;">{{ trek.name }}</h5>
              <p class="mb-1" style="color:#775B45;">
                📍 {{ trek.location }} &nbsp;|&nbsp; {{ trek.difficulty }} &nbsp;|&nbsp; {{ trek.duration }} days
              </p>
              <p class="mb-0" style="color:#2B2414;">
                Available Slots: <strong>{{ trek.available_slots }}/{{ trek.total_slots }}</strong>
              </p>
            </div>
            <span class="badge" :style="statusStyle(trek.status)" style="font-size:.95rem;">
              {{ trek.status }}
            </span>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm mb-4" style="background:#E9E4DC;">
        <div class="card-header fw-semibold" style="background:#BCA890;color:#2B2414;">Update Trek</div>
        <div class="card-body">
          <div v-if="msg" class="alert" style="background:#BCA890;color:#2B2414;border-color:#775B45;">{{ msg }}</div>
          <div class="row g-2 align-items-end">
            <div class="col-md-4">
              <label class="form-label fw-semibold" style="color:#2B2414;">Available Slots</label>
              <input v-model.number="updateForm.available_slots" type="number" min="0"
                     class="form-control" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold" style="color:#2B2414;">Trek Status</label>
              <select v-model="updateForm.status" class="form-select"
                      style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;">
                <option>Open</option><option>Closed</option><option>Completed</option>
              </select>
            </div>
            <div class="col-md-4">
              <button class="btn fw-semibold w-100"
                      style="background:#585D27;border:none;color:#E9E4DC;" @click="updateTrek">Update</button>
            </div>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm" style="background:#E9E4DC;">
        <div class="card-header fw-semibold" style="background:#BCA890;color:#2B2414;">
          Participants ({{ participants.length }})
        </div>
        <div class="card-body p-0">
          <table class="table mb-0" style="background:#E9E4DC;">
            <thead style="background:#BCA890;color:#2B2414;">
              <tr><th>#</th><th>Name</th><th>Email</th><th>Booked On</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr v-for="(p, index) in participants" :key="p.booking_id">
                <td style="color:#2B2414;">{{ index + 1 }}</td>
                <td class="fw-semibold" style="color:#2B2414;">{{ p.user_name }}</td>
                <td style="color:#775B45;">{{ p.user_email }}</td>
                <td style="color:#2B2414;">{{ p.booking_date }}</td>
                <td>
                  <span class="badge" style="background:#585D27;">{{ p.status }}</span>
                </td>
              </tr>
              <tr v-if="!participants.length">
                <td colspan="5" class="text-center py-4" style="color:#775B45;">No participants yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api'

const route = useRoute()
const trek = ref({})
const participants = ref([])
const loading = ref(true)
const msg = ref('')
const updateForm = ref({ available_slots: 0, status: 'Open' })

onMounted(async () => {
  const id = route.params.id
  const [dashRes, partRes] = await Promise.all([
    api.get('/staff/dashboard'),
    api.get(`/staff/treks/${id}/participants`)
  ])
  const found = dashRes.data.assigned_treks.find(t => t.id === parseInt(id))
  trek.value = found || {}
  updateForm.value.available_slots = found?.available_slots ?? 0
  updateForm.value.status = found?.status ?? 'Open'
  participants.value = partRes.data.participants || []
  loading.value = false
})

async function updateTrek() {
  await api.put(`/staff/treks/${route.params.id}/status`, { status: updateForm.value.status })
  await api.put(`/staff/treks/${route.params.id}`, { available_slots: updateForm.value.available_slots })
  trek.value.status = updateForm.value.status
  trek.value.available_slots = updateForm.value.available_slots
  msg.value = 'Trek updated successfully!'
  setTimeout(() => msg.value = '', 3000)
}

const statusStyle = s => {
  if (s === 'Open') return 'background:#585D27;'
  if (s === 'Closed') return 'background:#775B45;'
  if (s === 'Completed') return 'background:#2B2414;'
  return 'background:#BCA890;color:#2B2414;'
}
</script>