<template>
  <div class="min-h-screen pt-20 pb-16 px-4">
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center mb-12">
        <div>
          <span class="font-mono text-sm text-neon opacity-60 tracking-widest">// DOWNLOADS</span>
          <h1 class="text-4xl font-bold mt-2 gradient-text">工具下载</h1>
        </div>
        <button v-if="isAdmin" @click="showUploadForm = true" class="btn-primary">+ 上传工具</button>
      </div>
      
      <div class="max-w-2xl mx-auto mb-12">
        <div class="relative">
          <input v-model="searchKeyword" @keyup.enter="searchTools" type="text" placeholder="搜索工具..." class="input-cyber pl-12" />
          <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" style="color: var(--text-muted);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="tool in tools" :key="tool.id" class="card-neon p-6 relative group overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-neon-green via-neon-cyan to-neon-blue opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <button v-if="isAdmin" @click="handleDelete(tool.id)" class="absolute top-3 right-3 p-1.5 rounded-lg transition-all duration-300 z-10 opacity-0 group-hover:opacity-100"
                  style="background: rgba(236, 72, 153, 0.1); border: 1px solid rgba(236, 72, 153, 0.15);" title="删除">
            <svg class="h-4 w-4 text-neon-pink" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
          <div class="flex items-start gap-4 mb-4">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
                 style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.15);">
              <svg class="w-6 h-6 text-neon-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <h3 class="text-lg font-semibold group-hover:text-neon transition-colors truncate" style="color: var(--text-primary);">{{ tool.name }}</h3>
                <span class="text-xs px-2 py-0.5 rounded font-mono flex-shrink-0"
                      style="background: rgba(14, 165, 233, 0.06); color: var(--accent); border: 1px solid rgba(14, 165, 233, 0.1);">{{ tool.file_type }}</span>
              </div>
              <p class="text-sm mb-3 line-clamp-2" style="color: var(--text-secondary);">{{ tool.description }}</p>
            </div>
          </div>
          <div class="flex items-center justify-between pt-3" style="border-top: 1px solid var(--border-color);">
            <div class="flex gap-4 text-xs font-mono" style="color: var(--text-muted);">
              <span>{{ formatFileSize(tool.file_size) }}</span>
              <span class="text-neon-green opacity-60">{{ tool.download_count }} DL</span>
            </div>
            <button @click="handleDownload(tool.id, tool.filename)" class="btn-primary text-sm px-4 py-2">下载</button>
          </div>
        </div>
      </div>
      
      <div v-if="tools.length === 0 && !loading" class="text-center py-20">
        <p class="font-mono" style="color: var(--text-muted);"><span class="text-neon opacity-40">></span> 暂无工具数据</p>
      </div>
      
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-3 mt-8">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all duration-300 disabled:opacity-30 text-neon"
                style="background: rgba(14, 165, 233, 0.05); border: 1px solid rgba(14, 165, 233, 0.1);">← PREV</button>
        <span class="px-4 py-2 font-mono text-sm" style="color: var(--text-secondary);">{{ currentPage }} / {{ totalPages }}</span>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages"
                class="px-4 py-2 rounded-lg font-mono text-sm transition-all duration-300 disabled:opacity-30 text-neon"
                style="background: rgba(14, 165, 233, 0.05); border: 1px solid rgba(14, 165, 233, 0.1);">NEXT →</button>
      </div>
      
      <!-- 上传弹窗 -->
      <div v-if="showUploadForm" class="fixed inset-0 flex items-center justify-center z-50" style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px);" @click.self="closeUploadForm">
        <div class="card-neon p-6 w-full max-w-md">
          <h2 class="text-2xl font-bold mb-6 font-mono" style="color: var(--text-primary);"><span class="text-neon">></span> 上传工具</h2>
          <form @submit.prevent="submitUpload">
            <div class="mb-4">
              <label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">工具名称</label>
              <input v-model="uploadForm.name" type="text" class="input-cyber" />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">工具描述</label>
              <textarea v-model="uploadForm.description" rows="3" class="input-cyber"></textarea>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">选择文件 *</label>
              <input type="file" @change="handleFileChange" required class="input-cyber" />
              <p class="text-xs mt-1.5 font-mono" style="color: var(--text-muted);">支持格式：.zip, .rar, .7z, .exe, .py, .jar, .sh（最大 200MB）</p>
            </div>
            <div v-if="uploadProgress > 0" class="mb-4">
              <div class="w-full rounded-full h-1.5" style="background: rgba(14, 165, 233, 0.1);">
                <div class="h-1.5 rounded-full transition-all duration-300" :style="{ width: uploadProgress + '%', background: 'linear-gradient(90deg, var(--accent), var(--accent-purple))' }"></div>
              </div>
              <p class="text-xs mt-1.5 font-mono" style="color: var(--text-muted);">上传进度：{{ uploadProgress }}%</p>
            </div>
            <div class="flex gap-3">
              <button type="submit" class="btn-primary flex-1" :disabled="uploading">{{ uploading ? '上传中...' : '上传' }}</button>
              <button type="button" @click="closeUploadForm" class="btn-secondary flex-1">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTools, downloadTool, uploadTool, deleteTool, getAdminStatus } from '../composables/useApi'

const isAdmin = getAdminStatus()
const tools = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const total = ref(0)
const searchKeyword = ref('')
const loading = ref(false)
const showUploadForm = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadForm = ref({ name: '', description: '', file: null })

const loadTools = async () => {
  loading.value = true
  try { const r = await getTools(currentPage.value, 12, searchKeyword.value); tools.value = r.items; totalPages.value = r.pages; total.value = r.total }
  catch (e) { console.error('加载工具列表失败', e) }
  finally { loading.value = false }
}
const searchTools = () => { currentPage.value = 1; loadTools() }
const goToPage = (p) => { if (p < 1 || p > totalPages.value) return; currentPage.value = p; loadTools(); window.scrollTo({ top: 0, behavior: 'smooth' }) }
const formatFileSize = (b) => { if (!b) return '未知'; const s = ['B','KB','MB','GB']; const i = Math.floor(Math.log(b)/Math.log(1024)); return (b/Math.pow(1024,i)).toFixed(2)+' '+s[i] }
const handleDownload = async (id, filename) => {
  try { const r = await downloadTool(id); const u = window.URL.createObjectURL(r); const l = document.createElement('a'); l.href = u; l.setAttribute('download', filename||`tool_${id}`); document.body.appendChild(l); l.click(); l.remove(); window.URL.revokeObjectURL(u) }
  catch (e) { alert('下载失败') }
}
const handleFileChange = (e) => { uploadForm.value.file = e.target.files[0] }
const submitUpload = async () => {
  if (!uploadForm.value.file) { alert('请选择文件'); return }
  uploading.value = true; uploadProgress.value = 0
  try {
    const fd = new FormData(); fd.append('file', uploadForm.value.file)
    if (uploadForm.value.name) fd.append('name', uploadForm.value.name)
    if (uploadForm.value.description) fd.append('description', uploadForm.value.description)
    await uploadTool(fd, (e) => { uploadProgress.value = Math.round((e.loaded*100)/e.total) })
    closeUploadForm(); await loadTools(); alert('上传成功！')
  } catch (e) { alert('上传失败：' + (e.response?.data?.error || e.message)) }
  finally { uploading.value = false; uploadProgress.value = 0 }
}
const closeUploadForm = () => { showUploadForm.value = false; uploadForm.value = { name: '', description: '', file: null } }
const handleDelete = async (id) => {
  if (!confirm('确定要删除这个工具吗？')) return
  try { await deleteTool(id); await loadTools() } catch (e) { alert('删除失败：' + (e.response?.data?.error || e.message)) }
}
onMounted(loadTools)
</script>
