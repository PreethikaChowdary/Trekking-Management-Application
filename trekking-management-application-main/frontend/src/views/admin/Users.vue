<template>
  <div class="container-fluid py-4 px-4">
    <h4 class="fw-bold mb-4" style="color:#E9E4DC;">Manage Users</h4>

    <div class="mb-3">
      <input v-model="search" class="form-control" placeholder="🔍 Search users…"
             style="max-width:400px;border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
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
            <th>Bookings</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(u, index) in filteredUsers" :key="u.id">
            <td style="color:#2B2414;">{{ index + 1 }}</td>
            <td class="fw-semibold" style="color:#2B2414;">{{ u.name }}</td>
            <td style="color:#2B2414;">{{ u.email }}</td>
            <td style="color:#2B2414;">{{ u.contact || '—' }}</td>
            <td style="color:#2B2414;">{{ u.booking_count }}</td>
            <td>
              <span class="badge"
                    :style="u.is_active ? 'background:#585D27;' : 'background:#775B45;'">
                {{ u.is_active ? 'Active' : 'Blacklisted' }}
              </span>
            </td>
            <td>
              <div class="d-flex gap-1">
                <button class="btn btn-sm text-white"
                        :style="u.is_active ? 'background:#775B45;border:none;' : 'background:#585D27;border:none;'"
                        @click="toggleStatus(u.id)">
                  {{ u.is_active ? 'Blacklist' : 'Activate' }}
                </button>
                <button class="btn btn-sm text-white"
                        style="background:#2B2414;border:none;"
                        @click="deleteUser(u.id)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!filteredUsers.length">
            <td colspan="7" class="text-center py-4" style="color:#775B45;">No users found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const users = ref([])
const loading = ref(true)
const search = ref('')

const filteredUsers = computed(() =>
  users.value.filter(u =>
    u.name.toLowerCase().includes(search.value.toLowerCase()) ||
    u.email.toLowerCase().includes(search.value.toLowerCase())
  )
)

onMounted(async () => {
  await loadUsers()
  loading.value = false
})

async function loadUsers() {
  const { data } = await api.get('/admin/users')
  users.value = data
}

async function toggleStatus(id) {
  const { data } = await api.put(`/admin/users/${id}/deactivate`)
  const user = users.value.find(u => u.id === id)
  if (user) user.is_active = data.is_active
}

async function deleteUser(id) {
  if (!confirm('Are you sure you want to delete this user? This cannot be undone.')) return
  try {
    await api.delete(`/admin/users/${id}`)
    await loadUsers()
  } catch (e) {
    alert(e.response?.data?.message || 'Failed to delete user')
  }
}
</script>