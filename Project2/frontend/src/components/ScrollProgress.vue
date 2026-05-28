<template>
  <!-- 滚动进度条 -->
  <div class="scroll-progress-bar" :style="{ transform: `scaleX(${scrollProgress / 100})` }" />

  <!-- 回到顶部按钮 -->
  <Transition name="back-to-top">
    <button
      v-if="showBackToTop"
      @click="scrollToTop"
      class="fixed bottom-6 left-6 z-40 group"
      title="回到顶部 (T)"
    >
      <div class="relative">
        <!-- SVG 圆环进度 -->
        <svg class="w-12 h-12 -rotate-90" viewBox="0 0 48 48">
          <circle
            cx="24" cy="24" r="20"
            fill="none"
            stroke="rgba(0, 240, 255, 0.1)"
            stroke-width="3"
          />
          <circle
            cx="24" cy="24" r="20"
            fill="none"
            stroke="url(#progressGradient)"
            stroke-width="3"
            stroke-linecap="round"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="circumference - (circumference * scrollProgress / 100)"
            class="transition-all duration-150"
          />
          <defs>
            <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#00f0ff" />
              <stop offset="100%" stop-color="#ff00e5" />
            </linearGradient>
          </defs>
        </svg>
        <!-- 箭头图标 -->
        <div class="absolute inset-0 flex items-center justify-center">
          <svg class="w-5 h-5 text-neon group-hover:-translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
          </svg>
        </div>
        <!-- 发光效果 -->
        <div class="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity" style="box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);" />
      </div>
    </button>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const scrollY = ref(0)
const docHeight = ref(1)
const winHeight = ref(1)
const showBackToTop = ref(false)

const circumference = 2 * Math.PI * 20 // r=20

const scrollProgress = computed(() => {
  const maxScroll = docHeight.value - winHeight.value
  if (maxScroll <= 0) return 0
  return Math.min(100, (scrollY.value / maxScroll) * 100)
})

const handleScroll = () => {
  scrollY.value = window.scrollY
  showBackToTop.value = scrollY.value > 300
}

const updateDimensions = () => {
  docHeight.value = document.documentElement.scrollHeight
  winHeight.value = window.innerHeight
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 键盘快捷键 T 回到顶部
const handleKeydown = (e) => {
  // 只在没有输入框聚焦时触发
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return
  if (e.key === 't' || e.key === 'T') {
    scrollToTop()
  }
}

let resizeObserver = null

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', updateDimensions, { passive: true })
  document.addEventListener('keydown', handleKeydown)
  updateDimensions()

  // 监听 DOM 变化更新文档高度
  resizeObserver = new ResizeObserver(() => {
    updateDimensions()
  })
  resizeObserver.observe(document.body)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', updateDimensions)
  document.removeEventListener('keydown', handleKeydown)
  if (resizeObserver) resizeObserver.disconnect()
})
</script>

<style scoped>
/* 顶部滚动进度条 */
.scroll-progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #00f0ff, #ff00e5, #39ff14);
  transform-origin: left;
  z-index: 100;
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
}

/* 回到顶部按钮动画 */
.back-to-top-enter-active {
  transition: all 0.3s ease;
}
.back-to-top-leave-active {
  transition: all 0.2s ease;
}
.back-to-top-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.8);
}
.back-to-top-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.8);
}
</style>