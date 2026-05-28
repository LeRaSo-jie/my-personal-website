<template>
  <button
    @click="toggleTheme"
    class="p-2 rounded-lg transition-all duration-300"
    :style="isDark 
      ? 'background: rgba(255, 230, 0, 0.08); border: 1px solid rgba(255, 230, 0, 0.15);' 
      : 'background: rgba(0, 243, 255, 0.08); border: 1px solid rgba(0, 243, 255, 0.15);'"
    :title="isDark ? '切换到浅色模式' : '切换到深色模式'"
  >
    <!-- 太阳图标（深色模式时显示，点击切换到浅色） -->
    <svg
      v-if="isDark"
      class="w-5 h-5 text-neon-yellow"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>
    <!-- 月亮图标（浅色模式时显示，点击切换到深色） -->
    <svg
      v-else
      class="w-5 h-5 text-neon"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
      />
    </svg>
  </button>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// 深色模式状态（赛博朋克默认深色）
const isDark = ref(true)

// 切换主题
const toggleTheme = () => {
  isDark.value = !isDark.value
  updateTheme()
}

// 更新 DOM 上的 dark class
const updateTheme = () => {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  // 保存到 localStorage
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// 初始化主题
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDark.value = savedTheme === 'dark'
  } else {
    // 默认深色（赛博朋克风格）
    isDark.value = true
  }
  updateTheme()
})
</script>
