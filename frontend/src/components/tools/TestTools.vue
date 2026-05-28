<!-- 测试工具组件集合：HTTP请求测试、JWT解析器、cURL生成器、Mock数据生成、文本Diff对比 -->
<template>
  <div />
</template>
<script>
import { ref, computed } from 'vue'

// ==================== HTTP 请求测试 ====================
export const ToolHttpRequest = {
  name: 'ToolHttpRequest',
  setup() {
    const method = ref('GET')
    const url = ref('')
    const headers = ref([{ key: 'Content-Type', value: 'application/json' }])
    const body = ref('')
    const response = ref(null)
    const loading = ref(false)
    const error = ref('')
    const activeRespTab = ref('body')

    const methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']

    const addHeader = () => headers.value.push({ key: '', value: '' })
    const removeHeader = (i) => headers.value.splice(i, 1)

    const sendRequest = async () => {
      if (!url.value.trim()) { error.value = '请输入 URL'; return }
      loading.value = true; error.value = ''; response.value = null
      try {
        const hdrs = {}
        headers.value.forEach(h => { if (h.key.trim()) hdrs[h.key.trim()] = h.value })
        const opts = { method: method.value, headers: hdrs }
        if (['POST', 'PUT', 'PATCH'].includes(method.value) && body.value) opts.body = body.value
        const start = performance.now()
        const res = await fetch(url.value, opts)
        const elapsed = Math.round(performance.now() - start)
        const resHeaders = {}
        res.headers.forEach((v, k) => { resHeaders[k] = v })
        let resBody = await res.text()
        try { resBody = JSON.stringify(JSON.parse(resBody), null, 2) } catch {}
        response.value = { status: res.status, statusText: res.statusText, time: elapsed, headers: resHeaders, body: resBody }
      } catch (e) { error.value = '请求失败: ' + e.message }
      finally { loading.value = false }
    }

    const curlCommand = computed(() => {
      let cmd = `curl -X ${method.value}`
      headers.value.forEach(h => { if (h.key.trim()) cmd += ` -H "${h.key}: ${h.value}"` })
      if (['POST', 'PUT', 'PATCH'].includes(method.value) && body.value) cmd += ` -d '${body.value}'`
      cmd += ` "${url.value}"`
      return cmd
    })

    const copyCurl = () => { navigator.clipboard.writeText(curlCommand.value) }

    return { method, url, headers, body, response, loading, error, activeRespTab, methods, addHeader, removeHeader, sendRequest, curlCommand, copyCurl }
  },
  template: `
    <div class="space-y-4">
      <div class="flex gap-2">
        <select v-model="method" class="px-3 py-2.5 rounded-lg font-mono text-sm font-bold" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--accent); min-width: 100px;">
          <option v-for="m in methods" :key="m" :value="m">{{ m }}</option>
        </select>
        <input v-model="url" placeholder="https://api.example.com/endpoint" class="flex-1 px-4 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" @keyup.enter="sendRequest" />
        <button @click="sendRequest" :disabled="loading" class="px-6 py-2.5 rounded-lg font-mono text-sm font-bold transition-all" style="background: var(--accent); color: #fff;" :style="{ opacity: loading ? 0.6 : 1 }">
          {{ loading ? '发送中...' : '发送' }}
        </button>
      </div>

      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-mono" style="color: var(--text-muted);">请求头</span>
          <button @click="addHeader" class="text-xs font-mono px-2 py-1 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">+ 添加</button>
        </div>
        <div v-for="(h, i) in headers" :key="i" class="flex gap-2 mb-1.5">
          <input v-model="h.key" placeholder="Key" class="flex-1 px-3 py-1.5 rounded-lg font-mono text-xs" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
          <input v-model="h.value" placeholder="Value" class="flex-1 px-3 py-1.5 rounded-lg font-mono text-xs" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
          <button @click="removeHeader(i)" class="px-2 py-1.5 rounded-lg text-xs" style="color: var(--text-muted); background: var(--bg-secondary); border: 1px solid var(--border-color);">✕</button>
        </div>
      </div>

      <div v-if="['POST','PUT','PATCH'].includes(method)">
        <span class="text-xs font-mono mb-1 block" style="color: var(--text-muted);">请求体 (JSON)</span>
        <textarea v-model="body" rows="4" placeholder='{"key": "value"}' class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
      </div>

      <div class="flex items-center gap-2">
        <code class="text-xs font-mono flex-1 px-3 py-2 rounded-lg truncate" style="background: var(--bg-secondary); color: var(--text-muted);">{{ curlCommand }}</code>
        <button @click="copyCurl" class="text-xs font-mono px-3 py-2 rounded-lg" style="color: var(--accent); background: rgba(14,165,233,0.08); border: 1px solid rgba(14,165,233,0.15);">复制 cURL</button>
      </div>

      <div v-if="error" class="p-3 rounded-lg text-sm font-mono" style="background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); color: #ef4444;">{{ error }}</div>

      <div v-if="response" class="rounded-xl overflow-hidden" style="border: 1px solid var(--border-color);">
        <div class="flex items-center gap-4 px-4 py-2.5" style="background: var(--bg-secondary); border-bottom: 1px solid var(--border-color);">
          <span class="font-mono text-sm font-bold" :style="{ color: response.status < 400 ? '#10b981' : '#ef4444' }">{{ response.status }} {{ response.statusText }}</span>
          <span class="font-mono text-xs" style="color: var(--text-muted);">{{ response.time }}ms</span>
          <div class="flex-1" />
          <button v-for="tab in ['body','headers']" :key="tab" @click="activeRespTab = tab"
                  class="text-xs font-mono px-3 py-1 rounded-lg transition-colors"
                  :style="{ background: activeRespTab === tab ? 'rgba(14,165,233,0.1)' : 'transparent', color: activeRespTab === tab ? 'var(--accent)' : 'var(--text-muted)' }">
            {{ tab === 'body' ? 'Body' : 'Headers' }}
          </button>
        </div>
        <div v-if="activeRespTab === 'body'" class="p-4">
          <pre class="text-xs font-mono whitespace-pre-wrap break-all" style="color: var(--text-primary); max-height: 300px; overflow-y: auto;">{{ response.body }}</pre>
        </div>
        <div v-else class="p-4">
          <div v-for="(v, k) in response.headers" :key="k" class="flex gap-2 py-1" style="border-bottom: 1px solid var(--border-color);">
            <span class="font-mono text-xs font-bold" style="color: var(--accent); min-width: 200px;">{{ k }}</span>
            <span class="font-mono text-xs" style="color: var(--text-primary);">{{ v }}</span>
          </div>
        </div>
      </div>
    </div>
  `
}

// ==================== JWT 解析器 ====================
export const ToolJwtDecoder = {
  name: 'ToolJwtDecoder',
  setup() {
    const token = ref('')
    const error = ref('')

    const decoded = computed(() => {
      if (!token.value.trim()) return null
      try {
        const parts = token.value.trim().split('.')
        if (parts.length !== 3) { error.value = '无效的 JWT 格式（需要 3 段）'; return null }
        const decode = (str) => JSON.parse(atob(str.replace(/-/g, '+').replace(/_/g, '/')))
        const header = decode(parts[0])
        const payload = decode(parts[1])
        error.value = ''
        const now = Math.floor(Date.now() / 1000)
        const expStatus = payload.exp ? (payload.exp > now ? '有效' : '已过期') : '无过期时间'
        const iatStr = payload.iat ? new Date(payload.iat * 1000).toLocaleString() : '-'
        const expStr = payload.exp ? new Date(payload.exp * 1000).toLocaleString() : '-'
        return { header, payload, expStatus, iatStr, expStr, signature: parts[2] }
      } catch (e) { error.value = '解码失败: ' + e.message; return null }
    })

    const copyJson = (obj) => { navigator.clipboard.writeText(JSON.stringify(obj, null, 2)) }

    return { token, error, decoded, copyJson }
  },
  template: `
    <div class="space-y-4">
      <div>
        <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 粘贴 JWT Token</span>
        <textarea v-model="token" rows="4" placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U" class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
      </div>
      <div v-if="error" class="p-3 rounded-lg text-sm font-mono" style="background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); color: #ef4444;">{{ error }}</div>
      <div v-if="decoded" class="space-y-3">
        <div class="flex items-center gap-2 mb-2">
          <span class="px-2 py-0.5 rounded text-xs font-mono" :style="{ background: decoded.expStatus === '有效' ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)', color: decoded.expStatus === '有效' ? '#10b981' : '#ef4444', border: '1px solid ' + (decoded.expStatus === '有效' ? 'rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.2)') }">
            {{ decoded.expStatus }}
          </span>
          <span class="text-xs font-mono" style="color: var(--text-muted);">签发: {{ decoded.iatStr }} | 过期: {{ decoded.expStr }}</span>
        </div>
        <div v-for="section in [{key:'header',label:'Header'},{key:'payload',label:'Payload'}]" :key="section.key" class="rounded-xl overflow-hidden" style="border: 1px solid var(--border-color);">
          <div class="flex items-center justify-between px-4 py-2" style="background: var(--bg-secondary); border-bottom: 1px solid var(--border-color);">
            <span class="font-mono text-xs font-bold" style="color: var(--accent);">{{ section.label }}</span>
            <button @click="copyJson(decoded[section.key])" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--text-muted);">复制</button>
          </div>
          <pre class="p-4 text-xs font-mono whitespace-pre-wrap" style="color: var(--text-primary);">{{ JSON.stringify(decoded[section.key], null, 2) }}</pre>
        </div>
        <div class="rounded-xl overflow-hidden" style="border: 1px solid var(--border-color);">
          <div class="px-4 py-2" style="background: var(--bg-secondary); border-bottom: 1px solid var(--border-color);">
            <span class="font-mono text-xs font-bold" style="color: var(--accent);">Signature</span>
          </div>
          <pre class="p-4 text-xs font-mono break-all" style="color: var(--text-muted);">{{ decoded.signature }}</pre>
        </div>
      </div>
    </div>
  `
}

// ==================== 文本 Diff 对比 ====================
export const ToolTextDiff = {
  name: 'ToolTextDiff',
  setup() {
    const textA = ref('')
    const textB = ref('')

    const diffResult = computed(() => {
      if (!textA.value && !textB.value) return []
      const linesA = textA.value.split('\n')
      const linesB = textB.value.split('\n')
      const maxLen = Math.max(linesA.length, linesB.length)
      const result = []
      for (let i = 0; i < maxLen; i++) {
        const a = i < linesA.length ? linesA[i] : undefined
        const b = i < linesB.length ? linesB[i] : undefined
        if (a === b) result.push({ type: 'same', line: i + 1, text: a })
        else {
          if (a !== undefined) result.push({ type: 'removed', line: i + 1, text: a })
          if (b !== undefined) result.push({ type: 'added', line: i + 1, text: b })
        }
      }
      return result
    })

    const stats = computed(() => {
      const added = diffResult.value.filter(d => d.type === 'added').length
      const removed = diffResult.value.filter(d => d.type === 'removed').length
      return { added, removed, unchanged: diffResult.value.filter(d => d.type === 'same').length }
    })

    return { textA, textB, diffResult, stats }
  },
  template: `
    <div class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 原始文本</span>
          <textarea v-model="textA" rows="8" placeholder="输入原始文本..." class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 对比文本</span>
          <textarea v-model="textB" rows="8" placeholder="输入对比文本..." class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
      </div>
      <div v-if="diffResult.length > 0" class="flex items-center gap-4 text-xs font-mono" style="color: var(--text-muted);">
        <span style="color: #10b981;">+{{ stats.added }} 新增</span>
        <span style="color: #ef4444;">-{{ stats.removed }} 删除</span>
        <span>{{ stats.unchanged }} 未变</span>
      </div>
      <div v-if="diffResult.length > 0" class="rounded-xl overflow-hidden" style="border: 1px solid var(--border-color);">
        <div v-for="(d, i) in diffResult" :key="i" class="flex font-mono text-xs" style="border-bottom: 1px solid var(--border-color);"
             :style="{ background: d.type === 'added' ? 'rgba(16,185,129,0.06)' : d.type === 'removed' ? 'rgba(239,68,68,0.06)' : 'transparent' }">
          <span class="w-8 text-center py-1.5 select-none" style="color: var(--text-muted); background: var(--bg-secondary); border-right: 1px solid var(--border-color);">{{ d.line }}</span>
          <span class="w-6 text-center py-1.5 select-none" :style="{ color: d.type === 'added' ? '#10b981' : d.type === 'removed' ? '#ef4444' : 'var(--text-muted)' }">{{ d.type === 'added' ? '+' : d.type === 'removed' ? '-' : ' ' }}</span>
          <span class="flex-1 py-1.5 px-2 whitespace-pre-wrap break-all" :style="{ color: d.type === 'added' ? '#10b981' : d.type === 'removed' ? '#ef4444' : 'var(--text-primary)', textDecoration: d.type === 'removed' ? 'line-through' : 'none' }">{{ d.text }}</span>
        </div>
      </div>
    </div>
  `
}

// ==================== Mock 数据生成 ====================
export const ToolMockData = {
  name: 'ToolMockData',
  setup() {
    const count = ref(10)
    const result = ref('')

    const surnames = '王李张刘陈杨赵黄周吴徐孙马胡朱郭何罗高林梁郑谢韩唐冯于董萧程曹袁邓许傅'.split('')
    const names = '伟芳娜秀英敏静丽强磊洋艳勇军杰娟涛超明刚平辉鑫蕾亮峰'.split('')
    const domains = ['qq.com', '163.com', 'gmail.com', 'outlook.com', 'foxmail.com']
    const cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京', '西安', '重庆']

    const rand = (arr) => arr[Math.floor(Math.random() * arr.length)]
    const randNum = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min
    const randPhone = () => '1' + ['3', '5', '7', '8', '9'][randNum(0, 4)] + String(randNum(100000000, 999999999))

    const fields = ref([
      { key: 'id', label: 'ID', enabled: true },
      { key: 'name', label: '姓名', enabled: true },
      { key: 'phone', label: '手机号', enabled: true },
      { key: 'email', label: '邮箱', enabled: true },
      { key: 'age', label: '年龄', enabled: true },
      { key: 'city', label: '城市', enabled: true },
      { key: 'address', label: '地址', enabled: false },
      { key: 'company', label: '公司', enabled: false },
      { key: 'date', label: '日期', enabled: false },
      { key: 'boolean', label: '布尔值', enabled: false },
    ])

    const generate = () => {
      const data = []
      for (let i = 0; i < count.value; i++) {
        const item = {}
        const sur = rand(surnames)
        const nm = rand(names)
        fields.value.forEach(f => {
          if (!f.enabled) return
          switch (f.key) {
            case 'id': item.id = i + 1; break
            case 'name': item.name = sur + nm; break
            case 'phone': item.phone = randPhone(); break
            case 'email': item.email = (sur + nm).toLowerCase() + randNum(1, 999) + '@' + rand(domains); break
            case 'age': item.age = randNum(18, 60); break
            case 'city': item.city = rand(cities); break
            case 'address': item.address = rand(cities) + '市XX区XX路' + randNum(1, 999) + '号'; break
            case 'company': item.company = rand(['腾讯', '阿里', '字节', '百度', '华为', '小米', '美团', '京东']) + '科技有限公司'; break
            case 'date': item.date = '2024-' + String(randNum(1, 12)).padStart(2, '0') + '-' + String(randNum(1, 28)).padStart(2, '0'); break
            case 'boolean': item.active = Math.random() > 0.5; break
          }
        })
        data.push(item)
      }
      result.value = JSON.stringify(data, null, 2)
    }

    const copyResult = () => { navigator.clipboard.writeText(result.value) }

    return { count, result, fields, generate, copyResult }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-4 flex-wrap">
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono" style="color: var(--text-muted);">生成数量:</span>
          <input v-model.number="count" type="number" min="1" max="1000" class="w-20 px-3 py-1.5 rounded-lg font-mono text-sm text-center" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <button @click="generate" class="px-5 py-2 rounded-lg font-mono text-sm font-bold" style="background: var(--accent); color: #fff;">生成数据</button>
      </div>
      <div>
        <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 选择字段</span>
        <div class="flex flex-wrap gap-2">
          <label v-for="f in fields" :key="f.key" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg cursor-pointer text-xs font-mono transition-all"
                 :style="{ background: f.enabled ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (f.enabled ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: f.enabled ? 'var(--accent)' : 'var(--text-muted)' }">
            <input type="checkbox" v-model="f.enabled" class="accent-sky-500" />
            {{ f.label }}
          </label>
        </div>
      </div>
      <div v-if="result" class="relative">
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-xs font-mono" style="color: var(--text-muted);">// 生成结果</span>
          <button @click="copyResult" class="text-xs font-mono px-3 py-1 rounded-lg" style="color: var(--accent); background: rgba(14,165,233,0.08);">复制</button>
        </div>
        <pre class="p-4 rounded-xl text-xs font-mono whitespace-pre-wrap" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary); max-height: 400px; overflow-y: auto;">{{ result }}</pre>
      </div>
    </div>
  `
}
</script>
