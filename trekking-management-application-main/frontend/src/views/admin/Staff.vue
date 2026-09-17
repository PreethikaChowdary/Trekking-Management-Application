<template>
  <div class="container-fluid py-4 px-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="fw-bold mb-0" style="color:#E9E4DC;">Manage Staff</h4>
      <button class="btn fw-semibold" style="background:#585D27;border:none;color:#E9E4DC;" @click="showModal=true">+ Add Staff</button>
    </div>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else class="table-responsive">
      <table class="table table-hover align-middle rounded shadow-sm" style="background:#E9E4DC;">
        <thead style="background:#BCA890;color:#2B2414;">
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Email</th>
            <th>Contact</th>
            <th>Assigned Treks</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(s, index) in staff" :key="s.id">
            <td style="color:#2B2414;">{{ index + 1 }}</td>
            <td class="fw-semibold" style="color:#2B2414;">{{ s.name }}</td>
            <td style="color:#2B2414;">{{ s.email }}</td>
            <td style="color:#2B2414;">{{ s.contact || '—' }}</td>
            <td>
              <span v-if="s.assigned_treks?.length">
                <span v-for="t in s.assigned_treks" :key="t.id"
                      class="badge me-1" style="background:#585D27;">{{ t.name }}</span>
              </span>
              <span v-else style="color:#775B45;">None</span>
            </td>
            <td>
              <span class="badge"
                    :style="s.is_active ? 'background:#585D27;' : 'background:#775B45;'">
                {{ s.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td>
              <div class="d-flex gap-1">
                <button class="btn btn-sm text-white"
                        :style="s.is_active ? 'background:#775B45;border:none;' : 'background:#585D27;border:none;'"
                        @click="toggleStatus(s.id)">
                  {{ s.is_active ? 'Deactivate' : 'Activate' }}
                </button>
                <button class="btn btn-sm text-white"
                        style="background:#2B2414;border:none;"
                        @click="deleteStaff(s.id)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!staff.length">
            <td colspan="7" class="text-center py-4" style="color:#775B45;">No staff added yet.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Staff Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal=false">
      <div class="card shadow p-4" style="width:100%;max-width:440px;background:#E9E4DC;">
        <h5 class="mb-3 fw-bold" style="color:#585D27;">Add Trek Staff</h5>
        <div v-if="formError" class="alert py-2" style="background:#775B45;color:#E9E4DC;border:none;">{{ formError }}</div>
        <form @submit.prevent novalidate>
          <div class="mb-2">
            <label class="form-label fw-semibold" style="color:#2B2414;">Full Name *</label>
            <input v-model="form.name" class="form-control"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="mb-2">
            <label class="form-label fw-semibold" style="color:#2B2414;">Email *</label>
            <input v-model="form.email" type="email" class="form-control"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="mb-2">
            <label class="form-label fw-semibold" style="color:#2B2414;">Password *</label>
            <input v-model="form.password" type="password" class="form-control"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="mb-2">
            <label class="form-label fw-semibold" style="color:#2B2414;">Contact</label>
            <input v-model="form.contact" class="form-control"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold" style="color:#2B2414;">Experience (years)</label>
            <input v-model.number="form.experience_years" type="number" min="0" class="form-control"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="d-flex gap-2">
            <button type="button" class="btn fw-semibold"
                    style="background:#585D27;border:none;color:#E9E4DC;"
                    @click="createStaff">Create</button>
            <button type="button" class="btn"
                    style="border-color:#BCA890;color:#775B45;"
                    @click="showModal=false">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const staff = ref([])
const loading = ref(true)
const showModal = ref(false)
const formError = ref('')
const form = ref({ name:'', email:'', password:'', contact:'', experience_years:0 })

onMounted(async () => {
  await loadStaff()
  loading.value = false
})

async function loadStaff() {
  const { data } = await api.get('/admin/staff')
  staff.value = data
}

async function createStaff() {
  formError.value = ''
  if (!form.value.name || !form.value.email || !form.value.password) {
    formError.value = 'Name, email and password are required.'
    return
  }
  try {
    await api.post('/admin/staff', form.value)
    await loadStaff()
    showModal.value = false
    form.value = { name:'', email:'', password:'', contact:'', experience_years:0 }
  } catch (e) {
    formError.value = e.response?.data?.message || 'Failed to create staff'
  }
}

async function toggleStatus(id) {
  await api.put(`/admin/users/${id}/deactivate`)
  await loadStaff()
}

async function deleteStaff(id) {
  if (!confirm('Are you sure you want to delete this staff member? Their assigned treks will be unassigned.')) return
  try {
    await api.delete(`/admin/staff/${id}`)
    await loadStaff()
  } catch (e) {
    alert(e.response?.data?.message || 'Failed to delete staff')
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; background: rgba(43,36,20,.6);
  display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem;
}
</style>