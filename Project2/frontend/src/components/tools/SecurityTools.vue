<!-- 安全加密工具组件集合：密码生成器、AES/DES加解密 -->
<template><div /></template>
<script>
import { ref, computed, watch } from 'vue'
import CryptoJS from 'crypto-js'

// ==================== 密码生成器 ====================
export const ToolPasswordGenerator = {
  name: 'ToolPasswordGenerator',
  setup() {
    const length = ref(16)
    const count = ref(5)
    const options = ref({
      uppercase: true,
      lowercase: true,
      numbers: true,
      symbols: true
    })
    const passwords = ref([])
    const excludeAmbiguous = ref(false)

    const chars = computed(() => {
      let c = ''
      if (options.value.uppercase) c += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      if (options.value.lowercase) c += 'abcdefghijklmnopqrstuvwxyz'
      if (options.value.numbers) c += '0123456789'
      if (options.value.symbols) c += '!@#$%^&*()_+-=[]{}|;:,.<>?'
      if (excludeAmbiguous.value) {
        c = c.replace(/[0OIl1|]/g, '')
      }
      return c
    })

    const strength = computed(() => {
      const len = length.value
      const hasUpper = options.value.uppercase
      const hasLower = options.value.lowercase
      const hasNum = options.value.numbers
      const hasSym = options.value.symbols
      const types = [hasUpper, hasLower, hasNum, hasSym].filter(Boolean).length
      if (len >= 16 && types >= 3) return { level: '\u6781\u5f3a', color: '#10b981', percent: 100 }
      if (len >= 12 && types >= 3) return { level: '\u5f3a', color: '#22c55e', percent: 80 }
      if (len >= 8 && types >= 2) return { level: '\u4e2d\u7b49', color: '#f59e0b', percent: 60 }
      return { level: '\u5f31', color: '#ef4444', percent: 30 }
    })

    const generate = () => {
      if (chars.value.length === 0) return
      const result = []
      const c = chars.value
      for (let i = 0; i < count.value; i++) {
        let pwd = ''
        const arr = new Uint32Array(length.value)
        crypto.getRandomValues(arr)
        for (let j = 0; j < length.value; j++) {
          pwd += c[arr[j] % c.length]
        }
        result.push(pwd)
      }
      passwords.value = result
    }

    const copyPwd = (pwd) => { navigator.clipboard.writeText(pwd) }
    const copyAll = () => { navigator.clipboard.writeText(passwords.value.join('\n')) }

    // initial generate
    generate()

    return { length, count, options, passwords, excludeAmbiguous, strength, generate, copyPwd, copyAll }
  },
  template: `
    <div class="space-y-4">
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">\u957f\u5ea6: {{ length }}</span>
          <input v-model.number="length" type="range" min="4" max="64" class="w-full accent-sky-500" />
        </div>
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">\u6570\u91cf: {{ count }}</span>
          <input v-model.number="count" type="range" min="1" max="20" class="w-full accent-sky-500" />
        </div>
        <div class="flex flex-col gap-2">
          <label class="flex items-center gap-1.5 text-xs font-mono cursor-pointer" style="color: var(--text-muted);">
            <input type="checkbox" v-model="options.uppercase" class="accent-sky-500" /> \u5927\u5199 A-Z
          </label>
          <label class="flex items-center gap-1.5 text-xs font-mono cursor-pointer" style="color: var(--text-muted);">
            <input type="checkbox" v-model="options.lowercase" class="accent-sky-500" /> \u5c0f\u5199 a-z
          </label>
        </div>
        <div class="flex flex-col gap-2">
          <label class="flex items-center gap-1.5 text-xs font-mono cursor-pointer" style="color: var(--text-muted);">
            <input type="checkbox" v-model="options.numbers" class="accent-sky-500" /> \u6570\u5b57 0-9
          </label>
          <label class="flex items-center gap-1.5 text-xs font-mono cursor-pointer" style="color: var(--text-muted);">
            <input type="checkbox" v-model="options.symbols" class="accent-sky-500" /> \u7b26\u53f7 !@#
          </label>
        </div>
      </div>

      <div class="flex items-center gap-4">
        <label class="flex items-center gap-2 cursor-pointer text-xs font-mono" style="color: var(--text-muted);">
          <input type="checkbox" v-model="excludeAmbiguous" class="accent-sky-500" />
          \u6392\u9664\u6613\u6df7\u6dc6\u5b57\u7b26 (0OIl1|)
        </label>
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono" style="color: var(--text-muted);">\u5f3a\u5ea6:</span>
          <div class="w-24 h-1.5 rounded-full" style="background: var(--bg-tertiary);">
            <div class="h-full rounded-full transition-all" :style="{ width: strength.percent + '%', background: strength.color }" />
          </div>
          <span class="text-xs font-mono font-bold" :style="{ color: strength.color }">{{ strength.level }}</span>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <button @click="generate" class="px-5 py-2 rounded-lg font-mono text-sm font-bold" style="background: var(--accent); color: #fff;">\u91cd\u65b0\u751f\u6210</button>
        <button v-if="passwords.length > 1" @click="copyAll" class="px-4 py-2 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">\u590d\u5236\u5168\u90e8</button>
      </div>

      <div class="space-y-2">
        <div v-for="(pwd, i) in passwords" :key="i" class="flex items-center gap-2">
          <span class="text-xs font-mono" style="color: var(--text-muted); min-width: 24px;">{{ i + 1 }}.</span>
          <code class="flex-1 px-4 py-2 rounded-lg font-mono text-sm break-all select-all" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);">{{ pwd }}</code>
          <button @click="copyPwd(pwd)" class="px-3 py-2 rounded-lg font-mono text-xs shrink-0" style="background: rgba(14,165,233,0.08); border: 1px solid rgba(14,165,233,0.15); color: var(--accent);">\u590d\u5236</button>
        </div>
      </div>
    </div>
  `
}

// ==================== AES/DES 加解密 ====================
export const ToolEncryptDecrypt = {
  name: 'ToolEncryptDecrypt',
  setup() {
    const input = ref('')
    const key = ref('')
    const output = ref('')
    const mode = ref('encrypt')
    const algorithm = ref('aes')
    const error = ref('')


    const convert = () => {
      error.value = ''
      try {
        if (!input.value.trim()) { output.value = ''; return }
        if (!key.value.trim()) { error.value = '\u8bf7\u8f93\u5165\u5bc6\u94a5'; output.value = ''; return }
        const algo = algorithm.value === 'aes' ? CryptoJS.AES : CryptoJS.DES
        if (mode.value === 'encrypt') {
          const encrypted = algo.encrypt(input.value, key.value)
          output.value = encrypted.toString()
        } else {
          const decrypted = algo.decrypt(input.value, key.value)
          const result = decrypted.toString(CryptoJS.enc.Utf8)
          if (!result) { error.value = '\u89e3\u5bc6\u5931\u8d25\uff1a\u5bc6\u94a5\u53ef\u80fd\u4e0d\u6b63\u786e'; output.value = ''; return }
          output.value = result
        }
      } catch (e) { error.value = '\u64cd\u4f5c\u5931\u8d25: ' + e.message; output.value = '' }
    }

    const swap = () => { const t = input.value; input.value = output.value; output.value = t; mode.value = mode.value === 'encrypt' ? 'decrypt' : 'encrypt' }
    const copyOutput = () => { navigator.clipboard.writeText(output.value) }

    watch(input, convert)
    watch(key, convert)
    watch(mode, convert)
    watch(algorithm, convert)

    return { input, key, output, mode, algorithm, error, swap, copyOutput, convert }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-2 flex-wrap">
        <button v-for="a in ['aes','des']" :key="a" @click="algorithm = a"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: algorithm === a ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (algorithm === a ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: algorithm === a ? 'var(--accent)' : 'var(--text-muted)' }">
          {{ a.toUpperCase() }}
        </button>
        <div class="w-px h-6" style="background: var(--border-color);" />
        <button v-for="m in ['encrypt','decrypt']" :key="m" @click="mode = m"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: mode === m ? 'rgba(16,185,129,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (mode === m ? 'rgba(16,185,129,0.25)' : 'var(--border-color)'), color: mode === m ? '#10b981' : 'var(--text-muted)' }">
          {{ m === 'encrypt' ? '\u52a0\u5bc6' : '\u89e3\u5bc6' }}
        </button>
        <button @click="swap" class="px-3 py-2 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">\u21c4 \u4ea4\u6362</button>
      </div>

      <div>
        <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// \u5bc6\u94a5</span>
        <input v-model="key" type="text" placeholder="\u8f93\u5165\u52a0\u5bc6/\u89e3\u5bc6\u5bc6\u94a5..." class="w-full px-4 py-2.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// {{ mode === 'encrypt' ? '\u660e\u6587\u8f93\u5165' : '\u5bc6\u6587\u8f93\u5165' }}</span>
          <textarea v-model="input" rows="6" class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono" style="color: var(--text-muted);">// {{ mode === 'encrypt' ? '\u5bc6\u6587\u8f93\u51fa' : '\u660e\u6587\u8f93\u51fa' }}</span>
            <button @click="copyOutput" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">\u590d\u5236</button>
          </div>
          <textarea :value="output" rows="6" readonly class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}
</script>
