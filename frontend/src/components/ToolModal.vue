<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="$emit('close')">
        <!-- 背景遮罩 -->
        <div class="absolute inset-0" style="background: rgba(0,0,0,0.6); backdrop-filter: blur(8px);" />
        
        <!-- 弹窗主体 -->
        <div class="relative w-full max-w-4xl max-h-[90vh] rounded-2xl overflow-hidden animate-modal-in"
             style="background: var(--bg-primary); border: 1px solid var(--border-color); box-shadow: 0 25px 60px rgba(0,0,0,0.5);">
          
          <!-- 顶部标题栏 -->
          <div class="flex items-center justify-between px-6 py-4" style="border-bottom: 1px solid var(--border-color);">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center"
                   :style="{ background: tool?.color + '15', border: '1px solid ' + tool?.color + '30' }">
                <span class="text-sm" v-html="tool?.icon" />
              </div>
              <div>
                <h3 class="text-lg font-bold font-mono" style="color: var(--text-primary);">{{ tool?.name }}</h3>
                <p class="text-xs font-mono" style="color: var(--text-muted);">{{ tool?.description }}</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-[10px] font-mono"
                    :style="{ background: tool?.color + '15', color: tool?.color, border: '1px solid ' + tool?.color + '30' }">
                {{ tool?.category }}
              </span>
              <button @click="$emit('close')"
                      class="w-8 h-8 rounded-lg flex items-center justify-center transition-colors hover:opacity-80"
                      style="background: var(--bg-secondary); border: 1px solid var(--border-color);">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: var(--text-muted);">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 工具内容区 -->
          <div class="overflow-y-auto" style="max-height: calc(90vh - 70px);">
            <div class="p-6">
              <slot />
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  show: Boolean,
  tool: Object
})
defineEmits(['close'])
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.animate-modal-in {
  animation: modalIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes modalIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
