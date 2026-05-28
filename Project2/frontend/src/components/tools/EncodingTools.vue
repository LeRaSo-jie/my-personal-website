<!-- 编码转换工具组件集合：Base64、URL编解码、HTML实体、Unicode/Hex、JSON转类型 -->
<template><div /></template>
<script>
import { ref, computed, watch } from 'vue'

// ==================== Base64 编解码 ====================
export const ToolBase64 = {
  name: 'ToolBase64',
  setup() {
    const input = ref('')
    const output = ref('')
    const mode = ref('encode')
    const error = ref('')

    const convert = () => {
      error.value = ''
      try {
        if (mode.value === 'encode') {
          output.value = btoa(unescape(encodeURIComponent(input.value)))
        } else {
          output.value = decodeURIComponent(escape(atob(input.value.trim())))
        }
      } catch (e) { error.value = '转换失败: ' + e.message; output.value = '' }
    }

    const swap = () => { const t = input.value; input.value = output.value; output.value = t; mode.value = mode.value === 'encode' ? 'decode' : 'encode' }
    const copyOutput = () => { navigator.clipboard.writeText(output.value) }

    watch(input, convert)
    watch(mode, convert)

    return { input, output, mode, error, swap, copyOutput }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <button v-for="m in ['encode','decode']" :key="m" @click="mode = m"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: mode === m ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (mode === m ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: mode === m ? 'var(--accent)' : 'var(--text-muted)' }">
          {{ m === 'encode' ? '编码' : '解码' }}
        </button>
        <button @click="swap" class="px-3 py-2 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">⇄ 交换</button>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 输入</span>
          <textarea v-model="input" rows="6" class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono" style="color: var(--text-muted);">// 输出</span>
            <button @click="copyOutput" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">复制</button>
          </div>
          <textarea :value="output" rows="6" readonly class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== URL 编解码 ====================
export const ToolUrlEncode = {
  name: 'ToolUrlEncode',
  setup() {
    const input = ref('')
    const output = ref('')
    const mode = ref('encode')
    const error = ref('')

    const convert = () => {
      error.value = ''
      try {
        output.value = mode.value === 'encode' ? encodeURIComponent(input.value) : decodeURIComponent(input.value)
      } catch (e) { error.value = '转换失败: ' + e.message; output.value = '' }
    }

    const swap = () => { const t = input.value; input.value = output.value; output.value = t; mode.value = mode.value === 'encode' ? 'decode' : 'encode' }
    const copyOutput = () => { navigator.clipboard.writeText(output.value) }

    watch(input, convert)
    watch(mode, convert)

    return { input, output, mode, error, swap, copyOutput }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <button v-for="m in ['encode','decode']" :key="m" @click="mode = m"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: mode === m ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (mode === m ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: mode === m ? 'var(--accent)' : 'var(--text-muted)' }">
          {{ m === 'encode' ? '编码' : '解码' }}
        </button>
        <button @click="swap" class="px-3 py-2 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">⇄ 交换</button>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 输入</span>
          <textarea v-model="input" rows="6" class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono" style="color: var(--text-muted);">// 输出</span>
            <button @click="copyOutput" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">复制</button>
          </div>
          <textarea :value="output" rows="6" readonly class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== HTML 实体编解码 ====================
export const ToolHtmlEntity = {
  name: 'ToolHtmlEntity',
  setup() {
    const input = ref('')
    const output = ref('')
    const mode = ref('encode')
    const error = ref('')

    // 使用 DOM API 进行 HTML 实体编解码，避免在 JS 中硬编码实体字符串
    const encodeHTML = (str) => {
      const el = document.createElement('div')
      el.textContent = str
      return el.innerHTML
    }

    const decodeHTML = (str) => {
      const el = document.createElement('textarea')
      el.innerHTML = str
      return el.value
    }

    const convert = () => {
      error.value = ''
      try {
        output.value = mode.value === 'encode' ? encodeHTML(input.value) : decodeHTML(input.value)
      } catch (e) { error.value = '转换失败: ' + e.message }
    }

    const swap = () => { const t = input.value; input.value = output.value; output.value = t; mode.value = mode.value === 'encode' ? 'decode' : 'encode' }
    const copyOutput = () => { navigator.clipboard.writeText(output.value) }

    watch(input, convert)
    watch(mode, convert)

    return { input, output, mode, error, swap, copyOutput }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <button v-for="m in ['encode','decode']" :key="m" @click="mode = m"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: mode === m ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (mode === m ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: mode === m ? 'var(--accent)' : 'var(--text-muted)' }">
          {{ m === 'encode' ? '编码' : '解码' }}
        </button>
        <button @click="swap" class="px-3 py-2 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">⇄ 交换</button>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 输入</span>
          <textarea v-model="input" rows="6" class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono" style="color: var(--text-muted);">// 输出</span>
            <button @click="copyOutput" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">复制</button>
          </div>
          <textarea :value="output" rows="6" readonly class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== Unicode/Hex 编解码 ====================
export const ToolUnicodeHex = {
  name: 'ToolUnicodeHex',
  setup() {
    const input = ref('')
    const output = ref('')
    const mode = ref('unicode')
    const direction = ref('encode')
    const error = ref('')

    const convert = () => {
      error.value = ''
      try {
        if (direction.value === 'encode') {
          if (mode.value === 'unicode') {
            output.value = Array.from(input.value).map(c => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0')).join('')
          } else {
            output.value = Array.from(input.value).map(c => '0x' + c.charCodeAt(0).toString(16).padStart(2, '0')).join(' ')
          }
        } else {
          if (mode.value === 'unicode') {
            output.value = input.value.replace(/\\u([0-9a-fA-F]{4})/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
          } else {
            output.value = input.value.replace(/0x([0-9a-fA-F]{1,4})/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
          }
        }
      } catch (e) { error.value = '转换失败: ' + e.message }
    }

    const copyOutput = () => { navigator.clipboard.writeText(output.value) }

    watch(input, convert)
    watch(mode, convert)
    watch(direction, convert)

    return { input, output, mode, direction, error, copyOutput }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-2 flex-wrap">
        <button v-for="m in ['unicode','hex']" :key="m" @click="mode = m"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: mode === m ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (mode === m ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: mode === m ? 'var(--accent)' : 'var(--text-muted)' }">
          {{ m === 'unicode' ? 'Unicode' : 'Hex' }}
        </button>
        <div class="w-px h-6" style="background: var(--border-color);" />
        <button v-for="d in ['encode','decode']" :key="d" @click="direction = d"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: direction === d ? 'rgba(16,185,129,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (direction === d ? 'rgba(16,185,129,0.25)' : 'var(--border-color)'), color: direction === d ? '#10b981' : 'var(--text-muted)' }">
          {{ d === 'encode' ? '编码' : '解码' }}
        </button>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 输入</span>
          <textarea v-model="input" rows="6" class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono" style="color: var(--text-muted);">// 输出</span>
            <button @click="copyOutput" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">复制</button>
          </div>
          <textarea :value="output" rows="6" readonly class="w-full px-4 py-3 rounded-lg font-mono text-sm resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== JSON 转 Go/TS 类型 ====================
export const ToolJsonToType = {
  name: 'ToolJsonToType',
  setup() {
    const input = ref('')
    const output = ref('')
    const lang = ref('typescript')
    const error = ref('')

    const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1)
    const toPascalCase = (s) => s.split(/[_-]/).map(capitalize).join('')

    const getType = (val, key) => {
      if (val === null) return 'any'
      if (Array.isArray(val)) {
        if (val.length === 0) return 'any[]'
        return getType(val[0], key) + '[]'
      }
      if (typeof val === 'object') return toPascalCase(key)
      if (typeof val === 'number') return 'number'
      if (typeof val === 'boolean') return 'boolean'
      return 'string'
    }

    const getGoType = (val, key) => {
      if (val === null) return 'interface{}'
      if (Array.isArray(val)) {
        if (val.length === 0) return '[]interface{}'
        return '[]' + getGoType(val[0], key)
      }
      if (typeof val === 'object') return toPascalCase(key)
      if (typeof val === 'number') return Number.isInteger(val) ? 'int' : 'float64'
      if (typeof val === 'boolean') return 'bool'
      return 'string'
    }

    const generatedTypes = new Set()

    const generateTypes = (obj, name, lines, langType) => {
      if (generatedTypes.has(name)) return
      generatedTypes.add(name)
      if (langType === 'typescript') {
        lines.push('interface ' + name + ' {')
        for (const [key, val] of Object.entries(obj)) {
          const type = getType(val, key)
          lines.push('  ' + key + ': ' + type + ';')
          if (typeof val === 'object' && val !== null && !Array.isArray(val)) generateTypes(val, toPascalCase(key), lines, langType)
          if (Array.isArray(val) && val.length > 0 && typeof val[0] === 'object' && val[0] !== null) generateTypes(val[0], toPascalCase(key), lines, langType)
        }
        lines.push('}')
      } else {
        lines.push('type ' + name + ' struct {')
        for (const [key, val] of Object.entries(obj)) {
          const goKey = toPascalCase(key)
          const goType = getGoType(val, key)
          lines.push('\t' + goKey + ' ' + goType + ' `json:"' + key + '"`')
          if (typeof val === 'object' && val !== null && !Array.isArray(val)) generateTypes(val, toPascalCase(key), lines, langType)
          if (Array.isArray(val) && val.length > 0 && typeof val[0] === 'object' && val[0] !== null) generateTypes(val[0], toPascalCase(key), lines, langType)
        }
        lines.push('}')
      }
    }

    const convert = () => {
      error.value = ''
      generatedTypes.clear()
      try {
        const obj = JSON.parse(input.value)
        const lines = []
        const name = 'RootObject'
        if (Array.isArray(obj)) {
          if (obj.length > 0 && typeof obj[0] === 'object') generateTypes(obj[0], name, lines, lang.value)
          else { error.value = '数组元素不是对象类型'; return }
        } else {
          generateTypes(obj, name, lines, lang.value)
        }
        output.value = lines.join('\n')
      } catch (e) { error.value = 'JSON 解析失败: ' + e.message; output.value = '' }
    }

    const copyOutput = () => { navigator.clipboard.writeText(output.value) }

    watch(input, convert)
    watch(lang, convert)

    return { input, output, lang, error, convert, copyOutput }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <button v-for="l in ['typescript','go']" :key="l" @click="lang = l"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: lang === l ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (lang === l ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: lang === l ? 'var(--accent)' : 'var(--text-muted)' }">
          {{ l === 'typescript' ? 'TypeScript' : 'Go' }}
        </button>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 输入 JSON</span>
          <textarea v-model="input" rows="8" placeholder='{"name": "test", "age": 25}' class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono" style="color: var(--text-muted);">// {{ lang === 'typescript' ? 'TypeScript' : 'Go' }} 类型定义</span>
            <button @click="copyOutput" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">复制</button>
          </div>
          <textarea :value="output" rows="8" readonly class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}
</script>
