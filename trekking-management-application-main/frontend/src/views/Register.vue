<template>
  <div class="d-flex justify-content-center align-items-center"
       style="min-height:100vh;background:#775B45;">
    <div class="card shadow" style="width:100%;max-width:440px;border:none;background:#E9E4DC;">
      <div class="card-body p-4">
        <h3 class="text-center mb-1 fw-bold" style="color:#585D27;">🏔️ Join TrekApp</h3>
        <p class="text-center mb-4" style="color:#775B45;">Create your trekker account</p>

        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
        <div v-if="success" class="alert alert-success py-2">{{ success }}</div>

        <form @submit.prevent="register" novalidate>
          <div class="mb-3">
            <label class="form-label fw-semibold" style="color:#2B2414;">Full Name</label>
            <input v-model="form.name" type="text" class="form-control" required placeholder="John Doe"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold" style="color:#2B2414;">Email</label>
            <input v-model="form.email" type="email" class="form-control" required placeholder="you@email.com"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold" style="color:#2B2414;">Password</label>
            <input v-model="form.password" type="password" class="form-control" required placeholder="Min 6 characters"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold" style="color:#2B2414;">Contact (optional)</label>
            <input v-model="form.contact" type="text" class="form-control" placeholder="Phone number"
                   style="border-color:#BCA890;background:#E9E4DC;color:#2B2414;" />
          </div>
          <button type="submit" class="btn w-100 text-white fw-semibold"
                  style="background:#585D27;border:none;" :disabled="loading">
            {{ loading ? 'Registering…' : 'Register' }}
          </button>
        </form>

        <hr style="border-color:#BCA890;" />
        <p class="text-center mb-0" style="color:#775B45;">
          Already have an account?
          <router-link to="/login" style="color:#585D27;">Login</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const form = ref({ name: '', email: '', password: '', contact: '' })
const error = ref('')
const success = ref('')
const loading = ref(false)

async function register() {
  error.value = ''
  success.value = ''
  if (!form.value.name || !form.value.email || !form.value.password) {
    error.value = 'Name, email and password are required.'
    return
  }
  if (form.value.password.length < 6) {
    error.value = 'Password must be at least 6 characters.'
    return
  }
  loading.value = true
  try {
    await api.post('/auth/register', form.value)
    success.value = 'Registration successful! Redirecting to login…'
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>