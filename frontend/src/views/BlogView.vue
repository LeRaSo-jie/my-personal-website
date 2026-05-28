<template>
  <div class="min-h-screen py-24 px-4 sm:px-6 lg:px-8" style="background: var(--bg-primary);">
    <div class="max-w-6xl mx-auto">
      <!-- 页头 -->
      <div class="text-center mb-12">
        <h1 class="text-4xl sm:text-5xl font-bold font-mono mb-4">
          <span class="text-neon"><</span>
          <span style="color: var(--text-primary);">Blog</span>
          <span class="text-neon" style="letter-spacing: 0.02em;"> /></span>
        </h1>
        <p class="text-lg" style="color: var(--text-secondary);">
          技术笔记、踩坑记录、学习心得
        </p>
        <div class="mt-4 h-px w-32 mx-auto" style="background: linear-gradient(90deg, transparent, var(--accent-color), transparent);"></div>
      </div>

      <!-- 搜索栏 -->
      <div class="mb-4">
        <div class="relative w-full">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style="color: var(--text-tertiary);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索文章标题、摘要..."
            class="search-input w-full pl-10 pr-4 py-2.5 rounded-lg text-sm font-mono"
            @input="debounceSearch"
          />
        </div>
      </div>
      <!-- 标签筛选 -->
      <div class="mb-8 flex flex-wrap gap-2">
        <button
          v-for="tag in allTags"
          :key="tag"
          @click="toggleTag(tag)"
          class="tag-btn px-3 py-1.5 rounded-full text-xs font-mono transition-all duration-300"
          :class="activeTags.includes(tag) ? 'tag-active' : ''"
        >
          {{ tag }}
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block w-8 h-8 border-2 border-neon/30 border-t-neon rounded-full animate-spin mb-4"></div>
        <p class="text-sm font-mono" style="color: var(--text-tertiary);">加载中...</p>
      </div>

      <template v-else>
        <!-- 文章统计 -->
        <div class="mb-6 flex items-center justify-between flex-wrap gap-3">
          <div class="flex items-center gap-3">
            <span class="text-sm font-mono" style="color: var(--text-tertiary);">
              共 {{ total }} 篇文章
              <span v-if="searchQuery || activeTags.length > 0" class="ml-1">· 当前页 {{ filteredPosts.length }} 篇</span>
            </span>
            <button v-if="isAdmin" @click="openEditor(null)" class="px-3 py-1.5 rounded-lg text-xs font-mono transition-all hover:scale-105" style="background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3); color: #00f0ff;">
              + 新建文章
            </button>
          </div>
          <div class="flex gap-2 items-center">
            <!-- 排序切换 -->
            <button
              @click="toggleSort"
              class="sort-btn flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-mono transition-all"
              :title="sortOrder === 'desc' ? '最新在前，点击切换' : '最早在前，点击切换'"
            >
              <svg class="w-3.5 h-3.5 transition-transform" :class="sortOrder === 'asc' ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
              </svg>
              <span>{{ sortOrder === 'desc' ? '最新' : '最早' }}</span>
            </button>
            <button
              @click="viewMode = 'list'"
              class="p-2 rounded-lg transition-all"
              :class="viewMode === 'list' ? 'text-neon' : ''"
              :style="viewMode !== 'list' ? 'color: var(--text-tertiary)' : ''"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
            </button>
            <button
              @click="viewMode = 'grid'"
              class="p-2 rounded-lg transition-all"
              :class="viewMode === 'grid' ? 'text-neon' : ''"
              :style="viewMode !== 'grid' ? 'color: var(--text-tertiary)' : ''"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 列表视图 -->
        <div v-if="viewMode === 'list'" class="space-y-4">
          <TransitionGroup name="post-list">
            <article
              v-for="(post, index) in filteredPosts"
              :key="post.id"
              class="post-card group cursor-pointer"
              :style="{ animationDelay: `${index * 80}ms` }"
              @click="openPost(post)"
            >
              <div class="flex flex-col sm:flex-row gap-4">
                <!-- 左侧装饰 -->
                <div class="flex-shrink-0 sm:w-20 text-center">
                  <div class="text-3xl font-bold font-mono text-neon opacity-60 group-hover:opacity-100 transition-opacity">
                    {{ String(index + 1).padStart(2, '0') }}
                  </div>
                </div>
                <!-- 内容 -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-2 flex-wrap">
                    <span
                      v-for="tag in post.tags"
                      :key="tag"
                      class="px-2 py-0.5 rounded text-xs font-mono"
                      :style="{ background: getTagColor(tag).bg, color: getTagColor(tag).text }"
                    >
                      {{ tag }}
                    </span>
                    <span v-if="isAdmin && post.status === 'draft'" class="px-2 py-0.5 rounded text-xs font-mono" style="background: rgba(251, 191, 36, 0.15); color: #fbbf24;">草稿</span>
                    <span class="text-xs font-mono" style="color: var(--text-tertiary);">
                      {{ post.date }}
                    </span>
                    <span class="text-xs font-mono" style="color: var(--text-tertiary);">
                      · {{ post.readTime }} min read
                    </span>
                  </div>
                  <h2 class="text-lg font-bold mb-2 group-hover:text-neon transition-colors" style="color: var(--text-primary);">
                    {{ post.title }}
                  </h2>
                  <p class="text-sm leading-relaxed line-clamp-2" style="color: var(--text-secondary);">
                    {{ post.summary }}
                  </p>
                  <!-- 底部元信息 -->
                  <div class="mt-3 flex items-center gap-4 text-xs font-mono" style="color: var(--text-tertiary);">
                    <span class="flex items-center gap-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      {{ post.views }}
                    </span>
                    <span class="flex items-center gap-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                      </svg>
                      {{ post.likes }}
                    </span>
                  </div>
                </div>
                <!-- 右侧操作 -->
                <div class="hidden sm:flex items-center gap-2">
                  <button v-if="isAdmin" @click.stop="openEditor(post)" class="p-2 rounded-lg transition-all opacity-0 group-hover:opacity-100" style="background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); color: #00f0ff;" title="编辑">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                  </button>
                  <button v-if="isAdmin" @click.stop="handleDeletePost(post)" class="p-2 rounded-lg transition-all opacity-0 group-hover:opacity-100" style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); color: #ef4444;" title="删除">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                  </button>
                  <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" style="color: var(--text-tertiary);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </article>
          </TransitionGroup>
        </div>

        <!-- 网格视图 -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <article
            v-for="(post, index) in filteredPosts"
            :key="post.id"
            class="grid-card group cursor-pointer"
            :style="{ animationDelay: `${index * 100}ms` }"
            @click="openPost(post)"
          >
            <!-- 卡片顶部装饰条 -->
            <div class="h-1 w-full rounded-t-xl" :style="{ background: getCardGradient(index) }" />
            <div class="p-5">
              <!-- 标签 -->
              <div class="flex flex-wrap gap-1.5 mb-3">
                <span
                  v-for="tag in post.tags"
                  :key="tag"
                  class="px-2 py-0.5 rounded text-xs font-mono"
                  :style="{ background: getTagColor(tag).bg, color: getTagColor(tag).text }"
                >
                  {{ tag }}
                </span>
                <span v-if="isAdmin && post.status === 'draft'" class="px-2 py-0.5 rounded text-xs font-mono" style="background: rgba(251, 191, 36, 0.15); color: #fbbf24;">草稿</span>
              </div>
              <!-- 标题 -->
              <h2 class="text-base font-bold mb-2 group-hover:text-neon transition-colors line-clamp-2" style="color: var(--text-primary);">
                {{ post.title }}
              </h2>
              <!-- 摘要 -->
              <p class="text-sm leading-relaxed line-clamp-3 mb-4" style="color: var(--text-secondary);">
                {{ post.summary }}
              </p>
              <!-- 底部 -->
              <div class="flex items-center justify-between text-xs font-mono" style="color: var(--text-tertiary);">
                <span>{{ post.date }}</span>
                <div class="flex items-center gap-1">
                  <button v-if="isAdmin" @click.stop="openEditor(post)" class="p-1.5 rounded transition-all opacity-0 group-hover:opacity-100" style="background: rgba(0, 240, 255, 0.1); color: #00f0ff;" title="编辑">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                  </button>
                  <button v-if="isAdmin" @click.stop="handleDeletePost(post)" class="p-1.5 rounded transition-all opacity-0 group-hover:opacity-100" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;" title="删除">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                  </button>
                  <span>{{ post.readTime }} min</span>
                </div>
              </div>
            </div>
          </article>
        </div>

        <!-- 分页 -->
        <div v-if="totalPages > 1" class="flex justify-center items-center gap-1.5 mt-8 flex-wrap">
          <!-- 上一页 -->
          <button
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage <= 1"
            class="pagination-btn"
            :class="currentPage <= 1 ? 'opacity-30 cursor-not-allowed' : ''"
            style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-secondary);"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          </button>
          <!-- 页码 -->
          <template v-for="page in paginationPages" :key="page">
            <span v-if="page === '...'" class="px-1 text-sm font-mono" style="color: var(--text-tertiary);">…</span>
            <button
              v-else
              @click="goToPage(page)"
              class="pagination-btn min-w-[36px]"
              :class="page === currentPage ? 'pagination-active' : ''"
              style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-secondary);"
            >
              {{ page }}
            </button>
          </template>
          <!-- 下一页 -->
          <button
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage >= totalPages"
            class="pagination-btn"
            :class="currentPage >= totalPages ? 'opacity-30 cursor-not-allowed' : ''"
            style="background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-secondary);"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </button>
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && filteredPosts.length === 0" class="text-center py-20">
          <div class="text-6xl mb-4">📝</div>
          <p class="text-lg font-mono" style="color: var(--text-secondary);">没有找到匹配的文章</p>
          <p class="text-sm mt-2" style="color: var(--text-tertiary);">试试其他关键词或标签</p>
        </div>
      </template>

      <!-- 文章详情弹窗 -->
      <Teleport to="body">
        <Transition name="modal">
          <div v-if="selectedPost" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="closePost">
            <div class="modal-overlay fixed inset-0 bg-black/70 backdrop-blur-sm" @click="closePost" />
            <div class="modal-content relative w-full max-w-3xl max-h-[85vh] overflow-y-auto rounded-2xl" style="background: var(--bg-secondary); border: 1px solid var(--border-color);">
              <!-- 关闭按钮 -->
              <button @click="closePost" class="absolute top-4 right-4 z-10 p-2 rounded-full transition-all hover:scale-110" style="background: rgba(0,0,0,0.5); color: var(--text-primary);">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <!-- 文章头图 -->
              <div class="h-48 sm:h-64 rounded-t-2xl relative overflow-hidden" :style="{ background: selectedPost.coverGradient || defaultCoverGradient }">
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-6xl">{{ selectedPost.icon || '📝' }}</span>
                </div>
                <!-- 阅读进度指示 -->
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-white/10">
                  <div class="h-full bg-neon transition-all" :style="{ width: readProgress + '%' }" />
                </div>
              </div>

              <!-- 文章内容 -->
              <div class="p-6 sm:p-8">
                <!-- 标签 + 元信息 -->
                <div class="flex flex-wrap gap-2 mb-4">
                  <span
                    v-for="tag in selectedPost.tags"
                    :key="tag"
                    class="px-2.5 py-1 rounded text-xs font-mono"
                    :style="{ background: getTagColor(tag).bg, color: getTagColor(tag).text }"
                  >
                    {{ tag }}
                  </span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-bold mb-3" style="color: var(--text-primary);">{{ selectedPost.title }}</h1>
                <div class="flex items-center gap-4 mb-6 text-sm font-mono" style="color: var(--text-tertiary);">
                  <span>📅 {{ selectedPost.date }}</span>
                  <span>⏱️ {{ selectedPost.readTime }} min read</span>
                  <span>👁️ {{ selectedPost.views }}</span>
                  <span>❤️ {{ selectedPost.likes }}</span>
                </div>

                <!-- 分割线 -->
                <div class="h-px mb-6" style="background: var(--border-color);" />

                <!-- 文章正文 -->
                <div class="prose-content" v-html="selectedPost.content" />

                <!-- 文章底部 -->
                <div class="mt-8 pt-6" style="border-top: 1px solid var(--border-color);">
                  <div class="flex items-center justify-between">
                    <div class="flex gap-3">
                      <button @click="handleLike(selectedPost)" class="action-btn">
                        ❤️ {{ selectedPost.likes }}
                      </button>
                      <button @click="handleShare(selectedPost)" class="action-btn" :style="shareMsg ? 'border-color: rgba(57, 255, 20, 0.3); color: #39ff14;' : ''">
                        {{ shareMsg || '🔗 分享' }}
                      </button>
                      <button v-if="isAdmin" @click="openEditor(selectedPost)" class="action-btn" style="border-color: rgba(0, 240, 255, 0.2); color: #00f0ff;">
                        ✏️ 编辑
                      </button>
                      <button v-if="isAdmin" @click="handleDeletePost(selectedPost)" class="action-btn" style="border-color: rgba(239, 68, 68, 0.2); color: #ef4444;">
                        🗑️ 删除
                      </button>
                    </div>
                    <span class="text-xs font-mono" style="color: var(--text-tertiary);">
                      最后更新: {{ selectedPost.date }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- 文章编辑器弹窗 -->
      <Teleport to="body">
        <Transition name="modal">
          <div v-if="showEditor" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="closeEditor">
            <div class="modal-overlay fixed inset-0 bg-black/70 backdrop-blur-sm" @click="closeEditor" />
            <div class="modal-content relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl p-6" style="background: var(--bg-secondary); border: 1px solid var(--border-color);">
              <!-- 编辑器标题栏 -->
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-bold font-mono" style="color: var(--text-primary);">
                  {{ editingPost ? '编辑文章' : '新建文章' }}
                </h2>
                <button @click="closeEditor" class="p-2 rounded-full transition-all hover:scale-110" style="background: rgba(255,255,255,0.05); color: var(--text-primary);">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>
              <!-- 错误提示 -->
              <div v-if="editorError" class="mb-4 p-3 rounded-lg text-sm font-mono" style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); color: #ef4444;">
                {{ editorError }}
              </div>
              <!-- 编辑表单 -->
              <form @submit.prevent="savePost" class="space-y-4">
                <div>
                  <label class="block text-xs font-mono mb-1.5" style="color: var(--text-tertiary);">标题 *</label>
                  <input v-model="editorForm.title" type="text" required placeholder="文章标题" class="editor-input w-full px-3 py-2 rounded-lg text-sm font-mono" />
                </div>
                <div>
                  <label class="block text-xs font-mono mb-1.5" style="color: var(--text-tertiary);">摘要</label>
                  <textarea v-model="editorForm.summary" rows="2" placeholder="文章摘要" class="editor-input w-full px-3 py-2 rounded-lg text-sm font-mono resize-none"></textarea>
                </div>
                <div>
                  <label class="block text-xs font-mono mb-1.5" style="color: var(--text-tertiary);">内容 (HTML)</label>
                  <textarea v-model="editorForm.content" rows="12" placeholder="文章正文 HTML 内容，支持 HTML 标签" class="editor-input w-full px-3 py-2 rounded-lg text-sm font-mono resize-y"></textarea>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label class="block text-xs font-mono mb-1.5" style="color: var(--text-tertiary);">标签 (逗号分隔)</label>
                    <input v-model="editorForm.tags" type="text" placeholder="Vue.js,前端" class="editor-input w-full px-3 py-2 rounded-lg text-sm font-mono" />
                  </div>
                  <div>
                    <label class="block text-xs font-mono mb-1.5" style="color: var(--text-tertiary);">图标 (Emoji)</label>
                    <input v-model="editorForm.icon" type="text" placeholder="📝" class="editor-input w-full px-3 py-2 rounded-lg text-sm font-mono" />
                  </div>
                  <div>
                    <label class="block text-xs font-mono mb-1.5" style="color: var(--text-tertiary);">阅读时间 (分钟)</label>
                    <input v-model.number="editorForm.read_time" type="number" min="1" max="120" class="editor-input w-full px-3 py-2 rounded-lg text-sm font-mono" />
                  </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs font-mono mb-1.5" style="color: var(--text-tertiary);">状态</label>
                    <select v-model="editorForm.status" class="editor-input w-full px-3 py-2 rounded-lg text-sm font-mono">
                      <option value="published">已发布</option>
                      <option value="draft">草稿</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-xs font-mono mb-1.5" style="color: var(--text-tertiary);">封面渐变 (CSS)</label>
                    <input v-model="editorForm.cover_gradient" type="text" placeholder="linear-gradient(135deg, #0c4a6e, #134e4a)" class="editor-input w-full px-3 py-2 rounded-lg text-sm font-mono" />
                  </div>
                </div>
                <div class="flex justify-end gap-3 pt-2">
                  <button type="button" @click="closeEditor" class="px-4 py-2 rounded-lg text-sm font-mono transition-all" style="background: var(--bg-primary); border: 1px solid var(--border-color); color: var(--text-secondary);">取消</button>
                  <button type="submit" :disabled="editorLoading" class="px-4 py-2 rounded-lg text-sm font-mono transition-all hover:scale-105" style="background: rgba(0, 240, 255, 0.15); border: 1px solid rgba(0, 240, 255, 0.3); color: #00f0ff;">
                    {{ editorLoading ? '保存中...' : (editingPost ? '更新文章' : '发布文章') }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getBlogPosts, getBlogTags, likeBlogPost, createBlogPost, updateBlogPost, deleteBlogPost, getAdminStatus } from '../composables/useApi'

const searchQuery = ref('')
const activeTags = ref([])
const sortOrder = ref('desc')  // desc=最新在前, asc=最早在前
const viewMode = ref('list')
const selectedPost = ref(null)
const readProgress = ref(0)
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const total = ref(0)
const allTags = ref([])
const isAdmin = getAdminStatus()

// 编辑器状态
const showEditor = ref(false)
const editingPost = ref(null)
const editorForm = ref({
  title: '', summary: '', content: '', tags: '',
  icon: '📝', read_time: 5, status: 'published', cover_gradient: ''
})
const editorLoading = ref(false)
const editorError = ref('')

// 默认封面渐变
const defaultCoverGradient = 'linear-gradient(135deg, #0c4a6e 0%, #164e63 50%, #134e4a 100%)'

// 格式化日期
const formatDate = (iso) => {
  if (!iso) return '未知'
  const d = new Date(iso)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// 文章列表（从 API 加载，转换字段名以兼容模板）
const posts = ref([])

// 加载文章
const loadPosts = async () => {
  loading.value = true
  try {
    const tag = activeTags.value.length > 0 ? activeTags.value[0] : ''
    const status = isAdmin.value ? '' : 'published'
    const data = await getBlogPosts(currentPage.value, 12, tag, searchQuery.value, status, sortOrder.value)
    posts.value = data.items.map(p => ({
      id: p.id,
      title: p.title,
      summary: p.summary,
      content: p.content,
      tags: p.tags || [],
      date: formatDate(p.published_at),
      readTime: p.read_time || 5,
      views: p.views || 0,
      likes: p.likes || 0,
      icon: p.icon || '📝',
      coverGradient: p.cover_gradient || defaultCoverGradient,
      status: p.status
    }))
    totalPages.value = data.pages
    total.value = data.total
  } catch (e) {
    console.error('加载博客文章失败:', e)
    posts.value = []
  } finally {
    loading.value = false
  }
}

// 加载标签
const loadTags = async () => {
  try {
    allTags.value = await getBlogTags()
  } catch (e) {
    console.error('加载标签失败:', e)
  }
}

// 标签切换
const toggleTag = (tag) => {
  const idx = activeTags.value.indexOf(tag)
  if (idx >= 0) {
    activeTags.value.splice(idx, 1)
  } else {
    activeTags.value = [tag] // 单选模式
  }
  currentPage.value = 1
  loadPosts()
}

// 排序切换
const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
  currentPage.value = 1
  loadPosts()
}

// 防抖搜索
let searchTimer = null
const debounceSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    loadPosts()
  }, 300)
}

// 分页
const goToPage = (p) => {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  loadPosts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 标签颜色映射
const tagColorMap = {
  'Vue.js': { bg: 'rgba(66, 184, 131, 0.15)', text: '#42b883' },
  'JavaScript': { bg: 'rgba(247, 223, 30, 0.15)', text: '#f7df1e' },
  'TypeScript': { bg: 'rgba(49, 120, 198, 0.15)', text: '#3178c6' },
  'Python': { bg: 'rgba(53, 114, 165, 0.15)', text: '#3572a5' },
  'Docker': { bg: 'rgba(36, 150, 237, 0.15)', text: '#2496ed' },
  'DevOps': { bg: 'rgba(255, 102, 0, 0.15)', text: '#ff6600' },
  'PostgreSQL': { bg: 'rgba(51, 103, 145, 0.15)', text: '#336791' },
  '数据库': { bg: 'rgba(255, 165, 0, 0.15)', text: '#ffa500' },
  'Redis': { bg: 'rgba(220, 56, 45, 0.15)', text: '#dc382d' },
  '前端': { bg: 'rgba(0, 240, 255, 0.15)', text: '#00f0ff' },
  'CSS': { bg: 'rgba(38, 77, 228, 0.15)', text: '#264de4' },
  '面试': { bg: 'rgba(255, 0, 229, 0.15)', text: '#ff00e5' },
  '性能优化': { bg: 'rgba(57, 255, 20, 0.15)', text: '#39ff14' },
  '网络编程': { bg: 'rgba(255, 102, 0, 0.15)', text: '#ff6600' },
  '布局': { bg: 'rgba(139, 92, 246, 0.15)', text: '#8b5cf6' },
}

const getTagColor = (tag) => tagColorMap[tag] || { bg: 'rgba(255,255,255,0.1)', text: 'var(--text-secondary)' }

// 卡片渐变
const gradients = [
  'linear-gradient(135deg, #00f0ff, #0080ff)',
  'linear-gradient(135deg, #ff00e5, #ff6600)',
  'linear-gradient(135deg, #39ff14, #00f0ff)',
  'linear-gradient(135deg, #f0f, #8b5cf6)',
  'linear-gradient(135deg, #ffa500, #ff00e5)',
  'linear-gradient(135deg, #3178c6, #42b883)',
]
const getCardGradient = (i) => gradients[i % gradients.length]

// 过滤（标签已在 API 层面筛选，这里做客户端二次过滤）
const filteredPosts = computed(() => {
  return posts.value.filter(p => {
    const matchSearch = !searchQuery.value ||
      p.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (p.summary && p.summary.toLowerCase().includes(searchQuery.value.toLowerCase()))
    const matchTags = activeTags.value.length === 0 ||
      activeTags.value.some(t => p.tags.includes(t))
    return matchSearch && matchTags
  })
})

// 分页页码计算（带省略号）
const paginationPages = computed(() => {
  const tp = totalPages.value
  const cp = currentPage.value
  if (tp <= 7) {
    return Array.from({ length: tp }, (_, i) => i + 1)
  }
  const pages = []
  pages.push(1)
  if (cp > 3) pages.push('...')
  const start = Math.max(2, cp - 1)
  const end = Math.min(tp - 1, cp + 1)
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  if (cp < tp - 2) pages.push('...')
  pages.push(tp)
  return pages
})

// 文章操作
const openPost = (post) => {
  selectedPost.value = post
  readProgress.value = 0
  document.body.style.overflow = 'hidden'
}

const closePost = () => {
  selectedPost.value = null
  document.body.style.overflow = ''
}

const handleLike = async (post) => {
  try {
    const data = await likeBlogPost(post.id)
    post.likes = data.likes
  } catch (e) {
    // 降级：本地 +1
    post.likes++
  }
}

// 分享功能
const shareMsg = ref('')
let shareTimer = null
const handleShare = async (post) => {
  const url = window.location.origin + '/blog?id=' + post.id
  const title = post.title
  try {
    if (navigator.share) {
      await navigator.share({ title, url })
    } else {
      await navigator.clipboard.writeText(url)
      shareMsg.value = '✓ 已复制'
      clearTimeout(shareTimer)
      shareTimer = setTimeout(() => { shareMsg.value = '' }, 2000)
    }
  } catch (e) {
    // 用户取消分享或 clipboard 失败，静默处理
  }
}

// ============================================================
//  管理员：文章编辑器
// ============================================================
const resetEditorForm = () => {
  editorForm.value = { title: '', summary: '', content: '', tags: '', icon: '📝', read_time: 5, status: 'published', cover_gradient: '' }
  editorError.value = ''
}

const openEditor = (post) => {
  if (post) {
    editingPost.value = post
    editorForm.value = {
      title: post.title,
      summary: post.summary || '',
      content: post.content || '',
      tags: (post.tags || []).join(', '),
      icon: post.icon || '📝',
      read_time: post.readTime || 5,
      status: post.status || 'published',
      cover_gradient: post.coverGradient || ''
    }
  } else {
    editingPost.value = null
    resetEditorForm()
  }
  showEditor.value = true
  document.body.style.overflow = 'hidden'
}

const closeEditor = () => {
  showEditor.value = false
  editingPost.value = null
  resetEditorForm()
  document.body.style.overflow = ''
}

const savePost = async () => {
  if (!editorForm.value.title.trim()) { editorError.value = '标题不能为空'; return }
  editorLoading.value = true
  editorError.value = ''
  try {
    const payload = {
      title: editorForm.value.title.trim(),
      summary: editorForm.value.summary.trim(),
      content: editorForm.value.content,
      tags: editorForm.value.tags.trim(),
      icon: editorForm.value.icon || '📝',
      read_time: editorForm.value.read_time || 5,
      status: editorForm.value.status,
      cover_gradient: editorForm.value.cover_gradient
    }
    if (editingPost.value) {
      await updateBlogPost(editingPost.value.id, payload)
    } else {
      await createBlogPost(payload)
    }
    closeEditor()
    loadPosts()
    loadTags()
  } catch (e) {
    editorError.value = e.response?.data?.error || '保存失败，请重试'
  } finally {
    editorLoading.value = false
  }
}

const handleDeletePost = async (post) => {
  if (!confirm(`确定要删除文章「${post.title}」吗？此操作不可撤销。`)) return
  try {
    await deleteBlogPost(post.id)
    if (selectedPost.value && selectedPost.value.id === post.id) closePost()
    loadPosts()
    loadTags()
  } catch (e) {
    alert('删除失败: ' + (e.response?.data?.error || '未知错误'))
  }
}

// ESC 关闭 + 模拟阅读进度
const handleKeydown = (e) => {
  if (e.key === 'Escape') {
    if (showEditor.value) closeEditor()
    else if (selectedPost.value) closePost()
  }
}

let progressInterval = null
const startReadProgress = () => {
  progressInterval = setInterval(() => {
    if (readProgress.value < 100) {
      readProgress.value += Math.random() * 2
    }
  }, 500)
}

const stopReadProgress = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  loadPosts()
  loadTags()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  stopReadProgress()
  if (searchTimer) clearTimeout(searchTimer)
})
</script>

<style scoped>
/* 搜索输入框 */
.search-input {
  background: var(--bg-secondary, #1a1a2e);
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
  color: var(--text-primary, #e0e0e0);
  outline: none;
  transition: all 0.3s ease;
}
.search-input:focus {
  border-color: rgba(0, 240, 255, 0.5);
  box-shadow: 0 0 0 3px rgba(0, 240, 255, 0.1);
}
.search-input::placeholder {
  color: var(--text-tertiary, #666);
}

/* 排序按钮 */
.sort-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}
.sort-btn:hover {
  background: rgba(0, 240, 255, 0.1);
  border-color: rgba(0, 240, 255, 0.3);
  color: #00f0ff;
}

/* 标签按钮 */
.tag-btn {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary, #aaa);
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
}
.tag-btn:hover {
  background: rgba(0, 240, 255, 0.1);
  color: #00f0ff;
  border-color: rgba(0, 240, 255, 0.3);
}
.tag-active {
  background: rgba(0, 240, 255, 0.15) !important;
  color: #00f0ff !important;
  border-color: rgba(0, 240, 255, 0.4) !important;
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
}

/* 文章卡片 (列表视图) */
.post-card {
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
  background: var(--bg-secondary, #1a1a2e);
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.06));
  transition: all 0.3s ease;
  animation: slideUp 0.5s ease forwards;
  opacity: 0;
}
.post-card:hover {
  border-color: rgba(0, 240, 255, 0.3);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.08);
  transform: translateX(4px);
}

/* 文章卡片 (网格视图) */
.grid-card {
  border-radius: 12px;
  background: var(--bg-secondary, #1a1a2e);
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.06));
  overflow: hidden;
  transition: all 0.3s ease;
  animation: slideUp 0.5s ease forwards;
  opacity: 0;
}
.grid-card:hover {
  border-color: rgba(0, 240, 255, 0.3);
  box-shadow: 0 0 25px rgba(0, 240, 255, 0.1);
  transform: translateY(-4px);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 弹窗 */
.modal-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 240, 255, 0.3) transparent;
}
.modal-content::-webkit-scrollbar {
  width: 6px;
}
.modal-content::-webkit-scrollbar-thumb {
  background: rgba(0, 240, 255, 0.3);
  border-radius: 3px;
}

/* 操作按钮 */
.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary, #aaa);
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
}
.action-btn:hover {
  background: rgba(255, 0, 229, 0.1);
  border-color: rgba(255, 0, 229, 0.3);
  color: #ff00e5;
}

/* 编辑器输入框 */
.editor-input {
  background: var(--bg-primary, #0d0d1a);
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
  color: var(--text-primary, #e0e0e0);
  outline: none;
  transition: all 0.3s ease;
}
.editor-input:focus {
  border-color: rgba(0, 240, 255, 0.5);
  box-shadow: 0 0 0 3px rgba(0, 240, 255, 0.1);
}
.editor-input::placeholder {
  color: var(--text-tertiary, #666);
}
select.editor-input {
  cursor: pointer;
}

/* 文章正文样式 */
.prose-content :deep(h2) {
  font-size: 1.35rem;
  font-weight: 700;
  margin: 2rem 0 1rem;
  color: var(--text-primary, #e0e0e0);
}
.prose-content :deep(h3) {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 1.5rem 0 0.75rem;
  color: var(--text-primary, #e0e0e0);
}
.prose-content :deep(p) {
  margin: 0.75rem 0;
  line-height: 1.8;
  color: var(--text-secondary, #aaa);
}
.prose-content :deep(ul),
.prose-content :deep(ol) {
  padding-left: 1.5rem;
  margin: 0.75rem 0;
  color: var(--text-secondary, #aaa);
}
.prose-content :deep(li) {
  margin: 0.35rem 0;
  line-height: 1.7;
}
.prose-content :deep(code) {
  font-family: 'Courier New', monospace;
  background: rgba(0, 240, 255, 0.08);
  color: #00f0ff;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-size: 0.85em;
}
.prose-content :deep(pre) {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(0, 240, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
  overflow-x: auto;
  margin: 1rem 0;
}
.prose-content :deep(pre code) {
  background: transparent;
  padding: 0;
  color: #e0e0e0;
}
.prose-content :deep(strong) {
  color: var(--text-primary, #e0e0e0);
  font-weight: 600;
}

/* 列表动画 */
.post-list-enter-active {
  transition: all 0.4s ease;
}
.post-list-leave-active {
  transition: all 0.3s ease;
}
.post-list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.post-list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* 弹窗动画 */
.modal-enter-active {
  transition: all 0.3s ease;
}
.modal-leave-active {
  transition: all 0.2s ease;
}
.modal-enter-from {
  opacity: 0;
}
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .modal-content {
  transform: scale(0.95) translateY(20px);
}
.modal-leave-to .modal-content {
  transform: scale(0.95) translateY(20px);
}

/* 行截断 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 分页按钮 */
.pagination-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  min-width: 36px;
  padding: 0 0.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-family: 'Courier New', monospace;
  transition: all 0.2s ease;
  cursor: pointer;
}
.pagination-btn:hover:not(:disabled):not(.pagination-active) {
  border-color: rgba(0, 240, 255, 0.3) !important;
  color: #00f0ff !important;
}
.pagination-active {
  background: rgba(0, 240, 255, 0.15) !important;
  border-color: rgba(0, 240, 255, 0.4) !important;
  color: #00f0ff !important;
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.15);
}

/* 响应式 */
@media (max-width: 640px) {
  .post-card {
    padding: 1rem;
  }
}
</style>
