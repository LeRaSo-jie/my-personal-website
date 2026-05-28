<template>
  <div ref="scrollContainer" class="snap-container" :class="{ 'photo-wall-active': isPhotoWallActive }" @wheel="handleWheel">
    <!-- 全局背景层（固定定位，覆盖整个页面） -->
    <div class="fixed inset-0" style="background: var(--bg-primary); z-index: 0;">
        <!-- A1: 星空连线网络（Canvas） -->
        <canvas ref="constellationCanvas" class="absolute inset-0 w-full h-full"></canvas>

        <!-- 粒子文字动画 Canvas -->
        <canvas ref="particleCanvas"
          class="absolute inset-0 w-full h-full pointer-events-none"
          :style="{ opacity: showParticleCanvas ? 1 : 0, transition: 'opacity 0.4s ease', zIndex: 5 }">
        </canvas>

        <!-- 动态渐变光斑（跟随鼠标） -->
        <div
          class="absolute w-[700px] h-[700px] rounded-full blur-[180px] pointer-events-none"
          :style="{
            background: 'radial-gradient(circle, var(--accent), transparent)',
            left: `${mouseX - 350}px`,
            top: `${mouseY - 350}px`,
            transition: 'left 0.35s ease-out, top 0.35s ease-out',
            opacity: isDark ? 0.22 : 0.08
          }"
        ></div>
        <div
          class="absolute w-[600px] h-[600px] rounded-full blur-[150px] pointer-events-none"
          :style="{
            background: 'radial-gradient(circle, var(--accent-purple), transparent)',
            left: `${mouseX - 300 + parallaxX * 3}px`,
            top: `${mouseY - 300 - parallaxY * 3}px`,
            transition: 'left 0.5s ease-out, top 0.5s ease-out',
            opacity: isDark ? 0.15 : 0.06
          }"
        ></div>
        <div
          class="absolute w-[500px] h-[500px] rounded-full blur-[120px] pointer-events-none"
          :style="{
            background: 'radial-gradient(circle, var(--accent-pink), transparent)',
            left: `${mouseX - 250 - parallaxX * 4}px`,
            top: `${mouseY - 250 + parallaxY * 4}px`,
            transition: 'left 0.7s ease-out, top 0.7s ease-out',
            opacity: isDark ? 0.1 : 0.04
          }"
        ></div>

        <!-- A3: 极光波浪 -->
        <div class="aurora-container">
          <div class="aurora-wave aurora-wave-1"></div>
          <div class="aurora-wave aurora-wave-2"></div>
          <div class="aurora-wave aurora-wave-3"></div>
          <div class="aurora-wave aurora-wave-4"></div>
        </div>

        <!-- 动画渐变网格背景 -->
        <div class="hero-mesh-bg"></div>

        <!-- 扫描环 -->
        <div class="absolute pointer-events-none" :style="{
          left: mouseX + 'px',
          top: mouseY + 'px',
          transform: 'translate(-50%, -50%)'
        }">
          <div class="scan-ring scan-ring-1"></div>
          <div class="scan-ring scan-ring-2"></div>
          <div class="scan-ring scan-ring-3"></div>
        </div>

        <!-- 鼠标光晕 -->
        <div class="cursor-glow" :style="{
          left: mouseX + 'px',
          top: mouseY + 'px',
          opacity: isDark ? 0.5 : 0.25
        }"></div>

        <!-- 扫描线（仅暗色） -->
        <div class="absolute inset-0 pointer-events-none scan-overlay"></div>
    </div>

    <!-- ========== 第一屏：Hero ========== -->
    <section
      class="snap-section relative flex items-center justify-center overflow-hidden"
      @mousemove="handleMouseMove"
      @mouseleave="handleMouseLeave"
    >
      <!-- Hero 内容（鼠标视差） -->
      <div
        class="relative z-10 text-center px-4 max-w-5xl mx-auto"
        :style="{
          transform: `translate(${parallaxX * 0.4}px, ${parallaxY * 0.4}px)`,
          transition: 'transform 0.3s ease-out'
        }"
      >
        <!-- 终端标签 -->
        <div class="mb-8 animate-fade-in">
          <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider"
                style="background: rgba(3, 105, 161, 0.08); border: 1px solid rgba(3, 105, 161, 0.2); color: var(--accent);">
            DIGITAL.NEXUS // v2.0
          </span>
        </div>

        <!-- B3+B4: 打字机标题（3D透视倾斜 + 渐变文字 + 霓虹发光） -->
        <h1 class="relative text-5xl md:text-7xl lg:text-8xl font-bold mb-6 font-mono hero-title select-none whitespace-nowrap"
            :style="{
              transform: `translate(${parallaxX * -0.6}px, ${parallaxY * -0.6}px) perspective(800px) rotateY(${titleTiltX}deg) rotateX(${titleTiltY}deg)`,
              transition: 'transform 0.15s ease-out',
              transformStyle: 'preserve-3d',
              visibility: showParticleCanvas ? 'hidden' : 'visible'
            }">
          <span class="relative inline-block">
          <span class="text-neon opacity-50 absolute right-full top-0 pointer-events-none" aria-hidden="true">> </span>
          <span>
            <span
              v-for="(char, idx) in displayChars"
              :key="idx"
              class="hero-char"
              :style="{
                background: char.animColor
                  ? char.animColor
                  : isDark
                    ? 'linear-gradient(135deg, #00f3ff, #b670ff, #ff2d75)'
                    : 'linear-gradient(135deg, #0369a1, #6d28d9, #be185d)',
                '-webkit-background-clip': 'text',
                '-webkit-text-fill-color': 'transparent',
                'background-clip': 'text',
                transform: `translate(${char.offsetX}px, ${char.offsetY}px)`,
                opacity: char.opacity,
                filter: char.glow > 0.05
                  ? `drop-shadow(0 0 ${char.glow * 8}px var(--accent)) drop-shadow(0 0 ${char.glow * 16}px var(--accent-purple))`
                  : 'none',
                transition: char.animating ? 'none' : 'filter 0.25s ease-out, transform 0.3s ease-out, opacity 0.3s ease-out'
              }"
            >{{ char.displayChar === ' ' ? '\u00A0' : char.displayChar }}</span>
          </span>
          </span>
          <span class="typewriter-cursor"></span>
        </h1>

        <!-- 副标题 -->
        <p class="text-lg md:text-xl mb-3 animate-fade-in-delay font-mono"
           :style="{
             color: 'var(--text-secondary)',
             transform: `translate(${parallaxX * 0.25}px, ${parallaxY * 0.25}px)`,
             transition: 'transform 0.3s ease-out'
           }">
          <span class="text-neon opacity-60">const</span> role = <span class="text-neon-pink">"{{ displayedRole }}"</span>
        </p>

        <!-- 个人 Slogan -->
        <p class="text-base md:text-lg mb-4 animate-fade-in-delay font-mono italic"
           :style="{
             color: 'var(--text-muted)',
             transform: `translate(${parallaxX * 0.2}px, ${parallaxY * 0.2}px)`,
             transition: 'transform 0.3s ease-out'
           }">
          <span class="opacity-50">/*</span>
          <span style="color: var(--text-tertiary);">Crafting ideas into code, one pixel at a time</span>
          <span class="opacity-50"> */</span>
        </p>

        <!-- 状态行 -->
        <div class="flex flex-wrap justify-center gap-4 mb-10 text-sm font-mono animate-fade-in-delay-2" style="color: var(--text-muted);">
          <span class="status-badge"><span class="text-neon-green">●</span> STATUS: ONLINE</span>
          <span class="status-badge"><span class="text-neon-purple">◆</span> MODE: CREATIVE</span>
          <span class="status-badge"><span class="text-neon-yellow">▲</span> LEVEL: PRO</span>
        </div>

        <!-- CTA 按钮 -->
        <div class="flex justify-center space-x-4 animate-fade-in-delay-2">
          <router-link to="/portfolio" class="btn-primary text-lg px-8 py-3 group">
            <span class="relative z-10 flex items-center gap-2">
              查看作品
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </span>
          </router-link>
          <router-link to="/tools" class="btn-secondary text-lg px-8 py-3">
            工具箱
          </router-link>
        </div>
      </div>

      <!-- 滚动提示 -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce z-10">
        <div class="flex flex-col items-center gap-2">
          <span class="text-xs font-mono tracking-widest" style="color: var(--text-muted);">SCROLL</span>
          <svg class="w-5 h-5 text-neon opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </div>

      <!-- 页码指示器 -->
      <div class="absolute right-6 top-1/2 -translate-y-1/2 z-20 flex flex-col gap-3">
        <button
          v-for="i in totalSections"
          :key="i"
          @click="scrollToSection(i - 1)"
          class="w-2 h-2 rounded-full transition-all duration-300 cursor-pointer"
          :class="currentSection === i - 1 ? 'w-2.5 h-6 rounded-full' : 'hover:scale-150'"
          :style="{
            background: currentSection === i - 1 ? 'var(--accent)' : 'var(--text-muted)',
            opacity: currentSection === i - 1 ? 1 : 0.4
          }"
        ></button>
      </div>
    </section>

    <!-- ========== 第二屏：关于我 ========== -->
    <section class="snap-section flex items-center px-4 relative overflow-hidden" @mousemove="handleSectionMouseMove">
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute top-20 left-10 w-64 h-64 rounded-full blur-[100px]"
             :style="{ background: 'var(--accent)', opacity: isDark ? 0.05 : 0.03, transform: `translate(${sectionMouseX * 0.02}px, ${sectionMouseY * 0.02}px)` }"></div>
        <div class="absolute bottom-20 right-10 w-48 h-48 rounded-full blur-[80px]"
             :style="{ background: 'var(--accent-purple)', opacity: isDark ? 0.05 : 0.03, transform: `translate(${sectionMouseX * -0.015}px, ${sectionMouseY * -0.015}px)` }"></div>
      </div>

      <div class="max-w-6xl mx-auto w-full py-16 relative z-10">
        <div class="text-center mb-12">
          <span class="font-mono text-sm text-neon opacity-60 tracking-widest">01 //</span>
          <h2 class="text-4xl font-bold mt-2 gradient-text">关于我</h2>
        </div>
        <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <div class="card-neon p-6 group">
            <div class="flex items-center gap-3 mb-5">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center transition-transform duration-300 group-hover:scale-110 group-hover:rotate-6"
                   style="background: rgba(3, 105, 161, 0.1); border: 1px solid rgba(3, 105, 161, 0.2);">
                <svg class="w-5 h-5 text-neon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold" style="color: var(--text-primary);">技能栈</h3>
            </div>
            <div class="flex flex-wrap gap-2">
              <span v-for="(skill, index) in skills" :key="skill" class="badge-cyber"
                    :style="{ animationDelay: index * 0.05 + 's' }">{{ skill }}</span>
            </div>
          </div>
          <div class="card-neon p-6 group">
            <div class="flex items-center gap-3 mb-5">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center transition-transform duration-300 group-hover:scale-110 group-hover:-rotate-6"
                   style="background: rgba(109, 40, 217, 0.1); border: 1px solid rgba(109, 40, 217, 0.2);">
                <svg class="w-5 h-5 text-neon-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold" style="color: var(--text-primary);">关于我</h3>
            </div>
            <p class="text-sm leading-relaxed font-mono" style="color: var(--text-secondary);">
              <span class="text-neon-green">></span> 全栈开发者，热爱技术，善于将创意转化为代码。<br>
              <span class="text-neon-green">></span> 专注于 Web 开发与自动化测试。<br>
              <span class="text-neon-green">></span> Always learning, always building.
            </p>
          </div>
        </div>
        <div class="text-center mt-8">
          <router-link to="/resume" class="inline-flex items-center gap-2 text-neon hover:underline font-mono text-sm group">
            查看完整简历
            <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ========== 第三屏：精选作品 ========== -->
    <section class="snap-section flex items-center px-4 relative overflow-hidden" @mousemove="handleSectionMouseMove">
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute top-1/4 right-20 w-80 h-80 rounded-full blur-[120px]"
             :style="{ background: 'var(--accent-purple)', opacity: isDark ? 0.06 : 0.03, transform: `translate(${sectionMouseX * 0.025}px, ${sectionMouseY * 0.025}px)` }"></div>
      </div>
      <div class="max-w-6xl mx-auto w-full py-16 relative z-10">
        <div class="flex justify-between items-end mb-8">
          <div>
            <span class="font-mono text-sm text-neon-purple opacity-60 tracking-widest">02 //</span>
            <h2 class="text-4xl font-bold mt-2" style="color: var(--text-primary);">精选作品</h2>
          </div>
          <router-link to="/portfolio" class="inline-flex items-center gap-2 text-neon hover:underline font-mono text-sm group">
            查看更多
            <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </router-link>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="item in featuredPortfolio" :key="item.id" class="card-neon p-6 group relative overflow-hidden">
            <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-neon-cyan via-neon-purple to-neon-pink opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <h3 class="text-xl font-semibold mb-2 group-hover:text-neon transition-colors" style="color: var(--text-primary);">{{ item.title }}</h3>
            <p class="text-sm mb-4 leading-relaxed" style="color: var(--text-secondary);">{{ item.description }}</p>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="tech in item.tech_stack" :key="tech" class="text-xs px-2 py-1 rounded font-mono"
                    style="background: rgba(3, 105, 161, 0.06); color: var(--accent); border: 1px solid rgba(3, 105, 161, 0.1);">{{ tech }}</span>
            </div>
          </div>
        </div>
        <div v-if="featuredPortfolio.length === 0" class="text-center mt-8">
          <div class="card-neon p-8 max-w-md mx-auto">
            <div class="text-4xl mb-3">🚀</div>
            <p class="font-mono text-sm" style="color: var(--text-secondary);">精彩项目即将上线</p>
            <p class="font-mono text-xs mt-1" style="color: var(--text-tertiary);">管理员可在后台添加作品数据</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ========== 第四屏：工具箱（在线工具 + 资源下载） ========== -->
    <section class="snap-section flex items-center px-4 relative overflow-hidden" @mousemove="handleSectionMouseMove">
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute bottom-20 left-1/4 w-72 h-72 rounded-full blur-[100px]"
             :style="{ background: 'var(--accent-green)', opacity: isDark ? 0.05 : 0.03, transform: `translate(${sectionMouseX * -0.02}px, ${sectionMouseY * -0.02}px)` }"></div>
      </div>
      <div class="max-w-6xl mx-auto w-full py-16 relative z-10">
        <div class="flex justify-between items-end mb-10">
          <div>
            <span class="font-mono text-sm text-neon-pink opacity-60 tracking-widest">03 //</span>
            <h2 class="text-4xl font-bold mt-2" style="color: var(--text-primary);">工具箱</h2>
          </div>
          <router-link to="/tools" class="inline-flex items-center gap-2 text-neon hover:underline font-mono text-sm group">
            进入工具箱
            <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </router-link>
        </div>

        <!-- 上下两栏布局 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- 左栏：在线工具 -->
          <div>
            <div class="flex items-center gap-2 mb-4">
              <svg class="w-4 h-4" style="color: var(--accent);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              <span class="font-mono text-sm font-semibold" style="color: var(--text-primary);">在线工具</span>
              <span class="text-xs px-2 py-0.5 rounded-full font-mono"
                    style="background: rgba(3, 105, 161, 0.08); border: 1px solid rgba(3, 105, 161, 0.15); color: var(--accent);">21 个工具</span>
              <router-link to="/tools" class="ml-auto text-xs font-mono text-neon hover:underline">查看全部 \u2192</router-link>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
              <router-link
                v-for="cat in homeToolCategories"
                :key="cat.key"
                :to="`/tools?category=${cat.key}`"
                class="card-neon p-3 group text-center hover:scale-[1.03] transition-all cursor-pointer"
              >
                <div class="w-9 h-9 rounded-lg flex items-center justify-center mx-auto mb-2"
                     :style="{ background: cat.color + '12', border: `1px solid ${cat.color}25` }">
                  <div class="w-4 h-4" :style="{ color: cat.color }" v-html="cat.icon"></div>
                </div>
                <div class="font-mono text-xs font-semibold group-hover:text-neon transition-colors" style="color: var(--text-primary);">{{ cat.name }}</div>
                <div class="text-[10px] mt-0.5 font-mono" style="color: var(--text-muted);">{{ cat.count }} \u4E2A</div>
              </router-link>
            </div>
          </div>

          <!-- 右栏：资源下载 -->
          <div>
            <div class="flex items-center gap-2 mb-4">
              <svg class="w-4 h-4 text-neon-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span class="font-mono text-sm font-semibold" style="color: var(--text-primary);">资源下载</span>
              <router-link to="/tools?tab=downloads" class="ml-auto text-xs font-mono text-neon-green hover:underline">查看全部 →</router-link>
            </div>
            <div v-if="popularTools.length > 0" class="space-y-3">
              <div v-for="tool in popularTools" :key="tool.id"
                   class="card-neon p-4 group flex items-center gap-4 hover:scale-[1.01] transition-all">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                     style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.15);">
                  <svg class="w-5 h-5 text-neon-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <span class="font-mono text-sm font-semibold group-hover:text-neon-green transition-colors" style="color: var(--text-primary);">{{ tool.name }}</span>
                    <span class="text-[10px] px-1.5 py-0.5 rounded font-mono"
                          style="background: rgba(14,165,233,0.06); color: var(--accent); border: 1px solid rgba(14,165,233,0.1);">{{ tool.file_type }}</span>
                  </div>
                  <p class="text-xs mt-0.5 truncate" style="color: var(--text-muted);">{{ tool.description }}</p>
                </div>
                <button @click="handleDownload(tool.id, tool.filename)"
                        class="px-3 py-1.5 rounded-lg text-xs font-mono transition-all duration-300 flex-shrink-0"
                        style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); color: #10b981;">
                  下载
                </button>
              </div>
            </div>
            <div v-else class="card-neon p-8 text-center">
              <div class="text-4xl mb-3">📦</div>
              <p class="font-mono text-sm" style="color: var(--text-secondary);">暂无工具包</p>
              <p class="font-mono text-xs mt-1" style="color: var(--text-tertiary);">管理员可在后台上传</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========== 第五区：照片墙（自由滚动） ========== -->
    <section ref="photoWallRef" v-show="isPhotoWallActive" class="photo-wall-section px-4 py-24 relative">
      
      <div class="max-w-6xl mx-auto relative z-10">
        <div class="text-center mb-14">
          <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider mb-4"
                style="background: rgba(236, 72, 153, 0.08); border: 1px solid rgba(236, 72, 153, 0.2); color: var(--accent-pink, #ec4899);">
            // LIFE_MOMENTS
          </span>
          <h2 class="text-4xl md:text-5xl font-bold mt-2 gradient-text">生活碎片</h2>
          <p class="text-sm font-mono mt-3" style="color: var(--text-muted);">// code by day, live by heart</p>
          <!-- 管理员：添加照片按钮 -->
          <div v-if="getAdminStatus()" class="mt-4">
            <button @click="openAddPhoto" class="photo-admin-btn">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
              <span>添加照片</span>
            </button>
          </div>
        </div>

        <!-- 照片网格 -->
        <div class="photo-grid">
          <div
            v-for="photo in photos"
            :key="photo.id"
            class="photo-card"
            :class="[`photo-${photo.size}`]"
            :style="{ '--rotate': photo.rotate + 'deg' }"
            @click="openLightbox(photo)"
          >
            <img :src="photo.url" :alt="photo.caption" loading="lazy" class="photo-img" :style="{ objectPosition: (photo.position_x ?? 50) + '% ' + (photo.position_y ?? 50) + '%' }" />
            <div class="photo-overlay">
              <span class="photo-caption">{{ photo.caption }}</span>
              <span class="photo-tag">{{ photo.tag }}</span>
            </div>
            <!-- 管理员操作按钮 -->
            <div v-if="getAdminStatus()" class="photo-admin-overlay" @click.stop>
              <button @click.stop="openEditPhoto(photo)" class="photo-admin-card-btn" title="编辑">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
              </button>
              <button @click.stop="handleDeletePhoto(photo)" class="photo-admin-card-btn photo-admin-delete" title="删除">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========== 底部收尾 ========== -->
    <section v-show="isPhotoWallActive" class="closing-section relative overflow-hidden">
      <!-- 背景装饰 -->
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute top-0 left-1/4 w-96 h-96 rounded-full blur-[160px]" style="background: var(--accent); opacity: 0.04;"></div>
        <div class="absolute bottom-0 right-1/4 w-80 h-80 rounded-full blur-[140px]" style="background: var(--accent-purple); opacity: 0.04;"></div>
      </div>

      <div class="relative z-10 max-w-3xl mx-auto text-center px-4 py-24">
        <!-- 分隔线 -->
        <div class="w-24 h-px mx-auto mb-12" style="background: linear-gradient(90deg, transparent, var(--accent), transparent);"></div>

        <!-- 感谢语 -->
        <h3 class="text-3xl md:text-4xl font-bold font-mono mb-4 gradient-text">Thanks for scrolling ✨</h3>
        <p class="text-sm font-mono leading-relaxed mb-8 max-w-lg mx-auto" style="color: var(--text-secondary);">
          <span style="color: var(--accent);">/**</span><br/>
          <span style="color: var(--accent);">&nbsp;*</span> Life is more than just code.<br/>
          <span style="color: var(--accent);">&nbsp;*</span> Thanks for browsing through my digital nexus.<br/>
          <span style="color: var(--accent);">&nbsp;*</span> Feel free to connect anytime.<br/>
          <span style="color: var(--accent);">&nbsp;*/</span>
        </p>

        <!-- 社交链接 -->
        <div class="flex items-center justify-center gap-4 mb-10">
          <a href="https://github.com/yourusername" target="_blank" class="social-btn" title="GitHub">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
          </a>
          <a href="https://gitee.com/yourusername" target="_blank" class="social-btn" title="Gitee">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M11.984 0C5.372 0 0 5.372 0 11.984c0 6.612 5.372 11.984 11.984 11.984 6.612 0 11.984-5.372 11.984-11.984C23.968 5.372 18.596 0 11.984 0zM9.062 18.628c-3.27 0-5.92-2.028-6.884-4.864h3.576c.712 1.44 2.184 2.424 3.88 2.424 2.388 0 4.32-1.932 4.32-4.32 0-2.388-1.932-4.32-4.32-4.32-1.696 0-3.168.984-3.88 2.424H2.178c.964-2.836 3.614-4.864 6.884-4.864 4.036 0 7.308 3.272 7.308 7.308 0 4.036-3.272 7.308-7.308 7.308z"/></svg>
          </a>
          <a href="mailto:your@email.com" class="social-btn" title="Email">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
          </a>
          <router-link to="/blog" class="social-btn" title="博客">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" /></svg>
          </router-link>
        </div>

        <!-- 回到顶部 -->
        <button @click="scrollToSection(0); isPhotoWallActive = false" class="back-to-top-btn group">
          <svg class="w-4 h-4 transition-transform group-hover:-translate-y-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
          </svg>
          <span class="font-mono text-xs">回到顶部</span>
        </button>

        <!-- 版权 -->
        <p class="mt-12 text-[11px] font-mono" style="color: var(--text-muted); opacity: 0.5;">
          &copy; {{ new Date().getFullYear() }} · Built with ❤️ and ☕
        </p>
      </div>
    </section>

    <!-- Lightbox 弹窗 -->
    <Teleport to="body">
      <Transition name="lightbox">
        <div v-if="lightboxPhoto" class="lightbox-overlay" @click.self="closeLightbox">
          <button class="lightbox-close" @click="closeLightbox">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
          <button class="lightbox-nav lightbox-prev" @click="lightboxPrev">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          </button>
          <div class="lightbox-content">
            <img :src="lightboxPhoto.url" :alt="lightboxPhoto.caption" class="lightbox-img" />
            <div class="lightbox-info">
              <span class="lightbox-caption">{{ lightboxPhoto.caption }}</span>
              <span class="lightbox-tag">{{ lightboxPhoto.tag }}</span>
            </div>
          </div>
          <button class="lightbox-nav lightbox-next" @click="lightboxNext">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </button>
        </div>
      </Transition>
    </Teleport>

    <!-- 照片管理弹窗 -->
    <Teleport to="body">
      <Transition name="lightbox">
        <div v-if="showPhotoModal" class="photo-modal-overlay" @click.self="showPhotoModal = false">
          <div class="photo-modal">
            <div class="photo-modal-header">
              <h3 class="text-lg font-bold font-mono" style="color: var(--text-primary);">
                {{ editingPhoto ? '编辑照片' : '添加照片' }}
              </h3>
              <button @click="showPhotoModal = false" class="photo-modal-close">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
            <div class="photo-modal-body">
              <!-- 图片上传/URL -->
              <div class="photo-form-group">
                <label class="photo-form-label">图片</label>
                <div class="flex items-center gap-3">
                  <label class="photo-upload-btn">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                    <span>选择文件</span>
                    <input type="file" accept="image/*" @change="onPhotoFileChange" class="hidden" />
                  </label>
                  <span v-if="photoFile" class="text-xs font-mono truncate" style="color: var(--text-secondary); max-width: 200px;">{{ photoFile.name }}</span>
                  <span v-else class="text-xs font-mono" style="color: var(--text-muted);">或填写URL</span>
                </div>
                <div v-if="photoPreview" class="mt-2">
                  <img :src="photoPreview" class="photo-preview-img" />
                </div>
                <input v-if="!photoFile" v-model="photoForm.url" type="text" placeholder="https://example.com/photo.jpg" class="photo-form-input mt-2" />
              </div>
              <!-- 描述 -->
              <div class="photo-form-group">
                <label class="photo-form-label">描述</label>
                <input v-model="photoForm.caption" type="text" placeholder="照片描述" class="photo-form-input" />
              </div>
              <!-- 标签 -->
              <div class="photo-form-group">
                <label class="photo-form-label">标签</label>
                <input v-model="photoForm.tag" type="text" placeholder="如：风景、美食、日常" class="photo-form-input" />
              </div>
              <!-- 尺寸 & 旋转 & 排序 -->
              <div class="grid grid-cols-3 gap-3">
                <div class="photo-form-group">
                  <label class="photo-form-label">尺寸</label>
                  <select v-model="photoForm.size" class="photo-form-input">
                    <option value="sm">小 (1×1)</option>
                    <option value="md">中 (2×1)</option>
                    <option value="tall">高 (1×2)</option>
                    <option value="lg">大 (2×2)</option>
                  </select>
                </div>
                <div class="photo-form-group">
                  <label class="photo-form-label">旋转°</label>
                  <input v-model="photoForm.rotate" type="number" step="0.1" class="photo-form-input" />
                </div>
                <div class="photo-form-group">
                  <label class="photo-form-label">排序</label>
                  <input v-model="photoForm.sort_order" type="number" class="photo-form-input" />
                </div>
              </div>
              <!-- 图片位置调整 -->
              <div class="photo-form-group" v-if="posPreviewUrl">
                <label class="photo-form-label">图片位置 <span style="opacity: 0.5; font-size: 10px;">（拖拽调整）</span></label>
                <div
                  class="pos-preview-container"
                  :style="{ aspectRatio: posPreviewAspect }"
                  @mousedown="onPosDragStart"
                  @touchstart="onPosDragStart"
                >
                  <img
                    :src="posPreviewUrl"
                    class="pos-preview-img"
                    :style="{
                      objectPosition: photoForm.position_x + '% ' + photoForm.position_y + '%',
                      transform: 'rotate(' + photoForm.rotate + 'deg)'
                    }"
                    draggable="false"
                  />
                  <div class="pos-crosshair"></div>
                </div>
                <div class="pos-controls">
                  <div class="pos-values">
                    <span class="pos-label">X: {{ photoForm.position_x }}%</span>
                    <span class="pos-label">Y: {{ photoForm.position_y }}%</span>
                  </div>
                  <button @click="resetPosition" class="pos-reset-btn" type="button">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                    居中
                  </button>
                </div>
              </div>
            </div>
            <div class="photo-modal-footer">
              <button @click="showPhotoModal = false" class="photo-btn-cancel">取消</button>
              <button @click="savePhoto" :disabled="photoSaving" class="photo-btn-save">
                {{ photoSaving ? '保存中...' : (editingPhoto ? '更新' : '添加') }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { getPortfolio, getTools, downloadTool, getAdminStatus, getPhotos, createPhoto, updatePhoto, deletePhoto } from '../composables/useApi'

// ============================================================
//  基础状态
// ============================================================
const isDark = ref(document.documentElement.classList.contains('dark'))
const skills = ['Python', 'JavaScript', 'Vue.js', 'Flask', 'SQL', 'Docker', 'Git', 'Linux', 'CI/CD']
const featuredPortfolio = ref([])
const popularTools = ref([])

// 首页工具分类预览（与 ToolsView 中的分类保持一致）
const homeToolCategories = [
  { key: '\u6D4B\u8BD5\u5DE5\u5177', name: '\u6D4B\u8BD5\u5DE5\u5177', count: 4, color: '#10b981', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>' },
  { key: '\u7F16\u7801\u8F6C\u6362', name: '\u7F16\u7801\u8F6C\u6362', count: 5, color: '#8b5cf6', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" /></svg>' },
  { key: '\u6570\u636E\u5904\u7406', name: '\u6570\u636E\u5904\u7406', count: 3, color: '#f97316', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7M4 7c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3M4 7c0-2 1.5-3 3.5-3h9c2 0 3.5 1 3.5 3" /></svg>' },
  { key: '\u5B89\u5168\u52A0\u5BC6', name: '\u5B89\u5168\u52A0\u5BC6', count: 2, color: '#ef4444', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>' },
  { key: '\u5B9E\u7528\u5DE5\u5177', name: '\u5B9E\u7528\u5DE5\u5177', count: 7, color: '#14b8a6', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>' },
]

// 鼠标
const mouseX = ref(window.innerWidth / 2)
const mouseY = ref(window.innerHeight / 2)
const mouseActive = ref(true)
const sectionMouseX = ref(0)
const sectionMouseY = ref(0)
const parallaxX = computed(() => ((mouseX.value / window.innerWidth) - 0.5) * 2)
const parallaxY = computed(() => ((mouseY.value / window.innerHeight) - 0.5) * 2)

// B4: 3D 透视倾斜（标题跟随鼠标轻微微倾斜）
const titleTiltX = computed(() => parallaxX.value * 3)   // 最大 ±3°
const titleTiltY = computed(() => parallaxY.value * -2)   // 最大 ±2°

// 滚动
const scrollContainer = ref(null)
const photoWallRef = ref(null)
const currentSection = ref(0)
const totalSections = 4
let isScrolling = false
const isPhotoWallActive = ref(false)

// ============================================================
//  照片墙数据
// ============================================================
const photos = ref([])

// 照片管理状态
const showPhotoModal = ref(false)
const editingPhoto = ref(null)
const photoForm = reactive({
  url: '',
  caption: '',
  tag: '',
  size: 'md',
  rotate: 0,
  position_x: 50,
  position_y: 50,
  sort_order: 0
})
const photoFile = ref(null)
const photoPreview = ref('')
const photoSaving = ref(false)
// 拖拽调整位置状态
const isDraggingPos = ref(false)
const posDragStart = { x: 0, y: 0, posX: 50, posY: 50 }

// 加载照片列表
async function loadPhotos() {
  try {
    photos.value = await getPhotos()
  } catch (e) {
    console.error('加载照片失败', e)
  }
}

// 打开添加照片弹窗
function openAddPhoto() {
  editingPhoto.value = null
  photoForm.url = ''
  photoForm.caption = ''
  photoForm.tag = ''
  photoForm.size = 'md'
  photoForm.rotate = 0
  photoForm.position_x = 50
  photoForm.position_y = 50
  photoForm.sort_order = photos.value.length
  photoFile.value = null
  photoPreview.value = ''
  showPhotoModal.value = true
}

// 打开编辑照片弹窗
function openEditPhoto(photo) {
  editingPhoto.value = photo
  photoForm.url = photo.url
  photoForm.caption = photo.caption || ''
  photoForm.tag = photo.tag || ''
  photoForm.size = photo.size || 'md'
  photoForm.rotate = photo.rotate || 0
  photoForm.position_x = photo.position_x ?? 50
  photoForm.position_y = photo.position_y ?? 50
  photoForm.sort_order = photo.sort_order || 0
  photoFile.value = null
  photoPreview.value = ''
  showPhotoModal.value = true
}

// 选择照片文件
function onPhotoFileChange(e) {
  const file = e.target.files[0]
  if (!file) return
  photoFile.value = file
  photoPreview.value = URL.createObjectURL(file)
}

// 保存照片（创建/更新）
async function savePhoto() {
  if (photoSaving.value) return
  photoSaving.value = true
  try {
    if (photoFile.value) {
      // 文件上传模式
      const formData = new FormData()
      formData.append('file', photoFile.value)
      formData.append('caption', photoForm.caption)
      formData.append('tag', photoForm.tag)
      formData.append('size', photoForm.size)
      formData.append('rotate', photoForm.rotate)
      formData.append('position_x', photoForm.position_x)
      formData.append('position_y', photoForm.position_y)
      formData.append('sort_order', photoForm.sort_order)
      if (editingPhoto.value) {
        await updatePhoto(editingPhoto.value.id, formData)
      } else {
        await createPhoto(formData)
      }
    } else {
      // JSON 模式
      const data = {
        url: photoForm.url,
        caption: photoForm.caption,
        tag: photoForm.tag,
        size: photoForm.size,
        rotate: parseFloat(photoForm.rotate) || 0,
        position_x: parseFloat(photoForm.position_x) || 50,
        position_y: parseFloat(photoForm.position_y) || 50,
        sort_order: parseInt(photoForm.sort_order) || 0
      }
      if (!data.url) {
        alert('请上传图片或填写图片 URL')
        photoSaving.value = false
        return
      }
      if (editingPhoto.value) {
        await updatePhoto(editingPhoto.value.id, data)
      } else {
        await createPhoto(data)
      }
    }
    showPhotoModal.value = false
    await loadPhotos()
  } catch (e) {
    alert('保存失败：' + (e.response?.data?.error || e.message))
  } finally {
    photoSaving.value = false
  }
}

// 位置调整：获取预览容器的尺寸比例（与实际网格卡片比例一致）
const posPreviewAspect = computed(() => {
  switch (photoForm.size) {
    case 'sm': return '1 / 1'
    case 'md': return '2.5 / 1'
    case 'tall': return '1 / 1.7'
    case 'lg': return '1.3 / 1'
    default: return '2 / 1'
  }
})

// 位置调整：获取当前预览图片 URL
const posPreviewUrl = computed(() => {
  if (photoPreview.value) return photoPreview.value
  if (photoForm.url) return photoForm.url
  return ''
})

// 位置调整：拖拽开始
function onPosDragStart(e) {
  if (!posPreviewUrl.value) return
  isDraggingPos.value = true
  const rect = e.currentTarget.getBoundingClientRect()
  posDragStart.x = (e.touches ? e.touches[0].clientX : e.clientX)
  posDragStart.y = (e.touches ? e.touches[0].clientY : e.clientY)
  posDragStart.posX = photoForm.position_x
  posDragStart.posY = photoForm.position_y
  e.preventDefault()
}

// 位置调整：拖拽中
function onPosDragMove(e) {
  if (!isDraggingPos.value) return
  const container = document.querySelector('.pos-preview-container')
  if (!container) return
  const rect = container.getBoundingClientRect()
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  const dx = clientX - posDragStart.x
  const dy = clientY - posDragStart.y
  // 将像素偏移转换为百分比偏移（相对于容器尺寸）
  const newX = posDragStart.posX - (dx / rect.width) * 100
  const newY = posDragStart.posY - (dy / rect.height) * 100
  photoForm.position_x = Math.round(Math.max(0, Math.min(100, newX)) * 10) / 10
  photoForm.position_y = Math.round(Math.max(0, Math.min(100, newY)) * 10) / 10
}

// 位置调整：拖拽结束
function onPosDragEnd() {
  isDraggingPos.value = false
}

// 位置调整：重置居中
function resetPosition() {
  photoForm.position_x = 50
  photoForm.position_y = 50
}

// 删除照片
async function handleDeletePhoto(photo) {
  if (!confirm(`确定删除照片「${photo.caption || '未命名'}」吗？`)) return
  try {
    await deletePhoto(photo.id)
    await loadPhotos()
  } catch (e) {
    alert('删除失败：' + (e.response?.data?.error || e.message))
  }
}

// Lightbox
const lightboxPhoto = ref(null)
const openLightbox = (photo) => { lightboxPhoto.value = photo }
const closeLightbox = () => { lightboxPhoto.value = null }
const lightboxPrev = () => {
  if (!lightboxPhoto.value) return
  const list = photos.value
  const idx = list.findIndex(p => p.id === lightboxPhoto.value.id)
  lightboxPhoto.value = list[(idx - 1 + list.length) % list.length]
}
const lightboxNext = () => {
  if (!lightboxPhoto.value) return
  const list = photos.value
  const idx = list.findIndex(p => p.id === lightboxPhoto.value.id)
  lightboxPhoto.value = list[(idx + 1) % list.length]
}

// 打字机
const fullText = 'Welcome to My Nexus'
const displayText = ref('')
const currentRole = ref('Full-Stack Developer')
const displayedRole = ref('Full-Stack Developer')
let roleScrambling = false
let charIndex = 0
let typewriterTimer = null
const roles = [
  '用代码构建数字世界的工程师',
  '把复杂问题变简单的产品思维',
  '在 0 和 1 之间寻找诗意的创作者',
  '持续学习，永远好奇的技术探索者',
  'Full-Stack Developer & Creative Coder',
  '热爱开源，拥抱变化的终身学习者',
  'Bug 是成长路上最好的老师',
  '用键盘书写逻辑，用代码表达思想',
  '从 Hello World 到改变世界',
  '代码是最好的简历，开源是最好的证明',
  'Console.log 是我最好的调试伙伴',
  '不只是写代码，更是解决问题',
  '在终端里寻找星辰大海',
  'Life is short, I use Python',
  'Git commit --amend 是人生常态',
  '程序员的浪漫是写一个 for 循环等你',
  '用像素和代码编织数字梦境',
  '代码如诗，架构如画',
  'There is no place like 127.0.0.1',
  '在 Stack Overflow 和咖啡之间找到平衡',
  '今天也要加油写代码鸭 (🦆)',
  'Talk is cheap, let me show you my portfolio',
  '左手 Vue，右手 Flask，全栈无畏',
  'I don\'t sleep, I just reload',
  '用 API 连接世界，用逻辑定义未来',
  'Ctrl+S 是世界上最安心的组合键',
  '一边修 Bug，一边写新 Bug 的勇士',
  '努力成为一个有温度的工程师',
  '代码改变生活，技术驱动创新',
  '在键盘上敲出属于自己的篇章',
  '404 not found, but passion always found',
  '每个项目都是一次新的冒险',
  '写代码是一门手艺，也是一种态度',
  'Debug 时的我：这不可能 → 找到了',
  '信仰开源，敬畏每一行代码',
  '从需求到上线，每一步都值得尊重'
]
let roleIndex = 0

// ============================================================
//  粒子文字动画系统
// ============================================================
const particleCanvas = ref(null)
const showParticleCanvas = ref(false)

// 颜文字定义（纯 ASCII 字符，确保 Canvas 可渲染 + 动画类型）
const KAOMOJIS = [
  { text: '(^_^)',    size: 96, anim: 'blink_bounce'  },
  { text: '(T_T)',    size: 96, anim: 'shake'         },
  { text: '(O_O)',    size: 96, anim: 'shrug'         },
  { text: '(>_<)',    size: 96, anim: 'sway'          },
  { text: '(^o^)',    size: 96, anim: 'wiggle'        },
  { text: '(-_-)',    size: 96, anim: 'celebrate'     },
  { text: '(*_*)',    size: 96, anim: 'shifty'        },
  { text: '(._. )',   size: 96, anim: 'excite'        },
  { text: '(>w<)',    size: 96, anim: 'heart'         },
  { text: '=^.^=',    size: 88, anim: 'sparkle'       },
]

const PTCL_COUNT = 480           // 粒子数量（更多更细腻）
const PTCL_PHASE_DUR = {         // 各阶段时长 (ms)
  textToScatter:   1200,
  scatterPause:     400,
  toKaomoji:      1000,          // 聚合更快
  kaomojiAnim:    2800,
  kaomojiScatter:  800,
  toText:          900,          // 回归更快
}

let textParticles = []           // 粒子数组
let ptclPhase = 'idle'           // 当前阶段
let ptclPhaseStart = 0           // 阶段起始时间
let ptclKaomojiDef = null        // 当前颜文字定义
let ptclTextPos = []             // 文字采样位置
let ptclKaomojiPos = []          // 颜文字采样位置
let ptclAnimFrame = null

// —— 采样文字像素位置 ——
function sampleTextPositions(text, fontSize, targetCount, fontFamily, centerY) {
  const off = document.createElement('canvas')
  const ctx = off.getContext('2d')
  const w = window.innerWidth, h = window.innerHeight
  off.width = w; off.height = h
  const ff = fontFamily || "'Courier New', monospace"
  ctx.font = `bold ${fontSize}px ${ff}`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillStyle = '#fff'
  const cy = centerY != null ? centerY : h / 2
  ctx.fillText(text, w / 2, cy)
  const imgData = ctx.getImageData(0, 0, w, h)
  const positions = []
  const step = 3   // 小步长确保精确采样文字形状
  for (let y = 0; y < h; y += step) {
    for (let x = 0; x < w; x += step) {
      if (imgData.data[(y * w + x) * 4 + 3] > 128) positions.push({ x, y })
    }
  }
  // 子采样到目标数量
  if (positions.length > targetCount) {
    const res = [], ratio = positions.length / targetCount
    for (let i = 0; i < targetCount; i++) res.push(positions[Math.floor(i * ratio)])
    return res
  }
  // 不够则复制并加随机偏移
  while (positions.length < targetCount) {
    const b = positions[Math.floor(Math.random() * positions.length)]
    positions.push({ x: b.x + (Math.random() - 0.5) * 4, y: b.y + (Math.random() - 0.5) * 4 })
  }
  return positions
}

// —— 创建/更新粒子数组 ——
function buildParticles(positions) {
  return positions.map((pos, i) => {
    const ex = textParticles[i]
    if (ex) { ex.targetX = pos.x; ex.targetY = pos.y; return ex }
    return {
      x: pos.x + (Math.random() - 0.5) * 20, y: pos.y + (Math.random() - 0.5) * 20,
      targetX: pos.x, targetY: pos.y,
      startX: 0, startY: 0,
      scatterX: 0, scatterY: 0,
      size: Math.random() * 1.2 + 0.8, alpha: 1,
      hue: (pos.x / window.innerWidth) * 160 + 170,   // 青 → 紫 → 粉
    }
  })
}

// —— 启动粒子动画循环 ——
function startParticleCycle() {
  if (ptclPhase !== 'idle') return
  const heroTitle = document.querySelector('.hero-title')
  if (!heroTitle) return
  const fs = parseInt(window.getComputedStyle(heroTitle).fontSize) || 64
  // 获取实际文字在屏幕上的位置，确保粒子位置与文字一致
  const rect = heroTitle.getBoundingClientRect()
  const textCenterY = rect.top + rect.height / 2
  ptclTextPos = sampleTextPositions('Welcome to My Nexus', fs, PTCL_COUNT, null, textCenterY)
  ptclKaomojiDef = KAOMOJIS[Math.floor(Math.random() * KAOMOJIS.length)]
  ptclKaomojiPos = sampleTextPositions(ptclKaomojiDef.text, ptclKaomojiDef.size, PTCL_COUNT, null, textCenterY)
  textParticles = buildParticles(ptclTextPos)
  textParticles.forEach(p => { p.startX = p.x; p.startY = p.y })
  idleAnimating.value = true
  showParticleCanvas.value = true
  ptclPhase = 'textToScatter'
  ptclPhaseStart = performance.now()
  if (ptclAnimFrame) cancelAnimationFrame(ptclAnimFrame)
  ptclAnimFrame = requestAnimationFrame(ptclLoop)
}

// —— 缓动函数 ——
function _easeOut(t)  { return 1 - Math.pow(1 - t, 3) }
function _easeInOut(t){ return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2 }

// —— 主动画循环 ——
function ptclLoop(ts) {
  const elapsed = ts - ptclPhaseStart
  const cvs = particleCanvas.value
  if (!cvs) return
  if (cvs.width !== window.innerWidth || cvs.height !== window.innerHeight) {
    cvs.width = window.innerWidth; cvs.height = window.innerHeight
  }
  const ctx = cvs.getContext('2d')
  ctx.clearRect(0, 0, cvs.width, cvs.height)
  const w = cvs.width, h = cvs.height

  switch (ptclPhase) {
    case 'textToScatter': {
      const p = Math.min(elapsed / PTCL_PHASE_DUR.textToScatter, 1)
      const t = _easeOut(p)
      textParticles.forEach(pt => {
        if (!pt._scInit) { pt.scatterX = (Math.random()-0.5)*w*0.35+w/2; pt.scatterY = (Math.random()-0.5)*h*0.25+h/2; pt._scInit = true }
        pt.x = pt.startX + (pt.scatterX - pt.startX) * t
        pt.y = pt.startY + (pt.scatterY - pt.startY) * t
      })
      if (p >= 1) { ptclPhase = 'scatterPause'; ptclPhaseStart = ts }
      break
    }
    case 'scatterPause': {
      textParticles.forEach(pt => { pt.x += (Math.random()-0.5)*2; pt.y += (Math.random()-0.5)*2 })
      if (elapsed >= PTCL_PHASE_DUR.scatterPause) {
        textParticles.forEach((pt, i) => { pt.startX = pt.x; pt.startY = pt.y; pt.targetX = ptclKaomojiPos[i].x; pt.targetY = ptclKaomojiPos[i].y })
        ptclPhase = 'toKaomoji'; ptclPhaseStart = ts
      }
      break
    }
    case 'toKaomoji': {
      const p = Math.min(elapsed / PTCL_PHASE_DUR.toKaomoji, 1)
      const t = _easeInOut(p)
      textParticles.forEach(pt => { pt.x = pt.startX + (pt.targetX - pt.startX)*t; pt.y = pt.startY + (pt.targetY - pt.startY)*t })
      if (p >= 1) { ptclPhase = 'kaomojiAnim'; ptclPhaseStart = ts }
      break
    }
    case 'kaomojiAnim': {
      const p = Math.min(elapsed / PTCL_PHASE_DUR.kaomojiAnim, 1)
      const sec = elapsed / 1000
      textParticles.forEach((pt, i) => {
        const o = _kaomojiOffset(pt, i, sec, ptclKaomojiDef.anim)
        pt.x = pt.targetX + o.x; pt.y = pt.targetY + o.y
        pt.alpha = 1 + (o.am || 0)
        pt.size = (Math.random()*1.2+0.8) * (o.sm || 1)
      })
      if (p >= 1) {
        textParticles.forEach(pt => { pt.size = Math.random()*1.2+0.8; pt.startX = pt.x; pt.startY = pt.y; pt._scInit = false })
        ptclPhase = 'kaomojiScatter'; ptclPhaseStart = ts
      }
      break
    }
    case 'kaomojiScatter': {
      const p = Math.min(elapsed / PTCL_PHASE_DUR.kaomojiScatter, 1)
      const t = _easeOut(p)
      textParticles.forEach(pt => {
        if (!pt._scInit) { pt.scatterX = (Math.random()-0.5)*w*0.35+w/2; pt.scatterY = (Math.random()-0.5)*h*0.25+h/2; pt._scInit = true }
        pt.x = pt.startX + (pt.scatterX - pt.startX)*t
        pt.y = pt.startY + (pt.scatterY - pt.startY)*t
      })
      if (p >= 1) {
        textParticles.forEach((pt, i) => { pt.startX = pt.x; pt.startY = pt.y; pt.targetX = ptclTextPos[i].x; pt.targetY = ptclTextPos[i].y })
        ptclPhase = 'toText'; ptclPhaseStart = ts
      }
      break
    }
    case 'toText': {
      const p = Math.min(elapsed / PTCL_PHASE_DUR.toText, 1)
      const t = _easeInOut(p)
      textParticles.forEach(pt => { pt.x = pt.startX + (pt.targetX - pt.startX)*t; pt.y = pt.startY + (pt.targetY - pt.startY)*t })
      if (p >= 1) {
        showParticleCanvas.value = false
        ptclPhase = 'idle'; textParticles = []
        idleAnimating.value = false
        if (ptclAnimFrame) { cancelAnimationFrame(ptclAnimFrame); ptclAnimFrame = null }
        scheduleIdle()
        return
      }
      break
    }
  }
  // 绘制粒子
  _drawPtcls(ctx, w, h)
  ptclAnimFrame = requestAnimationFrame(ptclLoop)
}

// —— 绘制粒子 ——
function _drawPtcls(ctx, w, h) {
  const dark = isDark.value
  const base = dark ? [0, 243, 255] : [3, 105, 161]
  const purp = dark ? [182, 112, 255] : [109, 40, 217]
  textParticles.forEach(p => {
    const t = Math.max(0, Math.min(1, p.x / w))
    const r = Math.round(base[0]*(1-t) + purp[0]*t)
    const g = Math.round(base[1]*(1-t) + purp[1]*t)
    const b = Math.round(base[2]*(1-t) + purp[2]*t)
    const a = Math.max(0, Math.min(1, p.alpha))
    ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2)
    ctx.fillStyle = `rgba(${r},${g},${b},${a})`; ctx.fill()
    ctx.beginPath(); ctx.arc(p.x, p.y, p.size*1.8, 0, Math.PI*2)
    ctx.fillStyle = `rgba(${r},${g},${b},${a*0.06})`; ctx.fill()
  })
}

// —— 颜文字专属动画偏移 ——
function _kaomojiOffset(pt, idx, t, anim) {
  const o = { x:0, y:0, am:0, sm:1 }
  const p = t * 2.5   // 速度倍率
  const w = window.innerWidth
  const h = window.innerHeight
  const cx = w / 2
  switch (anim) {
    case 'blink_bounce': {
      // 整体上下弹跳 + 周期性眨眼（上下两半粒子分离模拟闭眼）
      o.y = Math.sin(p*2)*12
      const blink = Math.sin(p*3)
      if (blink > 0.8) {
        // 眨眼：上半部分粒子下移，下半部分上移，模拟眼睛闭合
        const cy = h * 0.4
        if (pt.targetY < cy) o.y += 15
        else o.y -= 15
        o.sm = 0.4
      }
      break
    }
    case 'shake': {
      // 暴走摇晃：幅度大，带随机抖动
      const rage = Math.sin(p*0.8)*0.5+0.5
      o.x = Math.sin(p*18)*8*rage + (Math.random()-0.5)*4
      o.y = Math.cos(p*14)*5*rage + (Math.random()-0.5)*3
      break
    }
    case 'shrug': {
      // 耸肩：左右两侧粒子向上抬
      const nd = Math.min(Math.abs(pt.targetX - cx) / (cx*0.5), 1)
      o.y = -Math.sin(p*1.8)*28*nd
      o.x = Math.sin(p*1.2)*5*nd
      break
    }
    case 'sway': {
      // 左右摇摆：像钟摆一样
      o.x = Math.sin(p*1.8)*18
      o.y = Math.cos(p*2.5)*6 + Math.sin(p*1)*4
      break
    }
    case 'wiggle': {
      // 全身扭动：每个粒子独立运动
      o.x = Math.sin(p*5+idx*0.12)*10
      o.y = Math.cos(p*4+idx*0.18)*8
      o.sm = 1+Math.sin(p*3+idx*0.2)*0.3
      break
    }
    case 'celebrate': {
      // 欢呼跳跃：上下大幅跳动 + 放大
      o.y = -Math.abs(Math.sin(p*2.5))*25
      o.x = Math.sin(p*3)*8
      o.sm = 1+Math.abs(Math.sin(p*2))*0.4
      break
    }
    case 'shifty': {
      // 眼神飘移：左右平移 + 微微上下
      o.x = Math.sin(p*2.5)*16 + Math.sin(p*0.7)*6
      o.y = Math.cos(p*1.8)*5
      // 偶尔快速回弹
      if (Math.sin(p*0.4) > 0.9) o.x *= -1.5
      break
    }
    case 'excite': {
      // 兴奋跳动：大幅上下 + 左右摆动
      o.y = -Math.abs(Math.sin(p*3))*28
      o.x = Math.sin(p*4)*10
      o.sm = 1+Math.sin(p*4)*0.25
      break
    }
    case 'heart': {
      // 心跳脉冲：整体膨胀收缩 + 发光
      const pulse = Math.sin(p*2.5)*0.5+0.5
      o.sm = 1+pulse*0.8
      o.am = pulse*0.4
      o.y = -pulse*8
      break
    }
    case 'sparkle': {
      // 闪烁：随机粒子变大发光 + 微浮动
      if (Math.random()<0.08) { o.sm=3.5; o.am=0.6 }
      o.y = Math.sin(p*2+idx*0.06)*5
      o.x = Math.cos(p*1.5+idx*0.04)*3
      break
    }
  }
  return o
}

// ============================================================
//  A1: 星空连线网络（Canvas）
// ============================================================
const constellationCanvas = ref(null)
const CONSTELLATION_COUNT = 100
const CONSTELLATION_LINK_DIST = 140
const CONSTELLATION_MOUSE_DIST = 200
let constellationParticles = []

function initConstellation() {
  const w = window.innerWidth
  const h = window.innerHeight
  constellationParticles = []
  for (let i = 0; i < CONSTELLATION_COUNT; i++) {
    constellationParticles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      r: Math.random() * 1.5 + 0.5
    })
  }
}

function drawConstellation() {
  const canvas = constellationCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w = canvas.width
  const h = canvas.height

  ctx.clearRect(0, 0, w, h)

  // 颜色
  const dotColor = isDark.value ? 'rgba(0, 243, 255, 0.6)' : 'rgba(3, 105, 161, 0.5)'
  const lineColorBase = isDark.value ? [0, 243, 255] : [3, 105, 161]
  const purpleBase = isDark.value ? [182, 112, 255] : [109, 40, 217]

  // 更新粒子位置
  constellationParticles.forEach(p => {
    // 鼠标排斥
    if (mouseActive.value) {
      const dx = p.x - mouseX.value
      const dy = p.y - mouseY.value
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < CONSTELLATION_MOUSE_DIST && dist > 0) {
        const force = (1 - dist / CONSTELLATION_MOUSE_DIST) * 0.8
        p.vx += (dx / dist) * force
        p.vy += (dy / dist) * force
      }
    }

    // 速度衰减
    p.vx *= 0.98
    p.vy *= 0.98

    // 最小速度（保持漂浮）
    const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy)
    if (speed < 0.15) {
      p.vx += (Math.random() - 0.5) * 0.1
      p.vy += (Math.random() - 0.5) * 0.1
    }

    p.x += p.vx
    p.y += p.vy

    // 边界循环
    if (p.x < -10) p.x = w + 10
    if (p.x > w + 10) p.x = -10
    if (p.y < -10) p.y = h + 10
    if (p.y > h + 10) p.y = -10
  })

  // 绘制连线
  for (let i = 0; i < constellationParticles.length; i++) {
    for (let j = i + 1; j < constellationParticles.length; j++) {
      const a = constellationParticles[i]
      const b = constellationParticles[j]
      const dx = a.x - b.x
      const dy = a.y - b.y
      const dist = Math.sqrt(dx * dx + dy * dy)

      if (dist < CONSTELLATION_LINK_DIST) {
        let alpha = (1 - dist / CONSTELLATION_LINK_DIST) * 0.35

        // 鼠标附近的线更亮
        if (mouseActive.value) {
          const midX = (a.x + b.x) / 2
          const midY = (a.y + b.y) / 2
          const mDist = Math.sqrt((midX - mouseX.value) ** 2 + (midY - mouseY.value) ** 2)
          if (mDist < CONSTELLATION_MOUSE_DIST) {
            alpha += (1 - mDist / CONSTELLATION_MOUSE_DIST) * 0.4
          }
        }

        // 颜色：根据位置混合蓝色和紫色
        const t = (a.x + b.x) / (2 * w)
        const r = Math.round(lineColorBase[0] * (1 - t) + purpleBase[0] * t)
        const g = Math.round(lineColorBase[1] * (1 - t) + purpleBase[1] * t)
        const bl = Math.round(lineColorBase[2] * (1 - t) + purpleBase[2] * t)

        ctx.beginPath()
        ctx.moveTo(a.x, a.y)
        ctx.lineTo(b.x, b.y)
        ctx.strokeStyle = `rgba(${r}, ${g}, ${bl}, ${Math.min(alpha, 0.7)})`
        ctx.lineWidth = alpha > 0.4 ? 1.2 : 0.6
        ctx.stroke()
      }
    }
  }

  // 绘制粒子
  constellationParticles.forEach(p => {
    let alpha = 0.5
    if (mouseActive.value) {
      const dist = Math.sqrt((p.x - mouseX.value) ** 2 + (p.y - mouseY.value) ** 2)
      if (dist < CONSTELLATION_MOUSE_DIST) {
        alpha += (1 - dist / CONSTELLATION_MOUSE_DIST) * 0.5
      }
    }
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
    ctx.fillStyle = dotColor.replace(/[\d.]+\)$/, `${Math.min(alpha, 1)})`)
    ctx.fill()
  })
}

// ============================================================
//  B4: 字符交互系统（3D倾斜 + 霓虹发光）
// ============================================================
const INTERACT_RADIUS = 300 // 交互半径
const IDLE_INTERVAL = 8000  // 空闲间隔 8 秒

const displayChars = ref([])

function makeCharObj(ch) {
  return {
    char: ch,
    displayChar: ch,
    glow: 0,
    offsetX: 0,
    offsetY: 0,
    opacity: 1,
    animColor: null,
    animating: false
  }
}

function updateDisplayChars() {
  const text = displayText.value
  const newChars = []
  for (let i = 0; i < text.length; i++) {
    const existing = displayChars.value[i]
    if (existing && existing.char === text[i]) {
      newChars.push(existing)
    } else {
      newChars.push(makeCharObj(text[i]))
    }
  }
  displayChars.value = newChars
}

watch(displayText, updateDisplayChars)

function updateCharInteraction() {
  // 动画播放中跳过鼠标交互
  if (idleAnimating.value) return

  const titleEl = document.querySelector('.hero-title')
  if (!titleEl) return
  const chars = titleEl.querySelectorAll('.hero-char')
  if (!chars.length) return

  const mx = mouseX.value
  const my = mouseY.value

  chars.forEach((el, idx) => {
    if (idx >= displayChars.value.length) return
    const c = displayChars.value[idx]
    const rect = el.getBoundingClientRect()
    const cx = rect.left + rect.width / 2
    const cy = rect.top + rect.height / 2

    const dx = cx - mx
    const dy = cy - my
    const dist = Math.sqrt(dx * dx + dy * dy)

    if (mouseActive.value && dist < INTERACT_RADIUS && dist > 0) {
      const strength = 1 - dist / INTERACT_RADIUS
      const sq = strength * strength
      c.glow = sq * 1.0
    } else {
      c.glow *= 0.88
    }
  })
}

// ============================================================
//  赛博朋克空闲文字动画系统
// ============================================================
const idleAnimating = ref(false)
let idleTimer = null
let animTimers = []
let cyberAnimFrame = null

// 赛博朋克字符集（仅ASCII单宽度字符，避免撑开布局）
const CYBER_GLITCH = '!@#$%^&*<>{}[]|/\\~`'
const CYBER_ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
const CYBER_ALL = CYBER_GLITCH + CYBER_ALPHA

function _randCyber() {
  return CYBER_ALL[Math.floor(Math.random() * CYBER_ALL.length)]
}

function _neonC() {
  return isDark.value
    ? { cyan: '#00f3ff', pink: '#ff2d75', purple: '#b670ff', green: '#39ff14' }
    : { cyan: '#0369a1', pink: '#be185d', purple: '#6d28d9', green: '#047857' }
}

function clearAnimTimers() {
  animTimers.forEach(t => {
    if (typeof t === 'object' && t.cancel) t.cancel()
    else clearTimeout(t)
  })
  animTimers = []
  if (cyberAnimFrame) { cancelAnimationFrame(cyberAnimFrame); cyberAnimFrame = null }
}

function resetAllChars() {
  displayChars.value.forEach(c => {
    c.displayChar = c.char
    c.offsetX = 0
    c.offsetY = 0
    c.opacity = 1
    c.animColor = null
    c.animating = false
    c.glow = 0
  })
}

function scheduleIdle() {
  clearTimeout(idleTimer)
  const nextInterval = 8000 + Math.random() * 4000 // 8~12秒随机间隔
  idleTimer = setTimeout(() => {
    if (currentSection.value !== 0) {
      scheduleIdle()
      return
    }
    const effects = [effectCyberShatter, effectGlitchScan, effectDigitalDecay, effectMosaicBreach, startParticleCycle]
    const picked = effects[Math.floor(Math.random() * effects.length)]
    const prevPhase = ptclPhase
    picked()
    // 如果粒子动画未能启动（静默返回），重新调度下一次
    if (picked === startParticleCycle && ptclPhase === prevPhase && prevPhase === 'idle') {
      scheduleIdle()
    }
  }, nextInterval)
}

// --- 辅助: 设置单个字符为赛博乱码风格 ---
function _setCyber(c, nc) {
  c.displayChar = _randCyber()
  c.animating = true
  c.glow = 0.5 + Math.random() * 0.5
  const picks = [nc.cyan, nc.pink, nc.purple, nc.green]
  c.animColor = picks[Math.floor(Math.random() * picks.length)]
}

// --- 辅助: 恢复单个字符 ---
function _restoreChar(c) {
  c.displayChar = c.char; c.offsetX = 0; c.offsetY = 0
  c.opacity = 1; c.animColor = null; c.animating = false; c.glow = 0
}

// --- 辅助: 生成乱码/恢复顺序 ---
function _corruptOrder(len, mode) {
  const idx = Array.from({ length: len }, (_, i) => i)
  if (mode === 'left') return idx
  if (mode === 'right') return idx.reverse()
  for (let i = idx.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));[idx[i], idx[j]] = [idx[j], idx[i]]
  }
  return idx
}

// ========== C1: 赛博破碎 ==========
// 乱码方向: 左→右 | 特效: 粒子散射 + 颜色闪烁 | 恢复方向: 右→左
function effectCyberShatter() {
  idleAnimating.value = true
  const chars = displayChars.value
  const len = chars.length
  const nc = _neonC()

  // Phase 1: 左→右逐字变乱码
  const cOrd = _corruptOrder(len, 'left')
  cOrd.forEach((idx, i) => {
    animTimers.push(setTimeout(() => {
      _setCyber(chars[idx], nc)
      if (i === cOrd.length - 1) doShatter()
    }, i * 35))
  })

  function doShatter() {
    chars.forEach(c => {
      c._ox = (Math.random() - 0.5) * 280
      c._oy = (Math.random() - 0.5) * 180
      c._op = Math.random() * 0.3 + 0.15
    })
    const dur = 1600, start = performance.now()
    function loop(ts) {
      const p = Math.min((ts - start) / dur, 1)
      const ep = p < 0.5 ? 4*p*p*p : 1 - Math.pow(-2*p+2, 3)/2
      chars.forEach((c, i) => {
        c.displayChar = _randCyber()
        c.offsetX = c._ox * ep; c.offsetY = c._oy * ep
        c.opacity = 1 - (1 - c._op) * ep
        c.glow = 0.6 + Math.sin(ts * 0.008 + i) * 0.4
        if (Math.random() < 0.08) _setCyber(c, nc)
      })
      if (p < 1) { cyberAnimFrame = requestAnimationFrame(loop) } else { doRestoreShatter() }
    }
    cyberAnimFrame = requestAnimationFrame(loop)
  }

  function doRestoreShatter() {
    const rOrd = _corruptOrder(len, 'right')
    rOrd.forEach((idx, i) => {
      const base = i * 50
      const cycles = 2 + Math.floor(Math.random() * 3)
      for (let j = 0; j < cycles; j++) {
        animTimers.push(setTimeout(() => {
          chars[idx].displayChar = _randCyber()
          chars[idx].offsetX *= 0.4; chars[idx].offsetY *= 0.4
          chars[idx].opacity = Math.min(1, chars[idx].opacity + 0.2)
        }, base + j * 35))
      }
      animTimers.push(setTimeout(() => {
        _restoreChar(chars[idx])
        if (i === rOrd.length - 1) { resetAllChars(); idleAnimating.value = false; scheduleIdle() }
      }, base + cycles * 35))
    })
  }
}

// ========== C2: 扫描失真 ==========
// 乱码方向: 随机 | 特效: 水平扫描线 + RGB分离 + 随机抖动 | 恢复方向: 随机
function effectGlitchScan() {
  idleAnimating.value = true
  const chars = displayChars.value
  const len = chars.length
  const nc = _neonC()

  // Phase 1: 随机顺序逐个变乱码
  const cOrd = _corruptOrder(len, 'random')
  cOrd.forEach((idx, i) => {
    animTimers.push(setTimeout(() => {
      _setCyber(chars[idx], nc)
      if (i === cOrd.length - 1) doScan()
    }, i * 55))
  })

  function doScan() {
    const dur = 2200, start = performance.now()
    function loop(ts) {
      const el = ts - start, p = Math.min(el / dur, 1)
      const scanY = (el / 400) % 1
      chars.forEach((c, i) => {
        if (Math.random() < 0.3) c.displayChar = _randCyber()
        const cp = i / len, dist = Math.abs(cp - scanY)
        const si = Math.max(0, 1 - dist * 5)
        c.offsetX = si * (Math.random() - 0.5) * 16 + Math.sin(el * 0.01 + i * 0.7) * 2
        c.offsetY = si * (Math.random() - 0.5) * 8 + Math.cos(el * 0.008 + i * 0.5) * 1.5
        c.glow = 0.4 + si * 0.6 + Math.sin(el * 0.005 + i * 0.3) * 0.2
        c.opacity = 0.7 + Math.random() * 0.3 - si * 0.3
        if (Math.random() < 0.04) _setCyber(c, nc)
      })
      if (p < 1) { cyberAnimFrame = requestAnimationFrame(loop) } else { doRestoreScan() }
    }
    cyberAnimFrame = requestAnimationFrame(loop)
  }

  function doRestoreScan() {
    const rOrd = _corruptOrder(len, 'random')
    rOrd.forEach((idx, i) => {
      const cycles = 3 + Math.floor(Math.random() * 3)
      for (let j = 0; j < cycles; j++) {
        animTimers.push(setTimeout(() => {
          chars[idx].displayChar = _randCyber()
          chars[idx].offsetX = (Math.random() - 0.5) * 6; chars[idx].offsetY = (Math.random() - 0.5) * 3
        }, i * 40 + j * 25))
      }
      animTimers.push(setTimeout(() => {
        _restoreChar(chars[idx])
        if (i === rOrd.length - 1) { resetAllChars(); idleAnimating.value = false; scheduleIdle() }
      }, i * 40 + cycles * 25))
    })
  }
}

// ========== C3: 数字崩坏 ==========
// 乱码方向: 右→左 | 特效: 闪烁/呼吸/失真脉冲 | 恢复方向: 左→右
function effectDigitalDecay() {
  idleAnimating.value = true
  const chars = displayChars.value
  const len = chars.length
  const nc = _neonC()

  // Phase 1: 右→左逐字变乱码
  const cOrd = _corruptOrder(len, 'right')
  cOrd.forEach((idx, i) => {
    animTimers.push(setTimeout(() => {
      _setCyber(chars[idx], nc)
      if (i === cOrd.length - 1) doDecay()
    }, i * 35))
  })

  function doDecay() {
    const dur = 2000, start = performance.now()
    function loop(ts) {
      const el = ts - start, p = Math.min(el / dur, 1)
      chars.forEach((c, i) => {
        if (Math.random() < 0.2) c.displayChar = _randCyber()
        c.opacity = (Math.random() < 0.08 ? 0.15 + Math.random() * 0.2 : 1)
          * (0.7 + Math.sin(el * 0.003 + i * 0.4) * 0.3)
        c.offsetY = Math.sin(el * 0.004 + i * 0.6) * 4
          + (Math.random() < 0.05 ? (Math.random() - 0.5) * 20 : 0)
        c.offsetX = Math.sin(el * 0.006 + i * 0.8) * 2
          + (Math.random() < 0.04 ? (Math.random() - 0.5) * 14 : 0)
        c.glow = 0.3 + Math.abs(Math.sin(el * 0.005 + i * 0.5)) * 0.7
        if (Math.random() < 0.03) _setCyber(c, nc)
      })
      if (p < 1) { cyberAnimFrame = requestAnimationFrame(loop) } else { doRestoreDecay() }
    }
    cyberAnimFrame = requestAnimationFrame(loop)
  }

  function doRestoreDecay() {
    const rOrd = _corruptOrder(len, 'left')
    rOrd.forEach((idx, i) => {
      animTimers.push(setTimeout(() => {
        chars[idx].glow = 1.0; chars[idx].opacity = 1
        animTimers.push(setTimeout(() => {
          _restoreChar(chars[idx])
          if (i === rOrd.length - 1) { resetAllChars(); idleAnimating.value = false; scheduleIdle() }
        }, 80))
      }, i * 50))
    })
  }
}

// ========== C4: 马赛克侵蚀 ==========
// 乱码方向: 两侧→中间 | 特效: 方块字符 + 波动脉冲 | 恢复方向: 中间→两侧
function effectMosaicBreach() {
  idleAnimating.value = true
  const chars = displayChars.value
  const len = chars.length
  const nc = _neonC()

  // Phase 1: 从两侧向中间逐字变乱码
  const half = Math.ceil(len / 2)
  const cOrd = []
  for (let i = 0; i < half; i++) {
    if (i < len) cOrd.push(i)
    if (len - 1 - i > i) cOrd.push(len - 1 - i)
  }
  cOrd.forEach((idx, i) => {
    animTimers.push(setTimeout(() => {
      _setCyber(chars[idx], nc)
      if (i === cOrd.length - 1) doMosaic()
    }, i * 40))
  })

  function doMosaic() {
    const dur = 1800, start = performance.now()
    function loop(ts) {
      const el = ts - start, p = Math.min(el / dur, 1)
      chars.forEach((c, i) => {
        if (Math.random() < 0.25) c.displayChar = _randCyber()
        const dc = Math.abs(i - len / 2) / (len / 2)
        c.opacity = 0.5 + Math.sin(el * 0.006 - dc * 4) * 0.3 + dc * 0.3
        const gp = Math.floor(i / 3)
        c.offsetY = Math.sin(el * 0.005 + gp * 1.2) * 6
        c.offsetX = Math.sin(el * 0.008 + i * 0.9) * 1.5
        c.glow = 0.4 + Math.abs(Math.sin(el * 0.004 + i * 0.4)) * 0.6
        if (Math.random() < 0.04) {
          const picks = [nc.cyan, nc.purple, nc.pink]
          c.animColor = picks[Math.floor(Math.random() * picks.length)]
        }
      })
      if (p < 1) { cyberAnimFrame = requestAnimationFrame(loop) } else { doRestoreMosaic() }
    }
    cyberAnimFrame = requestAnimationFrame(loop)
  }

  function doRestoreMosaic() {
    const mid = Math.floor(len / 2)
    const rOrd = []
    for (let d = 0; d <= mid; d++) {
      if (mid - d >= 0) rOrd.push(mid - d)
      if (mid + d < len && d > 0) rOrd.push(mid + d)
    }
    rOrd.forEach((idx, i) => {
      const base = i * 45, cycles = 2 + Math.floor(Math.random() * 2)
      for (let j = 0; j < cycles; j++) {
        animTimers.push(setTimeout(() => {
          chars[idx].displayChar = _randCyber()
          chars[idx].opacity = Math.min(1, 0.5 + j * 0.2)
        }, base + j * 30))
      }
      animTimers.push(setTimeout(() => {
        _restoreChar(chars[idx])
        if (i === rOrd.length - 1) { resetAllChars(); idleAnimating.value = false; scheduleIdle() }
      }, base + cycles * 30))
    })
  }
}

// ============================================================
//  动画循环
// ============================================================
let animationFrame = null
let lastTime = 0
let constellationInited = false

function resizeCanvas() {
  const canvas = constellationCanvas.value
  if (canvas) {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  const pCanvas = particleCanvas.value
  if (pCanvas) {
    pCanvas.width = window.innerWidth
    pCanvas.height = window.innerHeight
  }
}

const animate = (timestamp) => {
  if (!lastTime) lastTime = timestamp

  // A1: 绘制星空连线
  drawConstellation()

  // B3+B4: 更新字符交互（发光/缩放/色相）
  updateCharInteraction()

  animationFrame = requestAnimationFrame(animate)
}

// ============================================================
//  事件处理
// ============================================================
function handleMouseMove(e) {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
  mouseActive.value = true
}

function handleMouseLeave() {
  mouseActive.value = false
}

function handleSectionMouseMove(e) {
  sectionMouseX.value = e.clientX - window.innerWidth / 2
  sectionMouseY.value = e.clientY - window.innerHeight / 2
}

function handleWheel(e) {
  const container = scrollContainer.value
  if (!container) return
  const delta = e.deltaY
  if (Math.abs(delta) < 30) return

  // 照片墙自由滚动模式
  if (isPhotoWallActive.value) {
    // 滚动到接近 snap 区域顶部时，重新启用 snap 模式
    const snapHeight = totalSections * window.innerHeight
    if (container.scrollTop < snapHeight - window.innerHeight * 0.3 && delta < 0) {
      isPhotoWallActive.value = false
      e.preventDefault()
      currentSection.value = totalSections - 1
      scrollToSection(currentSection.value)
      return
    }
    // 允许浏览器自然滚动
    return
  }

  // Snap 模式
  if (isScrolling) return
  e.preventDefault()
  isScrolling = true

  if (delta > 0 && currentSection.value >= totalSections - 1) {
    // 在最后一屏，向下滚动 → 切换到照片墙并平滑滚动
    isPhotoWallActive.value = true
    nextTick(() => {
      const container = scrollContainer.value
      const wallEl = photoWallRef.value
      if (container && wallEl) {
        container.scrollTo({ top: wallEl.offsetTop, behavior: 'smooth' })
      }
    })
    setTimeout(() => { isScrolling = false }, 800)
  } else if (delta > 0 && currentSection.value < totalSections - 1) {
    currentSection.value++
    scrollToSection(currentSection.value)
    setTimeout(() => { isScrolling = false }, 800)
  } else if (delta < 0 && currentSection.value > 0) {
    currentSection.value--
    scrollToSection(currentSection.value)
    setTimeout(() => { isScrolling = false }, 800)
  } else {
    isScrolling = false
  }
}

function scrollToSection(index) {
  currentSection.value = index
  const container = scrollContainer.value
  if (!container) return
  container.scrollTo({ top: index * window.innerHeight, behavior: 'smooth' })
}

// ============================================================
//  Role 乱码过渡动画
// ============================================================
const ROLE_GLITCH = '!@#$%^&*<>{}[]|;:,.?/~`0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
function scrambleRoleTransition(newRole) {
  roleScrambling = true
  const oldText = displayedRole.value
  const maxLen = Math.max(oldText.length, newRole.length)
  const phase1Dur = 750  // 乱码阶段
  const phase2Dur = 850  // 还原阶段
  const tickInterval = 35
  const totalTicks1 = Math.floor(phase1Dur / tickInterval)
  const totalTicks2 = Math.floor(phase2Dur / tickInterval)
  let tick = 0

  // Phase 1: 逐字替换为乱码
  const timer1 = setInterval(() => {
    tick++
    const progress = tick / totalTicks1
    let result = ''
    for (let i = 0; i < maxLen; i++) {
      if (i < oldText.length) {
        result += (i / oldText.length < progress)
          ? ROLE_GLITCH[Math.floor(Math.random() * ROLE_GLITCH.length)]
          : oldText[i]
      }
    }
    displayedRole.value = result || oldText
    if (tick >= totalTicks1) {
      clearInterval(timer1)
      currentRole.value = newRole
      // Phase 2: 逐字从乱码恢复为新文字
      tick = 0
      const timer2 = setInterval(() => {
        tick++
        const progress = tick / totalTicks2
        let result = ''
        for (let i = 0; i < maxLen; i++) {
          if (i < newRole.length) {
            result += (i / newRole.length < progress)
              ? newRole[i]
              : ROLE_GLITCH[Math.floor(Math.random() * ROLE_GLITCH.length)]
          }
        }
        displayedRole.value = result || newRole
        if (tick >= totalTicks2) {
          clearInterval(timer2)
          displayedRole.value = newRole
          roleScrambling = false
        }
      }, tickInterval)
    }
  }, tickInterval)
}

// ============================================================
//  打字机 + 数据加载
// ============================================================
function startTypewriter() {
  typewriterTimer = setInterval(() => {
    if (charIndex < fullText.length) {
      displayText.value += fullText[charIndex]
      charIndex++
    } else {
      clearInterval(typewriterTimer)
      // 启动角色轮播（乱码过渡）
      setInterval(() => {
        if (roleScrambling) return
        roleIndex = (roleIndex + 1) % roles.length
        const newRole = roles[roleIndex]
        scrambleRoleTransition(newRole)
      }, 12000 + Math.random() * 3000)
      // 打字机完成后启动空闲动画计时器
      scheduleIdle()
    }
  }, 80)
}

async function loadData() {
  try {
    const portfolio = await getPortfolio()
    featuredPortfolio.value = portfolio.slice(0, 3)
  } catch (e) { console.error('加载作品集失败', e) }
  try {
    const tools = await getTools(1, 6)
    popularTools.value = tools.items.slice(0, 3)
  } catch (e) { console.error('加载工具列表失败', e) }
  loadPhotos()
}

async function handleDownload(id, filename) {
  try {
    const response = await downloadTool(id)
    const url = window.URL.createObjectURL(response)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename || `tool_${id}`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (e) { alert('下载失败：' + e.message) }
}

// ============================================================
//  主题监听
// ============================================================
const themeObserver = new MutationObserver(() => {
  isDark.value = document.documentElement.classList.contains('dark')
})

// ============================================================
//  生命周期
// ============================================================
// Lightbox ESC + 左右键
const handleLightboxKey = (e) => {
  if (!lightboxPhoto.value) return
  if (e.key === 'Escape') closeLightbox()
  else if (e.key === 'ArrowLeft') lightboxPrev()
  else if (e.key === 'ArrowRight') lightboxNext()
}

onMounted(async () => {
  await nextTick()
  resizeCanvas()
  initConstellation()
  constellationInited = true
  startTypewriter()
  loadData()
  animationFrame = requestAnimationFrame(animate)
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
  window.addEventListener('resize', () => {
    resizeCanvas()
    initConstellation()
  })
  document.addEventListener('keydown', handleLightboxKey)
  // 位置拖拽全局事件
  document.addEventListener('mousemove', onPosDragMove)
  document.addEventListener('mouseup', onPosDragEnd)
  document.addEventListener('touchmove', onPosDragMove, { passive: false })
  document.addEventListener('touchend', onPosDragEnd)
})

onUnmounted(() => {
  if (typewriterTimer) clearInterval(typewriterTimer)
  if (animationFrame) cancelAnimationFrame(animationFrame)
  if (ptclAnimFrame) cancelAnimationFrame(ptclAnimFrame)
  clearTimeout(idleTimer)
  clearAnimTimers()
  themeObserver.disconnect()
  document.removeEventListener('keydown', handleLightboxKey)
  document.removeEventListener('mousemove', onPosDragMove)
  document.removeEventListener('mouseup', onPosDragEnd)
  document.removeEventListener('touchmove', onPosDragMove)
  document.removeEventListener('touchend', onPosDragEnd)
})
</script>

<style scoped>
/* 各 section 确保在固定背景之上 */
.snap-section {
  position: relative;
  z-index: 1;
}

/* ============================================================
   极光波浪 A3
   ============================================================ */
.aurora-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 45%;
  overflow: hidden;
  pointer-events: none;
  z-index: 1;
}
.aurora-wave {
  position: absolute;
  bottom: -20%;
  left: -10%;
  width: 120%;
  height: 100%;
  border-radius: 50% 50% 0 0;
  opacity: 0.6;
}
.aurora-wave-1 {
  background: linear-gradient(180deg, transparent 0%, rgba(3, 105, 161, 0.06) 40%, rgba(3, 105, 161, 0.12) 100%);
  animation: auroraFloat1 12s ease-in-out infinite;
}
.aurora-wave-2 {
  background: linear-gradient(180deg, transparent 0%, rgba(109, 40, 217, 0.05) 40%, rgba(109, 40, 217, 0.1) 100%);
  animation: auroraFloat2 15s ease-in-out infinite;
  bottom: -25%;
}
.aurora-wave-3 {
  background: linear-gradient(180deg, transparent 0%, rgba(190, 24, 93, 0.04) 40%, rgba(190, 24, 93, 0.08) 100%);
  animation: auroraFloat3 18s ease-in-out infinite;
  bottom: -30%;
}
.aurora-wave-4 {
  background: linear-gradient(180deg, transparent 0%, rgba(4, 120, 87, 0.03) 40%, rgba(4, 120, 87, 0.06) 100%);
  animation: auroraFloat4 20s ease-in-out infinite;
  bottom: -35%;
}

/* 暗色模式极光更亮 */
.dark .aurora-wave-1 {
  background: linear-gradient(180deg, transparent 0%, rgba(0, 243, 255, 0.05) 40%, rgba(0, 243, 255, 0.12) 100%);
}
.dark .aurora-wave-2 {
  background: linear-gradient(180deg, transparent 0%, rgba(182, 112, 255, 0.04) 40%, rgba(182, 112, 255, 0.1) 100%);
}
.dark .aurora-wave-3 {
  background: linear-gradient(180deg, transparent 0%, rgba(255, 45, 117, 0.03) 40%, rgba(255, 45, 117, 0.08) 100%);
}
.dark .aurora-wave-4 {
  background: linear-gradient(180deg, transparent 0%, rgba(57, 255, 20, 0.02) 40%, rgba(57, 255, 20, 0.05) 100%);
}

@keyframes auroraFloat1 {
  0%, 100% { transform: translateX(0) scaleY(1); }
  33% { transform: translateX(3%) scaleY(1.1); }
  66% { transform: translateX(-2%) scaleY(0.95); }
}
@keyframes auroraFloat2 {
  0%, 100% { transform: translateX(0) scaleY(1); }
  33% { transform: translateX(-4%) scaleY(1.05); }
  66% { transform: translateX(3%) scaleY(1.12); }
}
@keyframes auroraFloat3 {
  0%, 100% { transform: translateX(0) scaleY(1); }
  50% { transform: translateX(5%) scaleY(1.08); }
}
@keyframes auroraFloat4 {
  0%, 100% { transform: translateX(0) scaleY(1); }
  50% { transform: translateX(-3%) scaleY(1.15); }
}

/* ============================================================
   渐变网格背景
   ============================================================ */
.hero-mesh-bg {
  position: absolute;
  inset: 0;
  opacity: 0.5;
  pointer-events: none;
  animation: meshFloat 15s ease-in-out infinite;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(3, 105, 161, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(109, 40, 217, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 80%, rgba(190, 24, 93, 0.05) 0%, transparent 50%);
  z-index: 0;
}
.dark .hero-mesh-bg {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0, 243, 255, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(182, 112, 255, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 80%, rgba(255, 45, 117, 0.04) 0%, transparent 50%);
  opacity: 0.7;
}
@keyframes meshFloat {
  0%, 100% { background-position: 0% 0%, 100% 0%, 50% 100%; }
  25% { background-position: 30% 20%, 70% 40%, 20% 80%; }
  50% { background-position: 60% 40%, 40% 70%, 80% 20%; }
  75% { background-position: 20% 60%, 80% 30%, 40% 60%; }
}

/* ============================================================
   扫描环
   ============================================================ */
.scan-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid;
  transform: translate(-50%, -50%);
  pointer-events: none;
}
.scan-ring-1 {
  width: 100px; height: 100px;
  border-color: rgba(3, 105, 161, 0.15);
  animation: scanRingPulse 3s ease-in-out infinite;
}
.scan-ring-2 {
  width: 160px; height: 160px;
  border-color: rgba(109, 40, 217, 0.1);
  animation: scanRingPulse 3s ease-in-out 1s infinite;
}
.scan-ring-3 {
  width: 220px; height: 220px;
  border-color: rgba(190, 24, 93, 0.07);
  animation: scanRingPulse 3s ease-in-out 2s infinite;
}
.dark .scan-ring-1 { border-color: rgba(0, 243, 255, 0.2); }
.dark .scan-ring-2 { border-color: rgba(182, 112, 255, 0.15); }
.dark .scan-ring-3 { border-color: rgba(255, 45, 117, 0.1); }
@keyframes scanRingPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.3; }
}

/* ============================================================
   鼠标光晕
   ============================================================ */
.cursor-glow {
  position: absolute;
  width: 200px; height: 200px;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  background: radial-gradient(circle, rgba(3, 105, 161, 0.08) 0%, transparent 70%);
  transition: left 0.1s ease-out, top 0.1s ease-out;
  z-index: 2;
}
.dark .cursor-glow {
  background: radial-gradient(circle, rgba(0, 243, 255, 0.1) 0%, transparent 70%);
}

/* ============================================================
   Hero 字符
   ============================================================ */
.hero-title { will-change: transform; }
.hero-char {
  will-change: filter;
  cursor: default;
  display: inline;
}

/* ============================================================
   状态徽章
   ============================================================ */
.status-badge {
  padding: 4px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
  background: rgba(3, 105, 161, 0.04);
  border: 1px solid rgba(3, 105, 161, 0.08);
}
.dark .status-badge { background: transparent; border: none; }
.status-badge:hover {
  background: rgba(3, 105, 161, 0.08);
  transform: translateY(-1px);
}

/* ============================================================
   淡入动画
   ============================================================ */
.animate-fade-in { animation: fadeIn 1s ease-out forwards; opacity: 0; }
.animate-fade-in-delay { animation: fadeIn 1s ease-out 0.5s forwards; opacity: 0; }
.animate-fade-in-delay-2 { animation: fadeIn 1s ease-out 1s forwards; opacity: 0; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
/* ============================================================
   照片墙
   ============================================================ */
.photo-wall-active {
  scroll-snap-type: none !important;
}

.photo-wall-section {
  min-height: auto;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 220px;
  grid-auto-flow: dense;
  gap: 14px;
}

.photo-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transform: rotate(var(--rotate, 0deg));
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  content-visibility: auto;
  contain-intrinsic-size: 300px 220px;
  background: var(--border-color);
  will-change: transform;
}

.photo-card:hover {
  transform: rotate(0deg) scale(1.03);
  box-shadow: 0 8px 40px rgba(14, 165, 233, 0.2);
  z-index: 10;
}

.photo-card .photo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.photo-card:hover .photo-img {
  transform: scale(1.08);
}

.photo-card .photo-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 50%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 16px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.photo-card:hover .photo-overlay {
  opacity: 1;
}

.photo-caption {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  font-family: monospace;
}

.photo-tag {
  display: inline-block;
  margin-top: 6px;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-family: monospace;
  background: rgba(14, 165, 233, 0.2);
  border: 1px solid rgba(14, 165, 233, 0.3);
  color: #0ea5e9;
  width: fit-content;
}

/* 照片尺寸 */
.photo-sm { grid-column: span 1; grid-row: span 1; }
.photo-md { grid-column: span 2; grid-row: span 1; }
.photo-tall { grid-column: span 1; grid-row: span 2; }
.photo-lg { grid-column: span 2; grid-row: span 2; }

@media (max-width: 768px) {
  .photo-grid {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: 180px;
    gap: 10px;
  }
  .photo-md { grid-column: span 2; }
  .photo-lg { grid-column: span 2; }
  .photo-tall { grid-row: span 2; }
}

@media (max-width: 480px) {
  .photo-grid {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: 150px;
    gap: 8px;
  }
}

/* ============================================================
   Lightbox
   ============================================================ */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.92);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.lightbox-content {
  max-width: 90vw;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.lightbox-img {
  max-width: 100%;
  max-height: 75vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.lightbox-info {
  margin-top: 16px;
  text-align: center;
}

.lightbox-caption {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  font-family: monospace;
}

.lightbox-tag {
  display: inline-block;
  margin-left: 12px;
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-family: monospace;
  background: rgba(14, 165, 233, 0.2);
  border: 1px solid rgba(14, 165, 233, 0.3);
  color: #0ea5e9;
}

.lightbox-close {
  position: absolute;
  top: 20px;
  right: 20px;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.lightbox-close:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.15);
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.lightbox-nav:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.15);
}

.lightbox-prev { left: 20px; }
.lightbox-next { right: 20px; }

.lightbox-enter-active { transition: all 0.3s ease; }
.lightbox-leave-active { transition: all 0.2s ease; }
.lightbox-enter-from { opacity: 0; }
.lightbox-leave-to { opacity: 0; }
.lightbox-enter-from .lightbox-content { transform: scale(0.9); }
.lightbox-leave-to .lightbox-content { transform: scale(0.95); }

/* ============================================================
   底部收尾
   ============================================================ */
.closing-section {
  min-height: auto;
}

.social-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  color: var(--text-muted);
  background: rgba(14, 165, 233, 0.06);
  border: 1px solid var(--border-color);
}

.social-btn:hover {
  color: var(--accent);
  background: rgba(14, 165, 233, 0.12);
  border-color: rgba(14, 165, 233, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(14, 165, 233, 0.15);
}

.back-to-top-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border-radius: 12px;
  color: var(--text-secondary);
  background: rgba(14, 165, 233, 0.06);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s;
  font-family: monospace;
}

.back-to-top-btn:hover {
  color: var(--accent);
  border-color: rgba(14, 165, 233, 0.3);
  background: rgba(14, 165, 233, 0.1);
  transform: translateY(-2px);
}

/* ============================================================
   照片墙管理员 UI
   ============================================================ */
.photo-admin-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border-radius: 10px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  color: #ec4899;
  background: rgba(236, 72, 153, 0.08);
  border: 1px solid rgba(236, 72, 153, 0.25);
  cursor: pointer;
  transition: all 0.2s;
}
.photo-admin-btn:hover {
  background: rgba(236, 72, 153, 0.15);
  border-color: rgba(236, 72, 153, 0.4);
  box-shadow: 0 0 12px rgba(236, 72, 153, 0.15);
}

.photo-admin-overlay {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 6px;
  z-index: 20;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.photo-card:hover .photo-admin-overlay {
  opacity: 1;
}

.photo-admin-card-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #fff;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.15);
}
.photo-admin-card-btn:hover {
  background: rgba(0, 240, 255, 0.3);
  border-color: rgba(0, 240, 255, 0.5);
}
.photo-admin-delete:hover {
  background: rgba(239, 68, 68, 0.5);
  border-color: rgba(239, 68, 68, 0.7);
}

/* 照片管理弹窗 */
.photo-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.photo-modal {
  width: 100%;
  max-width: 520px;
  border-radius: 16px;
  overflow: hidden;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}
.photo-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}
.photo-modal-close {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.2s;
  background: transparent;
  border: none;
}
.photo-modal-close:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}
.photo-modal-body {
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
}
.photo-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 14px 20px;
  border-top: 1px solid var(--border-color);
}

.photo-form-group {
  margin-bottom: 14px;
}
.photo-form-label {
  display: block;
  font-size: 12px;
  font-family: 'Courier New', monospace;
  color: var(--text-tertiary);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.photo-form-input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.2s;
}
.photo-form-input:focus {
  border-color: rgba(236, 72, 153, 0.4);
}

.photo-upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 12px;
  font-family: 'Courier New', monospace;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
}
.photo-upload-btn:hover {
  border-color: rgba(236, 72, 153, 0.3);
  color: var(--accent-pink, #ec4899);
}

.photo-preview-img {
  width: 100%;
  max-height: 160px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.photo-btn-cancel {
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
  background: transparent;
  border: 1px solid var(--border-color);
}
.photo-btn-cancel:hover {
  background: rgba(255, 255, 255, 0.03);
}
.photo-btn-save {
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  cursor: pointer;
  transition: all 0.2s;
  color: #fff;
  background: rgba(236, 72, 153, 0.8);
  border: 1px solid rgba(236, 72, 153, 0.5);
}
.photo-btn-save:hover:not(:disabled) {
  background: rgba(236, 72, 153, 1);
  box-shadow: 0 0 16px rgba(236, 72, 153, 0.3);
}
.photo-btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 位置调整预览 */
.pos-preview-container {
  position: relative;
  height: 160px;
  max-width: 100%;
  margin: 0 auto;
  overflow: hidden;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  cursor: grab;
  user-select: none;
}
.pos-preview-container:active {
  cursor: grabbing;
}
.pos-preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
  transition: object-position 0.05s ease-out;
}
.pos-crosshair {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  transform: translate(-50%, -50%);
  pointer-events: none;
}
.pos-crosshair::before,
.pos-crosshair::after {
  content: '';
  position: absolute;
  background: rgba(236, 72, 153, 0.6);
}
.pos-crosshair::before {
  top: 50%;
  left: 0;
  width: 100%;
  height: 1px;
  transform: translateY(-50%);
}
.pos-crosshair::after {
  left: 50%;
  top: 0;
  width: 1px;
  height: 100%;
  transform: translateX(-50%);
}
.pos-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
}
.pos-values {
  display: flex;
  gap: 12px;
}
.pos-label {
  font-size: 11px;
  font-family: 'Courier New', monospace;
  color: var(--text-tertiary);
  background: var(--bg-primary);
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
}
.pos-reset-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-family: 'Courier New', monospace;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
}
.pos-reset-btn:hover {
  border-color: rgba(236, 72, 153, 0.4);
  color: var(--accent-pink, #ec4899);
}
</style>
