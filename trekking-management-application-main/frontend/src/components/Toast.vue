<template>
  <div style="position:fixed;top:20px;right:20px;z-index:9999;min-width:300px;">
    <div v-for="toast in toasts" :key="toast.id"
         class="alert fw-semibold shadow mb-2 d-flex align-items-center gap-2"
         :style="toast.type === 'success'
           ? 'background:#585D27;color:#E9E4DC;border:none;'
           : 'background:#775B45;color:#E9E4DC;border:none;'">
      <span>{{ toast.type === 'success' ? '✅' : '❌' }}</span>
      <span>{{ toast.message }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])

function show(message, type = 'success') {
  const id = Date.now()
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 4000)
}

defineExpose({ show })
</script>