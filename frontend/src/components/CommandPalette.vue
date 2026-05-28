<template>
  <Teleport to="body">
    <Transition name="palette">
      <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh]" @click.self="close">
        <!-- 遮罩 -->
        <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="close" />

        <!-- 面板 -->
        <div class="relative w-full max-w-xl mx-4 rounded-2xl overflow-hidden" style="background: var(--bg-secondary); border: 1px solid var(--border-color); box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);">

          <!-- 搜索输入 -->
          <div class="flex items-center gap-3 px-5 py-4" style="border-bottom: 1px solid var(--border-color);">
            <svg class="w-5 h-5 flex-shrink-0 text-neon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              ref="searchInput"
              v-model="query"
              type="text"
              placeholder="搜索页面、功能、项目..."
              class="flex-1 bg-transparent outline-none text-base font-mono"
              style="color: var(--text-primary);"
              @keydown.escape="close"
              @keydown.down.prevent="moveDown"
              @keydown.up.prevent="moveUp"
              @keydown.enter="selectCurrent"
            />
            <kbd class="hidden sm:inline-flex items-center px-2 py-0.5 rounded text-xs font-mono" style="background: rgba(255,255,255,0.06); color: var(--text-tertiary); border: 1px solid var(--border-color);">
              ESC
            </kbd>
          </div>

          <!-- 搜索结果 -->
          <div class="max-h-[50vh] overflow-y-auto py-2 px-2" ref="resultsList">
            <!-- 无结果 -->
            <div v-if="filteredResults.length === 0 && query.length > 0" class="py-8 text-center">
              <div class="text-3xl mb-2">🔍</div>
              <p class="text-sm font-mono" style="color: var(--text-tertiary);">
                没有找到 "{{ query }}" 的结果
              </p>
              <p class="text-xs mt-1" style="color: var(--text-tertiary);">
                试试其他关键词
              </p>
            </div>

            <!-- 默认建议 -->
            <div v-if="query.length === 0">
              <div class="px-3 py-1.5 text-xs font-mono uppercase tracking-wider" style="color: var(--text-tertiary);">
                快速导航
              </div>
              <button
                v-for="(item, index) in quickLinks"
                :key="item.id"
                @click="navigate(item)"
                @mouseenter="selectedIndex = index"
                class="result-item w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-all duration-150"
                :class="selectedIndex === index ? 'result-active' : ''"
              >
                <span class="text-lg">{{ item.icon }}</span>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-medium" style="color: var(--text-primary);">{{ item.title }}</div>
                  <div class="text-xs truncate" style="color: var(--text-tertiary);">{{ item.description }}</div>
                </div>
                <svg class="w-4 h-4 flex-shrink-0" style="color: var(--text-tertiary);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            <!-- 搜索结果分组 -->
            <template v-if="filteredResults.length > 0">
              <div
                v-for="group in groupedResults"
                :key="group.category"
              >
                <div class="px-3 py-1.5 text-xs font-mono uppercase tracking-wider" style="color: var(--text-tertiary);">
                  {{ group.category }}
                </div>
                <button
                  v-for="item in group.items"
                  :key="item.id"
                  @click="navigate(item)"
                  @mouseenter="selectedIndex = getGlobalIndex(item)"
                  class="result-item w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-all duration-150"
                  :class="selectedIndex === getGlobalIndex(item) ? 'result-active' : ''"
                >
                  <span class="text-lg">{{ item.icon }}</span>
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium" style="color: var(--text-primary);">{{ item.title }}</div>
                    <div class="text-xs truncate" style="color: var(--text-tertiary);">{{ item.description }}</div>
                  </div>
                  <kbd v-if="item.shortcut" class="hidden sm:inline-flex items-center px-1.5 py-0.5 rounded text-xs font-mono" style="background: rgba(255,255,255,0.06); color: var(--text-tertiary); border: 1px solid var(--border-color);">
                    {{ item.shortcut }}
                  </kbd>
                </button>
              </div>
            </template>
          </div>

          <!-- 底部提示 -->
          <div class="flex items-center justify-between px-4 py-2.5 text-xs font-mono" style="background: rgba(0,0,0,0.2); border-top: 1px solid var(--border-color); color: var(--text-tertiary);">
            <div class="flex items-center gap-3">
              <span class="flex items-center gap-1">
                <kbd class="px-1 py-0.5 rounded" style="background: rgba(255,255,255,0.06); border: 1px solid var(--border-color);">↑↓</kbd>
                导航
              </span>
              <span class="flex items-center gap-1">
                <kbd class="px-1 py-0.5 rounded" style="background: rgba(255,255,255,0.06); border: 1px solid var(--border-color);">↵</kbd>
                打开
              </span>
              <span class="flex items-center gap-1">
                <kbd class="px-1 py-0.5 rounded" style="background: rgba(255,255,255,0.06); border: 1px solid var(--border-color);">esc</kbd>
                关闭
              </span>
            </div>
            <span class="text-neon">YuJie's Portfolio</span>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isOpen = ref(false)
const query = ref('')
const selectedIndex = ref(0)
const searchInput = ref(null)
const resultsList = ref(null)

// 所有可搜索项
const allItems = [
  // 页面
  { id: 'home', title: '首页', description: '回到主页，查看个人介绍', icon: '🏠', path: '/', category: '页面', keywords: ['home', '首页', '主页', '介绍'] },
  { id: 'resume', title: '简历', description: '查看教育背景、工作经历、技能', icon: '📄', path: '/resume', category: '页面', keywords: ['resume', '简历', '经历', '技能', '教育'] },
  { id: 'portfolio', title: '作品集', description: '浏览项目作品和技术方案', icon: '💼', path: '/portfolio', category: '页面', keywords: ['portfolio', '作品', '项目', '案例'] },
  { id: 'tools', title: '工具箱', description: '在线开发小工具 + 工具包资源下载', icon: '🛠️', path: '/tools', category: '页面', keywords: ['tools', '工具', 'json', 'base64', 'hash', '下载', 'download', '工具包', '压缩包'] },
  { id: 'blog', title: '技术博客', description: '技术笔记、踩坑记录、学习心得', icon: '📝', path: '/blog', category: '页面', keywords: ['blog', '博客', '文章', '笔记', '技术'] },
  { id: 'code', title: '代码动态', description: 'GitHub & Gitee 活动面板和贡献统计', icon: '🐙', path: '/code', category: '页面', keywords: ['github', 'gitee', 'git', '代码', '仓库', '贡献', 'code'] },
  { id: 'playground', title: '互动彩蛋', description: '试试 Konami Code、贪吃蛇等小游戏（快捷键 G）', icon: '🎮', path: '/playground', category: '页面', keywords: ['playground', '游戏', '彩蛋', 'snake', '贪吃蛇'] },

  // 技能
  { id: 'skill-vue', title: 'Vue.js', description: '前端框架 - Composition API', icon: '💚', path: '/resume', category: '技能', keywords: ['vue', 'vuejs', '前端', '框架'] },
  { id: 'skill-python', title: 'Python', description: '后端开发 - Flask / Django', icon: '🐍', path: '/resume', category: '技能', keywords: ['python', 'flask', 'django', '后端'] },
  { id: 'skill-docker', title: 'Docker', description: '容器化部署', icon: '🐳', path: '/resume', category: '技能', keywords: ['docker', '容器', '部署'] },
  { id: 'skill-ts', title: 'TypeScript', description: '类型安全的 JavaScript', icon: '🔷', path: '/resume', category: '技能', keywords: ['typescript', 'ts', '类型'] },
  { id: 'skill-pg', title: 'PostgreSQL', description: '关系型数据库', icon: '🐘', path: '/resume', category: '技能', keywords: ['postgres', 'postgresql', '数据库', 'sql'] },

  // 操作
  { id: 'action-theme', title: '切换主题', description: '在亮色和暗色模式之间切换', icon: '🎨', action: 'toggleTheme', category: '操作', keywords: ['theme', '主题', '暗色', '亮色', 'dark', 'light'], shortcut: 'T' },
]

// 快速导航
const quickLinks = computed(() => {
  return [
    allItems.find(i => i.id === 'home'),
    allItems.find(i => i.id === 'resume'),
    allItems.find(i => i.id === 'portfolio'),
    allItems.find(i => i.id === 'tools'),
    allItems.find(i => i.id === 'blog'),
    allItems.find(i => i.id === 'code'),
    allItems.find(i => i.id === 'playground'),
    allItems.find(i => i.id === 'action-theme'),
  ]
})

// 过滤结果
const filteredResults = computed(() => {
  if (!query.value) return []
  const q = query.value.toLowerCase()
  return allItems.filter(item => {
    return item.title.toLowerCase().includes(q) ||
           item.description.toLowerCase().includes(q) ||
           item.keywords.some(k => k.includes(q))
  })
})

// 分组结果
const groupedResults = computed(() => {
  const groups = {}
  filteredResults.value.forEach(item => {
    if (!groups[item.category]) groups[item.category] = []
    groups[item.category].push(item)
  })
  return Object.entries(groups).map(([category, items]) => ({ category, items }))
})

// 全局索引
const getGlobalIndex = (item) => {
  return filteredResults.value.findIndex(r => r.id === item.id)
}

const totalItems = computed(() => {
  return query.value ? filteredResults.value.length : quickLinks.value.length
})

// 键盘导航
const moveDown = () => {
  selectedIndex.value = (selectedIndex.value + 1) % totalItems.value
  scrollToSelected()
}

const moveUp = () => {
  selectedIndex.value = (selectedIndex.value - 1 + totalItems.value) % totalItems.value
  scrollToSelected()
}

const scrollToSelected = () => {
  nextTick(() => {
    if (resultsList.value) {
      const active = resultsList.value.querySelector('.result-active')
      if (active) {
        active.scrollIntoView({ block: 'nearest' })
      }
    }
  })
}

const selectCurrent = () => {
  if (query.value) {
    if (filteredResults.value[selectedIndex.value]) {
      navigate(filteredResults.value[selectedIndex.value])
    }
  } else {
    navigate(quickLinks.value[selectedIndex.value])
  }
}

// 导航
const navigate = (item) => {
  if (!item) return
  close()

  if (item.action === 'toggleTheme') {
    document.documentElement.classList.toggle('dark')
    return
  }

  if (item.path) {
    router.push(item.path)
  }
}

// 打开/关闭
const open = () => {
  isOpen.value = true
  query.value = ''
  selectedIndex.value = 0
  nextTick(() => {
    searchInput.value?.focus()
  })
}

const close = () => {
  isOpen.value = false
  query.value = ''
  selectedIndex.value = 0
}

// Ctrl+K 全局快捷键
const handleKeydown = (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    if (isOpen.value) {
      close()
    } else {
      open()
    }
  }
}

// 查询变化时重置选中
watch(query, () => {
  selectedIndex.value = 0
})

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})

defineExpose({ open, close })
</script>

<style scoped>
/* 结果项 */
.result-item {
  color: var(--text-secondary, #aaa);
}
.result-item:hover,
.result-active {
  background: rgba(0, 240, 255, 0.08);
}
.result-active {
  box-shadow: inset 2px 0 0 #00f0ff;
}

/* 滚动条 */
.max-h-\[50vh\] {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 240, 255, 0.2) transparent;
}
.max-h-\[50vh\]::-webkit-scrollbar {
  width: 4px;
}
.max-h-\[50vh\]::-webkit-scrollbar-thumb {
  background: rgba(0, 240, 255, 0.2);
  border-radius: 2px;
}

/* 动画 */
.palette-enter-active {
  transition: all 0.2s ease;
}
.palette-leave-active {
  transition: all 0.15s ease;
}
.palette-enter-from {
  opacity: 0;
}
.palette-leave-to {
  opacity: 0;
}
.palette-enter-from > div:last-child {
  transform: scale(0.96) translateY(-10px);
}
.palette-leave-to > div:last-child {
  transform: scale(0.96) translateY(-10px);
}

/* 输入框 placeholder */
input::placeholder {
  color: var(--text-tertiary, #666);
}
</style>