<template>
  <div class="container-fluid py-4 px-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="fw-bold mb-0" style="color:#E9E4DC;">Manage Treks</h4>
      <button class="btn fw-semibold" style="background:#585D27;border:none;color:#E9E4DC;" @click="openCreate">+ Add Trek</button>
    </div>

    <div class="mb-3">
      <input v-model="search" class="form-control" placeholder="🔍 Search treks by name…"
             style="max-width:400px;border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
    </div>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else class="table-responsive">
      <table class="table table-hover align-middle rounded shadow-sm" style="background:#E9E4DC;">
        <thead style="background:#BCA890;color:#2B2414;">
          <tr>
            <th>#</th><th>Name</th><th>Location</th><th>Difficulty</th>
            <th>Duration</th><th>Slots</th><th>Status</th><th>Assigned Staff</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(trek, index) in filteredTreks" :key="trek.id">
            <td style="color:#2B2414;">{{ index + 1 }}</td>
            <td class="fw-semibold" style="color:#2B2414;">{{ trek.name }}</td>
            <td style="color:#2B2414;">{{ trek.location }}</td>
            <td><span :class="diffBadge(trek.difficulty)">{{ trek.difficulty }}</span></td>
            <td style="color:#2B2414;">{{ trek.duration }}d</td>
            <td style="color:#2B2414;">{{ trek.available_slots }}/{{ trek.total_slots }}</td>
            <td><span :class="statusBadge(trek.status)">{{ trek.status }}</span></td>
            <td style="color:#2B2414;">{{ trek.assigned_staff_name || '—' }}</td>
            <td>
              <button class="btn btn-sm me-1 text-white" style="background:#585D27;" @click="openEdit(trek)">Edit</button>
              <button class="btn btn-sm me-1 text-white" style="background:#BCA890;color:#2B2414!important;" @click="openAssign(trek)">Assign</button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteTrek(trek.id)">Delete</button>
            </td>
          </tr>
          <tr v-if="!filteredTreks.length">
            <td colspan="9" class="text-center py-4" style="color:#775B45;">No treks found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal=false">
      <div class="card shadow p-4" style="width:100%;max-width:520px;background:#E9E4DC;">
        <h5 class="mb-3 fw-bold" style="color:#585D27;">{{ editingTrek ? 'Edit Trek' : 'Create Trek' }}</h5>
        <div v-if="formError" class="alert py-2" style="background:#775B45;color:#E9E4DC;border:none;">{{ formError }}</div>
        <form @submit.prevent novalidate>
          <div class="row g-2">
            <div class="col-12">
              <label class="form-label fw-semibold" style="color:#2B2414;">Trek Name *</label>
              <input v-model="form.name" class="form-control" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold" style="color:#2B2414;">Location *</label>
              <input v-model="form.location" class="form-control" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold" style="color:#2B2414;">Difficulty *</label>
              <select v-model="form.difficulty" class="form-select" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;">
                <option value="">Select…</option>
                <option>Easy</option><option>Moderate</option><option>Hard</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold" style="color:#2B2414;">Duration (days)</label>
              <input v-model.number="form.duration" type="number" min="1" class="form-control" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold" style="color:#2B2414;">Total Slots</label>
              <input v-model.number="form.available_slots" type="number" min="1" class="form-control" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold" style="color:#2B2414;">Start Date</label>
              <input v-model="form.start_date" type="date" class="form-control" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold" style="color:#2B2414;">End Date</label>
              <input v-model="form.end_date" type="date" class="form-control" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
            </div>
            <div v-if="editingTrek" class="col-12">
              <label class="form-label fw-semibold" style="color:#2B2414;">Status</label>
              <select v-model="form.status" class="form-select" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;">
                <option>Pending</option><option>Approved</option>
                <option>Open</option><option>Closed</option><option>Completed</option>
              </select>
            </div>
          </div>
          <div class="d-flex gap-2 mt-3">
            <button type="button" class="btn fw-semibold" style="background:#585D27;border:none;color:#E9E4DC;" @click="saveTrek">Save</button>
            <button type="button" class="btn" style="border-color:#BCA890;color:#775B45;" @click="showModal=false">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Assign Staff Modal -->
    <div v-if="showAssign" class="modal-overlay" @click.self="showAssign=false">
      <div class="card shadow p-4" style="width:100%;max-width:400px;background:#E9E4DC;">
        <h5 class="mb-3 fw-bold" style="color:#585D27;">Assign Staff to "{{ assignTrek?.name }}"</h5>
        <select v-model="selectedStaff" class="form-select mb-3" style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;">
          <option value="">— Select Staff —</option>
          <option v-for="s in staffList" :key="s.id" :value="s.id">{{ s.name }} ({{ s.email }})</option>
        </select>
        <div class="d-flex gap-2">
          <button class="btn fw-semibold" style="background:#585D27;border:none;color:#E9E4DC;" @click="assignStaff">Assign</button>
          <button class="btn" style="border-color:#BCA890;color:#775B45;" @click="showAssign=false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const treks = ref([])
const staffList = ref([])
const loading = ref(true)
const search = ref('')
const showModal = ref(false)
const showAssign = ref(false)
const editingTrek = ref(null)
const assignTrek = ref(null)
const selectedStaff = ref('')
const formError = ref('')
const form = ref({ name:'', location:'', difficulty:'', duration:1, available_slots:10, start_date:'', end_date:'', status:'Pending' })

const filteredTreks = computed(() =>
  treks.value.filter(t => t.name.toLowerCase().includes(search.value.toLowerCase()))
)

onMounted(async () => {
  await loadTreks()
  const { data } = await api.get('/admin/staff')
  staffList.value = data
  loading.value = false
})

async function loadTreks() {
  const { data } = await api.get('/admin/treks')
  treks.value = data
}

function openCreate() {
  editingTrek.value = null
  form.value = { name:'', location:'', difficulty:'', duration:1, available_slots:10, start_date:'', end_date:'', status:'Pending' }
  formError.value = ''
  showModal.value = true
}

function openEdit(trek) {
  editingTrek.value = trek
  form.value = { ...trek, start_date: trek.start_date || '', end_date: trek.end_date || '' }
  formError.value = ''
  showModal.value = true
}

function openAssign(trek) {
  assignTrek.value = trek
  selectedStaff.value = trek.assigned_staff_id || ''
  showAssign.value = true
}

async function saveTrek() {
  formError.value = ''
  if (!form.value.name || !form.value.location || !form.value.difficulty) {
    formError.value = 'Name, location and difficulty are required.'
    return
  }
  try {
    if (editingTrek.value) {
      await api.put(`/admin/treks/${editingTrek.value.id}`, form.value)
    } else {
      await api.post('/admin/treks', form.value)
    }
    await loadTreks()
    showModal.value = false
  } catch (e) {
    formError.value = e.response?.data?.message || 'Failed to save trek'
  }
}

async function deleteTrek(id) {
  if (!confirm('Delete this trek?')) return
  await api.delete(`/admin/treks/${id}`)
  await loadTreks()
}

async function assignStaff() {
  if (!selectedStaff.value) return
  await api.put(`/admin/treks/${assignTrek.value.id}/assign-staff`, { staff_id: selectedStaff.value })
  await loadTreks()
  showAssign.value = false
}

const diffBadge = d => ({
  'badge': true, 'bg-success': d === 'Easy',
  'bg-warning text-dark': d === 'Moderate', 'bg-danger': d === 'Hard'
})

const statusBadge = s => ({
  'badge': true, 'bg-secondary': s === 'Pending',
  'bg-info text-dark': s === 'Approved', 'bg-success': s === 'Open',
  'bg-warning text-dark': s === 'Closed', 'bg-dark': s === 'Completed'
})
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; background: rgba(43,36,20,.6);
  display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem;
}
</style>