<template>
  <div class="min-h-screen pt-20 pb-16 px-4">
    <div class="max-w-5xl mx-auto">
      <!-- 简历头部 -->
      <div class="text-center mb-16 animate-fade-in">
        <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider mb-4"
              style="background: rgba(3, 105, 161, 0.08); border: 1px solid rgba(3, 105, 161, 0.2); color: var(--accent);">
          // RESUME.TIMELINE
        </span>
        <h1 class="text-4xl md:text-5xl font-bold mb-3 font-mono gradient-text">
          {{ resume.title || '个人简历' }}
        </h1>
        <p class="text-lg font-mono mb-6" style="color: var(--text-secondary);">
          {{ resume.subtitle || '全栈开发工程师 | 软件测试自动化专家' }}
        </p>

        <!-- 联系方式条 -->
        <div class="flex flex-wrap justify-center gap-6 text-sm font-mono" style="color: var(--text-muted);">
          <a :href="'mailto:' + resume.email" class="flex items-center gap-2 hover:text-neon transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
            {{ resume.email || 'email@example.com' }}
          </a>
          <a :href="resume.github" target="_blank" class="flex items-center gap-2 hover:text-neon-purple transition-colors">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            {{ resume.github || 'github.com/yourname' }}
          </a>
        </div>

        <button v-if="isAdmin" @click="editSection('header')" class="mt-4 px-4 py-1.5 rounded-lg text-xs font-mono transition-all"
                style="background: rgba(14,165,233,0.08); border: 1px solid rgba(14,165,233,0.15); color: var(--accent);">
          ✎ 编辑头部
        </button>
      </div>

      <!-- 时间轴 -->
      <div class="timeline-container">
        <!-- 时间轴中线 -->
        <div class="timeline-line"></div>

        <!-- 时间轴节点 -->
        <div
          v-for="(item, index) in timelineItems"
          :key="index"
          class="timeline-item"
          :class="[index % 2 === 0 ? 'timeline-left' : 'timeline-right', { 'timeline-visible': item.visible }]"
          :ref="el => { if (el) timelineRefs[index] = el }"
        >
          <!-- 时间节点圆点 -->
          <div class="timeline-dot" :style="{ background: item.color }">
            <span class="timeline-dot-icon" v-html="item.icon"></span>
          </div>

          <!-- 时间标签（另一侧） -->
          <div class="timeline-date">
            <span class="font-mono text-sm font-semibold" :style="{ color: item.color }">{{ item.period }}</span>
          </div>

          <!-- 内容卡片 -->
          <div class="timeline-card card-neon group">
            <!-- 顶部装饰条 -->
            <div class="absolute top-0 left-0 right-0 h-0.5 opacity-0 group-hover:opacity-100 transition-opacity"
                 :style="{ background: `linear-gradient(to right, ${item.color}, transparent)` }"></div>

            <!-- 类型标签 -->
            <span class="inline-block px-2.5 py-0.5 rounded text-[10px] font-mono tracking-wider mb-3"
                  :style="{ background: item.color + '15', border: `1px solid ${item.color}30`, color: item.color }">
              {{ item.type }}
            </span>

            <h3 class="text-lg font-bold mb-1 font-mono" style="color: var(--text-primary);">
              {{ item.title }}
            </h3>
            <p v-if="item.company" class="text-sm font-mono mb-3" :style="{ color: item.color }">
              {{ item.company }}
            </p>
            <p class="text-sm leading-relaxed" style="color: var(--text-secondary);">
              {{ item.description }}
            </p>

            <!-- 技能标签 -->
            <div v-if="item.tags" class="flex flex-wrap gap-1.5 mt-3">
              <span v-for="tag in item.tags" :key="tag"
                    class="px-2 py-0.5 rounded text-[10px] font-mono"
                    :style="{ background: item.color + '10', border: `1px solid ${item.color}20`, color: item.color }">
                {{ tag }}
              </span>
            </div>

            <!-- 管理员编辑 -->
            <button v-if="isAdmin && item.editKey" @click="editSection(item.editKey)"
                    class="absolute top-3 right-3 p-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"
                    style="background: rgba(14,165,233,0.08); border: 1px solid rgba(14,165,233,0.15);" title="编辑">
              <svg class="h-3.5 w-3.5" style="color: var(--accent);" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 技能图标网格 -->
      <div class="mt-16 mb-8 animate-fade-in">
        <div class="text-center mb-8">
          <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider mb-4"
                style="background: rgba(182,112,255,0.08); border: 1px solid rgba(182,112,255,0.2); color: var(--accent-purple);">
            // TECH_STACK
          </span>
          <h2 class="text-2xl md:text-3xl font-bold font-mono gradient-text">技术栈</h2>
        </div>

        <!-- 分类网格 -->
        <div v-for="cat in skillCategories" :key="cat.name" class="mb-8">
          <h3 class="text-sm font-mono tracking-wider mb-4 text-center" style="color: var(--text-muted);">
            <span style="color: var(--accent-purple);">#</span> {{ cat.name }}
          </h3>
          <div class="flex flex-wrap justify-center gap-3">
            <div
              v-for="skill in cat.skills"
              :key="skill.name"
              class="skill-icon-card group"
              :style="{ '--skill-color': skill.color }"
            >
              <div class="skill-icon" v-html="skill.icon"></div>
              <span class="skill-name">{{ skill.name }}</span>
            </div>
          </div>
        </div>

        <button v-if="isAdmin" @click="editSection('skills')"
                class="mx-auto block mt-4 px-4 py-1.5 rounded-lg text-xs font-mono transition-all"
                style="background: rgba(14,165,233,0.08); border: 1px solid rgba(14,165,233,0.15); color: var(--accent);">
          ✎ 编辑技能
        </button>
      </div>

      <!-- 编辑弹窗 -->
      <div v-if="showEditForm" class="fixed inset-0 flex items-center justify-center z-50" style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px);" @click.self="closeEditForm">
        <div class="card-neon p-6 w-full max-w-md max-h-[80vh] overflow-y-auto">
          <h2 class="text-2xl font-bold mb-6 font-mono" style="color: var(--text-primary);"><span class="text-neon">></span> 编辑{{ editingSectionName }}</h2>
          <form @submit.prevent="saveResume">
            <template v-if="editingSection === 'header'">
              <div class="mb-4"><label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">标题</label><input v-model="editForm.title" type="text" class="input-cyber" /></div>
              <div class="mb-4"><label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">副标题</label><input v-model="editForm.subtitle" type="text" class="input-cyber" /></div>
              <div class="mb-4"><label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">邮箱</label><input v-model="editForm.email" type="email" class="input-cyber" /></div>
              <div class="mb-4"><label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">GitHub</label><input v-model="editForm.github" type="text" class="input-cyber" /></div>
            </template>
            <template v-if="editingSection === 'skills'">
              <div class="mb-4"><label class="block text-sm font-medium mb-1.5 font-mono" style="color: var(--text-secondary);">技能（逗号分隔）</label><input v-model="editForm.skillsStr" type="text" class="input-cyber" /></div>
            </template>
            <div class="flex gap-3 mt-6">
              <button type="submit" class="btn-primary flex-1">保存</button>
              <button type="button" @click="closeEditForm" class="btn-secondary flex-1">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { getAdminStatus, getResume, updateResume } from '../composables/useApi'

const isAdmin = getAdminStatus()

// 简历数据（含丰富测试数据）
const resume = reactive({
  title: '个人简历',
  subtitle: '全栈开发工程师 | 软件测试自动化专家',
  email: 'your.email@example.com',
  github: 'https://github.com/yourusername',
  skills: ['Python', 'JavaScript', 'Vue.js', 'Flask', 'SQL', 'Docker', 'Git', 'Linux', 'CI/CD', 'React', 'TypeScript', 'Redis', 'Nginx', 'AWS'],
  workExperience: [
    {
      title: '高级软件工程师',
      company: 'ABC 科技有限公司',
      period: '2022.06 - 至今',
      description: '主导公司核心产品的前端架构重构，将 jQuery 单体应用迁移至 Vue 3 + Vite 技术栈，首屏加载时间降低 60%。设计并实现了自动化测试框架，覆盖率从 35% 提升至 85%。带领 5 人前端团队，推动代码规范和 CI/CD 流程标准化。',
      tags: ['Vue 3', 'Vite', '自动化测试', '团队管理']
    },
    {
      title: '全栈开发工程师',
      company: 'XYZ 互联网科技',
      period: '2020.03 - 2022.05',
      description: '负责公司 SaaS 平台的全栈开发，使用 Flask + Vue.js 构建微服务架构。独立完成了用户权限系统、数据可视化仪表盘、实时消息推送等核心模块。优化数据库查询性能，API 响应时间降低 40%。',
      tags: ['Flask', 'Vue.js', 'PostgreSQL', 'WebSocket']
    },
    {
      title: '初级开发工程师',
      company: '创新软件工作室',
      period: '2019.07 - 2020.02',
      description: '参与多个企业级 Web 项目的开发与维护，积累了全栈开发经验。负责编写单元测试和集成测试，建立了代码审查流程。学习并实践敏捷开发方法论。',
      tags: ['Python', 'JavaScript', 'MySQL', 'Docker']
    }
  ],
  education: {
    degree: '计算机科学与技术 学士',
    school: '浙江大学',
    period: '2015.09 - 2019.06'
  }
})

// 时间轴数据（合并工作经历和教育背景，按时间倒序）
const timelineItems = reactive([])

function buildTimeline() {
  const items = []

  // 工作经历
  resume.workExperience.forEach((job, idx) => {
    items.push({
      type: 'WORK',
      title: job.title,
      company: job.company,
      period: job.period,
      description: job.description,
      tags: job.tags,
      color: idx === 0 ? 'var(--accent)' : idx === 1 ? 'var(--accent-purple)' : 'var(--accent-green)',
      icon: '<svg class="w-3.5 h-3.5" fill="none" stroke="white" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>',
      editKey: 'work',
      visible: false
    })
  })

  // 教育背景
  items.push({
    type: 'EDUCATION',
    title: resume.education.degree,
    company: resume.education.school,
    period: resume.education.period,
    description: '主修课程：数据结构与算法、操作系统、计算机网络、数据库原理、软件工程。GPA 3.8/4.0，连续三年获得校级奖学金。参与 ACM 竞赛获省级二等奖。',
    tags: ['计算机科学', 'ACM 竞赛', '校级奖学金'],
    color: 'var(--accent-yellow)',
    icon: '<svg class="w-3.5 h-3.5" fill="none" stroke="white" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /></svg>',
    editKey: 'education',
    visible: false
  })

  timelineItems.splice(0, timelineItems.length, ...items)
}

// 技能图标分类数据
const skillSVGs = {
  'Python': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9.585 11.692h4.328s2.432.039 2.432-2.35V5.391S16.714 3 11.936 3C7.362 3 7.647 4.984 7.647 4.984l.006 2.055h4.363v.617H5.92S3 7.283 3 11.748s2.551 4.306 2.551 4.306h1.523v-2.073s-.082-2.551 2.511-2.551v.262zm-.249-4.83a.814.814 0 110-1.627.814.814 0 010 1.627zm8.294 4.965s2.218.107 2.218-2.134V5.706S19.455 3 15.18 3h-3.67s-2.557-.168-2.557 2.466v2.252h4.42v.617h-6.04S5.15 8.024 5.15 12.268c0 4.244 2.168 4.132 2.168 4.132h1.762v-1.985s.093-2.168 2.173-2.168h3.59s2.145-.035 2.145-2.14v-2.91h-.185zm-2.777-2.634a.814.814 0 110-1.627.814.814 0 010 1.627z"/></svg>',
  'JavaScript': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M0 0h24v24H0V0zm22.034 18.276c-.175-1.095-.888-2.015-3.003-2.873-.736-.345-1.554-.585-1.797-1.14-.091-.33-.105-.51-.046-.705.15-.646.915-.84 1.515-.66.39.12.75.42.976.9 1.034-.676 1.034-.676 1.755-1.125-.27-.42-.405-.6-.586-.78-.63-.705-1.469-1.065-2.834-1.034l-.705.089c-.676.165-1.32.525-1.71 1.005-1.14 1.291-.811 3.541.569 4.471 1.365 1.02 3.361 1.244 3.616 2.205.24 1.17-.87 1.545-1.966 1.41-.811-.18-1.26-.586-1.755-1.336l-1.83 1.051c.21.48.45.689.81 1.109 1.74 1.756 6.09 1.666 6.871-1.004.029-.09.24-.705.074-1.65l.046.067zm-8.983-7.245h-2.248c0 1.938-.009 3.864-.009 5.805 0 1.232.063 2.363-.138 2.711-.33.689-1.18.601-1.566.48-.396-.196-.597-.466-.83-.855-.063-.105-.11-.196-.127-.196l-1.825 1.125c.305.63.75 1.172 1.324 1.517.855.51 2.004.675 3.207.405.783-.226 1.458-.691 1.811-1.411.51-.93.402-2.07.397-3.346.012-2.054 0-4.109 0-6.179l.004-.056z"/></svg>',
  'TypeScript': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M1.125 0C.502 0 0 .502 0 1.125v21.75C0 23.498.502 24 1.125 24h21.75c.623 0 1.125-.502 1.125-1.125V1.125C24 .502 23.498 0 22.875 0zm17.363 9.75c.612 0 1.154.037 1.627.111a6.38 6.38 0 011.306.34v2.458a3.95 3.95 0 00-.643-.361 5.093 5.093 0 00-.717-.26 5.453 5.453 0 00-1.426-.2c-.3 0-.573.028-.819.086a2.1 2.1 0 00-.623.242c-.17.104-.3.229-.393.374a.888.888 0 00-.14.49c0 .196.053.373.156.529.104.156.252.304.443.444s.423.276.696.41c.273.135.582.274.926.416.47.197.892.407 1.266.628.374.222.695.473.963.753.268.279.472.598.614.957.142.359.214.776.214 1.253 0 .657-.125 1.21-.373 1.656a3.033 3.033 0 01-1.012 1.085 4.38 4.38 0 01-1.487.596c-.566.12-1.163.18-1.79.18a9.916 9.916 0 01-1.84-.164 5.544 5.544 0 01-1.512-.493v-2.63a5.033 5.033 0 003.237 1.2c.333 0 .624-.03.872-.09.249-.06.456-.144.623-.25.166-.108.29-.234.373-.38a1.023 1.023 0 00-.074-1.089 2.12 2.12 0 00-.537-.5 5.597 5.597 0 00-.807-.444 27.72 27.72 0 00-1.007-.436c-.918-.383-1.602-.852-2.053-1.405-.45-.553-.676-1.222-.676-2.005 0-.614.123-1.141.369-1.582.246-.441.58-.804 1.004-1.089a4.494 4.494 0 011.47-.629 7.536 7.536 0 011.77-.201zm-15.113.188h9.563v2.166H9.506v9.646H6.789v-9.646H3.375z"/></svg>',
  'Vue.js': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M24,1.61H14.06L12,5.16,9.94,1.61H0L12,22.39ZM12,14.08,5.16,2.23H9.59L12,6.41l2.41-4.18h4.43Z"/></svg>',
  'React': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14.23 12.004a2.236 2.236 0 01-2.235 2.236 2.236 2.236 0 01-2.236-2.236 2.236 2.236 0 012.235-2.236 2.236 2.236 0 012.236 2.236zm2.648-10.69c-1.346 0-3.107.96-4.888 2.622-1.78-1.653-3.542-2.602-4.887-2.602-.31 0-.594.066-.838.192-.803.428-1.162 1.49-.813 2.67.27.893.875 1.75 1.588 2.424a9.654 9.654 0 00-.553.674c-.442.626-.76 1.34-.93 2.058-.246 1.04-.14 2.063.32 2.823.428.703 1.113 1.1 1.884 1.1.39 0 .755-.097 1.057-.27.627-.36 1.102-1.01 1.27-1.847.113-.567.072-1.15-.1-1.68a5.792 5.792 0 00-.612-1.365c.18-.16.352-.326.514-.498a9.586 9.586 0 002.532-5.21c.076-.782-.05-1.517-.347-2.096a2.304 2.304 0 00-.364-.454 2.096 2.096 0 00-.248-.212zm-6.49 5.113c.205.393.45.763.726 1.108a7.397 7.397 0 01-.372.468c-.256.293-.492.523-.71.69-.155.118-.29.198-.407.244-.085.033-.152.048-.205.048-.156 0-.29-.116-.397-.356-.07-.157-.105-.35-.105-.575 0-.39.087-.797.25-1.17.085-.19.185-.372.3-.544.07-.105.144-.205.224-.3l.034-.038zm11.578 2.79c-.367-.554-.888-.895-1.52-1.002-.297-.05-.59-.044-.86.017a4.35 4.35 0 00-.534.145c-.15.055-.29.123-.42.204a5.618 5.618 0 00-1.61 1.3c-.565.697-.865 1.456-.865 2.18 0 .39.077.745.22 1.05.187.395.49.7.882.887.396.188.856.252 1.342.18.585-.086 1.12-.365 1.546-.8.426-.434.724-.99.87-1.63.117-.506.113-.996-.01-1.436a2.254 2.254 0 00-.606-.91z"/></svg>',
  'Flask': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>',
  'SQL': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 4.02 2 6.5S6.48 11 12 11s10-2.02 10-4.5S17.52 2 12 2zm0 2c3.31 0 6 1.34 6 2.5S15.31 9 12 9 6 7.66 6 6.5 8.69 4 12 4zM2 9v2c0 1.16 2.69 2 6 2s6-.84 6-2V9c0 1.16-2.69 2-6 2s-6-.84-6-2zm0 4v2c0 1.16 2.69 2 6 2s6-.84 6-2v-2c0 1.16-2.69 2-6 2s-6-.84-6-2zm0 4v2c0 1.16 2.69 2 6 2s6-.84 6-2v-2c0 1.16-2.69 2-6 2s-6-.84-6-2z"/></svg>',
  'Docker': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.983 11.078h2.119a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.119a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m-2.954-5.43h2.118a.186.186 0 00.186-.186V3.574a.186.186 0 00-.186-.185h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.186m0 2.716h2.118a.187.187 0 00.186-.186V6.29a.186.186 0 00-.186-.185h-2.118a.185.185 0 00-.185.185v1.887c0 .102.082.186.185.186m-2.93 0h2.12a.186.186 0 00.184-.186V6.29a.185.185 0 00-.185-.185H8.1a.185.185 0 00-.185.185v1.887c0 .102.083.186.185.186m-2.964 0h2.119a.186.186 0 00.185-.186V6.29a.185.185 0 00-.185-.185H5.136a.186.186 0 00-.186.185v1.887c0 .102.084.186.186.186m5.893 2.715h2.118a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.185m-2.93 0h2.12a.185.185 0 00.184-.185V9.006a.185.185 0 00-.184-.186h-2.12a.185.185 0 00-.184.185v1.888c0 .102.083.185.185.185m-2.964 0h2.119a.185.185 0 00.185-.185V9.006a.185.185 0 00-.185-.186H5.136a.186.186 0 00-.186.186v1.887c0 .102.084.185.186.185m-2.92 0h2.12a.185.185 0 00.184-.185V9.006a.185.185 0 00-.184-.186h-2.12a.186.186 0 00-.184.186v1.887c0 .102.082.185.185.185M23.763 9.89c-.065-.051-.672-.51-1.954-.51-.338.001-.676.03-1.01.087-.248-1.7-1.653-2.53-1.716-2.566l-.344-.199-.226.327c-.284.438-.49.922-.612 1.43-.23.97-.09 1.882.403 2.661-.595.332-1.55.413-1.744.42H.751a.751.751 0 00-.75.748 11.376 11.376 0 00.692 4.062c.545 1.428 1.355 2.48 2.41 3.124 1.18.723 3.1 1.137 5.275 1.137.983.003 1.963-.086 2.93-.266a12.248 12.248 0 003.823-1.389c.98-.567 1.86-1.288 2.61-2.136 1.252-1.418 1.998-2.997 2.553-4.4h.221c1.372 0 2.215-.549 2.68-1.009.309-.293.55-.65.707-1.046l.098-.288Z"/></svg>',
  'Git': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.546 10.93L13.067.452a1.55 1.55 0 00-2.188 0L8.708 2.627l2.76 2.76a1.838 1.838 0 012.327 2.341l2.66 2.66a1.838 1.838 0 11-1.103 1.033l-2.48-2.48v6.53a1.838 1.838 0 11-1.512-.065V8.73a1.838 1.838 0 01-.998-2.41L7.629 3.587.452 10.765a1.55 1.55 0 000 2.188l10.48 10.48a1.55 1.55 0 002.186 0l10.43-10.43a1.55 1.55 0 000-2.073z"/></svg>',
  'Linux': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.504 0c-.155 0-.315.008-.48.021-4.226.333-3.105 4.807-3.17 6.298-.076 1.092-.3 1.953-1.05 3.02-.885 1.051-2.127 2.75-2.716 4.521-.278.832-.41 1.684-.287 2.489a.424.424 0 00-.11.135c-.26.268-.45.6-.663.839-.199.199-.485.267-.797.4-.313.136-.658.269-.864.68-.09.189-.136.394-.132.602 0 .199.027.4.055.536.058.399.116.728.04.97-.249.68-.28 1.145-.106 1.484.174.334.535.47.94.601.81.2 1.91.135 2.774.6.926.466 1.866.67 2.616.47.526-.116.97-.464 1.208-.946.587-.003 1.23-.269 2.26-.334.699-.058 1.574.267 2.577.2.025.134.063.198.114.333l.003.003c.391.778 1.113 1.368 1.884 1.43.094.007.187.012.28.012.6 0 1.174-.239 1.597-.617.465-.419.81-.991.979-1.648.074-.29.11-.565.115-.813.012-.42.003-.803-.111-1.125.18-.295.312-.63.372-1.009.065-.409.053-.836-.056-1.254-.133-.51-.317-.92-.422-1.22-.036-.106-.071-.208-.102-.308-.075-.241-.14-.399-.14-.562 0-.134.023-.287.062-.464.062-.257.155-.553.264-.877.193-.574.44-1.213.63-1.764.19-.55.326-1.008.352-1.38.012-.162.013-.309.003-.439a2.2 2.2 0 00-.175-.737 2.116 2.116 0 00-.122-.208c-.055-.086-.103-.16-.142-.224-.056-.091-.104-.162-.152-.227-.07-.093-.134-.168-.2-.261-.195-.263-.42-.557-.722-.79-.315-.244-.69-.412-1.095-.473-.405-.06-.86-.026-1.305.073-.195.044-.39.101-.586.172-.213.078-.428.171-.622.272-.19.1-.377.215-.554.337-.19.132-.353.275-.489.427-.134.152-.26.33-.343.464a.58.58 0 00-.075.138c-.02.044-.036.09-.048.136-.036.135-.06.274-.073.418z"/></svg>',
  'CI/CD': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 00-3.7-3.7 48.678 48.678 0 00-7.324 0 4.006 4.006 0 00-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3l-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 003.7 3.7 48.656 48.656 0 007.324 0 4.006 4.006 0 003.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3l-3 3"/></svg>',
  'Redis': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M10.5 2.661l.54.997-1.797.644 2.409.166.54.997-1.797.644 2.409.166.54.997L10.5 7.921l-2.834-1.64.54-.997 2.409-.166-1.797-.644.54-.997 2.409-.166zm7 0l.54.997-1.797.644 2.409.166.54.997-1.797.644 2.409.166.54.997-2.834 1.644-2.834-1.64.54-.997 2.409-.166-1.797-.644.54-.997 2.409-.166zM10.5 8.661l.54.997-1.797.644 2.409.166.54.997-1.797.644 2.409.166.54.997-2.834 1.644-2.834-1.64.54-.997 2.409-.166-1.797-.644.54-.997 2.409-.166zm7 0l.54.997-1.797.644 2.409.166.54.997-1.797.644 2.409.166.54.997-2.834 1.644-2.834-1.64.54-.997 2.409-.166-1.797-.644.54-.997 2.409-.166zM10.5 14.661l.54.997-1.797.644 2.409.166.54.997-1.797.644 2.409.166.54.997-2.834 1.644-2.834-1.64.54-.997 2.409-.166-1.797-.644.54-.997 2.409-.166zm7 0l.54.997-1.797.644 2.409.166.54.997-1.797.644 2.409.166.54.997-2.834 1.644-2.834-1.64.54-.997 2.409-.166-1.797-.644.54-.997 2.409-.166z"/></svg>',
  'Nginx': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0L1.608 6v12L12 24l10.392-6V6L12 0zm-1.073 1.445h.001a2.886 2.886 0 012.144 0l7.321 4.224-7.322 4.224a2.886 2.886 0 01-2.143 0L4.68 5.67l7.247-4.224zM21.119 7.39L13.8 11.61a2.886 2.886 0 01-.726.383v8.472l7.321-4.225V7.39zm-17.512 0v8.45l7.322 4.225v-8.472a2.886 2.886 0 01-.727-.383L3.607 7.39z"/></svg>',
  'AWS': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.763 10.036c0 .296.032.535.088.71.064.176.144.368.256.576.04.063.056.127.056.183 0 .08-.048.16-.152.24l-.503.335a.383.383 0 01-.208.072c-.08 0-.16-.04-.239-.112a2.47 2.47 0 01-.287-.375 6.18 6.18 0 01-.248-.471c-.622.734-1.405 1.101-2.347 1.101-.67 0-1.205-.191-1.596-.574-.391-.384-.59-.894-.59-1.533 0-.678.239-1.23.726-1.644.487-.415 1.133-.623 1.955-.623.272 0 .551.024.846.064.296.04.6.104.918.176v-.583c0-.607-.127-1.03-.375-1.277-.255-.248-.686-.367-1.3-.367-.28 0-.568.031-.863.103a6.395 6.395 0 00-.862.271 2.287 2.287 0 01-.28.104.488.488 0 01-.127.023c-.112 0-.168-.08-.168-.247v-.391c0-.128.016-.224.056-.28a.597.597 0 01.224-.167c.279-.144.614-.263 1.005-.36a4.84 4.84 0 011.246-.151c.95 0 1.644.216 2.091.647.44.43.662 1.085.662 1.963v2.586zm-3.24 1.214c.263 0 .534-.048.822-.144.287-.096.543-.271.758-.51.128-.152.224-.32.272-.512.047-.191.08-.423.08-.694v-.335a6.66 6.66 0 00-.735-.136 6.02 6.02 0 00-.75-.048c-.535 0-.926.104-1.19.32-.263.215-.39.518-.39.917 0 .375.095.655.295.846.191.2.47.295.838.295zm6.41.862c-.144 0-.24-.024-.304-.08-.064-.048-.12-.16-.168-.311L7.586 5.55a1.398 1.398 0 01-.072-.32c0-.128.064-.2.191-.2h.783c.151 0 .255.025.31.08.065.048.113.16.16.312l1.342 5.284 1.245-5.284c.04-.16.088-.264.151-.312a.549.549 0 01.32-.08h.638c.152 0 .256.025.32.08.063.048.12.16.151.312l1.261 5.348 1.381-5.348c.048-.16.104-.264.16-.312a.52.52 0 01.311-.08h.743c.127 0 .2.065.2.2 0 .04-.009.08-.017.128a1.137 1.137 0 01-.056.2l-1.923 6.17c-.048.16-.104.264-.168.312a.549.549 0 01-.303.08h-.687c-.151 0-.255-.024-.32-.08-.063-.056-.119-.16-.15-.32l-1.238-5.148-1.23 5.14c-.04.16-.087.272-.15.328-.065.056-.177.08-.32.08zm10.256.215c-.415 0-.83-.048-1.229-.143-.399-.096-.71-.2-.918-.32-.128-.071-.215-.151-.247-.223a.563.563 0 01-.048-.224v-.407c0-.167.064-.247.183-.247.048 0 .096.008.144.024.048.016.12.048.2.08.271.12.566.215.878.279.319.064.63.096.95.096.502 0 .894-.088 1.165-.264a.86.86 0 00.415-.758.777.777 0 00-.215-.559c-.144-.151-.416-.287-.807-.414l-1.157-.36c-.583-.183-1.014-.454-1.277-.813a1.902 1.902 0 01-.4-1.158c0-.335.073-.63.216-.886.144-.255.336-.479.575-.654.24-.184.51-.32.83-.415A3.72 3.72 0 0118.382 6c.215 0 .438.016.654.048.224.032.431.08.63.136.192.056.367.12.527.2.16.08.28.16.36.24a.74.74 0 01.167.207c.032.072.048.16.048.264v.375c0 .168-.064.256-.184.256a.83.83 0 01-.303-.096 3.652 3.652 0 00-1.532-.311c-.455 0-.815.071-1.062.223-.248.152-.375.383-.375.695 0 .224.08.416.24.567.159.152.454.304.878.44l1.133.358c.574.184.99.44 1.237.775.247.335.367.718.367 1.142 0 .343-.072.655-.207.926a2.16 2.16 0 01-.583.67 2.85 2.85 0 01-.862.423 4.112 4.112 0 01-1.077.144z"/></svg>',
  'PostgreSQL': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.128 0a10.134 10.134 0 00-2.755.403l-.063.02A10.922 10.922 0 0012.6.258C11.433.238 10.45.524 9.72 1 8.995.524 7.582.163 6.084.348c-.912.112-1.87.438-2.71.987C2.39 1.97 1.646 2.934 1.28 3.828c-.367.895-.46 1.722-.354 2.412.105.69.416 1.252.82 1.698.405.446.932.794 1.502 1.04.57.246 1.194.39 1.797.47.604.08 1.187.1 1.69.068.503-.032.93-.116 1.232-.223.15-.054.277-.114.374-.174.097-.06.167-.118.212-.16.045-.043.065-.07.078-.088l.002-.003.002-.002c.003-.004.008-.01.015-.015a.27.27 0 01.065-.05l.006-.003.015-.008a.213.213 0 01.06-.02l.01-.002.025-.004a.287.287 0 01.075-.002h.003a.287.287 0 01.075.002l.025.004.01.002a.213.213 0 01.06.02l.015.008.006.003a.27.27 0 01.065.05c.007.005.012.011.015.015l.002.002.002.003c.013.018.033.045.078.088.045.042.115.1.212.16.097.06.224.12.374.174.302.107.73.191 1.232.223.503.032 1.086.012 1.69-.068.603-.08 1.227-.224 1.797-.47.57-.246 1.097-.594 1.502-1.04.404-.446.715-1.008.82-1.698.106-.69.013-1.517-.354-2.412C22.354 2.934 21.61 1.97 20.626 1.355c-.84-.549-1.798-.875-2.71-.987-1.498-.185-2.911.176-3.636.652a10.134 10.134 0 01-1.475-.233A10.134 10.134 0 0017.128 0z"/></svg>',
  'WebSocket': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5"/></svg>',
  'MySQL': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 4.02 2 6.5S6.48 11 12 11s10-2.02 10-4.5S17.52 2 12 2zm0 2c3.31 0 6 1.34 6 2.5S15.31 9 12 9 6 7.66 6 6.5 8.69 4 12 4zM2 9v2c0 1.16 2.69 2 6 2s6-.84 6-2V9c0 1.16-2.69 2-6 2s-6-.84-6-2zm0 4v2c0 1.16 2.69 2 6 2s6-.84 6-2v-2c0 1.16-2.69 2-6 2s-6-.84-6-2zm0 4v2c0 1.16 2.69 2 6 2s6-.84 6-2v-2c0 1.16-2.69 2-6 2s-6-.84-6-2z"/></svg>',
}
const skillColors = {
  'Python': '#3776ab', 'JavaScript': '#f7df1e', 'TypeScript': '#3178c6', 'Vue.js': '#42b883',
  'React': '#61dafb', 'Flask': '#000000', 'SQL': '#e48e00', 'Docker': '#2496ed',
  'Git': '#f05032', 'Linux': '#fcc624', 'CI/CD': '#4caf50', 'Redis': '#dc382d',
  'Nginx': '#009639', 'AWS': '#ff9900', 'PostgreSQL': '#336791', 'WebSocket': '#ff6b35',
  'MySQL': '#4479a1',
}
const skillCategories = computed(() => {
  const map = {}
  resume.skills.forEach(name => {
    const cat = name.match(/^(Python|JavaScript|TypeScript|Vue\.js|React|Flask|SQL|Docker|Git|Linux|CI\/CD|Redis|Nginx|AWS|PostgreSQL|WebSocket|MySQL)$/)?.[0]
    const category = ['Python', 'Flask'].includes(name) ? '后端开发'
      : ['JavaScript', 'TypeScript', 'Vue.js', 'React'].includes(name) ? '前端开发'
      : ['Docker', 'Linux', 'Nginx', 'AWS', 'CI/CD'].includes(name) ? 'DevOps & 云'
      : ['SQL', 'PostgreSQL', 'MySQL', 'Redis'].includes(name) ? '数据库'
      : ['Git', 'WebSocket'].includes(name) ? '工具 & 协议'
      : '其他'
    if (!map[category]) map[category] = []
    map[category].push({
      name,
      color: skillColors[name] || 'var(--accent)',
      icon: skillSVGs[name] || '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>'
    })
  })
  const order = ['前端开发', '后端开发', '数据库', 'DevOps & 云', '工具 & 协议', '其他']
  return order.filter(k => map[k]).map(k => ({ name: k, skills: map[k] }))
})

// IntersectionObserver 实现滚动入场动画
const timelineRefs = ref({})
let observer = null

function setupObserver() {
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const idx = Object.keys(timelineRefs.value).find(k => timelineRefs.value[k] === entry.target)
        if (idx !== undefined) {
          timelineItems[idx].visible = true
        }
      }
    })
  }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' })

  nextTick(() => {
    Object.values(timelineRefs.value).forEach(el => {
      if (el) observer.observe(el)
    })
  })
}

// 编辑功能
const showEditForm = ref(false)
const editingSection = ref('')
const editForm = ref({})
const sectionNames = { header: '头部信息', work: '工作经历', education: '教育背景', skills: '技能栈' }
const editingSectionName = ref('')

const editSection = (s) => {
  editingSection.value = s
  editingSectionName.value = sectionNames[s] || s
  if (s === 'header') editForm.value = { title: resume.title, subtitle: resume.subtitle, email: resume.email, github: resume.github }
  else if (s === 'skills') editForm.value = { skillsStr: resume.skills.join(', ') }
  showEditForm.value = true
}
const closeEditForm = () => { showEditForm.value = false; editForm.value = {} }
const saveResume = async () => {
  try {
    if (editingSection.value === 'header') {
      resume.title = editForm.value.title
      resume.subtitle = editForm.value.subtitle
      resume.email = editForm.value.email
      resume.github = editForm.value.github
    } else if (editingSection.value === 'skills') {
      resume.skills = editForm.value.skillsStr.split(',').map(s => s.trim()).filter(s => s)
    }
    await updateResume({ ...resume })
    buildTimeline()
    closeEditForm()
    alert('保存成功！')
  } catch (e) { alert('保存失败：' + (e.response?.data?.error || e.message)) }
}

const loadResume = async () => {
  try {
    const d = await getResume()
    if (d && Object.keys(d).length > 0) Object.assign(resume, d)
  } catch (e) { console.error('加载简历数据失败', e) }
  buildTimeline()
  nextTick(setupObserver)
}

onMounted(loadResume)
onUnmounted(() => { if (observer) observer.disconnect() })
</script>

<style scoped>
/* ============================================================
   时间轴布局
   ============================================================ */
.timeline-container {
  position: relative;
  padding: 20px 0;
}

/* 中线 */
.timeline-line {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, transparent, var(--border-color) 5%, var(--border-color) 95%, transparent);
  transform: translateX(-50%);
}

/* 时间轴节点 */
.timeline-item {
  position: relative;
  width: 50%;
  padding: 0 40px 60px;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.timeline-item.timeline-visible {
  opacity: 1;
  transform: translateY(0);
}

/* 左侧节点 */
.timeline-left {
  left: 0;
  padding-right: 60px;
  text-align: right;
}

.timeline-left .timeline-card {
  text-align: left;
}

.timeline-left .timeline-date {
  position: absolute;
  right: -70px;
  top: 8px;
  text-align: left;
}

/* 右侧节点 */
.timeline-right {
  left: 50%;
  padding-left: 60px;
  text-align: left;
}

.timeline-right .timeline-date {
  position: absolute;
  left: -70px;
  top: 8px;
  text-align: right;
}

/* 时间节点圆点 */
.timeline-dot {
  position: absolute;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  box-shadow: 0 0 0 4px var(--bg-primary), 0 0 15px rgba(3, 105, 161, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.timeline-left .timeline-dot {
  right: -18px;
}

.timeline-right .timeline-dot {
  left: -18px;
}

.timeline-item:hover .timeline-dot {
  transform: scale(1.15);
  box-shadow: 0 0 0 4px var(--bg-primary), 0 0 25px rgba(3, 105, 161, 0.5);
}

.timeline-dot-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 内容卡片 */
.timeline-card {
  position: relative;
  padding: 24px;
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.timeline-card:hover {
  transform: translateY(-2px);
}

/* 时间标签 */
.timeline-date {
  white-space: nowrap;
}

/* 暗色模式圆点阴影增强 */
.dark .timeline-dot {
  box-shadow: 0 0 0 4px var(--bg-primary), 0 0 15px rgba(0, 243, 255, 0.3);
}

.dark .timeline-item:hover .timeline-dot {
  box-shadow: 0 0 0 4px var(--bg-primary), 0 0 25px rgba(0, 243, 255, 0.5);
}

/* ============================================================
   响应式：移动端改为单列
   ============================================================ */
@media (max-width: 768px) {
  .timeline-line {
    left: 20px;
  }

  .timeline-item {
    width: 100%;
    padding-left: 60px;
    padding-right: 16px;
    text-align: left;
  }

  .timeline-left,
  .timeline-right {
    left: 0;
    padding-left: 60px;
    padding-right: 16px;
    text-align: left;
  }

  .timeline-left .timeline-dot,
  .timeline-right .timeline-dot {
    left: 2px;
    right: auto;
  }

  .timeline-left .timeline-date,
  .timeline-right .timeline-date {
    position: relative;
    left: auto;
    right: auto;
    text-align: left;
    margin-bottom: 4px;
  }
}

/* ============================================================
   入场动画
   ============================================================ */
.animate-fade-in {
  animation: fadeInUp 0.8s ease-out forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================================
   技能图标网格
   ============================================================ */
.skill-icon-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 12px;
  cursor: default;
  transition: all 0.3s ease;
  position: relative;
  background: var(--bg-secondary, rgba(148,163,184,0.04));
  border: 1px solid var(--border-color);
}

.skill-icon-card:hover {
  transform: translateY(-4px) scale(1.05);
  border-color: var(--skill-color);
  box-shadow: 0 0 20px color-mix(in srgb, var(--skill-color) 20%, transparent),
              0 4px 12px rgba(0,0,0,0.1);
}

.skill-icon-card:hover .skill-name {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

.skill-icon-card:hover .skill-icon {
  color: var(--skill-color);
}

.skill-icon {
  width: 28px;
  height: 28px;
  color: var(--text-secondary);
  transition: color 0.3s ease;
}

.skill-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.skill-name {
  position: absolute;
  bottom: -24px;
  left: 50%;
  transform: translateX(-50%) translateY(-4px);
  font-size: 10px;
  font-family: monospace;
  white-space: nowrap;
  color: var(--text-secondary);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}
</style>
