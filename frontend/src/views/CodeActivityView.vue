<template>
  <div class="min-h-screen pt-20 pb-16 px-4">
    <div class="max-w-5xl mx-auto">
      <!-- 页面头部（标题 + Tab 切换器在同一行） -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-10 animate-fade-in">
        <div>
          <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider mb-4"
                style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.2); color: var(--accent);">
            // CODE_ACTIVITY
          </span>
          <h1 class="text-4xl md:text-5xl font-bold font-mono gradient-text">代码动态</h1>
          <p class="text-sm font-mono mt-2" style="color: var(--text-muted);">// open source contributions & activity</p>
        </div>

        <!-- 外部链接按钮 + Tab 切换器（右侧对齐） -->
        <div class="flex items-center gap-2 mt-4 sm:mt-0">
          <!-- 外部链接按钮 -->
          <a :href="currentProfile.url" target="_blank"
             class="btn-primary font-mono flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            View Profile
          </a>

          <div class="relative flex rounded-xl p-1" style="background: var(--bg-secondary); border: 1px solid var(--border-color);">
            <!-- 滑动指示器 -->
            <div class="absolute top-1 bottom-1 rounded-lg transition-all duration-300 ease-out"
                 :style="{
                   width: 'calc(50% - 4px)',
                   left: activeTab === 'gitee' ? '4px' : 'calc(50%)',
                   background: activeTab === 'gitee'
                     ? 'linear-gradient(135deg, rgba(199, 29, 35, 0.15), rgba(199, 29, 35, 0.08))'
                     : 'linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(14, 165, 233, 0.08))',
                   border: activeTab === 'gitee'
                     ? '1px solid rgba(199, 29, 35, 0.25)'
                     : '1px solid rgba(14, 165, 233, 0.25)'
                 }">
            </div>
            
            <button @click="switchTab('gitee')"
                    class="relative z-10 flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-mono transition-colors duration-300"
                    :style="{ color: activeTab === 'gitee' ? '#c71d23' : 'var(--text-muted)' }">
              <!-- Gitee SVG Logo -->
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.984 0C5.372 0 0 5.372 0 11.984c0 6.612 5.372 11.984 11.984 11.984 6.612 0 11.984-5.372 11.984-11.984C23.968 5.372 18.596 0 11.984 0zM9.062 18.628c-3.27 0-5.92-2.028-6.884-4.864h3.576c.712 1.44 2.184 2.424 3.88 2.424 2.388 0 4.32-1.932 4.32-4.32 0-2.388-1.932-4.32-4.32-4.32-1.696 0-3.168.984-3.88 2.424H2.178c.964-2.836 3.614-4.864 6.884-4.864 4.036 0 7.308 3.272 7.308 7.308 0 4.036-3.272 7.308-7.308 7.308z"/>
              </svg>
              Gitee
            </button>
            
            <button @click="switchTab('github')"
                    class="relative z-10 flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-mono transition-colors duration-300"
                    :style="{ color: activeTab === 'github' ? 'var(--accent)' : 'var(--text-muted)' }">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub
            </button>
          </div>
        </div>
      </div>

      <!-- 内容区域（带动画切换） -->
      <Transition name="tab-fade" mode="out-in">
        <div :key="activeTab">
          <!-- 统计卡片 -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10 animate-fade-in" style="animation-delay: 0.1s;">
            <div v-for="stat in currentStats" :key="stat.label" class="card-neon p-5 text-center group hover:scale-[1.02] transition-transform">
              <div class="text-2xl md:text-3xl font-bold font-mono mb-1" :style="{ color: stat.color }">
                {{ stat.value }}
              </div>
              <div class="text-xs font-mono" style="color: var(--text-muted);">{{ stat.label }}</div>
            </div>
          </div>

          <!-- 贡献热力图 -->
          <div class="card-neon p-6 mb-10 animate-fade-in" style="animation-delay: 0.2s;">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-bold font-mono" style="color: var(--text-primary);">
                <span :style="{ color: activeTab === 'github' ? 'var(--accent)' : '#c71d23' }">#</span> 贡献热力图
                <span class="text-xs font-normal ml-2" style="color: var(--text-muted);">过去 365 天</span>
              </h2>
              <!-- 平台标识 -->
              <span class="text-[10px] px-2 py-1 rounded font-mono"
                    :style="{
                      background: activeTab === 'github' ? 'rgba(14,165,233,0.08)' : 'rgba(199,29,35,0.08)',
                      border: `1px solid ${activeTab === 'github' ? 'rgba(14,165,233,0.2)' : 'rgba(199,29,35,0.2)'}`,
                      color: activeTab === 'github' ? 'var(--accent)' : '#c71d23'
                    }">
                {{ activeTab === 'github' ? 'GitHub' : 'Gitee' }} Punch Card
              </span>
            </div>
            <div class="contribution-grid">
              <div v-for="(week, wi) in currentContributionData" :key="wi" class="contribution-week">
                <div
                  v-for="(day, di) in week"
                  :key="di"
                  class="contribution-cell"
                  :style="{ background: getContributionColor(day.level) }"
                  :title="`${day.count} contributions on ${day.date}`"
                ></div>
              </div>
            </div>
            <div class="flex items-center justify-between mt-3">
              <span class="text-[11px] font-mono" style="color: var(--text-muted);">
                {{ currentTotalContributions }} contributions in the last year
              </span>
              <div class="flex items-center gap-1.5">
                <span class="text-[10px] font-mono" style="color: var(--text-muted);">Less</span>
                <div v-for="level in 5" :key="level" class="w-3 h-3 rounded-sm" :style="{ background: getContributionColor(level - 1) }"></div>
                <span class="text-[10px] font-mono" style="color: var(--text-muted);">More</span>
              </div>
            </div>
          </div>

          <!-- 两列布局：语言统计 + 最近活动 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
            <!-- 语言统计 -->
            <div class="card-neon p-6 animate-fade-in" style="animation-delay: 0.3s;">
              <h2 class="text-lg font-bold font-mono mb-5" style="color: var(--text-primary);">
                <span style="color: var(--accent-purple);">#</span> 语言分布
              </h2>
              <div class="space-y-3">
                <div v-for="lang in currentLanguages" :key="lang.name" class="group">
                  <div class="flex items-center justify-between mb-1.5">
                    <div class="flex items-center gap-2">
                      <span class="w-3 h-3 rounded-full" :style="{ background: lang.color }"></span>
                      <span class="text-sm font-mono" style="color: var(--text-primary);">{{ lang.name }}</span>
                    </div>
                    <span class="text-xs font-mono" style="color: var(--text-muted);">{{ lang.percent }}%</span>
                  </div>
                  <div class="h-1.5 rounded-full overflow-hidden" style="background: var(--border-color);">
                    <div class="h-full rounded-full transition-all duration-1000 ease-out"
                         :style="{ width: lang.percent + '%', background: lang.color }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 最近活动 -->
            <div class="card-neon p-6 animate-fade-in" style="animation-delay: 0.4s;">
              <h2 class="text-lg font-bold font-mono mb-5" style="color: var(--text-primary);">
                <span style="color: var(--accent-green);">#</span> 最近活动
              </h2>
              <div class="space-y-4">
                <div v-for="event in currentEvents" :key="event.id" class="flex gap-3 group">
                  <!-- 事件图标 -->
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                       :style="{ background: event.iconBg, border: `1px solid ${event.iconBorder}` }">
                    <div v-html="event.icon" class="w-4 h-4" :style="{ color: event.iconColor }"></div>
                  </div>
                  <!-- 事件内容 -->
                  <div class="flex-1 min-w-0">
                    <p class="text-sm" style="color: var(--text-secondary);">
                      <span class="font-semibold" style="color: var(--text-primary);">{{ event.action }}</span>
                      <a :href="event.repoUrl" target="_blank" class="font-mono hover:underline transition-colors" 
                         :style="{ color: activeTab === 'github' ? 'var(--accent)' : '#c71d23' }">{{ event.repo }}</a>
                    </p>
                    <span class="text-[11px] font-mono" style="color: var(--text-muted);">{{ event.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 置顶仓库 -->
          <div class="animate-fade-in" style="animation-delay: 0.5s;">
            <h2 class="text-lg font-bold font-mono mb-5" style="color: var(--text-primary);">
              <span style="color: var(--accent-pink, #ec4899);">#</span> {{ activeTab === 'github' ? '置顶仓库' : '推荐项目' }}
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="repo in currentRepos" :key="repo.name" 
                   class="card-neon p-5 group hover:scale-[1.01] transition-all cursor-pointer" 
                   @click="openRepo(repo.url)">
                <div class="flex items-start justify-between mb-3">
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4" style="color: var(--text-muted);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                    </svg>
                    <span class="font-mono font-semibold group-hover:text-neon transition-colors" 
                          style="color: var(--text-primary);">{{ repo.name }}</span>
                  </div>
                  <span class="text-[10px] px-2 py-0.5 rounded font-mono"
                        :style="{ background: repo.langColor + '15', border: `1px solid ${repo.langColor}30`, color: repo.langColor }">
                    {{ repo.language }}
                  </span>
                </div>
                <p class="text-sm mb-3 leading-relaxed" style="color: var(--text-secondary);">{{ repo.description }}</p>
                <div class="flex items-center gap-4 text-xs font-mono" style="color: var(--text-muted);">
                  <span class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 .587l3.668 7.431 8.332 1.21-6.029 5.874 1.42 8.311L12 19.897l-7.391 3.516 1.42-8.311-6.029-5.874 8.332-1.21z"/></svg>
                    {{ repo.stars }}
                  </span>
                  <span class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M6 3a3 3 0 00-3 3v.024A3 3 0 006 9h.024A3 3 0 009 6.024V6a3 3 0 00-3-3zm0 12a3 3 0 00-3 3v.024A3 3 0 006 21h.024A3 3 0 009 18.024V18a3 3 0 00-3-3zm12-12a3 3 0 00-3 3v.024A3 3 0 0018 9h.024A3 3 0 0021 6.024V6a3 3 0 00-3-3z"/></svg>
                    {{ repo.forks }}
                  </span>
                  <span class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    {{ repo.updated }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 平台对比统计（底部彩蛋） -->
          <div class="mt-12 card-neon p-6 animate-fade-in" style="animation-delay: 0.6s;">
            <h2 class="text-lg font-bold font-mono mb-5" style="color: var(--text-primary);">
              <span style="color: var(--accent);">#</span> 双平台总览
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <!-- 总仓库数 -->
              <div class="text-center">
                <div class="text-3xl font-bold font-mono mb-1" style="color: var(--accent);">
                  {{ totalRepos }}
                </div>
                <div class="text-xs font-mono" style="color: var(--text-muted);">总仓库数</div>
                <div class="flex items-center justify-center gap-3 mt-2">
                  <span class="text-[11px] font-mono" style="color: #c71d23;">GE: {{ giteeData.repos }}</span>
                  <span class="text-[11px] font-mono" style="color: var(--accent);">GH: {{ githubData.repos }}</span>
                </div>
              </div>
              <!-- 总 Stars -->
              <div class="text-center">
                <div class="text-3xl font-bold font-mono mb-1" style="color: #f59e0b;">
                  {{ totalStars }}
                </div>
                <div class="text-xs font-mono" style="color: var(--text-muted);">总 Stars</div>
                <div class="flex items-center justify-center gap-3 mt-2">
                  <span class="text-[11px] font-mono" style="color: #c71d23;">GE: {{ giteeData.stars }}</span>
                  <span class="text-[11px] font-mono" style="color: var(--accent);">GH: {{ githubData.stars }}</span>
                </div>
              </div>
              <!-- 总贡献 -->
              <div class="text-center">
                <div class="text-3xl font-bold font-mono mb-1" style="color: var(--accent-green, #10b981);">
                  {{ totalContributions }}
                </div>
                <div class="text-xs font-mono" style="color: var(--text-muted);">总贡献数</div>
                <div class="flex items-center justify-center gap-3 mt-2">
                  <span class="text-[11px] font-mono" style="color: #c71d23;">GE: {{ giteeData.contributions }}</span>
                  <span class="text-[11px] font-mono" style="color: var(--accent);">GH: {{ githubData.contributions }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getGitHubData, getGiteeData } from '../composables/useApi'

const activeTab = ref('gitee')
const loading = ref(true)
const error = ref(null)

const switchTab = (tab) => {
  activeTab.value = tab
}

// ============================================================
// 语言颜色映射
// ============================================================
const langColorMap = {
  'Python': '#3776ab', 'JavaScript': '#f7df1e', 'TypeScript': '#3178c6',
  'Vue': '#42b883', 'Go': '#00add8', 'Java': '#b07219',
  'Shell': '#89e051', 'C++': '#f34b7d', 'C': '#555555',
  'Rust': '#dea584', 'Ruby': '#701516', 'PHP': '#4F5D95',
  'Swift': '#F05138', 'Kotlin': '#A97BFF', 'Dart': '#00B4AB',
  'HTML': '#e34c26', 'CSS': '#563d7c', 'Jupyter Notebook': '#DA5B0B',
  'Other': '#8b949e'
}

// ============================================================
// 响应式数据（初始为空壳，API 返回后填充）
// ============================================================
const githubData = ref({
  profileUrl: '',
  repos: 0,
  stars: '0',
  contributions: '0',
  followers: 0,
  languages: [],
  events: [],
  pinnedRepos: [],
  contributions_weeks: []
})

const giteeData = ref({
  profileUrl: '',
  repos: 0,
  stars: '0',
  contributions: '0',
  followers: 0,
  languages: [],
  events: [],
  pinnedRepos: [],
  contributions_weeks: []
})

// 空贡献热力图（52 周 x 7 天）
function emptyWeeks() {
  const data = []
  const today = new Date()
  for (let w = 0; w < 52; w++) {
    const week = []
    for (let d = 0; d < 7; d++) {
      const date = new Date(today)
      date.setDate(date.getDate() - (51 - w) * 7 - (6 - d))
      week.push({ date: date.toISOString().split('T')[0], count: 0, level: 0 })
    }
    data.push(week)
  }
  return data
}

const githubContributions = ref(emptyWeeks())
const giteeContributions = ref(emptyWeeks())

// ============================================================
// 加载数据
// ============================================================
function processRepos(repos) {
  return repos.map(r => ({
    ...r,
    langColor: langColorMap[r.language] || '#8b949e'
  }))
}

async function loadGitHubData() {
  try {
    const res = await getGitHubData()
    if (res.success) {
      const d = res.data
      githubData.value = {
        profileUrl: d.profile_url || '',
        repos: d.repos || 0,
        stars: d.stars || '0',
        contributions: d.contributions || '0',
        followers: d.followers || 0,
        languages: d.languages || [],
        events: d.events || [],
        pinnedRepos: processRepos(d.pinnedRepos || []),
        contributions_weeks: d.contributions_weeks || []
      }
      if (d.contributions_weeks && d.contributions_weeks.length > 0) {
        githubContributions.value = d.contributions_weeks
      }
    }
  } catch (e) {
    console.error('GitHub data fetch error:', e)
  }
}

async function loadGiteeData() {
  try {
    const res = await getGiteeData()
    if (res.success) {
      const d = res.data
      giteeData.value = {
        profileUrl: d.profile_url || '',
        repos: d.repos || 0,
        stars: d.stars || '0',
        contributions: d.contributions || '0',
        followers: d.followers || 0,
        languages: d.languages || [],
        events: d.events || [],
        pinnedRepos: processRepos(d.pinnedRepos || []),
        contributions_weeks: d.contributions_weeks || []
      }
      if (d.contributions_weeks && d.contributions_weeks.length > 0) {
        giteeContributions.value = d.contributions_weeks
      }
    }
  } catch (e) {
    console.error('Gitee data fetch error:', e)
  }
}

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([loadGitHubData(), loadGiteeData()])
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

// ============================================================
// Computed: 根据当前 Tab 返回对应数据
// ============================================================
const currentProfile = computed(() => activeTab.value === 'github'
  ? { url: githubData.value.profileUrl }
  : { url: giteeData.value.profileUrl }
)

const currentStats = computed(() => {
  if (activeTab.value === 'github') {
    return [
      { label: 'Public Repos', value: githubData.value.repos, color: 'var(--accent)' },
      { label: 'Total Stars', value: githubData.value.stars, color: '#f59e0b' },
      { label: 'Contributions', value: githubData.value.contributions, color: 'var(--accent-green, #10b981)' },
      { label: 'Followers', value: githubData.value.followers, color: 'var(--accent-purple)' }
    ]
  }
  return [
    { label: '公开仓库', value: giteeData.value.repos, color: '#c71d23' },
    { label: '总 Stars', value: giteeData.value.stars, color: '#f59e0b' },
    { label: '总贡献数', value: giteeData.value.contributions, color: 'var(--accent-green, #10b981)' },
    { label: '关注者', value: giteeData.value.followers, color: 'var(--accent-purple)' }
  ]
})

const currentLanguages = computed(() => activeTab.value === 'github' ? githubData.value.languages : giteeData.value.languages)
const currentEvents = computed(() => activeTab.value === 'github' ? githubData.value.events : giteeData.value.events)
const currentRepos = computed(() => activeTab.value === 'github' ? githubData.value.pinnedRepos : giteeData.value.pinnedRepos)

// 双平台总览
const totalRepos = computed(() => githubData.value.repos + giteeData.value.repos)
const totalStars = computed(() => {
  const parseNum = (v) => {
    if (typeof v === 'number') return v
    const s = String(v).replace(/,/g, '')
    if (s.includes('k')) return parseFloat(s) * 1000
    if (s.includes('m')) return parseFloat(s) * 1000000
    return parseFloat(s) || 0
  }
  return (parseNum(githubData.value.stars) + parseNum(giteeData.value.stars)).toLocaleString()
})
const totalContributions = computed(() => {
  const parseNum = (v) => {
    if (typeof v === 'number') return v
    return parseInt(String(v).replace(/,/g, '')) || 0
  }
  return (parseNum(githubData.value.contributions) + parseNum(giteeData.value.contributions)).toLocaleString()
})

// ============================================================
// 贡献热力图
// ============================================================
const currentContributionData = computed(() =>
  activeTab.value === 'github' ? githubContributions.value : giteeContributions.value
)

const currentTotalContributions = computed(() =>
  activeTab.value === 'github' ? githubData.value.contributions : giteeData.value.contributions
)

const getContributionColor = (level) => {
  if (activeTab.value === 'github') {
    const colors = [
      'rgba(148, 163, 184, 0.08)',
      'rgba(14, 165, 233, 0.25)',
      'rgba(14, 165, 233, 0.45)',
      'rgba(14, 165, 233, 0.7)',
      'var(--accent, #0ea5e9)'
    ]
    return colors[level] || colors[0]
  }
  const colors = [
    'rgba(148, 163, 184, 0.08)',
    'rgba(199, 29, 35, 0.2)',
    'rgba(199, 29, 35, 0.4)',
    'rgba(199, 29, 35, 0.65)',
    '#c71d23'
  ]
  return colors[level] || colors[0]
}

const openRepo = (url) => { window.open(url, '_blank') }
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
   Tab 切换动画
   ============================================================ */
.tab-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.tab-fade-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.tab-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ============================================================
   贡献热力图
   ============================================================ */
.contribution-grid {
  display: flex;
  gap: 3px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.contribution-week {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.contribution-cell {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  transition: transform 0.15s ease;
  cursor: pointer;
}

.contribution-cell:hover {
  transform: scale(1.3);
  outline: 1px solid var(--accent);
}

@media (max-width: 640px) {
  .contribution-cell {
    width: 8px;
    height: 8px;
  }
}
</style>
