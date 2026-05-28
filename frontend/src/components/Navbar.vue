<template>
  <nav class="fixed top-0 left-0 right-0 z-50 glass">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2 group">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center"
               style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(139, 92, 246, 0.15)); border: 1px solid rgba(14, 165, 233, 0.2);">
            <span class="text-neon font-bold font-mono text-sm">N</span>
          </div>
          <span class="text-lg font-bold font-mono tracking-wider">
            <span class="text-neon">DIGITAL</span><span style="color: var(--text-primary);"> NEXUS</span>
          </span>
        </router-link>

        <!-- 桌面端导航链接 -->
        <div class="hidden md:flex items-center space-x-1">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="relative px-4 py-2 text-sm font-medium transition-all duration-300 rounded-lg group"
            :class="$route.path === link.path ? 'text-neon' : ''"
            :style="$route.path !== link.path ? 'color: var(--text-secondary)' : ''"
          >
            <div v-if="$route.path === link.path"
                 class="absolute inset-0 rounded-lg"
                 style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.15);">
            </div>
            <div v-else
                 class="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"
                 style="background: rgba(14, 165, 233, 0.04);">
            </div>
            <span class="relative font-mono text-xs tracking-wider">{{ link.name }}</span>
          </router-link>
          <div class="ml-3 pl-3" style="border-left: 1px solid var(--border-color);">
            <ThemeToggle />
          </div>
        </div>

        <!-- 移动端汉堡菜单按钮 -->
        <div class="md:hidden flex items-center space-x-4">
          <ThemeToggle />
          <button
            @click="isMenuOpen = !isMenuOpen"
            class="p-2 rounded-lg transition-all duration-200"
            style="background: rgba(14, 165, 233, 0.05); border: 1px solid var(--border-color);"
          >
            <svg class="w-5 h-5 text-neon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!isMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 移动端菜单 -->
    <div v-if="isMenuOpen" class="md:hidden glass">
      <div class="px-4 py-4 space-y-1">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          @click="isMenuOpen = false"
          class="block px-4 py-2.5 rounded-lg text-sm font-mono transition-all duration-200"
          :class="$route.path === link.path ? 'text-neon' : ''"
          :style="$route.path === link.path 
            ? 'background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.15);' 
            : 'color: var(--text-secondary); border: 1px solid transparent;'"
        >
          {{ link.name }}
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import ThemeToggle from './ThemeToggle.vue'

const isMenuOpen = ref(false)

const navLinks = [
  { path: '/', name: '首页' },
  { path: '/resume', name: '简历' },
  { path: '/portfolio', name: '作品集' },
  { path: '/tools', name: '工具箱' },
  { path: '/blog', name: '博客' },
  { path: '/code', name: '代码' },
]
</script>
