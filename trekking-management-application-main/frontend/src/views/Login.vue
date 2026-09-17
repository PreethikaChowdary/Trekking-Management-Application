<template>
  <div class="d-flex justify-content-center align-items-center"
       style="min-height:100vh;background:#775B45;">
    <div class="card shadow" style="width:100%;max-width:420px;border:none;background:#E9E4DC;">
      <div class="card-body p-4">
        <h3 class="text-center mb-1 fw-bold" style="color:#585D27;">🏔️ TrekApp</h3>
        <p class="text-center mb-4" style="color:#775B45;">Sign in to your account</p>

        <div v-if="errorVisible" class="alert fw-semibold mb-3"
             style="background:#775B45;color:#E9E4DC;border:none;padding:12px;">
          ⚠️ {{ errorMsg }}
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold" style="color:#2B2414;">Login As</label>
          <select v-model="form.role" class="form-select"
                  style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;">
            <option value="">— Select Role —</option>
            <option value="admin">👑 Admin</option>
            <option value="staff">👷 Trek Staff</option>
            <option value="trekker">🧗 Trekker</option>
          </select>
          <div v-if="errors.role" class="small mt-1 fw-semibold" style="color:#2B2414;">
            ⚠️ {{ errors.role }}
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold" style="color:#2B2414;">Email</label>
          <input v-model="form.email" type="email" class="form-control"
                 placeholder="you@email.com"
                 style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          <div v-if="errors.email" class="small mt-1 fw-semibold" style="color:#2B2414;">
            ⚠️ {{ errors.email }}
          </div>
        </div>

        <div class="mb-4">
          <label class="form-label fw-semibold" style="color:#2B2414;">Password</label>
          <input v-model="form.password" type="password" class="form-control"
                 placeholder="Password"
                 style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          <div v-if="errors.password" class="small mt-1 fw-semibold" style="color:#2B2414;">
            ⚠️ {{ errors.password }}
          </div>
        </div>

        <button type="button" @click="login" class="btn w-100 fw-semibold"
                style="background:#585D27;border:none;color:#E9E4DC;"
                :disabled="loading">
          {{ loading ? 'Signing in…' : 'Login' }}
        </button>

        <hr style="border-color:#BCA890;" />
        <p class="text-center mb-0" style="color:#775B45;">
          New trekker?
          <router-link to="/register" style="color:#585D27;">Create an account</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const form = ref({ role: '', email: '', password: '' })
const errorMsg = ref('')
const errorVisible = ref(false)
const errors = reactive({ role: '', email: '', password: '' })
const loading = ref(false)
let errorTimer = null

function showError(msg) {
  errorMsg.value = msg
  errorVisible.value = true
  if (errorTimer) clearTimeout(errorTimer)
  errorTimer = setTimeout(() => {
    errorVisible.value = false
    errorMsg.value = ''
  }, 8000)
}

function validate() {
  let valid = true
  errors.role = ''
  errors.email = ''
  errors.password = ''

  if (!form.value.role) {
    errors.role = 'Please select a role.'
    valid = false
  }
  if (!form.value.email) {
    errors.email = 'Email is required.'
    valid = false
  }
  if (!form.value.password) {
    errors.password = 'Password is required.'
    valid = false
  }

  if (!valid) {
    if (errorTimer) clearTimeout(errorTimer)
    errorTimer = setTimeout(() => {
      errors.role = ''
      errors.email = ''
      errors.password = ''
    }, 8000)
  }

  return valid
}

async function login() {
  errorVisible.value = false
  errorMsg.value = ''
  errors.role = ''
  errors.email = ''
  errors.password = ''
  if (errorTimer) clearTimeout(errorTimer)

  if (!validate()) return

  loading.value = true

  try {
    const { data } = await api.post('/auth/login', {
      email: form.value.email,
      password: form.value.password
    })

    if (data.role !== form.value.role) {
      showError(`This account is not registered as ${form.value.role}. Please select the correct role.`)
      loading.value = false
      return
    }

    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify({
      name: data.name,
      role: data.role
    }))

    const dashMap = {
      admin: '/admin',
      staff: '/staff',
      trekker: '/user'
    }
    router.push(dashMap[data.role] || '/')

  } catch (e) {
    showError(e.response?.data?.message || 'Invalid email or password. Please try again.')
    loading.value = false
  }
}
</script>