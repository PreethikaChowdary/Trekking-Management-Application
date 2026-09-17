<template>
  <div class="container py-4" style="max-width:520px;">
    <h4 class="fw-bold mb-4" style="color:#E9E4DC;">My Profile</h4>

    <div v-if="loading" class="text-center py-5"><div class="spinner-border" style="color:#E9E4DC;"></div></div>

    <div v-else class="card border-0 shadow-sm" style="background:#E9E4DC;">
      <div class="card-body p-4">
        <div class="text-center mb-4">
          <div class="rounded-circle d-inline-flex align-items-center justify-content-center fw-bold"
               style="width:80px;height:80px;font-size:2rem;background:#585D27;color:#E9E4DC;">
            {{ profile.name?.charAt(0)?.toUpperCase() }}
          </div>
          <div class="mt-2 small" style="color:#775B45;">{{ profile.email }}</div>
          <span class="badge mt-1" style="background:#585D27;">{{ profile.role }}</span>
        </div>

        <div v-if="msg" class="alert py-2"
             style="background:#585D27;color:#E9E4DC;border-color:#585D27;">{{ msg }}</div>
        <div v-if="error" class="alert py-2"
             style="background:#775B45;color:#E9E4DC;border-color:#775B45;">{{ error }}</div>

        <form @submit.prevent="saveProfile" novalidate>
          <div class="mb-3">
            <label class="form-label fw-semibold" style="color:#2B2414;">Full Name</label>
            <input v-model="form.name" class="form-control" required
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold" style="color:#2B2414;">Email</label>
            <input :value="profile.email" class="form-control" disabled
                   style="border-color:#BCA890;background:#BCA890;color:#2B2414;" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold" style="color:#2B2414;">Contact</label>
            <input v-model="form.contact" class="form-control" placeholder="Phone number"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <button type="submit" class="btn w-100 fw-semibold"
                  style="background:#585D27;border:none;color:#E9E4DC;" :disabled="saving">
            {{ saving ? 'Saving…' : 'Save Changes' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const profile = ref({})
const form = ref({ name: '', contact: '' })
const loading = ref(true)
const saving = ref(false)
const msg = ref('')
const error = ref('')

onMounted(async () => {
  const { data } = await api.get('/user/profile')
  profile.value = data
  form.value = { name: data.name, contact: data.contact || '' }
  loading.value = false
})

async function saveProfile() {
  msg.value = ''
  error.value = ''
  if (!form.value.name) { error.value = 'Name is required.'; return }
  saving.value = true
  try {
    await api.put('/user/profile', form.value)
    profile.value.name = form.value.name
    const stored = JSON.parse(localStorage.getItem('user') || '{}')
    stored.name = form.value.name
    localStorage.setItem('user', JSON.stringify(stored))
    msg.value = 'Profile updated successfully!'
    setTimeout(() => msg.value = '', 4000)
  } catch (e) {
    error.value = e.response?.data?.message || 'Update failed'
  } finally {
    saving.value = false
  }
}
</script>