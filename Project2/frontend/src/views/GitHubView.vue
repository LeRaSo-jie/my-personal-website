<template>
  <div class="min-h-screen pt-20 pb-16 px-4">
    <div class="max-w-5xl mx-auto">
      <!-- 页面头部 -->
      <div class="flex items-center justify-between mb-10 animate-fade-in">
        <div>
          <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider mb-4"
                style="background: rgba(3, 105, 161, 0.08); border: 1px solid rgba(3, 105, 161, 0.2); color: var(--accent);">
            // GITHUB_ACTIVITY
          </span>
          <h1 class="text-4xl md:text-5xl font-bold font-mono gradient-text">GitHub</h1>
          <p class="text-sm font-mono mt-2" style="color: var(--text-muted);">// open source contributions</p>
        </div>
        <a :href="githubUrl" target="_blank"
           class="btn-primary font-mono flex items-center gap-2">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
          View Profile
        </a>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10 animate-fade-in" style="animation-delay: 0.1s;">
        <div v-for="stat in stats" :key="stat.label" class="card-neon p-5 text-center group hover:scale-[1.02] transition-transform">
          <div class="text-2xl md:text-3xl font-bold font-mono mb-1" :style="{ color: stat.color }">
            {{ stat.value }}
          </div>
          <div class="text-xs font-mono" style="color: var(--text-muted);">{{ stat.label }}</div>
        </div>
      </div>

      <!-- 贡献热力图 -->
      <div class="card-neon p-6 mb-10 animate-fade-in" style="animation-delay: 0.2s;">
        <h2 class="text-lg font-bold font-mono mb-4" style="color: var(--text-primary);">
          <span style="color: var(--accent);">#</span> 贡献热力图
          <span class="text-xs font-normal ml-2" style="color: var(--text-muted);">过去 365 天</span>
        </h2>
        <div class="contribution-grid">
          <div v-for="(week, wi) in contributionData" :key="wi" class="contribution-week">
            <div
              v-for="(day, di) in week"
              :key="di"
              class="contribution-cell"
              :style="{ background: getContributionColor(day.level) }"
              :title="`${day.count} contributions on ${day.date}`"
            ></div>
          </div>
        </div>
        <div class="flex items-center justify-end gap-1.5 mt-3">
          <span class="text-[10px] font-mono" style="color: var(--text-muted);">Less</span>
          <div v-for="level in 5" :key="level" class="w-3 h-3 rounded-sm" :style="{ background: getContributionColor(level - 1) }"></div>
          <span class="text-[10px] font-mono" style="color: var(--text-muted);">More</span>
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
            <div v-for="lang in languages" :key="lang.name" class="group">
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
            <div v-for="event in recentEvents" :key="event.id" class="flex gap-3 group">
              <!-- 事件图标 -->
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                   :style="{ background: event.iconBg, border: `1px solid ${event.iconBorder}` }">
                <div v-html="event.icon" class="w-4 h-4" :style="{ color: event.iconColor }"></div>
              </div>
              <!-- 事件内容 -->
              <div class="flex-1 min-w-0">
                <p class="text-sm" style="color: var(--text-secondary);">
                  <span class="font-semibold" style="color: var(--text-primary);">{{ event.action }}</span>
                  <a :href="event.repoUrl" target="_blank" class="font-mono hover:underline transition-colors" style="color: var(--accent);">{{ event.repo }}</a>
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
          <span style="color: var(--accent-pink, #ec4899);">#</span> 置顶仓库
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="repo in pinnedRepos" :key="repo.name" class="card-neon p-5 group hover:scale-[1.01] transition-all cursor-pointer" @click="openRepo(repo.url)">
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4" style="color: var(--text-muted);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                <span class="font-mono font-semibold group-hover:text-neon transition-colors" style="color: var(--text-primary);">{{ repo.name }}</span>
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getGitHubData } from '../composables/useApi'

const langColorMap = {
  'Python': '#3776ab', 'JavaScript': '#f7df1e', 'TypeScript': '#3178c6',
  'Vue': '#42b883', 'Go': '#00add8', 'Java': '#b07219',
  'Shell': '#89e051', 'C++': '#f34b7d', 'C': '#555555',
  'Rust': '#dea584', 'Ruby': '#701516', 'PHP': '#4F5D95',
  'HTML': '#e34c26', 'CSS': '#563d7c', 'Other': '#8b949e'
}

const loading = ref(true)
const githubUrl = ref('')
const stats = ref([
  { label: 'Public Repos', value: '0', color: 'var(--accent)' },
  { label: 'Total Stars', value: '0', color: '#f59e0b' },
  { label: 'Contributions', value: '0', color: 'var(--accent-green, #10b981)' },
  { label: 'Followers', value: '0', color: 'var(--accent-purple)' }
])
const languages = ref([])
const recentEvents = ref([])
const pinnedRepos = ref([])
const contributionData = ref([])

// 空热力图
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
contributionData.value = emptyWeeks()

onMounted(async () => {
  loading.value = true
  try {
    const res = await getGitHubData()
    if (res.success) {
      const d = res.data
      githubUrl.value = d.profile_url || ''
      stats.value = [
        { label: 'Public Repos', value: String(d.repos || 0), color: 'var(--accent)' },
        { label: 'Total Stars', value: d.stars || '0', color: '#f59e0b' },
        { label: 'Contributions', value: d.contributions || '0', color: 'var(--accent-green, #10b981)' },
        { label: 'Followers', value: String(d.followers || 0), color: 'var(--accent-purple)' }
      ]
      languages.value = d.languages || []
      recentEvents.value = d.events || []
      pinnedRepos.value = (d.pinnedRepos || []).map(r => ({
        ...r,
        langColor: langColorMap[r.language] || '#8b949e'
      }))
      if (d.contributions_weeks && d.contributions_weeks.length > 0) {
        contributionData.value = d.contributions_weeks
      }
    }
  } catch (e) {
    console.error('GitHub data fetch error:', e)
  } finally {
    loading.value = false
  }
})

const getContributionColor = (level) => {
  const colors = [
    'rgba(148, 163, 184, 0.08)',
    'rgba(14, 165, 233, 0.25)',
    'rgba(14, 165, 233, 0.45)',
    'rgba(14, 165, 233, 0.7)',
    'var(--accent, #0ea5e9)'
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
