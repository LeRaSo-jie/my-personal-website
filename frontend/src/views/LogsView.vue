<template>
  <div class="min-h-screen pt-20 pb-16 px-4">
    <div class="max-w-7xl mx-auto">
      <div class="mb-8">
        <span class="font-mono text-sm text-neon-purple opacity-60 tracking-widest">// ACTIVITY_LOG</span>
        <h1 class="text-4xl font-bold mt-2 gradient-text">活动日志</h1>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="card-neon p-4 text-center group">
          <div class="text-3xl font-bold font-mono text-neon">{{ stats.total || 0 }}</div>
          <div class="text-xs font-mono mt-1" style="color: var(--text-muted);">TOTAL</div>
        </div>
        <div class="card-neon p-4 text-center group">
          <div class="text-3xl font-bold font-mono text-neon-green">{{ stats.recent_24h || 0 }}</div>
          <div class="text-xs font-mono mt-1" style="color: var(--text-muted);">24H</div>
        </div>
        <div class="card-neon p-4 text-center group">
          <div class="text-3xl font-bold font-mono text-neon-blue">{{ stats.recent_7d || 0 }}</div>
          <div class="text-xs font-mono mt-1" style="color: var(--text-muted);">7 DAYS</div>
        </div>
        <div class="card-neon p-4 text-center group">
          <div class="text-3xl font-bold font-mono text-neon-purple">{{ stats.today_counts?.download || 0 }}</div>
          <div class="text-xs font-mono mt-1" style="color: var(--text-muted);">DL TODAY</div>
        </div>
      </div>

      <div class="flex flex-wrap gap-2 mb-6">
        <button v-for="type in logTypes" :key="type.value"
          @click="filterType = type.value; loadLogs()"
          class="px-3 py-1.5 rounded-lg text-xs font-mono transition-all duration-300"
          :style="filterType === type.value 
            ? 'background: rgba(14,165,233,0.12); border: 1px solid rgba(14,165,233,0.25); color: var(--accent);' 
            : 'background: var(--bg-surface); border: 1px solid var(--border-color); color: var(--text-secondary);'">
          {{ type.icon }} {{ type.label }}
          <span v-if="stats.type_counts?.[type.value]" class="ml-1 opacity-60">({{ stats.type_counts[type.value] }})</span>
        </button>
      </div>

      <div class="flex flex-col sm:flex-row gap-3 mb-6">
        <div class="relative flex-1">
          <input v-model="searchQuery" @keyup.enter="loadLogs()" type="text" placeholder="搜索日志..." class="input-cyber pl-10" />
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5" style="color: var(--text-muted);" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select v-model="dayFilter" @change="loadLogs()" class="input-cyber w-auto">
          <option :value="1">最近 24 小时</option><option :value="7">最近 7 天</option><option :value="30">最近 30 天</option><option :value="90">最近 90 天</option><option :value="0">全部</option>
        </select>
      </div>

      <div class="space-y-2">
        <div v-if="loading" class="text-center py-16">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-2 border-t-transparent" style="border-color: var(--accent); border-top-color: transparent;"></div>
          <p class="mt-3 font-mono text-sm" style="color: var(--text-muted);">LOADING...</p>
        </div>
        <div v-else-if="logs.length === 0" class="text-center py-16">
          <p class="font-mono text-sm" style="color: var(--text-muted);"><span class="text-neon opacity-40">></span> 暂无日志记录</p>
        </div>
        <div v-for="log in logs" :key="log.id" class="card-neon p-4 flex items-start gap-4 group">
          <div :class="['flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center text-lg', getTypeStyle(log.log_type)]">{{ getTypeIcon(log.log_type) }}</div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span :class="['text-xs px-2 py-0.5 rounded font-mono font-medium', getTypeBadgeStyle(log.log_type)]">{{ getTypeLabel(log.log_type) }}</span>
              <span v-if="log.status === 'fail'" class="text-xs px-2 py-0.5 rounded font-mono" style="background: rgba(236,72,153,0.1); color: var(--accent-pink); border: 1px solid rgba(236,72,153,0.2);">FAIL</span>
            </div>
            <p class="font-medium text-sm" style="color: var(--text-primary);">{{ log.action }}</p>
            <p v-if="log.target" class="text-xs font-mono mt-1" style="color: var(--text-muted);">TARGET: {{ log.target }}</p>
            <p v-if="log.detail" class="text-xs font-mono mt-1 truncate" style="color: var(--text-muted);">{{ formatDetail(log.detail) }}</p>
          </div>
          <div class="flex-shrink-0 text-right">
            <p class="text-xs font-mono" style="color: var(--text-secondary);">{{ formatTime(log.created_at) }}</p>
            <p class="text-xs font-mono mt-0.5" style="color: var(--text-muted);">{{ log.ip }}</p>
          </div>
        </div>
      </div>

      <div v-if="totalPages > 1" class="flex justify-center items-center gap-3 mt-8">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage <= 1"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all duration-300 disabled:opacity-30 text-neon"
                style="background: rgba(14,165,233,0.05); border: 1px solid rgba(14,165,233,0.1);">← PREV</button>
        <span class="text-sm font-mono" style="color: var(--text-secondary);">{{ currentPage }} / {{ totalPages }}</span>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all duration-300 disabled:opacity-30 text-neon"
                style="background: rgba(14,165,233,0.05); border: 1px solid rgba(14,165,233,0.1);">NEXT →</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAdminStatus, getLogs, getLogStats } from '../composables/useApi'

const isAdmin = getAdminStatus()
const logTypes = [
  { value: '', label: '全部', icon: '📊' }, { value: 'visit', label: '访问', icon: '👁️' },
  { value: 'modify', label: '修改', icon: '✏️' }, { value: 'download', label: '下载', icon: '⬇️' },
  { value: 'upload', label: '上传', icon: '⬆️' }, { value: 'delete', label: '删除', icon: '🗑️' },
  { value: 'tool_use', label: '工具使用', icon: '🔧' }, { value: 'auth', label: '认证', icon: '🔐' }
]
const logs = ref([]); const stats = ref({}); const loading = ref(false)
const currentPage = ref(1); const totalPages = ref(1); const filterType = ref(''); const searchQuery = ref(''); const dayFilter = ref(30)

const goToPage = (p) => { if (p < 1 || p > totalPages.value) return; currentPage.value = p; loadLogs(); window.scrollTo({ top: 0, behavior: 'smooth' }) }
const loadLogs = async () => {
  loading.value = true
  try { const d = await getLogs(currentPage.value, 20, filterType.value, searchQuery.value, dayFilter.value); logs.value = d.items || []; totalPages.value = d.pages || 1 }
  catch (e) { console.error('加载日志失败', e) } finally { loading.value = false }
}
const loadStats = async () => { try { stats.value = await getLogStats() } catch (e) { console.error('加载统计失败', e) } }

const getTypeIcon = (t) => ({ visit:'👁️',modify:'✏️',download:'⬇️',upload:'⬆️',delete:'🗑️',tool_use:'🔧',auth:'🔐' }[t]||'📝')
const getTypeLabel = (t) => ({ visit:'访问',modify:'修改',download:'下载',upload:'上传',delete:'删除',tool_use:'工具使用',auth:'认证' }[t]||t)
const getTypeStyle = (t) => {
  const s = { visit:'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400', modify:'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400', download:'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400', upload:'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400', delete:'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400', tool_use:'bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400', auth:'bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400' }
  return s[t] || 'bg-gray-100 dark:bg-gray-900/30 text-gray-600 dark:text-gray-400'
}
const getTypeBadgeStyle = (t) => {
  const s = { visit:'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-500/20', modify:'bg-yellow-50 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400 border border-yellow-200 dark:border-yellow-500/20', download:'bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 border border-green-200 dark:border-green-500/20', upload:'bg-purple-50 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 border border-purple-200 dark:border-purple-500/20', delete:'bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 border border-red-200 dark:border-red-500/20', tool_use:'bg-cyan-50 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400 border border-cyan-200 dark:border-cyan-500/20', auth:'bg-orange-50 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 border border-orange-200 dark:border-orange-500/20' }
  return s[t] || 'bg-gray-50 dark:bg-gray-900/30 text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-500/20'
}

const formatTime = (iso) => {
  if (!iso) return ''; const d = new Date(iso); const diff = Date.now() - d
  if (diff < 60000) return '刚刚'; if (diff < 3600000) return `${Math.floor(diff/60000)} 分钟前`
  if (diff < 86400000) return `${Math.floor(diff/3600000)} 小时前`; if (diff < 604800000) return `${Math.floor(diff/86400000)} 天前`
  return d.toLocaleString('zh-CN', { month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit' })
}
const formatDetail = (d) => { try { const o = typeof d==='string'?JSON.parse(d):d; return Object.entries(o).map(([k,v])=>`${k}: ${v}`).join(' | ') } catch { return d } }

onMounted(() => { loadLogs(); loadStats() })
</script>
