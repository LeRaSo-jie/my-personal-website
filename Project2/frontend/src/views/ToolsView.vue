<template>
  <div class="min-h-screen pt-20 pb-16 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- 页面头部（标题 + Tab 切换器在同一行） -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-10 animate-fade-in">
        <div>
          <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider mb-4"
                style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.2); color: var(--accent);">
            // TOOLBOX
          </span>
          <h1 class="text-4xl md:text-5xl font-bold font-mono gradient-text">工具箱</h1>
          <p class="text-sm font-mono mt-2" style="color: var(--text-muted);">// online tools & resource downloads</p>
        </div>

        <!-- 管理员按钮 + Tab 切换器（右侧对齐） -->
        <div class="flex items-center gap-2 mt-4 sm:mt-0">
          <!-- 管理员上传按钮（仅下载 tab 显示） -->
          <button v-if="isAdmin && activeTab === 'downloads'" @click="showUploadForm = true"
                  class="btn-primary font-mono flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            上传工具
          </button>

          <div class="relative flex rounded-xl p-1" style="background: var(--bg-secondary); border: 1px solid var(--border-color);">
            <!-- 滑动指示器 -->
            <div class="absolute top-1 bottom-1 rounded-lg transition-all duration-300 ease-out"
                 :style="{
                   width: 'calc(50% - 4px)',
                   left: activeTab === 'online' ? '4px' : 'calc(50%)',
                   background: activeTab === 'online'
                     ? 'linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(14, 165, 233, 0.08))'
                     : 'linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.08))',
                   border: activeTab === 'online'
                     ? '1px solid rgba(14, 165, 233, 0.25)'
                     : '1px solid rgba(16, 185, 129, 0.25)'
                 }">
            </div>

            <button @click="switchTab('online')"
                    class="relative z-10 flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-mono transition-colors duration-300"
                    :style="{ color: activeTab === 'online' ? 'var(--accent)' : 'var(--text-muted)' }">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              在线工具
            </button>

            <button @click="switchTab('downloads')"
                    class="relative z-10 flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-mono transition-colors duration-300"
                    :style="{ color: activeTab === 'downloads' ? '#10b981' : 'var(--text-muted)' }">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              资源下载
            </button>
          </div>
        </div>
      </div>

      <!-- 内容区域（带动画切换） -->
      <Transition name="tab-fade" mode="out-in">
        <div :key="activeTab">

          <!-- ========== 在线工具 Tab ========== -->
          <div v-if="activeTab === 'online'">
            <!-- 搜索框 -->
            <div class="max-w-2xl mx-auto mb-6 animate-fade-in">
              <div class="relative">
                <input v-model="searchQuery" type="text" placeholder="搜索工具..."
                       class="input-cyber" style="padding-left: 3rem;" />
                <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" style="color: var(--text-muted);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            <!-- 分类筛选栏 -->
            <div class="flex flex-wrap items-center gap-2 mb-8 animate-fade-in" style="animation-delay: 0.1s;">
              <button v-for="cat in categories" :key="cat.key"
                      @click="activeCategory = cat.key"
                      class="px-4 py-2 rounded-xl font-mono text-sm transition-all duration-300"
                      :style="{
                        background: activeCategory === cat.key ? cat.color + '15' : 'var(--bg-secondary)',
                        border: '1px solid ' + (activeCategory === cat.key ? cat.color + '40' : 'var(--border-color)'),
                        color: activeCategory === cat.key ? cat.color : 'var(--text-muted)'
                      }">
                <span v-html="cat.icon" class="inline-block w-4 h-4 mr-1.5 align-text-bottom" />
                {{ cat.label }}
                <span class="ml-1.5 px-1.5 py-0.5 rounded text-[10px]"
                      :style="{ background: activeCategory === cat.key ? cat.color + '20' : 'rgba(148,163,184,0.1)' }">
                  {{ getCategoryCount(cat.key) }}
                </span>
              </button>
            </div>

            <!-- 工具卡片网格 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="(tool, index) in filteredTools" :key="tool.id"
                   class="tool-card group cursor-pointer animate-fade-in"
                   :style="{ animationDelay: `${index * 0.05 + 0.2}s` }"
                   @click="openTool(tool)">
                <!-- 顶部渐变条 -->
                <div class="absolute top-0 left-0 right-0 h-0.5 rounded-t-xl transition-opacity duration-300 opacity-0 group-hover:opacity-100"
                     :style="{ background: `linear-gradient(90deg, ${tool.color}, ${tool.color}66)` }" />
                
                <div class="flex items-start gap-4">
                  <!-- 图标 -->
                  <div class="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 transition-transform duration-300 group-hover:scale-110"
                       :style="{ background: tool.color + '12', border: '1px solid ' + tool.color + '25' }">
                    <span v-html="tool.icon" class="w-5 h-5" :style="{ color: tool.color }" />
                  </div>
                  
                  <!-- 信息 -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-1">
                      <h3 class="font-mono font-bold text-sm truncate transition-colors duration-300"
                          style="color: var(--text-primary);"
                          :style="{ }">
                        {{ tool.name }}
                      </h3>
                      <span v-if="tool.tag" class="text-[10px] font-mono px-1.5 py-0.5 rounded"
                            :style="{ background: tool.tagColor + '15', color: tool.tagColor, border: '1px solid ' + tool.tagColor + '30' }">
                        {{ tool.tag }}
                      </span>
                    </div>
                    <p class="text-xs line-clamp-2 mb-2" style="color: var(--text-secondary);">{{ tool.description }}</p>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded-full"
                          :style="{ background: tool.color + '10', color: tool.color, border: '1px solid ' + tool.color + '20' }">
                      {{ tool.category }}
                    </span>
                  </div>

                  <!-- 箭头 -->
                  <svg class="w-4 h-4 flex-shrink-0 mt-1 transition-all duration-300 opacity-0 group-hover:opacity-100 group-hover:translate-x-1"
                       style="color: var(--text-muted);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </div>
              </div>
            </div>

            <!-- 空状态 -->
            <div v-if="filteredTools.length === 0" class="text-center py-20">
              <div class="text-4xl mb-3">🔍</div>
              <p class="font-mono text-sm" style="color: var(--text-secondary);">未找到匹配的工具</p>
              <p class="font-mono text-xs mt-1" style="color: var(--text-tertiary);">尝试其他关键词或分类</p>
            </div>

            <!-- 底部统计 -->
            <div class="mt-10 text-center animate-fade-in" style="animation-delay: 0.5s;">
              <div class="inline-flex items-center gap-3 px-6 py-3 rounded-xl" style="background: rgba(148,163,184,0.04); border: 1px solid var(--border-color);">
                <svg class="w-5 h-5" style="color: var(--text-muted);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-sm font-mono" style="color: var(--text-muted);">
                  共 <span style="color: var(--accent);">{{ allTools.length }}</span> 个在线工具，
                  <span style="color: var(--accent);">{{ categories.length - 1 }}</span> 个分类
                </span>
              </div>
            </div>
          </div>

          <!-- ========== 资源下载 Tab ========== -->
          <div v-if="activeTab === 'downloads'">
            <!-- 搜索栏 -->
            <div class="max-w-2xl mx-auto mb-10 animate-fade-in">
              <div class="relative">
                <input v-model="searchKeyword" @keyup.enter="searchTools" type="text" placeholder="搜索工具包..." class="input-cyber" style="padding-left: 3rem;" />
                <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" style="color: var(--text-muted);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            <!-- 加载状态 -->
            <div v-if="dlLoading" class="text-center py-20">
              <div class="inline-flex items-center gap-3">
                <svg class="animate-spin w-5 h-5" style="color: var(--accent);" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                <span class="font-mono text-sm" style="color: var(--text-muted);">加载中...</span>
              </div>
            </div>

            <!-- 下载列表 -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="tool in dlTools" :key="tool.id" class="card-neon p-6 relative group overflow-hidden animate-fade-in">
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

            <!-- 空状态 -->
            <div v-if="dlTools.length === 0 && !dlLoading" class="text-center py-20">
              <div class="card-neon p-8 max-w-md mx-auto">
                <div class="text-4xl mb-3">📦</div>
                <p class="font-mono text-sm" style="color: var(--text-secondary);">暂无工具包数据</p>
                <p class="font-mono text-xs mt-1" style="color: var(--text-tertiary);">管理员可在后台上传工具包</p>
              </div>
            </div>

            <!-- 分页 -->
            <div v-if="dlTotalPages > 1" class="flex justify-center items-center gap-3 mt-8">
              <button @click="goToPage(dlCurrentPage - 1)" :disabled="dlCurrentPage === 1"
                      class="px-4 py-2 rounded-lg font-mono text-sm transition-all duration-300 disabled:opacity-30 text-neon"
                      style="background: rgba(14, 165, 233, 0.05); border: 1px solid rgba(14, 165, 233, 0.1);">← PREV</button>
              <span class="px-4 py-2 font-mono text-sm" style="color: var(--text-secondary);">{{ dlCurrentPage }} / {{ dlTotalPages }}</span>
              <button @click="goToPage(dlCurrentPage + 1)" :disabled="dlCurrentPage === dlTotalPages"
                      class="px-4 py-2 rounded-lg font-mono text-sm transition-all duration-300 disabled:opacity-30 text-neon"
                      style="background: rgba(14, 165, 233, 0.05); border: 1px solid rgba(14, 165, 233, 0.1);">NEXT →</button>
            </div>
          </div>
        </div>
      </Transition>

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

      <!-- 工具弹窗 -->
      <ToolModal :show="showModal" :tool="activeTool" @close="closeTool">
        <component v-if="activeToolComponent" :is="activeToolComponent" />
      </ToolModal>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, markRaw, shallowRef, onErrorCaptured } from 'vue'
import { useRoute } from 'vue-router'
import { getTools, downloadTool, uploadTool, deleteTool, getAdminStatus } from '../composables/useApi'
import ToolModal from '../components/ToolModal.vue'

// 导入工具组件
import { ToolHttpRequest, ToolJwtDecoder, ToolTextDiff, ToolMockData } from '../components/tools/TestTools.vue'
import { ToolBase64, ToolUrlEncode, ToolHtmlEntity, ToolUnicodeHex, ToolJsonToType } from '../components/tools/EncodingTools.vue'
import { ToolSqlFormatter, ToolCsvToJson, ToolMarkdown } from '../components/tools/DataTools.vue'
import { ToolPasswordGenerator, ToolEncryptDecrypt } from '../components/tools/SecurityTools.vue'
import { ToolRegexTester, ToolTimestamp, ToolHashGenerator, ToolQrCode, ToolImageToBase64, ToolIpLookup, ToolColorPicker } from '../components/tools/UtilityTools.vue'

const route = useRoute()

// ============================================================
// Tab 切换
// ============================================================
const activeTab = ref('online')
const switchTab = (tab) => { activeTab.value = tab }

onMounted(() => {
  if (route.query.tab === 'downloads') activeTab.value = 'downloads'
  // 支持从首页分类卡片跳转时预选分类
  if (route.query.category) {
    const cat = route.query.category
    const validKeys = categories.map(c => c.key)
    if (validKeys.includes(cat)) {
      activeCategory.value = cat
    }
  }
})

// ============================================================
// 在线工具数据
// ============================================================
const allTools = ref([
  // 测试工具
  {
    id: 'http-request',
    name: 'HTTP 请求测试',
    description: '发送 HTTP 请求并查看响应，支持多种方法和自定义 Headers',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    color: '#10b981',
    category: '测试工具',
    tag: 'HOT',
    tagColor: '#ef4444',
    component: markRaw(ToolHttpRequest)
  },
  {
    id: 'jwt-decoder',
    name: 'JWT 解析器',
    description: '解码和分析 JWT Token，查看 Header、Payload 和签名信息',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" /></svg>',
    color: '#f59e0b',
    category: '测试工具',
    tag: null,
    tagColor: null,
    component: markRaw(ToolJwtDecoder)
  },
  {
    id: 'text-diff',
    name: '文本 Diff 对比',
    description: '逐行对比两段文本，高亮显示差异部分',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>',
    color: '#8b5cf6',
    category: '测试工具',
    tag: null,
    tagColor: null,
    component: markRaw(ToolTextDiff)
  },
  {
    id: 'mock-data',
    name: 'Mock 数据生成',
    description: '快速生成测试用的模拟数据，支持自定义字段和数量',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>',
    color: '#ec4899',
    category: '测试工具',
    tag: null,
    tagColor: null,
    component: markRaw(ToolMockData)
  },
  // 编码转换
  {
    id: 'base64',
    name: 'Base64 编解码',
    description: 'Base64 编码与解码，支持中文和特殊字符',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" /></svg>',
    color: '#8b5cf6',
    category: '编码转换',
    tag: null,
    tagColor: null,
    component: markRaw(ToolBase64)
  },
  {
    id: 'url-encode',
    name: 'URL 编解码',
    description: 'URL 编码与解码转换',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>',
    color: '#06b6d4',
    category: '编码转换',
    tag: null,
    tagColor: null,
    component: markRaw(ToolUrlEncode)
  },
  {
    id: 'html-entity',
    name: 'HTML 实体编解码',
    description: 'HTML 特殊字符实体编码与解码',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>',
    color: '#ef4444',
    category: '编码转换',
    tag: null,
    tagColor: null,
    component: markRaw(ToolHtmlEntity)
  },
  {
    id: 'unicode-hex',
    name: 'Unicode / Hex 编解码',
    description: 'Unicode 转义序列和十六进制编码转换',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>',
    color: '#f59e0b',
    category: '编码转换',
    tag: null,
    tagColor: null,
    component: markRaw(ToolUnicodeHex)
  },
  {
    id: 'json-to-type',
    name: 'JSON 转类型定义',
    description: '将 JSON 数据转换为 TypeScript interface 或 Go struct',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" /></svg>',
    color: '#3b82f6',
    category: '编码转换',
    tag: 'NEW',
    tagColor: '#3b82f6',
    component: markRaw(ToolJsonToType)
  },
  // 数据处理
  {
    id: 'sql-formatter',
    name: 'SQL 格式化',
    description: 'SQL 语句美化和格式化，支持关键字大写和缩进配置',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7M4 7c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3M4 7c0-2 1.5-3 3.5-3h9c2 0 3.5 1 3.5 3" /></svg>',
    color: '#10b981',
    category: '数据处理',
    tag: 'HOT',
    tagColor: '#ef4444',
    component: markRaw(ToolSqlFormatter)
  },
  {
    id: 'csv-json',
    name: 'CSV \u2194 JSON',
    description: 'CSV \u4e0e JSON \u4e92\u8f6c\uff0c\u652f\u6301\u81ea\u5b9a\u4e49\u5206\u9694\u7b26\u3001\u8868\u5934\u548c\u6279\u91cf\u8f6c\u6362',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>',
    color: '#f97316',
    category: '数据处理',
    tag: null,
    tagColor: null,
    component: markRaw(ToolCsvToJson)
  },
  {
    id: 'markdown',
    name: 'Markdown 编辑器',
    description: '实时预览的 Markdown 编辑器，支持 GFM 语法',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>',
    color: '#6366f1',
    category: '数据处理',
    tag: null,
    tagColor: null,
    component: markRaw(ToolMarkdown)
  },
  // 安全加密
  {
    id: 'password-gen',
    name: '密码生成器',
    description: '生成安全随机密码，支持自定义长度、字符类型和强度检测',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>',
    color: '#10b981',
    category: '安全加密',
    tag: null,
    tagColor: null,
    component: markRaw(ToolPasswordGenerator)
  },
  {
    id: 'encrypt-decrypt',
    name: 'AES / DES 加解密',
    description: 'AES 和 DES 对称加密与解密工具',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>',
    color: '#ef4444',
    category: '安全加密',
    tag: null,
    tagColor: null,
    component: markRaw(ToolEncryptDecrypt)
  },
  // 实用工具
  {
    id: 'regex-tester',
    name: '正则表达式测试',
    description: '在线正则表达式测试和匹配，支持预设模式和高亮显示',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>',
    color: '#ef4444',
    category: '实用工具',
    tag: 'HOT',
    tagColor: '#ef4444',
    component: markRaw(ToolRegexTester)
  },
  {
    id: 'timestamp',
    name: '时间戳转换',
    description: 'Unix 时间戳与日期格式互转，支持秒/毫秒级',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    color: '#f59e0b',
    category: '实用工具',
    tag: null,
    tagColor: null,
    component: markRaw(ToolTimestamp)
  },
  {
    id: 'hash-gen',
    name: '哈希生成器',
    description: '计算文本的 MD5、SHA1、SHA256、SHA512 哈希值',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>',
    color: '#06b6d4',
    category: '实用工具',
    tag: null,
    tagColor: null,
    component: markRaw(ToolHashGenerator)
  },
  {
    id: 'qr-code',
    name: '二维码生成器',
    description: '将文本或 URL 生成二维码图片，支持下载',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" /></svg>',
    color: '#6366f1',
    category: '实用工具',
    tag: 'NEW',
    tagColor: '#6366f1',
    component: markRaw(ToolQrCode)
  },
  {
    id: 'img-to-base64',
    name: '图片转 Base64',
    description: '将图片文件转换为 Base64 编码，或从 Base64 还原图片',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>',
    color: '#ec4899',
    category: '实用工具',
    tag: null,
    tagColor: null,
    component: markRaw(ToolImageToBase64)
  },
  {
    id: 'ip-lookup',
    name: 'IP 地址查询',
    description: '查询 IP 地址的地理位置、ISP 和网络信息',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>',
    color: '#14b8a6',
    category: '实用工具',
    tag: null,
    tagColor: null,
    component: markRaw(ToolIpLookup)
  },
  {
    id: 'color-picker',
    name: '颜色选择器',
    description: 'RGB / HSL / HEX 颜色格式转换和取色',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" /></svg>',
    color: '#ec4899',
    category: '实用工具',
    tag: null,
    tagColor: null,
    component: markRaw(ToolColorPicker)
  }
])

// ============================================================
// 分类筛选
// ============================================================
const categories = [
  { key: 'all', label: '全部', color: '#0ea5e9', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>' },
  { key: '测试工具', label: '测试工具', color: '#10b981', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>' },
  { key: '编码转换', label: '编码转换', color: '#8b5cf6', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" /></svg>' },
  { key: '数据处理', label: '数据处理', color: '#f97316', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7M4 7c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3M4 7c0-2 1.5-3 3.5-3h9c2 0 3.5 1 3.5 3" /></svg>' },
  { key: '安全加密', label: '安全加密', color: '#ef4444', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>' },
  { key: '实用工具', label: '实用工具', color: '#14b8a6', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>' }
]

const activeCategory = ref('all')
const searchQuery = ref('')

const getCategoryCount = (key) => {
  if (key === 'all') return allTools.value.length
  return allTools.value.filter(t => t.category === key).length
}

const filteredTools = computed(() => {
  let tools = allTools.value
  if (activeCategory.value !== 'all') {
    tools = tools.filter(t => t.category === activeCategory.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    tools = tools.filter(t =>
      t.name.toLowerCase().includes(q) ||
      t.description.toLowerCase().includes(q) ||
      t.category.toLowerCase().includes(q)
    )
  }
  return tools
})

// ============================================================
// 工具弹窗
// ============================================================
const showModal = ref(false)
const activeTool = ref(null)
const activeToolComponent = shallowRef(null)

const openTool = (tool) => {
  activeTool.value = tool
  activeToolComponent.value = tool.component
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeTool = () => {
  showModal.value = false
  activeTool.value = null
  activeToolComponent.value = null
  document.body.style.overflow = ''
}

// 错误边界：捕获工具组件渲染错误，防止弹窗卡死
onErrorCaptured((err, instance, info) => {
  console.error('[ToolModal] Component render error:', err, info)
  closeTool()
  return false
})

// ESC 关闭弹窗
const handleEsc = (e) => {
  if (e.key === 'Escape' && showModal.value) closeTool()
}
onMounted(() => { document.addEventListener('keydown', handleEsc) })

// ============================================================
// 资源下载逻辑
// ============================================================
const isAdmin = getAdminStatus()
const dlTools = ref([])
const dlCurrentPage = ref(1)
const dlTotalPages = ref(1)
const dlTotal = ref(0)
const searchKeyword = ref('')
const dlLoading = ref(false)
const showUploadForm = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadForm = ref({ name: '', description: '', file: null })

const loadDlTools = async () => {
  dlLoading.value = true
  try {
    const r = await getTools(dlCurrentPage.value, 12, searchKeyword.value)
    dlTools.value = r.items
    dlTotalPages.value = r.pages
    dlTotal.value = r.total
  } catch (e) { console.error('加载工具列表失败', e) }
  finally { dlLoading.value = false }
}

const searchTools = () => { dlCurrentPage.value = 1; loadDlTools() }

const goToPage = (p) => {
  if (p < 1 || p > dlTotalPages.value) return
  dlCurrentPage.value = p
  loadDlTools()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const formatFileSize = (b) => {
  if (!b) return '未知'
  const s = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(b) / Math.log(1024))
  return (b / Math.pow(1024, i)).toFixed(2) + ' ' + s[i]
}

const handleDownload = async (id, filename) => {
  try {
    const r = await downloadTool(id)
    const u = window.URL.createObjectURL(r)
    const l = document.createElement('a')
    l.href = u
    l.setAttribute('download', filename || `tool_${id}`)
    document.body.appendChild(l)
    l.click()
    l.remove()
    window.URL.revokeObjectURL(u)
  } catch (e) { alert('下载失败') }
}

const handleFileChange = (e) => { uploadForm.value.file = e.target.files[0] }

const submitUpload = async () => {
  if (!uploadForm.value.file) { alert('请选择文件'); return }
  uploading.value = true
  uploadProgress.value = 0
  try {
    const fd = new FormData()
    fd.append('file', uploadForm.value.file)
    if (uploadForm.value.name) fd.append('name', uploadForm.value.name)
    if (uploadForm.value.description) fd.append('description', uploadForm.value.description)
    await uploadTool(fd, (e) => { uploadProgress.value = Math.round((e.loaded * 100) / e.total) })
    closeUploadForm()
    await loadDlTools()
    alert('上传成功！')
  } catch (e) { alert('上传失败：' + (e.response?.data?.error || e.message)) }
  finally { uploading.value = false; uploadProgress.value = 0 }
}

const closeUploadForm = () => {
  showUploadForm.value = false
  uploadForm.value = { name: '', description: '', file: null }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这个工具吗？')) return
  try { await deleteTool(id); await loadDlTools() }
  catch (e) { alert('删除失败：' + (e.response?.data?.error || e.message)) }
}

watch(activeTab, (tab) => {
  if (tab === 'downloads' && dlTools.value.length === 0) loadDlTools()
})
</script>

<style scoped>
/* 工具卡片 */
.tool-card {
  position: relative;
  padding: 1.25rem;
  border-radius: 0.75rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.tool-card:hover {
  border-color: rgba(14, 165, 233, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Tab 切换动画 */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.tab-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 输入框 */
.input-cyber {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  transition: all 0.3s;
}
.input-cyber:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
}

/* 按钮 */
.btn-primary {
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  font-size: 0.875rem;
  background: var(--accent);
  color: #fff;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
}
.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}
.btn-secondary {
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  font-size: 0.875rem;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  transition: all 0.3s;
  cursor: pointer;
}
.btn-secondary:hover {
  border-color: var(--accent);
  color: var(--accent);
}

/* 渐变文字 */
.gradient-text {
  background: linear-gradient(135deg, var(--accent), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 卡片发光效果 */
.card-neon {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  transition: all 0.3s;
}
.card-neon:hover {
  border-color: rgba(14, 165, 233, 0.3);
  box-shadow: 0 0 20px rgba(14, 165, 233, 0.05);
}

/* 动画 */
.animate-fade-in {
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 弹性收缩 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
