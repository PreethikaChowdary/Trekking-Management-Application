<template>
  <div class="container-fluid py-4 px-4">
    <h4 class="fw-bold mb-4" style="color:#E9E4DC;">Staff Dashboard</h4>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else>
      <p class="mb-3" style="color:#E9E4DC;">You have <strong>{{ data.total_assigned }}</strong> assigned trek(s).</p>

      <div class="row g-3">
        <div class="col-12 col-md-6 col-lg-4" v-for="trek in data.assigned_treks" :key="trek.id">
          <div class="card border-0 shadow-sm h-100" style="background:#E9E4DC;">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h6 class="fw-bold mb-0" style="color:#2B2414;">{{ trek.name }}</h6>
                <span class="badge" :style="statusStyle(trek.status)">{{ trek.status }}</span>
              </div>
              <p class="small mb-1" style="color:#775B45;">📍 {{ trek.location }}</p>
              <p class="small mb-1" style="color:#2B2414;">Difficulty: <strong>{{ trek.difficulty }}</strong></p>
              <p class="small mb-2" style="color:#2B2414;">
                Slots: <strong>{{ trek.available_slots }}/{{ trek.total_slots }}</strong> &nbsp;|&nbsp;
                Trekkers: <strong>{{ trek.registered_trekkers }}</strong>
              </p>
              <router-link :to="`/staff/trek/${trek.id}`" class="btn btn-sm fw-semibold"
                           style="background:#585D27;border:none;color:#E9E4DC;">
                Manage →
              </router-link>
            </div>
          </div>
        </div>

        <div v-if="!data.assigned_treks?.length" class="col-12">
          <div class="alert" style="background:#E9E4DC;color:#775B45;border-color:#BCA890;">
            No treks assigned to you yet.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const data = ref({ assigned_treks: [], total_assigned: 0 })
const loading = ref(true)

onMounted(async () => {
  const res = await api.get('/staff/dashboard')
  data.value = res.data
  loading.value = false
})

const statusStyle = s => {
  if (s === 'Open') return 'background:#585D27;'
  if (s === 'Closed') return 'background:#775B45;'
  if (s === 'Completed') return 'background:#2B2414;'
  return 'background:#BCA890;color:#2B2414;'
}
</script>