<!-- 数据处理工具组件集合：SQL格式化、CSV转JSON、Markdown编辑器 -->
<template><div /></template>
<script>
import { ref, computed, watch } from 'vue'
import { marked } from 'marked'

// ==================== SQL 格式化 ====================
export const ToolSqlFormatter = {
  name: 'ToolSqlFormatter',
  setup() {
    const input = ref('')
    const output = ref('')
    const indent = ref(2)
    const upper = ref(true)
    const error = ref('')

    const keywords = [
      'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'BETWEEN', 'LIKE', 'IS', 'NULL',
      'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'TABLE',
      'JOIN', 'INNER', 'LEFT', 'RIGHT', 'OUTER', 'FULL', 'CROSS', 'ON', 'AS',
      'GROUP', 'BY', 'ORDER', 'ASC', 'DESC', 'HAVING', 'LIMIT', 'OFFSET', 'UNION', 'ALL',
      'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'EXISTS', 'DISTINCT', 'TOP', 'WITH',
      'INDEX', 'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'CONSTRAINT', 'DEFAULT',
      'BEGIN', 'COMMIT', 'ROLLBACK', 'TRANSACTION', 'IF', 'DECLARE', 'EXEC', 'PROCEDURE',
      'FUNCTION', 'RETURNS', 'TRIGGER', 'VIEW', 'GRANT', 'REVOKE', 'REPLACE'
    ]

    const formatSQL = () => {
      error.value = ''
      try {
        if (!input.value.trim()) { output.value = ''; return }
        let sql = input.value.trim().replace(/\s+/g, ' ')
        const indentStr = ' '.repeat(indent.value)
        const newLineKeywords = [
          'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'ORDER BY', 'GROUP BY', 'HAVING',
          'LIMIT', 'OFFSET', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
          'FULL JOIN', 'CROSS JOIN', 'ON', 'SET', 'VALUES', 'INSERT INTO',
          'UPDATE', 'DELETE FROM', 'CREATE TABLE', 'ALTER TABLE', 'DROP TABLE',
          'UNION', 'UNION ALL', 'WITH', 'ELSE', 'END', 'THEN'
        ]

        // 先把关键字标准化
        for (const kw of keywords) {
          const regex = new RegExp('\\b' + kw + '\\b', 'gi')
          sql = sql.replace(regex, upper.value ? kw : kw.toLowerCase())
        }

        // 在关键子句前换行
        for (const kw of newLineKeywords.reverse()) {
          const searchKw = upper.value ? kw : kw.toLowerCase()
          const regex = new RegExp('\\b(' + searchKw.replace(/ /g, '\\s+') + ')\\b', 'gi')
          sql = sql.replace(regex, '\n$1')
        }

        // 处理逗号后换行（仅在 SELECT 子句内）
        sql = sql.replace(/,/g, ',\n' + indentStr)

        // 缩进处理
        const lines = sql.split('\n').filter(l => l.trim())
        let depth = 0
        const result = []
        for (const line of lines) {
          const trimmed = line.trim()
          const lowerLine = trimmed.toLowerCase()
          if (/^(end|else|union|union all)/i.test(trimmed)) depth = Math.max(0, depth - 1)
          result.push(indentStr.repeat(depth) + trimmed)
          if (/^(case|when|then)\b/i.test(trimmed) && !/^(end)\b/i.test(trimmed)) depth++
        }
        output.value = result.join('\n')
      } catch (e) { error.value = '格式化失败: ' + e.message }
    }

    const swap = () => { const t = input.value; input.value = output.value; output.value = t }
    const copyOutput = () => { navigator.clipboard.writeText(output.value) }

    watch(input, formatSQL)
    watch(indent, formatSQL)
    watch(upper, formatSQL)

    return { input, output, indent, upper, error, formatSQL, swap, copyOutput }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-4 flex-wrap">
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono" style="color: var(--text-muted);">缩进:</span>
          <select v-model.number="indent" class="px-3 py-1.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);">
            <option :value="2">2 空格</option>
            <option :value="4">4 空格</option>
            <option :value="1">Tab</option>
          </select>
        </div>
        <label class="flex items-center gap-2 cursor-pointer text-xs font-mono" style="color: var(--text-muted);">
          <input type="checkbox" v-model="upper" class="accent-sky-500" />
          关键字大写
        </label>
        <button @click="swap" class="px-3 py-1.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">⇄ 交换</button>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 输入 SQL</span>
          <textarea v-model="input" rows="10" placeholder="SELECT id, name, email FROM users WHERE age > 18 ORDER BY name" class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono" style="color: var(--text-muted);">// 格式化结果</span>
            <button @click="copyOutput" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08);">复制</button>
          </div>
          <textarea :value="output" rows="10" readonly class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== CSV \u2194 JSON ====================
export const ToolCsvToJson = {
  name: 'ToolCsvToJson',
  setup() {
    const input = ref('')
    const output = ref('')
    const delimiter = ref(',')
    const hasHeader = ref(true)
    const error = ref('')
    const mode = ref('csv2json')

    // 实际分隔符（tab 需要特殊处理）
    const rawDl = computed(() => delimiter.value === 'tab' ? '\t' : delimiter.value)

    // CSV \u2192 JSON
    const csvToJson = () => {
      if (!input.value.trim()) { output.value = ''; return }
      const lines = input.value.trim().split('\n').map(l => l.trim()).filter(l => l)
      if (lines.length === 0) { output.value = '[]'; return }
      const parseRow = (line) => {
        const result = []
        let current = ''
        let inQuotes = false
        for (let i = 0; i < line.length; i++) {
          const ch = line[i]
          if (inQuotes) {
            if (ch === '"' && line[i + 1] === '"') { current += '"'; i++ }
            else if (ch === '"') { inQuotes = false }
            else { current += ch }
          } else {
            if (ch === '"') { inQuotes = true }
            else if (ch === rawDl.value) { result.push(current); current = '' }
            else { current += ch }
          }
        }
        result.push(current)
        return result
      }
      const rows = lines.map(parseRow)
      const data = []
      if (hasHeader.value && rows.length > 1) {
        const headers = rows[0]
        for (let i = 1; i < rows.length; i++) {
          const obj = {}
          headers.forEach((h, j) => { obj[h.trim()] = rows[i][j] !== undefined ? rows[i][j].trim() : '' })
          data.push(obj)
        }
      } else {
        data.push(...rows.map(r => r.map(c => c.trim())))
      }
      output.value = JSON.stringify(data, null, 2)
    }

    // JSON \u2192 CSV
    const escapeField = (val) => {
      const str = val === null || val === undefined ? '' : String(val)
      if (str.includes(rawDl.value) || str.includes('"') || str.includes('\n')) {
        return '"' + str.replace(/"/g, '""') + '"'
      }
      return str
    }

    const jsonToCsv = () => {
      if (!input.value.trim()) { output.value = ''; return }
      let data
      try { data = JSON.parse(input.value) } catch (e) { throw new Error('JSON \u89e3\u6790\u5931\u8d25: ' + e.message) }
      if (!Array.isArray(data)) throw new Error('\u8bf7\u8f93\u5165 JSON \u6570\u7ec4')
      if (data.length === 0) { output.value = ''; return }
      const csvLines = []
      const dl = rawDl.value
      if (hasHeader.value) {
        const first = data[0]
        if (typeof first === 'object' && first !== null && !Array.isArray(first)) {
          const headers = Object.keys(first)
          csvLines.push(headers.map(h => escapeField(h)).join(dl))
          data.forEach(row => { csvLines.push(headers.map(h => escapeField(row[h])).join(dl)) })
        } else if (Array.isArray(first)) {
          csvLines.push(first.map((_, i) => 'col' + (i + 1)).join(dl))
          data.forEach(row => { csvLines.push(row.map(c => escapeField(c)).join(dl)) })
        } else {
          throw new Error('\u6570\u7ec4\u5143\u7d20\u5e94\u4e3a\u5bf9\u8c61\u6216\u6570\u7ec4')
        }
      } else {
        data.forEach(row => {
          if (Array.isArray(row)) csvLines.push(row.map(c => escapeField(c)).join(dl))
          else if (typeof row === 'object' && row !== null) csvLines.push(Object.values(row).map(v => escapeField(v)).join(dl))
        })
      }
      output.value = csvLines.join('\n')
    }

    const convert = () => {
      error.value = ''
      try {
        if (mode.value === 'csv2json') csvToJson()
        else jsonToCsv()
      } catch (e) { error.value = '\u8f6c\u6362\u5931\u8d25: ' + e.message; output.value = '' }
    }

    const swap = () => {
      const tmp = input.value; input.value = output.value; output.value = tmp
      mode.value = mode.value === 'csv2json' ? 'json2csv' : 'csv2json'
    }

    const copyOutput = () => { if (output.value) navigator.clipboard.writeText(output.value) }

    watch(input, convert)
    watch(delimiter, convert)
    watch(hasHeader, convert)
    watch(mode, convert)

    // 模式按钮样式
    const btnStyle = (target) => {
      const a = mode.value === target
      return {
        padding: '8px 16px', borderRadius: '8px', fontFamily: 'monospace', fontSize: '14px', cursor: 'pointer',
        border: '1px solid ' + (a ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'),
        background: a ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)',
        color: a ? 'var(--accent)' : 'var(--text-muted)'
      }
    }

    const headerLabel = computed(() => mode.value === 'csv2json' ? '\u9996\u884c\u4e3a\u8868\u5934' : '\u8f93\u51fa\u8868\u5934')
    const inputLabel = computed(() => mode.value === 'csv2json' ? '\u8f93\u5165 CSV' : '\u8f93\u5165 JSON')
    const outputLabel = computed(() => mode.value === 'csv2json' ? 'JSON \u7ed3\u679c' : 'CSV \u7ed3\u679c')
    const ph = computed(() => mode.value === 'csv2json'
      ? 'name,age,city\nAlice,25,Beijing\nBob,30,Shanghai'
      : '[{"name":"Alice","age":25},{"name":"Bob","age":30}]')

    return { input, output, delimiter, hasHeader, error, mode, convert, swap, copyOutput, btnStyle, headerLabel, inputLabel, outputLabel, ph }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-2 flex-wrap">
        <button @click="mode = 'csv2json'" :style="btnStyle('csv2json')">CSV \u2192 JSON</button>
        <button @click="mode = 'json2csv'" :style="btnStyle('json2csv')">JSON \u2192 CSV</button>
        <div class="w-px h-6" style="background: var(--border-color);"></div>
        <button @click="swap" class="px-3 py-2 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted); cursor: pointer;">\u21c4 \u4ea4\u6362</button>
        <div class="w-px h-6" style="background: var(--border-color);"></div>
        <span class="text-xs font-mono" style="color: var(--text-muted);">\u5206\u9694\u7b26:</span>
        <select v-model="delimiter" class="px-3 py-1.5 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);">
          <option value=",">\u9017\u53f7</option>
          <option value=";">\u5206\u53f7</option>
          <option value="tab">Tab</option>
          <option value="|">\u7ad6\u7ebf</option>
        </select>
        <label class="flex items-center gap-2 cursor-pointer text-xs font-mono" style="color: var(--text-muted);">
          <input type="checkbox" v-model="hasHeader" class="accent-sky-500" />
          {{ headerLabel }}
        </label>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// {{ inputLabel }}</span>
          <textarea v-model="input" rows="10" :placeholder="ph" class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);"></textarea>
        </div>
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono" style="color: var(--text-muted);">// {{ outputLabel }}</span>
            <button @click="copyOutput" class="text-xs font-mono px-2 py-0.5 rounded" style="color: var(--accent); background: rgba(14,165,233,0.08); cursor: pointer;">\u590d\u5236</button>
          </div>
          <textarea :value="output" rows="10" readonly class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);"></textarea>
        </div>
      </div>
      <p v-if="error" class="text-sm font-mono" style="color: #ef4444;">{{ error }}</p>
    </div>
  `
}

// ==================== Markdown 编辑器 ====================
export const ToolMarkdown = {
  name: 'ToolMarkdown',
  setup() {
    const input = ref(`# Hello Markdown

这是一个 **Markdown** 编辑器。

## 功能

- 实时预览
- 代码高亮
- 表格支持

\`\`\`javascript
console.log("Hello World")
\`\`\`

| 姓名 | 年龄 |
| --- | --- |
| Alice | 25 |
| Bob | 30 |`)
    const showPreview = ref(true)

    const rendered = computed(() => {
      try {
        // 使用 marked 库进行 Markdown 渲染
        marked.setOptions({ breaks: true, gfm: true })
        return marked.parse(input.value || '')
      } catch {
        // 降级：简单的 Markdown 渲染
        let html = input.value
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>')
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>')
        html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>')
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>')
        html = html.replace(/^- (.+)$/gm, '<li>$1</li>')
        html = html.replace(/\n/g, '<br>')
        return html
      }
    })

    const copyMd = () => { navigator.clipboard.writeText(input.value) }

    return { input, showPreview, rendered, copyMd }
  },
  template: `
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <button @click="showPreview = !showPreview"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all"
                :style="{ background: showPreview ? 'rgba(14,165,233,0.1)' : 'var(--bg-secondary)', border: '1px solid ' + (showPreview ? 'rgba(14,165,233,0.25)' : 'var(--border-color)'), color: showPreview ? 'var(--accent)' : 'var(--text-muted)' }">
          {{ showPreview ? '隐藏预览' : '显示预览' }}
        </button>
        <button @click="copyMd" class="px-4 py-2 rounded-lg font-mono text-sm" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-muted);">复制源码</button>
      </div>
      <div :class="showPreview ? 'grid grid-cols-2 gap-4' : ''">
        <div>
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// Markdown 源码</span>
          <textarea v-model="input" :rows="showPreview ? 16 : 20" class="w-full px-4 py-3 rounded-lg font-mono text-xs resize-y" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary);" />
        </div>
        <div v-if="showPreview">
          <span class="text-xs font-mono mb-1.5 block" style="color: var(--text-muted);">// 实时预览</span>
          <div class="prose-preview px-4 py-3 rounded-lg overflow-y-auto" style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary); min-height: 300px; max-height: 500px;" v-html="rendered" />
        </div>
      </div>
    </div>
  `
}
</script>
