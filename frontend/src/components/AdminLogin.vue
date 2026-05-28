<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50" style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px);" @click.self="close">
    <div class="card-neon p-8 w-96">
      <div class="text-center mb-6">
        <div class="w-14 h-14 mx-auto mb-4 rounded-full flex items-center justify-center"
             style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.2);">
          <svg class="h-7 w-7 text-neon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold font-mono" style="color: var(--text-primary);">ADMIN ACCESS</h2>
        <p class="text-xs font-mono mt-1" style="color: var(--text-muted);">请输入管理员密码</p>
      </div>
      <input v-model="password" type="password" placeholder="Password..." class="input-cyber mb-4 font-mono" @keyup.enter="login" />
      <div class="flex gap-3">
        <button @click="login" class="btn-primary flex-1 font-mono">CONNECT</button>
        <button @click="close" class="btn-secondary flex-1 font-mono">CANCEL</button>
      </div>
      <p v-if="error" class="text-neon-pink text-xs mt-3 text-center font-mono"><span class="opacity-60">></span> {{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { loginAsAdmin, verifyAdmin } from '../composables/useApi'

const props = defineProps(['show'])
const emit = defineEmits(['close', 'success'])
const password = ref(''); const error = ref('')

const login = async () => {
  error.value = ''
  const success = await verifyAdmin(password.value)
  if (success) { loginAsAdmin(password.value); emit('success'); emit('close'); password.value = ''; window.location.reload() }
  else { error.value = 'ACCESS DENIED' }
}
const close = () => { emit('close'); password.value = ''; error.value = '' }
</script>
