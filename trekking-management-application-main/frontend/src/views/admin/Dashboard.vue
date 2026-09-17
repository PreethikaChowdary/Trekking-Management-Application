<template>
  <div class="container-fluid py-4 px-4">
    <h4 class="mb-4 fw-bold" style="color:#E9E4DC;">Admin Dashboard</h4>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else class="row g-3 mb-4">
      <div class="col-6 col-md-4 col-lg-2" v-for="card in statCards" :key="card.label">
        <div class="card text-center border-0 shadow-sm h-100" style="background:#E9E4DC;">
          <div class="card-body py-3 d-flex flex-column align-items-center justify-content-center">
            <div style="font-size:1.8rem;margin-bottom:6px;">{{ card.icon }}</div>
            <div class="fw-bold" style="font-size:1.8rem;color:#585D27;line-height:1;">{{ card.value }}</div>
            <div class="fw-semibold mt-1" style="font-size:0.85rem;color:#2B2414;">{{ card.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-12 col-md-6 col-lg-3" v-for="action in quickActions" :key="action.label">
        <router-link :to="action.to" class="text-decoration-none">
          <div class="card border-0 shadow-sm h-100" style="cursor:pointer;background:#E9E4DC;">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <span style="font-size:1.8rem">{{ action.icon }}</span>
              <div>
                <div class="fw-bold" style="color:#2B2414;font-size:0.95rem;">{{ action.label }}</div>
                <div class="fw-semibold" style="color:#775B45;font-size:0.8rem;">{{ action.desc }}</div>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../../api'

const stats = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/dashboard')
    stats.value = data
  } finally {
    loading.value = false
  }
})

const statCards = computed(() => [
  { label: 'Total Treks', value: stats.value.total_treks ?? 0, icon: '🗺️' },
  { label: 'Open Treks', value: stats.value.open_treks ?? 0, icon: '🟢' },
  { label: 'Completed', value: stats.value.completed_treks ?? 0, icon: '✅' },
  { label: 'Total Users', value: stats.value.total_users ?? 0, icon: '🧑' },
  { label: 'Trek Staff', value: stats.value.total_staff ?? 0, icon: '👷' },
  { label: 'Bookings', value: stats.value.total_bookings ?? 0, icon: '📋' },
])

const quickActions = [
  { label: 'Manage Treks', desc: 'Create, edit, assign staff', to: '/admin/treks', icon: '🗺️' },
  { label: 'Manage Staff', desc: 'Add or deactivate staff', to: '/admin/staff', icon: '👷' },
  { label: 'Manage Users', desc: 'View and deactivate users', to: '/admin/users', icon: '🧑' },
  { label: 'View Stats', desc: 'Charts and analytics', to: '/admin/stats', icon: '📊' },
]
</script>