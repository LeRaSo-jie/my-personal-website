<template>
  <div class="min-h-screen transition-colors duration-300" style="background: var(--bg-primary);">
    <!-- 全局页面加载进度条 -->
    <Transition name="loading-bar">
      <div v-if="isPageLoading" class="page-loading-bar" />
    </Transition>
    <Navbar />
    <main>
      <router-view v-slot="{ Component, route }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="route.path" />
        </Transition>
      </router-view>
    </main>
    <Footer v-if="route.path !== '/'" />
    <CommandPalette />
    <ScrollProgress />
    
    <!-- 管理员登录按钮（固定在右下角） -->
    <button
      v-if="!isAdmin"
      @click="showLogin = true"
      class="fixed bottom-6 right-6 p-3 rounded-full transition-all duration-300 z-40 group"
      style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.2);"
      title="管理员登录"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neon group-hover:drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </button>
    
    <!-- 管理员操作按钮组（已登录时显示） -->
    <div v-if="isAdmin" class="fixed bottom-6 right-6 flex flex-col gap-3 z-40">
      <!-- 日志按钮 -->
      <router-link
        to="/logs"
        class="p-3 rounded-full transition-all duration-300 group"
        style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2);"
        title="活动日志"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neon-purple group-hover:drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
      </router-link>
      
      <!-- 登出按钮 -->
      <button
        @click="showLogoutConfirm = true"
        class="p-3 rounded-full transition-all duration-300 group"
        style="background: rgba(236, 72, 153, 0.1); border: 1px solid rgba(236, 72, 153, 0.2);"
        title="管理员登出"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neon-pink group-hover:drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
      </button>
    </div>
    
    <!-- 管理员登录弹窗 -->
    <AdminLogin :show="showLogin" @close="showLogin = false" @success="onLoginSuccess" />
    
    <!-- 登出确认弹窗 -->
    <div v-if="showLogoutConfirm" class="fixed inset-0 flex items-center justify-center z-50" style="background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px);" @click.self="showLogoutConfirm = false">
      <div class="card-neon p-8 w-full max-w-sm mx-4 text-center">
        <div class="w-16 h-16 mx-auto mb-5 rounded-full flex items-center justify-center"
             style="background: rgba(236, 72, 153, 0.1); border: 1px solid rgba(236, 72, 153, 0.2);">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-neon-pink" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </div>
        <h2 class="text-xl font-bold mb-2 font-mono" style="color: var(--text-primary);">退出管理员模式</h2>
        <p class="text-sm mb-6" style="color: var(--text-secondary);">确定要退出管理员模式吗？</p>
        <div class="flex gap-3">
          <button @click="showLogoutConfirm = false" class="btn-secondary flex-1">取消</button>
          <button @click="confirmLogout" class="flex-1 px-4 py-2.5 rounded-lg font-medium transition-all duration-300"
                  style="background: linear-gradient(135deg, #ec4899, #f472b6); color: white; box-shadow: 0 2px 8px rgba(236, 72, 153, 0.25);">
            确定退出
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import AdminLogin from './components/AdminLogin.vue'
import CommandPalette from './components/CommandPalette.vue'
import ScrollProgress from './components/ScrollProgress.vue'
import { checkAdminOnLoad, logoutAdmin } from './composables/useApi'

const router = useRouter()
const route = useRoute()

const showLogin = ref(false)
const showLogoutConfirm = ref(false)
const isAdmin = ref(false)
const isPageLoading = ref(false)

// 全局页面切换 loading 指示器 (G-5)
router.beforeEach(() => {
  isPageLoading.value = true
})
router.afterEach(() => {
  setTimeout(() => {
    isPageLoading.value = false
  }, 400)
})

const onLoginSuccess = () => { isAdmin.value = true }

const confirmLogout = () => {
  logoutAdmin()
  isAdmin.value = false
  showLogoutConfirm.value = false
  if (route.path === '/logs') {
    router.push('/')
  } else {
    window.location.reload()
  }
}

// 快捷键导航 (F-C4)
const navOrder = ['/', '/resume', '/portfolio', '/tools', '/blog', '/code']
// 按 G 跳转到 Playground（彩蛋入口）

const handleGlobalKeydown = (e) => {
  // 忽略输入框中的快捷键
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return
  // 忽略带修饰键的组合（Ctrl+K 等由 CommandPalette 处理）
  if (e.ctrlKey || e.metaKey || e.altKey) return

  // 数字键 1-6 快速跳转页面
  const num = parseInt(e.key)
  if (num >= 1 && num <= 6 && navOrder[num - 1]) {
    e.preventDefault()
    router.push(navOrder[num - 1])
    return
  }

  // G 键跳转 Playground（彩蛋入口）
  if (e.key === 'g' || e.key === 'G') {
    e.preventDefault()
    router.push('/playground')
    return
  }
}

onMounted(() => {
  isAdmin.value = checkAdminOnLoad()
  document.addEventListener('keydown', handleGlobalKeydown)
})
</script>

<style scoped>
/* 页面切换动画 (F-C2) */
.page-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.page-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* 全局页面加载进度条 (G-5) */
.page-loading-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  z-index: 9999;
  background: linear-gradient(90deg, #0ea5e9, #8b5cf6, #ec4899, #0ea5e9);
  background-size: 300% 100%;
  animation: loading-progress 1.2s ease-in-out infinite;
  box-shadow: 0 0 10px rgba(14, 165, 233, 0.5), 0 0 20px rgba(139, 92, 246, 0.3);
}

@keyframes loading-progress {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.loading-bar-enter-active {
  transition: opacity 0.15s ease;
}
.loading-bar-leave-active {
  transition: opacity 0.4s ease;
}
.loading-bar-enter-from,
.loading-bar-leave-to {
  opacity: 0;
}
</style>
