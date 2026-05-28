<template>
  <div v-if="isAdmin" class="absolute top-2 right-2 flex gap-1 z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
    <button 
      @click.stop="$emit('edit')"
      class="p-1.5 rounded-lg transition-all duration-200"
      style="background: rgba(0, 243, 255, 0.08); border: 1px solid rgba(0, 243, 255, 0.15);"
      title="编辑"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-neon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
      </svg>
    </button>
    <button 
      @click.stop="$emit('delete')"
      class="p-1.5 rounded-lg transition-all duration-200"
      style="background: rgba(255, 45, 117, 0.08); border: 1px solid rgba(255, 45, 117, 0.15);"
      title="删除"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-neon-pink" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { getAdminStatus } from '../composables/useApi'

const isAdmin = getAdminStatus()

defineEmits(['edit', 'delete'])
</script>
