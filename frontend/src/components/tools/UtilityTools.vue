<!-- 实用工具组件集合：正则测试、时间戳、哈希、二维码、图片转Base64、IP查询、颜色选择器 -->
<template><div /></template>
<script>
import { ref, computed, watch, onMounted } from 'vue'
import CryptoJS from 'crypto-js'
import QRCode from 'qrcode'

// ==================== 正则表达式测试 ====================
export const ToolRegexTester = {
  name: 'ToolRegexTester',
  setup() {
    const pattern = ref('')
    const flags = ref('g')
    const testStr = ref('')
    const error = ref('')

    const flagOptions = [
      { key: 'g', label: 'global' },
      { key: 'i', label: 'insensitive' },
      { key: 'm', label: 'multiline' },
      { key: 's', label: 'dotAll' }
    ]

    const toggleFlag = (f) => {
      flags.value = flags.value.includes(f) ? flags.value.replace(f, '') : flags.value + f
    }

    const escapeHtml = (str) => str.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>')

    const matches = computed(() => {
      if (!pattern.value || !testStr.value) return { list: [], count: 0, highlighted: testStr.value }
      try {
        const regex = new RegExp(pattern.value, flags.value)
        const list = []
        let match
        if (flags.value.includes('g')) {
          while ((match = regex.exec(testStr.value)) !== null) {
            list.push({ text: match[0], index: match.index, groups: match.slice(1) })
            if (!match[0]) { regex.lastIndex++ }
          }
        } else {
          match = regex.exec(testStr.value)
          if (match) list.push({ text: match[0], index: match.index, groups: match.slice(1) })
        }
        error.value = ''
        let highlighted = ''
        let lastIdx = 0
        for (const m of list) {
          highlighted += escapeHtml(testStr.value.slice(lastIdx, m.index))
          highlighted += '<mark style="background:rgba(14,165,233,0.2);color:var(--accent);border-radius:2px;padding:0 2px;">' + escapeHtml(m.text) + '</mark>'
          lastIdx = m.index + m.text.length
        }
        highlighted += escapeHtml(testStr.value.slice(lastIdx))
        return { list, count: list.length, highlighted }
      } catch (e) { error.value = '\u6b63\u5219\u8868\u8fbe\u5f0f\u9519\u8bef: ' + e.message; return { list: [], count: 0, highlighted: testStr.value } }
    })

    const presets = [
      { label: '\u90ae\u7bb1', pattern: '[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}' },
      { label: '\u624b\u673a\u53f7', pattern: '1[3-9]\\d{9}' },
      { label: 'URL', pattern: 'https?://[\\w.-]+(?:/[\\w.-]*)*' },
      { label: 'IP\u5730\u5740', pattern: '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}' },
      { label: '\u65e5\u671f', pattern: '\\d{4}[-/]\\d{2}[-/]\\d{2}' },
      { label: '\u4e2d\u6587', pattern: '[\\u4e00-\\u9fa5]+' }
    ]

    return { pattern, flags, testStr, error, matches, flagOptions, toggleFlag, presets }
  },
  template: `
    <div class="space-y-4">
      <div>
        <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// \u6b63\u5219\u8868\u8fbe\u5f0f</span>
        <div class="flex gap-2">
          <span class="px-3 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">/</span>
          <input v-model="pattern" placeholder="\u8f93\u5165\u6b63\u5219\u8868\u8fbe\u5f0f..." class="flex-1 px-4 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
          <span class="px-3 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">/</span>
          <input v-model="flags" class="w-16 px-3 py-2.5 rounded-lg font-mono text-sm text-center" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--accent);" />
        </div>
        <div class="flex items-center gap-2 mt-2">
          <button v-for="f in flagOptions" :key="f.key" @click="toggleFlag(f.key)"
                  class="px-3 py-1 rounded-lg font-mono text-xs transition-all"
                  :style="{ background: flags.includes(f.key) ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (flags.includes(f.key) ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: flags.includes(f.key) ? 'var(--accent)' : 'var(--text-muted)' }">
            {{ f.label }}
          </button>
        </div>
      </div>

      <div>
        <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// \u5feb\u6377\u9884\u8bbe</span>
        <div class="flex flex-wrap gap-2">
          <button v-for="p in presets" :key="p.label" @click="pattern = p.pattern"
                  class="px-3 py-1.5 rounded-lg font-mono text-xs transition-all"
                  style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">
            {{ p.label }}
          </button>
        </div>
      </div>

      <div>
        <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// \u6d4b\u8bd5\u6587\u672c</span>
        <textarea v-model="testStr" rows="6" placeholder="\u8f93\u5165\u8981\u6d4b\u8bd5\u7684\u6587\u672c..." class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
      </div>

      <div v-if="error" class="p-3 rounded-lg text-sm font-mono" style="background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); color: #ef4444;">{{ error }}</div>

      <div v-if="matches.count > 0" class="space-y-3">
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 rounded text-xs font-mono font-bold" style="background: rgba(14,165,233,0.1); color: var(--accent); border: 1px solid rgba(14,165,233,0.25);">\u5339\u914d {{ matches.count }} \u9879</span>
        </div>
        <div class="p-4 rounded-xl font-mono text-xs whitespace-pre-wrap break-all" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" v-html="matches.highlighted" />
        <div class="rounded-xl overflow-hidden" style="border: 1px solid var(--border-color);">
          <div v-for="(m, i) in matches.list" :key="i" class="flex items-start gap-4 px-4 py-2 font-mono text-xs" style="border-bottom: 1px solid var(--border-color);">
            <span style="color: var(--text-muted); min-width: 32px;">#{{ i + 1 }}</span>
            <span style="color: var(--accent);" class="break-all">"{{ m.text }}"</span>
            <span style="color: var(--text-muted);">\u7d22\u5f15: {{ m.index }}</span>
            <span v-if="m.groups.length > 0" style="color: var(--text-muted);">\u5206\u7ec4: {{ m.groups.join(', ') }}</span>
          </div>
        </div>
      </div>
      <div v-else-if="pattern && testStr && !error" class="p-4 rounded-xl text-center font-mono text-sm" style="background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.15); color: #ef4444;">
        \u65e0\u5339\u914d\u7ed3\u679c
      </div>
    </div>
  `
}

// ==================== 时间戳转换 ====================
export const ToolTimestamp = {
  name: 'ToolTimestamp',
  setup() {
    const timestamp = ref(Math.floor(Date.now() / 1000).toString())
    const datetime = ref('')
    const outputTimestamp = ref('')
    const outputDatetime = ref('')
    const nowTs = ref(Math.floor(Date.now() / 1000))
    const nowStr = ref(new Date().toLocaleString())
    const error = ref('')

    onMounted(() => {
      setInterval(() => {
        nowTs.value = Math.floor(Date.now() / 1000)
        nowStr.value = new Date().toLocaleString()
      }, 1000)
    })

    const getRelativeTime = (d) => {
      const diff = Date.now() - d.getTime()
      const absDiff = Math.abs(diff)
      const isFuture = diff < 0
      if (absDiff < 60000) return isFuture ? '\u5373\u5c06' : '\u521a\u521a'
      if (absDiff < 3600000) { const m = Math.floor(absDiff / 60000); return isFuture ? m + '\u5206\u949f\u540e' : m + '\u5206\u949f\u524d' }
      if (absDiff < 86400000) { const h = Math.floor(absDiff / 3600000); return isFuture ? h + '\u5c0f\u65f6\u540e' : h + '\u5c0f\u65f6\u524d' }
      const days = Math.floor(absDiff / 86400000)
      return isFuture ? days + '\u5929\u540e' : days + '\u5929\u524d'
    }

    const tsToDate = () => {
      error.value = ''
      try {
        let ts = parseInt(timestamp.value)
        if (isNaN(ts)) { error.value = '\u8bf7\u8f93\u5165\u6709\u6548\u7684\u65f6\u95f4\u6233'; return }
        if (ts > 1e12) ts = Math.floor(ts / 1000)
        const d = new Date(ts * 1000)
        outputDatetime.value = '\u672c\u5730\u65f6\u95f4: ' + d.toLocaleString() + '\nISO 8601: ' + d.toISOString() + '\nUTC: ' + d.toUTCString() + '\n\u76f8\u5bf9\u65f6\u95f4: ' + getRelativeTime(d)
      } catch (e) { error.value = '\u8f6c\u6362\u5931\u8d25: ' + e.message }
    }

    const dateToTs = () => {
      error.value = ''
      try {
        if (!datetime.value.trim()) { error.value = '\u8bf7\u8f93\u5165\u65e5\u671f\u65f6\u95f4'; return }
        const d = new Date(datetime.value)
        if (isNaN(d.getTime())) { error.value = '\u65e0\u6548\u7684\u65e5\u671f\u683c\u5f0f'; return }
        outputTimestamp.value = '\u79d2\u7ea7\u65f6\u95f4\u6233: ' + Math.floor(d.getTime() / 1000) + '\n\u6beb\u79d2\u65f6\u95f4\u6233: ' + d.getTime()
      } catch (e) { error.value = '\u8f6c\u6362\u5931\u8d25: ' + e.message }
    }

    const useNow = () => { timestamp.value = nowTs.value.toString(); tsToDate() }

    return { timestamp, datetime, outputTimestamp, outputDatetime, nowTs, nowStr, error, tsToDate, dateToTs, useNow }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-3 px-4 py-3 rounded-xl" style="background: rgba(14,165,233,0.05); border: 1px solid rgba(14,165,233,0.15);">
        <svg class="w-5 h-5 shrink-0" style="color: var(--accent);" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span class="font-mono text-sm" style="color: var(--text-primary);">\u5f53\u524d\u65f6\u95f4: <span style="color: var(--accent);">{{ nowStr }}</span></span>
        <span class="font-mono text-xs" style="color: var(--text-muted);">({{ nowTs }})</span>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-3">
          <div>
            <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// \u65f6\u95f4\u6233 \u2192 \u65e5\u671f</span>
            <div class="flex gap-2">
              <input v-model="timestamp" placeholder="1609459200" class="flex-1 px-4 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" @keyup.enter="tsToDate" />
              <button @click="tsToDate" class="px-4 py-2.5 rounded-lg font-mono text-sm font-bold" style="background: var(--accent); color: #fff;">\u8f6c\u6362</button>
            </div>
            <button @click="useNow" class="mt-2 text-xs font-mono px-3 py-1 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">\u4f7f\u7528\u5f53\u524d\u65f6\u95f4\u6233</button>
          </div>
          <div v-if="outputDatetime" class="p-4 rounded-xl font-mono text-xs whitespace-pre-wrap" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);">{{ outputDatetime }}</div>
        </div>

        <div class="space-y-3">
          <div>
            <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// \u65e5\u671f \u2192 \u65f6\u95f4\u6233</span>
            <div class="flex gap-2">
              <input v-model="datetime" placeholder="2025-01-01 12:00:00" class="flex-1 px-4 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" @keyup.enter="dateToTs" />
              <button @click="dateToTs" class="px-4 py-2.5 rounded-lg font-mono text-sm font-bold" style="background: var(--accent); color: #fff;">\u8f6c\u6362</button>
            </div>
            <button @click="datetime = new Date().toISOString().slice(0, 19).replace('T', ' '); dateToTs()" class="mt-2 text-xs font-mono px-3 py-1 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">\u4f7f\u7528\u5f53\u524d\u65f6\u95f4</button>
          </div>
          <div v-if="outputTimestamp" class="p-4 rounded-xl font-mono text-xs whitespace-pre-wrap" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);">{{ outputTimestamp }}</div>
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== 哈希生成器 ====================
export const ToolHashGenerator = {
  name: 'ToolHashGenerator',
  setup() {
    const input = ref('')
    const error = ref('')

    const hashes = computed(() => {
      if (!input.value) return []
      try {
        return [
          { name: 'MD5', value: CryptoJS.MD5(input.value).toString() },
          { name: 'SHA1', value: CryptoJS.SHA1(input.value).toString() },
          { name: 'SHA256', value: CryptoJS.SHA256(input.value).toString() },
          { name: 'SHA512', value: CryptoJS.SHA512(input.value).toString() },
          { name: 'HMAC-MD5', value: CryptoJS.HmacMD5(input.value, 'key').toString() },
          { name: 'HMAC-SHA256', value: CryptoJS.HmacSHA256(input.value, 'key').toString() }
        ]
      } catch (e) { error.value = '\u8ba1\u7b97\u5931\u8d25: ' + e.message; return [] }
    })

    const copyHash = (val) => { navigator.clipboard.writeText(val) }

    return { input, error, hashes, copyHash }
  },
  template: `
    <div class="space-y-4">
      <div>
        <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// \u8f93\u5165\u6587\u672c</span>
        <textarea v-model="input" rows="4" placeholder="\u8f93\u5165\u8981\u8ba1\u7b97\u54c8\u5e0c\u503c\u7684\u6587\u672c..." class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
      </div>
      <div v-if="hashes.length > 0" class="space-y-2">
        <div v-for="h in hashes" :key="h.name" class="flex items-center gap-2">
          <span class="font-mono text-xs font-bold px-2 py-1 rounded shrink-0" style="background: rgba(14,165,233,0.08); color: var(--accent); min-width: 100px;">{{ h.name }}</span>
          <code class="flex-1 px-3 py-1.5 rounded-lg font-mono text-xs break-all select-all" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);">{{ h.value }}</code>
          <button @click="copyHash(h.value)" class="px-2 py-1.5 rounded-lg font-mono text-xs shrink-0" style="color: var(--accent); background: rgba(14,165,233,0.08);">\u590d\u5236</button>
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== 二维码生成器 ====================
export const ToolQrCode = {
  name: 'ToolQrCode',
  setup() {
    const text = ref('')
    const size = ref(256)
    const qrDataUrl = ref('')
    const error = ref('')

    const generate = async () => {
      error.value = ''
      if (!text.value.trim()) { qrDataUrl.value = ''; return }
      try {
        qrDataUrl.value = await QRCode.toDataURL(text.value, {
          width: size.value,
          margin: 2,
          color: { dark: '#000000', light: '#ffffff' }
        })
      } catch (e) { error.value = '\u751f\u6210\u5931\u8d25: ' + e.message }
    }

    const download = () => {
      if (!qrDataUrl.value) return
      const a = document.createElement('a')
      a.href = qrDataUrl.value
      a.download = 'qrcode.png'
      a.click()
    }

    watch(text, generate)
    watch(size, generate)

    return { text, size, qrDataUrl, error, download }
  },
  template: `
    <div class="space-y-4">
      <div>
        <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// \u8f93\u5165\u5185\u5bb9\uff08\u6587\u672c\u6216URL\uff09</span>
        <input v-model="text" placeholder="https://example.com" class="w-full px-4 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
      </div>
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono" style="color: var(--text-muted);">\u5c3a\u5bf8:</span>
          <select v-model.number="size" class="px-3 py-1.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);">
            <option :value="128">128px</option>
            <option :value="256">256px</option>
            <option :value="512">512px</option>
            <option :value="1024">1024px</option>
          </select>
        </div>
        <button v-if="qrDataUrl" @click="download" class="px-4 py-1.5 rounded-lg font-mono text-sm" style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.25); color: #10b981;">\u4e0b\u8f7d PNG</button>
      </div>
      <div v-if="qrDataUrl" class="flex justify-center p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-color);">
        <img :src="qrDataUrl" alt="QR Code" class="rounded-lg" style="max-width: 300px;" />
      </div>
      <div v-else class="text-center py-12 font-mono text-sm" style="color: var(--text-muted);">\u8f93\u5165\u5185\u5bb9\u540e\u81ea\u52a8\u751f\u6210\u4e8c\u7ef4\u7801</div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== 图片转 Base64 ====================
export const ToolImageToBase64 = {
  name: 'ToolImageToBase64',
  setup() {
    const base64Output = ref('')
    const preview = ref('')
    const fileName = ref('')
    const fileSize = ref('')
    const error = ref('')
    const base64Input = ref('')
    const imagePreview = ref('')

    const isDragging = ref(false)
    const fileInputRef = ref(null)

    const processFile = (file) => {
      if (!file) return
      if (!file.type.startsWith('image/')) { error.value = '\u8bf7\u9009\u62e9\u56fe\u7247\u6587\u4ef6'; return }
      error.value = ''
      fileName.value = file.name
      fileSize.value = (file.size / 1024).toFixed(2) + ' KB'
      const reader = new FileReader()
      reader.onload = () => {
        base64Output.value = reader.result
        preview.value = reader.result
      }
      reader.readAsDataURL(file)
    }

    const handleFile = (e) => {
      processFile(e.target.files[0])
    }

    const handleDrop = (e) => {
      e.preventDefault()
      isDragging.value = false
      const file = e.dataTransfer.files[0]
      processFile(file)
    }

    const handleDragOver = (e) => {
      e.preventDefault()
      isDragging.value = true
    }

    const handleDragLeave = () => {
      isDragging.value = false
    }

    const triggerFileInput = () => {
      fileInputRef.value && fileInputRef.value.click()
    }

    const copyBase64 = () => { navigator.clipboard.writeText(base64Output.value) }

    const handleBase64Input = () => {
      try {
        if (!base64Input.value.trim()) { imagePreview.value = ''; return }
        let src = base64Input.value.trim()
        if (!src.startsWith('data:')) src = 'data:image/png;base64,' + src
        imagePreview.value = src
      } catch { imagePreview.value = '' }
    }

    const downloadImage = () => {
      if (!imagePreview.value) return
      const a = document.createElement('a')
      a.href = imagePreview.value
      a.download = 'image.png'
      a.click()
    }

    return { base64Output, preview, fileName, fileSize, error, handleFile, copyBase64, base64Input, imagePreview, handleBase64Input, downloadImage, isDragging, handleDrop, handleDragOver, handleDragLeave, triggerFileInput, fileInputRef }
  },
  template: `
    <div class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-3">
          <span class="text-xs font-mono block" style="color: var(--text-muted);">// \u56fe\u7247 \u2192 Base64</span>
          <input ref="fileInputRef" type="file" accept="image/*" @change="handleFile" class="hidden" />
          <div v-if="!preview" @click="triggerFileInput" @drop="handleDrop" @dragover="handleDragOver" @dragleave="handleDragLeave"
               class="flex flex-col items-center justify-center gap-3 p-6 rounded-xl cursor-pointer transition-all"
               :style="{ background: isDragging ? 'rgba(14,165,233,0.06)' : 'var(--bg-secondary)', border: '2px dashed ' + (isDragging ? 'var(--accent)' : 'var(--border-color)'), color: isDragging ? 'var(--accent)' : 'var(--text-muted)' }">
            <svg class="w-8 h-8 transition-all" :style="{ color: isDragging ? 'var(--accent)' : 'var(--text-muted)', opacity: isDragging ? '1' : '0.6' }" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            <span class="text-xs font-mono">{{ isDragging ? '\u62fe\u53d6\u653e\u4e0b\u56fe\u7247...' : '\u70b9\u51fb\u6216\u62fd\u62fd\u56fe\u7247\u5230\u6b64' }}</span>
            <span class="text-[10px] font-mono" style="color: var(--text-muted); opacity: 0.6;">PNG / JPG / GIF / WebP</span>
          </div>
          <div v-if="preview" class="flex justify-center p-4 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-color);">
            <img :src="preview" class="rounded-lg max-h-40" />
          </div>
          <div v-if="fileName" class="text-xs font-mono" style="color: var(--text-muted);">{{ fileName }} ({{ fileSize }})</div>
          <div v-if="base64Output" class="flex items-center gap-2">
            <button @click="copyBase64" class="px-3 py-1.5 rounded-lg font-mono text-xs font-semibold transition-all hover:opacity-80" style="color: var(--accent); background: rgba(14,165,233,0.1); border: 1px solid rgba(14,165,233,0.2);">\u590d\u5236 Base64</button>
            <span class="text-xs font-mono" style="color: var(--text-muted);">{{ (base64Output.length / 1024).toFixed(2) }} KB</span>
            <button @click="triggerFileInput" class="px-3 py-1.5 rounded-lg font-mono text-xs transition-all hover:opacity-80" style="color: var(--text-muted); background: var(--bg-secondary); border: 1px solid var(--border-color);">\u91cd\u65b0\u9009\u62e9</button>
          </div>
        </div>

        <div class="space-y-3">
          <span class="text-xs font-mono block" style="color: var(--text-muted);">// Base64 \u2192 \u56fe\u7247</span>
          <textarea v-model="base64Input" rows="4" placeholder="\u7c98\u8d34 Base64 \u5b57\u7b26\u4e32..." class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" @input="handleBase64Input" />
          <div v-if="imagePreview" class="flex flex-col items-center gap-2">
            <div class="p-4 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-color);">
              <img :src="imagePreview" class="rounded-lg max-h-40" />
            </div>
            <button @click="downloadImage" class="px-3 py-1.5 rounded-lg font-mono text-xs" style="color: #10b981; background: rgba(16,185,129,0.08);">\u4e0b\u8f7d\u56fe\u7247</button>
          </div>
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== IP 地址查询 ====================
export const ToolIpLookup = {
  name: 'ToolIpLookup',
  setup() {
    const ip = ref('')
    const result = ref(null)
    const loading = ref(false)
    const error = ref('')

    const lookup = async () => {
      if (!ip.value.trim()) { error.value = '\u8bf7\u8f93\u5165 IP \u5730\u5740'; return }
      loading.value = true; error.value = ''; result.value = null
      try {
        const res = await fetch('http://ip-api.com/json/' + ip.value + '?lang=zh-CN')
        const data = await res.json()
        if (data.status === 'fail') { error.value = '\u67e5\u8be2\u5931\u8d25: ' + data.message; return }
        result.value = data
      } catch (e) { error.value = '\u67e5\u8be2\u5931\u8d25: ' + e.message }
      finally { loading.value = false }
    }

    const lookupMyIp = async () => {
      loading.value = true; error.value = ''; result.value = null
      try {
        const res = await fetch('http://ip-api.com/json/?lang=zh-CN')
        const data = await res.json()
        if (data.status === 'fail') { error.value = '\u67e5\u8be2\u5931\u8d25: ' + data.message; return }
        ip.value = data.query
        result.value = data
      } catch (e) { error.value = '\u67e5\u8be2\u5931\u8d25: ' + e.message }
      finally { loading.value = false }
    }

    const fields = computed(() => {
      if (!result.value) return []
      const r = result.value
      return [
        { label: 'IP', value: r.query },
        { label: '\u56fd\u5bb6', value: r.country },
        { label: '\u5730\u533a', value: r.regionName },
        { label: '\u57ce\u5e02', value: r.city },
        { label: 'ISP', value: r.isp },
        { label: '\u7ec4\u7ec7', value: r.org },
        { label: 'AS', value: r.as },
        { label: '\u65f6\u533a', value: r.timezone },
        { label: '\u7ecf\u7eac\u5ea6', value: r.lat + ', ' + r.lon }
      ]
    })

    return { ip, result, loading, error, lookup, lookupMyIp, fields }
  },
  template: `
    <div class="space-y-4">
      <div class="flex gap-2">
        <input v-model="ip" placeholder="\u8f93\u5165 IP \u5730\u5740..." class="flex-1 px-4 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" @keyup.enter="lookup" />
        <button @click="lookup" :disabled="loading" class="px-5 py-2.5 rounded-lg font-mono text-sm font-bold" style="background: var(--accent); color: #fff;" :style="{ opacity: loading ? 0.6 : 1 }">
          {{ loading ? '\u67e5\u8be2\u4e2d...' : '\u67e5\u8be2' }}
        </button>
        <button @click="lookupMyIp" class="px-4 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">\u67e5\u8be2\u672c\u673a</button>
      </div>

      <div v-if="error" class="p-3 rounded-lg text-sm font-mono" style="background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); color: #ef4444;">{{ error }}</div>

      <div v-if="fields.length > 0" class="rounded-xl overflow-hidden" style="border: 1px solid var(--border-color);">
        <div v-for="f in fields" :key="f.label" class="flex items-center px-4 py-2.5 font-mono text-sm" style="border-bottom: 1px solid var(--border-color);">
          <span class="w-20 shrink-0 text-xs font-bold" style="color: var(--accent);">{{ f.label }}</span>
          <span class="flex-1 text-sm" style="color: var(--text-primary);">{{ f.value || '-' }}</span>
        </div>
      </div>

      <div v-if="!result && !loading && !error" class="text-center py-8 font-mono text-sm" style="color: var(--text-muted);">
        \u8f93\u5165 IP \u5730\u5740\u6216\u70b9\u51fb\u201c\u67e5\u8be2\u672c\u673a\u201d\u5f00\u59cb
      </div>
    </div>
  `
}

// ==================== 颜色选择器 ====================
export const ToolColorPicker = {
  name: 'ToolColorPicker',
  setup() {
    const color = ref('#0ea5e9')
    const r = ref(14)
    const g = ref(165)
    const b = ref(233)
    const h = ref(199)
    const s = ref(92)
    const l = ref(48)

    const hex = computed(() => color.value)

    const rgbToHex = (rr, gg, bb) => '#' + [rr, gg, bb].map(x => Math.max(0, Math.min(255, x)).toString(16).padStart(2, '0')).join('')

    const hexToRgb = (hexStr) => {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hexStr)
      return result ? { r: parseInt(result[1], 16), g: parseInt(result[2], 16), b: parseInt(result[3], 16) } : { r: 0, g: 0, b: 0 }
    }

    const rgbToHsl = (rr, gg, bb) => {
      rr /= 255; gg /= 255; bb /= 255
      const max = Math.max(rr, gg, bb), min = Math.min(rr, gg, bb)
      let hh = 0, ss = 0, ll = (max + min) / 2
      if (max !== min) {
        const d = max - min
        ss = ll > 0.5 ? d / (2 - max - min) : d / (max + min)
        switch (max) {
          case rr: hh = ((gg - bb) / d + (gg < bb ? 6 : 0)) / 6; break
          case gg: hh = ((bb - rr) / d + 2) / 6; break
          case bb: hh = ((rr - gg) / d + 4) / 6; break
        }
      }
      return { h: Math.round(hh * 360), s: Math.round(ss * 100), l: Math.round(ll * 100) }
    }

    const updateFromColor = () => {
      const rgb = hexToRgb(color.value)
      r.value = rgb.r; g.value = rgb.g; b.value = rgb.b
      const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b)
      h.value = hsl.h; s.value = hsl.s; l.value = hsl.l
    }

    const updateFromRgb = () => {
      color.value = rgbToHex(r.value, g.value, b.value)
      const hsl = rgbToHsl(r.value, g.value, b.value)
      h.value = hsl.h; s.value = hsl.s; l.value = hsl.l
    }

    const updateFromHsl = () => {
      const hh = h.value / 360, ss = s.value / 100, ll = l.value / 100
      let rr, gg, bb
      if (ss === 0) { rr = gg = bb = ll }
      else {
        const hue2rgb = (p, q, t) => { if (t < 0) t += 1; if (t > 1) t -= 1; if (t < 1/6) return p + (q - p) * 6 * t; if (t < 1/2) return q; if (t < 2/3) return p + (q - p) * (2/3 - t) * 6; return p }
        const q = ll < 0.5 ? ll * (1 + ss) : ll + ss - ll * ss
        const p = 2 * ll - q
        rr = hue2rgb(p, q, hh + 1/3)
        gg = hue2rgb(p, q, hh)
        bb = hue2rgb(p, q, hh - 1/3)
      }
      r.value = Math.round(rr * 255); g.value = Math.round(gg * 255); b.value = Math.round(bb * 255)
      color.value = rgbToHex(r.value, g.value, b.value)
    }

    const formats = computed(() => [
      { label: 'HEX', value: color.value },
      { label: 'RGB', value: 'rgb(' + r.value + ', ' + g.value + ', ' + b.value + ')' },
      { label: 'HSL', value: 'hsl(' + h.value + ', ' + s.value + '%, ' + l.value + '%)' }
    ])

    const copyColor = (val) => { navigator.clipboard.writeText(val) }

    const updateColorInput = (e) => {
      color.value = e.target.value
      updateFromColor()
    }

    return { color, r, g, b, h, s, l, hex, formats, copyColor, updateFromColor, updateFromRgb, updateFromHsl, updateColorInput }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-start gap-6">
        <div class="flex flex-col items-center gap-3">
          <div class="w-32 h-32 rounded-xl border-2" :style="{ background: color, borderColor: 'var(--border-color)' }" />
          <input type="color" :value="color" @input="updateColorInput" class="w-32 h-10 rounded-lg cursor-pointer" style="background: var(--bg-secondary);" />
        </div>

        <div class="flex-1 space-y-3">
          <div>
            <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">RGB</span>
            <div class="grid grid-cols-3 gap-2">
              <div>
                <label class="text-[10px] font-mono block mb-1" style="color: #ef4444;">R: {{ r }}</label>
                <input v-model.number="r" type="range" min="0" max="255" class="w-full accent-red-500" @input="updateFromRgb" />
              </div>
              <div>
                <label class="text-[10px] font-mono block mb-1" style="color: #10b981;">G: {{ g }}</label>
                <input v-model.number="g" type="range" min="0" max="255" class="w-full accent-green-500" @input="updateFromRgb" />
              </div>
              <div>
                <label class="text-[10px] font-mono block mb-1" style="color: #3b82f6;">B: {{ b }}</label>
                <input v-model.number="b" type="range" min="0" max="255" class="w-full accent-blue-500" @input="updateFromRgb" />
              </div>
            </div>
          </div>

          <div>
            <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">HSL</span>
            <div class="grid grid-cols-3 gap-2">
              <div>
                <label class="text-[10px] font-mono block mb-1" style="color: var(--accent);">H: {{ h }}\u00b0</label>
                <input v-model.number="h" type="range" min="0" max="360" class="w-full accent-sky-500" @input="updateFromHsl" />
              </div>
              <div>
                <label class="text-[10px] font-mono block mb-1" style="color: var(--accent);">S: {{ s }}%</label>
                <input v-model.number="s" type="range" min="0" max="100" class="w-full accent-sky-500" @input="updateFromHsl" />
              </div>
              <div>
                <label class="text-[10px] font-mono block mb-1" style="color: var(--accent);">L: {{ l }}%</label>
                <input v-model.number="l" type="range" min="0" max="100" class="w-full accent-sky-500" @input="updateFromHsl" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-2">
        <div v-for="f in formats" :key="f.label" class="flex items-center gap-2">
          <span class="font-mono text-xs font-bold px-2 py-1 rounded shrink-0" style="background: rgba(14,165,233,0.08); color: var(--accent); min-width: 48px;">{{ f.label }}</span>
          <code class="flex-1 px-3 py-1.5 rounded-lg font-mono text-sm select-all" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);">{{ f.value }}</code>
          <button @click="copyColor(f.value)" class="px-2 py-1.5 rounded-lg font-mono text-xs shrink-0" style="color: var(--accent); background: rgba(14,165,233,0.08);">\u590d\u5236</button>
        </div>
      </div>
    </div>
  `
}
</script>
