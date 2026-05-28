<template>
  <div class="min-h-screen pt-20 pb-16 px-4">
    <div class="max-w-7xl mx-auto">
      <!-- 页面头部 -->
      <div class="flex justify-between items-center mb-12 animate-fade-in">
        <div>
          <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider mb-4"
                style="background: rgba(3, 105, 161, 0.08); border: 1px solid rgba(3, 105, 161, 0.2); color: var(--accent);">
            // PORTFOLIO
          </span>
          <h1 class="text-4xl md:text-5xl font-bold font-mono gradient-text">作品集</h1>
          <p class="text-sm font-mono mt-2" style="color: var(--text-muted);">// {{ portfolioList.length }} projects loaded</p>
        </div>
        <button v-if="isAdmin" @click="openAddForm" class="btn-primary font-mono">+ 添加作品</button>
      </div>

      <!-- 筛选标签 -->
      <div class="flex flex-wrap gap-2 mb-8 animate-fade-in" style="animation-delay: 0.1s;">
        <button
          v-for="cat in categories"
          :key="cat"
          @click="activeCategory = cat"
          class="px-3 py-1.5 rounded-lg text-xs font-mono transition-all"
          :style="activeCategory === cat
            ? 'background: var(--accent); color: #fff;'
            : 'background: rgba(14,165,233,0.06); border: 1px solid rgba(14,165,233,0.12); color: var(--text-secondary);'"
        >
          {{ cat }}
        </button>
      </div>

      <!-- 作品卡片网格 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(item, index) in filteredList"
          :key="item.id"
          class="portfolio-card card-neon group cursor-pointer"
          :style="{ animationDelay: `${index * 0.08}s` }"
          @click="openDetail(item)"
        >
          <!-- 顶部装饰条 -->
          <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity"
               :style="{ background: `linear-gradient(to right, ${item.accentColor}, transparent)` }"></div>

          <!-- 封面区域 -->
          <div class="portfolio-cover" :style="{ background: item.coverGradient }">
            <!-- 无图片时显示项目图标 -->
            <div class="cover-icon" v-html="item.icon"></div>

            <!-- Hover 叠加层 -->
            <div class="cover-overlay">
              <div class="overlay-content">
                <span class="text-white text-sm font-mono font-semibold">查看详情</span>
                <svg class="w-5 h-5 text-white mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
            </div>

            <!-- 状态角标 -->
            <span v-if="item.status" class="absolute top-3 right-3 px-2 py-0.5 rounded text-[10px] font-mono font-semibold"
                  :style="{ background: item.statusColor + '20', border: `1px solid ${item.statusColor}40`, color: item.statusColor }">
              {{ item.status }}
            </span>
          </div>

          <!-- 内容区域 -->
          <div class="p-5">
            <EditControls @edit="openEditForm(item)" @delete="handleDelete(item.id)" />

            <h3 class="text-lg font-bold mb-2 font-mono group-hover:text-neon transition-colors" style="color: var(--text-primary);">
              {{ item.title }}
            </h3>
            <p class="text-sm mb-3 leading-relaxed line-clamp-2" style="color: var(--text-secondary);">
              {{ item.description }}
            </p>

            <!-- 技术标签 -->
            <div class="flex flex-wrap gap-1.5 mb-4">
              <span v-for="tech in item.tech_stack.slice(0, 4)" :key="tech"
                    class="text-[10px] px-2 py-0.5 rounded font-mono"
                    :style="{ background: item.accentColor + '10', border: `1px solid ${item.accentColor}20`, color: item.accentColor }">
                {{ tech }}
              </span>
              <span v-if="item.tech_stack.length > 4"
                    class="text-[10px] px-2 py-0.5 rounded font-mono"
                    style="background: rgba(148,163,184,0.08); border: 1px solid rgba(148,163,184,0.15); color: var(--text-muted);">
                +{{ item.tech_stack.length - 4 }}
              </span>
            </div>

            <!-- 底部链接 -->
            <div class="flex gap-4 pt-3" style="border-top: 1px solid var(--border-color);">
              <a v-if="item.github_url" :href="item.github_url" target="_blank" @click.stop
                 class="inline-flex items-center gap-1.5 text-xs font-mono transition-colors hover:text-neon" style="color: var(--text-muted);">
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                Source
              </a>
              <a v-if="item.demo_url" :href="item.demo_url" target="_blank" @click.stop
                 class="inline-flex items-center gap-1.5 text-xs font-mono transition-colors hover:text-neon-purple" style="color: var(--text-muted);">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                Demo
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredList.length === 0" class="text-center py-20">
        <div class="text-6xl mb-4 opacity-20">📂</div>
        <p class="font-mono" style="color: var(--text-muted);"><span class="text-neon opacity-40">></span> 暂无作品数据</p>
      </div>

      <!-- ============================================================
           详情弹窗
           ============================================================ -->
      <Teleport to="body">
        <Transition name="modal">
          <div v-if="detailItem" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="closeDetail">
            <div class="modal-backdrop" @click="closeDetail"></div>
            <div class="detail-modal card-neon relative w-full max-w-2xl max-h-[85vh] overflow-y-auto z-10">
              <!-- 关闭按钮 -->
              <button @click="closeDetail"
                      class="absolute top-4 right-4 z-20 w-8 h-8 rounded-full flex items-center justify-center transition-all hover:scale-110"
                      style="background: rgba(0,0,0,0.4); backdrop-filter: blur(8px);">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <!-- 封面大图 -->
              <div class="detail-cover" :style="{ background: detailItem.coverGradient }">
                <div class="cover-icon-large" v-html="detailItem.icon"></div>
                <span v-if="detailItem.status" class="absolute top-4 left-4 px-3 py-1 rounded-lg text-xs font-mono font-semibold"
                      :style="{ background: detailItem.statusColor + '30', border: `1px solid ${detailItem.statusColor}50`, color: detailItem.statusColor }">
                  {{ detailItem.status }}
                </span>
              </div>

              <!-- 内容 -->
              <div class="p-8">
                <h2 class="text-2xl md:text-3xl font-bold font-mono mb-3" style="color: var(--text-primary);">
                  {{ detailItem.title }}
                </h2>

                <!-- 技术标签 -->
                <div class="flex flex-wrap gap-2 mb-6">
                  <span v-for="tech in detailItem.tech_stack" :key="tech"
                        class="text-xs px-3 py-1 rounded-lg font-mono"
                        :style="{ background: detailItem.accentColor + '12', border: `1px solid ${detailItem.accentColor}25`, color: detailItem.accentColor }">
                    {{ tech }}
                  </span>
                </div>

                <!-- 讲故事风格展示 -->
                <div v-if="detailItem.story" class="mb-6 space-y-4">
                  <!-- 背景/问题 -->
                  <div class="story-block" style="border-left: 3px solid #ff00e5;">
                    <div class="story-label" style="color: #ff00e5;">💡 起因</div>
                    <p class="story-text">{{ detailItem.story.problem }}</p>
                  </div>
                  <!-- 解决方案 -->
                  <div class="story-block" style="border-left: 3px solid #00f0ff;">
                    <div class="story-label" style="color: #00f0ff;">🔧 过程</div>
                    <p class="story-text">{{ detailItem.story.solution }}</p>
                  </div>
                  <!-- 成果 -->
                  <div class="story-block" style="border-left: 3px solid #39ff14;">
                    <div class="story-label" style="color: #39ff14;">🎯 成果</div>
                    <p class="story-text">{{ detailItem.story.result }}</p>
                  </div>
                </div>

                <!-- 详细描述（无 story 时回退） -->
                <div v-else class="mb-6 p-4 rounded-xl" style="background: rgba(148,163,184,0.04); border: 1px solid var(--border-color);">
                  <p class="text-sm leading-relaxed font-mono" style="color: var(--text-secondary);">
                    {{ detailItem.fullDescription || detailItem.description }}
                  </p>
                </div>

                <!-- 项目信息 -->
                <div class="grid grid-cols-2 gap-4 mb-6">
                  <div v-if="detailItem.category" class="p-3 rounded-lg" style="background: rgba(148,163,184,0.04); border: 1px solid var(--border-color);">
                    <span class="block text-[10px] font-mono tracking-wider mb-1" style="color: var(--text-muted);">CATEGORY</span>
                    <span class="text-sm font-mono font-semibold" style="color: var(--text-primary);">{{ detailItem.category }}</span>
                  </div>
                  <div v-if="detailItem.created_at" class="p-3 rounded-lg" style="background: rgba(148,163,184,0.04); border: 1px solid var(--border-color);">
                    <span class="block text-[10px] font-mono tracking-wider mb-1" style="color: var(--text-muted);">CREATED</span>
                    <span class="text-sm font-mono font-semibold" style="color: var(--text-primary);">{{ formatDate(detailItem.created_at) }}</span>
                  </div>
                </div>

                <!-- 操作按钮 -->
                <div class="flex gap-3">
                  <a v-if="detailItem.github_url" :href="detailItem.github_url" target="_blank"
                     class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-mono font-semibold transition-all hover:scale-[1.02]"
                     style="background: rgba(14,165,233,0.1); border: 1px solid rgba(14,165,233,0.2); color: var(--accent);">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                    查看源码
                  </a>
                  <a v-if="detailItem.demo_url" :href="detailItem.demo_url" target="_blank"
                     class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-mono font-semibold transition-all hover:scale-[1.02]"
                     style="background: rgba(182,112,255,0.1); border: 1px solid rgba(182,112,255,0.2); color: var(--accent-purple);">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                    在线演示
                  </a>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- 添加/编辑表单弹窗 -->
      <div v-if="showForm" class="fixed inset-0 flex items-center justify-center z-50" style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px);" @click.self="closeForm">
        <div class="card-neon p-6 w-full max-w-md max-h-[80vh] overflow-y-auto">
          <h2 class="text-2xl font-bold mb-6 font-mono" style="color: var(--text-primary);"><span class="text-neon">></span> {{ isEditing ? '编辑作品' : '添加作品' }}</h2>
          <form @submit.prevent="submitForm">
            <div class="mb-4">
              <label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">标题 *</label>
              <input v-model="form.title" type="text" required class="input-cyber" />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">描述</label>
              <textarea v-model="form.description" rows="3" class="input-cyber"></textarea>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">技术栈（逗号分隔）</label>
              <input v-model="form.tech_stack" type="text" placeholder="Vue, Flask, SQLite" class="input-cyber" />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">GitHub 链接</label>
              <input v-model="form.github_url" type="url" class="input-cyber" />
            </div>
            <div class="mb-6">
              <label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">在线演示链接</label>
              <input v-model="form.demo_url" type="url" class="input-cyber" />
            </div>
            <div class="flex gap-3">
              <button type="submit" class="btn-primary flex-1" :disabled="submitting">{{ submitting ? '提交中...' : '保存' }}</button>
              <button type="button" @click="closeForm" class="btn-secondary flex-1">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getPortfolio, addPortfolio, deletePortfolio, getAdminStatus } from '../composables/useApi'
import EditControls from '../components/EditControls.vue'

const isAdmin = getAdminStatus()
const portfolioList = ref([])
const showForm = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const form = ref({ title: '', description: '', tech_stack: '', github_url: '', demo_url: '' })

// 详情弹窗
const detailItem = ref(null)
const openDetail = (item) => { detailItem.value = item }
const closeDetail = () => { detailItem.value = null }

// ESC 关闭详情
const handleEsc = (e) => { if (e.key === 'Escape' && detailItem.value) closeDetail() }
onMounted(() => document.addEventListener('keydown', handleEsc))
onUnmounted(() => document.removeEventListener('keydown', handleEsc))

// 日期格式化
const formatDate = (iso) => {
  if (!iso) return '未知'
  const d = new Date(iso)
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`
}

// 测试数据（API 无数据时使用）
const testPortfolio = [
  {
    id: -1, title: 'CyberPortfolio', description: '一个赛博朋克风格的个人作品集网站，支持暗色/亮色主题切换、时间轴简历、作品展示等功能。',
    fullDescription: '使用 Vue 3 + Flask 全栈开发的个人作品集网站。前端采用 Tailwind CSS + 自定义 CSS 变量实现赛博朋克主题系统，支持实时亮暗切换。首页集成 Canvas 星空连线背景和极光波浪效果，文字支持 5 种空闲动画轮播。简历页使用 IntersectionObserver 实现滚动入场时间轴。后端 Flask 提供 RESTful API，SQLite 存储数据，支持管理员认证和 CRUD 操作。',
    story: {
      problem: '市面上的个人作品集千篇一律，缺乏个性。我想打造一个能真正代表自己技术风格的网站，而不是套用模板。',
      solution: '选择 Vue 3 Composition API 作为前端框架，用 Canvas 实现星空连线和鼠标跟随光效，用 CSS 变量构建完整的亮暗主题系统。后端用 Flask 轻量化部署，SQLite 零配置存储。每个细节都经过反复打磨。',
      result: '网站上线后获得多位同行好评，首页的交互效果成为最大的亮点。通过这个项目，深入掌握了 Canvas 动画、CSS 主题系统和全栈部署流程。'
    },
    tech_stack: ['Vue 3', 'Flask', 'Tailwind CSS', 'SQLite', 'Canvas', 'Vite'],
    image_path: null, github_url: 'https://github.com/yourname/cyber-portfolio', demo_url: '#',
    created_at: '2025-03-15T00:00:00', category: 'Web 应用', status: 'Active', statusColor: '#10b981',
    accentColor: 'var(--accent)', coverGradient: 'linear-gradient(135deg, #0c4a6e 0%, #164e63 50%, #134e4a 100%)',
    icon: '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>'
  },
  {
    id: -2, title: 'AutoTest Framework', description: '企业级自动化测试框架，支持 Web/API/移动端多维度测试，集成 CI/CD 流水线。',
    fullDescription: '基于 Python + pytest 构建的企业级自动化测试框架。支持 Selenium WebDriver 进行 Web UI 测试，requests 库进行 API 测试，Appium 进行移动端测试。内置 HTML 报告生成、失败截图、重试机制。与 Jenkins CI/CD 集成，实现代码提交后自动触发测试并发送报告。已稳定运行 2 年，累计执行 50,000+ 测试用例。',
    story: {
      problem: '团队每次发版前都要手动执行回归测试，耗时 2-3 小时，且容易遗漏。测试结果依赖 Excel 记录，无法追溯。',
      solution: '设计了分层架构：Page Object 模式封装页面元素，pytest fixtures 管理测试数据，Allure 生成可视化报告。集成了失败自动截图和重试机制，与 Jenkins Pipeline 打通实现 CI/CD 自动触发。',
      result: '回归测试时间从 3 小时缩短到 15 分钟，测试覆盖率从 40% 提升到 85%。框架已在公司 3 个项目中推广使用，累计执行 50,000+ 用例。'
    },
    tech_stack: ['Python', 'pytest', 'Selenium', 'Jenkins', 'Docker', 'Allure'],
    image_path: null, github_url: 'https://github.com/yourname/autotest-framework', demo_url: null,
    created_at: '2024-08-20T00:00:00', category: '测试工具', status: 'Production', statusColor: '#f59e0b',
    accentColor: 'var(--accent-purple)', coverGradient: 'linear-gradient(135deg, #4c1d95 0%, #5b21b6 50%, #6d28d9 100%)',
    icon: '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>'
  },
  {
    id: -3, title: 'DataViz Dashboard', description: '实时数据可视化仪表盘，支持多数据源接入、自定义图表和告警配置。',
    fullDescription: '基于 Vue 3 + ECharts 构建的实时数据可视化平台。支持 WebSocket 实时数据推送，内置折线图、柱状图、饼图、地图等 20+ 图表类型。用户可通过拖拽方式自定义仪表盘布局，支持数据源管理（MySQL、PostgreSQL、API）。内置告警规则引擎，数据异常时自动发送邮件/钉钉通知。已在公司内部稳定服务 3 个业务线。',
    story: {
      problem: '运营团队每天要登录多个系统查看数据，手动导出 Excel 做报表。数据异常时往往发现太晚，错过最佳处理时机。',
      solution: '用 Vue 3 拖拽库实现仪表盘自定义布局，WebSocket 推送实时数据，ECharts 渲染 20+ 种图表。后端用 Node.js 做数据聚合，Redis 缓存热点数据。告警引擎支持阈值和趋势异常检测。',
      result: '运营团队的工作效率提升 60%，数据异常发现时间从"次日"缩短到"分钟级"。平台稳定服务 3 个业务线，日均处理 100 万+ 数据点。'
    },
    tech_stack: ['Vue 3', 'ECharts', 'WebSocket', 'Node.js', 'PostgreSQL', 'Redis'],
    image_path: null, github_url: null, demo_url: 'https://dataviz-demo.example.com',
    created_at: '2024-11-05T00:00:00', category: '数据平台', status: 'Beta', statusColor: '#8b5cf6',
    accentColor: 'var(--accent-green)', coverGradient: 'linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%)',
    icon: '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>'
  },
  {
    id: -4, title: 'SmartCLI', description: '智能命令行工具集，提供项目脚手架、代码生成、Git 工作流自动化等功能。',
    fullDescription: '使用 Go 语言开发的跨平台 CLI 工具。支持一键初始化 Vue/React/Flask/Django 项目模板，内置代码生成器可根据数据库 Schema 自动生成 CRUD 代码。Git 工作流模块提供自定义 commit message 规范检查、分支管理、自动 changelog 生成。插件系统支持用户自定义扩展。已发布至 Homebrew 和 npm。',
    story: {
      problem: '每次开新项目都要花半天时间配置环境、搭建目录结构、配置 CI/CD。不同项目的 commit 规范不统一，changelog 全靠手写。',
      solution: '用 Go + Cobra 构建跨平台 CLI，内置项目模板引擎和代码生成器。设计了插件系统让用户自定义扩展，Git 模块强制执行 commit 规范并自动生成 changelog。',
      result: '新项目初始化时间从半天缩短到 30 秒。工具发布到 Homebrew 和 npm 后获得 200+ star，被 3 个开源项目采用为官方脚手架工具。'
    },
    image_path: null, github_url: 'https://github.com/yourname/smart-cli', demo_url: null,
    created_at: '2025-01-10T00:00:00', category: '命令行工具', status: 'Active', statusColor: '#10b981',
    accentColor: 'var(--accent-pink)', coverGradient: 'linear-gradient(135deg, #831843 0%, #9d174d 50%, #be185d 100%)',
    icon: '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>'
  },
  {
    id: -5, title: 'ChatFlow', description: '基于 WebSocket 的实时聊天应用，支持群聊、文件传输、消息撤回和已读回执。',
    fullDescription: '全栈实时聊天应用，前端 Vue 3 + Vite，后端 Flask-SocketIO。支持一对一私聊和多人群聊，消息类型包括文本、图片、文件。实现了消息撤回（2分钟内）、已读回执、输入状态提示、离线消息推送等功能。使用 Redis 作为消息队列和在线状态存储，支持水平扩展。前端使用 IndexedDB 实现离线消息缓存。',
    story: {
      problem: '团队内部沟通依赖第三方工具，敏感信息外泄风险大。且现有工具不支持文件传输和消息撤回等刚需功能。',
      solution: '全栈自研聊天系统，WebSocket 实现实时通信，Redis 做消息队列和在线状态管理。前端用 IndexedDB 缓存离线消息，后端用 Flask-SocketIO 处理并发连接。',
      result: '系统上线后成为团队主力沟通工具，支持 500 人同时在线。消息撤回和已读回执功能获得高度好评，离线消息同步准确率达 99.9%。'
    },
    image_path: null, github_url: 'https://github.com/yourname/chatflow', demo_url: 'https://chatflow-demo.example.com',
    created_at: '2024-06-15T00:00:00', category: 'Web 应用', status: 'Archived', statusColor: '#6b7280',
    accentColor: '#f59e0b', coverGradient: 'linear-gradient(135deg, #78350f 0%, #92400e 50%, #b45309 100%)',
    icon: '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>'
  },
  {
    id: -6, title: 'LogInsight', description: '日志分析与监控平台，支持多源日志采集、实时告警和智能异常检测。',
    fullDescription: '分布式日志分析平台，使用 ELK 架构（Elasticsearch + Logstash + Kibana）结合自研前端。支持文件、syslog、HTTP 等多种日志采集方式。内置 KQL 查询语法，支持全文搜索和字段过滤。告警模块支持基于阈值和异常检测算法的自动告警。智能分析模块使用简单的统计方法识别日志模式异常。已在生产环境处理日均 500GB 日志数据。',
    story: {
      problem: '生产环境故障排查靠"人肉 grep"，几十台服务器的日志分散存储，定位一个问题要登录 5+ 台机器。告警全靠运维值班盯监控。',
      solution: '搭建 ELK 集群统一日志采集，自研前端提供更友好的查询界面。设计了基于阈值和统计异常的双重告警引擎，支持钉钉/邮件/短信多通道通知。',
      result: '故障定位时间从平均 30 分钟缩短到 3 分钟，告警覆盖率从 60% 提升到 95%。平台日均处理 500GB 日志，成为公司运维团队的核心工具。'
    },
    image_path: null, github_url: 'https://github.com/yourname/log-insight', demo_url: null,
    created_at: '2025-02-28T00:00:00', category: '运维工具', status: 'Active', statusColor: '#10b981',
    accentColor: '#06b6d4', coverGradient: 'linear-gradient(135deg, #164e63 0%, #155e75 50%, #0e7490 100%)',
    icon: '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'
  }
]

// 分类筛选
const activeCategory = ref('全部')
const categories = computed(() => {
  const cats = new Set(portfolioList.value.map(i => i.category).filter(Boolean))
  return ['全部', ...cats]
})
const filteredList = computed(() => {
  if (activeCategory.value === '全部') return portfolioList.value
  return portfolioList.value.filter(i => i.category === activeCategory.value)
})

// 增强数据（给后端数据添加前端展示属性）
function enhanceItem(item) {
  const gradients = [
    'linear-gradient(135deg, #0c4a6e 0%, #164e63 50%, #134e4a 100%)',
    'linear-gradient(135deg, #4c1d95 0%, #5b21b6 50%, #6d28d9 100%)',
    'linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%)',
    'linear-gradient(135deg, #831843 0%, #9d174d 50%, #be185d 100%)',
    'linear-gradient(135deg, #78350f 0%, #92400e 50%, #b45309 100%)',
    'linear-gradient(135deg, #164e63 0%, #155e75 50%, #0e7490 100%)',
  ]
  const icons = [
    '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>',
    '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>',
    '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" /></svg>',
    '<svg class="w-10 h-10" fill="none" stroke="rgba(255,255,255,0.6)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>',
  ]
  const colors = ['var(--accent)', 'var(--accent-purple)', 'var(--accent-green)', 'var(--accent-pink)', '#f59e0b', '#06b6d4']
  const idx = item.id % gradients.length
  return {
    ...item,
    accentColor: item.accentColor || colors[idx],
    coverGradient: item.coverGradient || gradients[idx],
    icon: item.icon || icons[idx],
    category: item.category || 'Web 应用',
    status: item.status || null,
    statusColor: item.statusColor || '#10b981',
    fullDescription: item.fullDescription || item.description
  }
}

// API 加载
const loadPortfolio = async () => {
  try {
    const data = await getPortfolio()
    if (data && data.length > 0) {
      portfolioList.value = data.map(enhanceItem)
    } else {
      // 无后端数据时使用测试数据
      portfolioList.value = testPortfolio
    }
  } catch (e) {
    console.error('加载作品集失败，使用测试数据', e)
    portfolioList.value = testPortfolio
  }
}

const openAddForm = () => { isEditing.value = false; editingId.value = null; form.value = { title: '', description: '', tech_stack: '', github_url: '', demo_url: '' }; showForm.value = true }
const openEditForm = (item) => { isEditing.value = true; editingId.value = item.id; form.value = { title: item.title, description: item.description, tech_stack: item.tech_stack.join(', '), github_url: item.github_url || '', demo_url: item.demo_url || '' }; showForm.value = true }
const closeForm = () => { showForm.value = false; form.value = { title: '', description: '', tech_stack: '', github_url: '', demo_url: '' } }
const submitForm = async () => {
  submitting.value = true
  try { await addPortfolio({ ...form.value, tech_stack: form.value.tech_stack }); closeForm(); await loadPortfolio() }
  catch (e) { alert('操作失败：' + (e.response?.data?.error || e.message)) }
  finally { submitting.value = false }
}
const handleDelete = async (id) => {
  if (!confirm('确定要删除这个作品吗？')) return
  try { await deletePortfolio(id); await loadPortfolio() } catch (e) { alert('删除失败：' + (e.response?.data?.error || e.message)) }
}
onMounted(loadPortfolio)
</script>

<style scoped>
/* ============================================================
   入场动画
   ============================================================ */
.animate-fade-in {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================================
   卡片入场动画
   ============================================================ */
.portfolio-card {
  opacity: 0;
  animation: cardFadeIn 0.5s ease-out forwards;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.portfolio-card:hover {
  transform: translateY(-4px);
}

@keyframes cardFadeIn {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================================
   封面区域
   ============================================================ */
.portfolio-cover {
  position: relative;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cover-icon {
  opacity: 0.5;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.portfolio-card:hover .cover-icon {
  opacity: 0.8;
  transform: scale(1.1);
}

/* Hover 叠加层 */
.cover-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.portfolio-card:hover .cover-overlay {
  opacity: 1;
}

.overlay-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  transform: translateY(8px);
  transition: transform 0.3s ease;
}

.portfolio-card:hover .overlay-content {
  transform: translateY(0);
}

/* ============================================================
   详情弹窗
   ============================================================ */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
}

.detail-modal {
  border-radius: 16px;
  overflow: hidden;
}

/* 讲故事风格 */
.story-block {
  padding: 0.75rem 1rem;
  border-radius: 0 8px 8px 0;
  background: rgba(148, 163, 184, 0.03);
}
.story-label {
  font-size: 0.75rem;
  font-weight: 700;
  font-family: 'Courier New', monospace;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.35rem;
}
.story-text {
  font-size: 0.85rem;
  line-height: 1.7;
  color: var(--text-secondary, #aaa);
  margin: 0;
}

.detail-cover {
  position: relative;
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-icon-large {
  opacity: 0.6;
}

/* 弹窗动画 */
.modal-enter-active {
  transition: all 0.3s ease-out;
}
.modal-leave-active {
  transition: all 0.2s ease-in;
}
.modal-enter-from {
  opacity: 0;
}
.modal-enter-from .detail-modal {
  transform: scale(0.95) translateY(20px);
}
.modal-leave-to {
  opacity: 0;
}
.modal-leave-to .detail-modal {
  transform: scale(0.95) translateY(20px);
}

/* ============================================================
   工具类
   ============================================================ */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
