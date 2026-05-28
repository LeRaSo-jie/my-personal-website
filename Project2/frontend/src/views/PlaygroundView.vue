<template>
  <div class="min-h-screen pt-20 pb-16 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- 页面头部 -->
      <div class="text-center mb-12 animate-fade-in">
        <span class="inline-block px-4 py-1.5 rounded-full text-xs font-mono tracking-wider mb-4"
              style="background: rgba(236,72,153,0.08); border: 1px solid rgba(236,72,153,0.2); color: #ec4899;">
          // PLAYGROUND
        </span>
        <h1 class="text-4xl md:text-5xl font-bold font-mono gradient-text">互动彩蛋</h1>
        <p class="text-sm font-mono mt-2" style="color: var(--text-muted);">// hidden gems for curious minds</p>
      </div>

      <!-- 彩蛋网格 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <div
          v-for="(egg, index) in eggs"
          :key="egg.name"
          class="card-neon p-6 cursor-pointer group relative overflow-hidden"
          :style="{ animationDelay: `${index * 0.1}s` }"
          @click="activateEgg(egg)"
        >
          <div class="absolute top-0 left-0 right-0 h-0.5 transition-opacity"
               :style="{ background: `linear-gradient(to right, ${egg.color}, transparent)`, opacity: activeEgg === egg.name ? 1 : 0 }"></div>

          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 transition-all duration-300 group-hover:scale-110"
                 :style="{ background: egg.color + '15', border: `1px solid ${egg.color}25` }">
              <span class="text-2xl">{{ egg.emoji }}</span>
            </div>
            <div>
              <h3 class="text-lg font-bold font-mono mb-1 group-hover:text-neon transition-colors" style="color: var(--text-primary);">
                {{ egg.name }}
              </h3>
              <p class="text-sm" style="color: var(--text-secondary);">{{ egg.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 活动区域 -->
      <div v-if="activeEgg" class="card-neon p-8 animate-fade-in">
        <h2 class="text-2xl font-bold font-mono mb-6 text-center" style="color: var(--text-primary);">
          <span style="color: var(--accent);">></span> {{ activeEgg }}
        </h2>

        <!-- Konami Code -->
        <div v-if="activeEgg === 'Konami Code'" class="text-center">
          <p class="font-mono text-sm mb-4" style="color: var(--text-secondary);">
            输入经典 Konami 指令序列：
          </p>
          <div class="flex justify-center gap-2 mb-4">
            <span v-for="(key, i) in konamiProgress" :key="i"
                  class="w-10 h-10 rounded-lg flex items-center justify-center font-mono text-sm font-bold"
                  :style="{ background: 'var(--accent)', color: '#fff' }">
              {{ key }}
            </span>
            <span v-for="i in (8 - konamiProgress.length)" :key="'p'+i"
                  class="w-10 h-10 rounded-lg flex items-center justify-center font-mono text-sm"
                  style="background: var(--border-color); color: var(--text-muted);">
              ?
            </span>
          </div>
          <p v-if="konamiComplete" class="text-lg font-mono font-bold animate-bounce" style="color: #f59e0b;">
            🎉 恭喜！你发现了隐藏彩蛋！
          </p>
        </div>

        <!-- 贪吃蛇 -->
        <div v-if="activeEgg === '像素贪吃蛇'" class="text-center">
          <div class="inline-block rounded-xl overflow-hidden mb-4" style="border: 2px solid var(--border-color);">
            <canvas ref="snakeCanvas" width="300" height="300" class="block"></canvas>
          </div>
          <p class="font-mono text-sm" style="color: var(--text-muted);">
            使用 <span class="help-key">↑↓←→</span> 方向键控制 · 得分: <span style="color: var(--accent);">{{ snakeScore }}</span>
          </p>
          <button @click="startSnake" class="btn-primary mt-3 font-mono text-sm">
            {{ snakePlaying ? '重新开始' : '开始游戏' }}
          </button>
        </div>

        <!-- 打字速度测试 -->
        <div v-if="activeEgg === '打字速度'" class="text-center">
          <p class="font-mono text-sm mb-4" style="color: var(--text-secondary);">
            输入以下文字，测试你的打字速度：
          </p>
          <div class="p-4 rounded-xl mb-4" style="background: rgba(148,163,184,0.04); border: 1px solid var(--border-color);">
            <p class="font-mono text-lg leading-relaxed" style="color: var(--text-primary);">
              <span v-for="(char, i) in typingText" :key="i"
                    :style="{ color: i < typingIndex ? (typingErrors.includes(i) ? '#ef4444' : '#10b981') : 'var(--text-muted)' }">
                {{ char }}
              </span>
            </p>
          </div>
          <input
            v-model="typingInput"
            @input="checkTyping"
            class="input-cyber text-center font-mono text-lg w-full max-w-md"
            placeholder="开始输入..."
            :disabled="typingComplete"
          />
          <div v-if="typingComplete" class="mt-4">
            <p class="font-mono text-lg font-bold" style="color: var(--accent);">
              {{ typingWPM }} WPM · 准确率 {{ typingAccuracy }}%
            </p>
          </div>
        </div>

        <!-- 随机颜色生成器 -->
        <div v-if="activeEgg === '调色板'" class="text-center">
          <div class="flex flex-wrap justify-center gap-3 mb-6">
            <div
              v-for="(color, i) in paletteColors"
              :key="i"
              class="w-20 h-20 rounded-xl cursor-pointer transition-transform hover:scale-110 flex items-end justify-center pb-2"
              :style="{ background: color }"
              @click="copyColor(color)"
            >
              <span class="text-[10px] font-mono font-bold" style="color: rgba(255,255,255,0.8);">{{ color }}</span>
            </div>
          </div>
          <button @click="generatePalette" class="btn-primary font-mono">
            🎨 生成新配色
          </button>
          <p v-if="copiedColor" class="mt-3 font-mono text-sm" style="color: var(--accent);">
            已复制 {{ copiedColor }} ✓
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const eggs = [
  { name: 'Konami Code', description: '输入经典游戏秘籍 ↑↑↓↓←→←→BA', emoji: '🎮', color: '#ef4444' },
  { name: '像素贪吃蛇', description: '在浏览器里玩经典贪吃蛇游戏', emoji: '🐍', color: '#10b981' },
  { name: '打字速度', description: '测试你的编程键盘打字速度', emoji: '⌨️', color: '#8b5cf6' },
  { name: '调色板', description: '随机生成赛博朋克风格配色方案', emoji: '🎨', color: '#ec4899' }
]

const activeEgg = ref(null)
const activateEgg = (egg) => { activeEgg.value = egg.name }

// Konami Code
const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a']
const konamiLabels = ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A']
const konamiProgress = ref([])
const konamiComplete = ref(false)

const handleKonami = (e) => {
  if (activeEgg.value !== 'Konami Code') return
  const expected = konamiCode[konamiProgress.value.length]
  if (e.key === expected) {
    konamiProgress.value.push(konamiLabels[konamiProgress.value.length])
    if (konamiProgress.value.length === 8) konamiComplete.value = true
  } else {
    konamiProgress.value = []
  }
}

// 贪吃蛇
const snakeCanvas = ref(null)
const snakeScore = ref(0)
const snakePlaying = ref(false)
let snakeInterval = null
let snake = []
let food = null
let direction = { x: 1, y: 0 }
const GRID = 15

const startSnake = () => {
  snakePlaying.value = true
  snakeScore.value = 0
  snake = [{ x: 5, y: 5 }]
  direction = { x: 1, y: 0 }
  placeFood()
  if (snakeInterval) clearInterval(snakeInterval)
  snakeInterval = setInterval(snakeStep, 150)
}

const placeFood = () => {
  food = { x: Math.floor(Math.random() * (300 / GRID)), y: Math.floor(Math.random() * (300 / GRID)) }
}

const snakeStep = () => {
  const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y }
  if (head.x < 0 || head.x >= 300 / GRID || head.y < 0 || head.y >= 300 / GRID || snake.some(s => s.x === head.x && s.y === head.y)) {
    clearInterval(snakeInterval)
    snakePlaying.value = false
    return
  }
  snake.unshift(head)
  if (head.x === food.x && head.y === food.y) {
    snakeScore.value += 10
    placeFood()
  } else {
    snake.pop()
  }
  drawSnake()
}

const drawSnake = () => {
  const ctx = snakeCanvas.value?.getContext('2d')
  if (!ctx) return
  ctx.fillStyle = '#0f172a'
  ctx.fillRect(0, 0, 300, 300)
  ctx.fillStyle = '#ef4444'
  ctx.fillRect(food.x * GRID, food.y * GRID, GRID - 1, GRID - 1)
  snake.forEach((s, i) => {
    ctx.fillStyle = i === 0 ? '#0ea5e9' : '#0284c7'
    ctx.fillRect(s.x * GRID, s.y * GRID, GRID - 1, GRID - 1)
  })
}

const handleSnakeKeys = (e) => {
  if (activeEgg.value !== '像素贪吃蛇' || !snakePlaying.value) return
  const map = { ArrowUp: { x: 0, y: -1 }, ArrowDown: { x: 0, y: 1 }, ArrowLeft: { x: -1, y: 0 }, ArrowRight: { x: 1, y: 0 } }
  if (map[e.key] && !(map[e.key].x === -direction.x && map[e.key].y === -direction.y)) {
    direction = map[e.key]
    e.preventDefault()
  }
}

// 打字速度
const typingText = 'The quick brown fox jumps over the lazy dog. Code is poetry written in logic.'
const typingInput = ref('')
const typingIndex = ref(0)
const typingErrors = ref([])
const typingComplete = ref(false)
const typingStartTime = ref(null)
const typingWPM = ref(0)
const typingAccuracy = ref(100)

const checkTyping = () => {
  if (!typingStartTime.value) typingStartTime.value = Date.now()
  typingIndex.value = typingInput.value.length
  typingErrors.value = []
  for (let i = 0; i < typingInput.value.length; i++) {
    if (typingInput.value[i] !== typingText[i]) typingErrors.value.push(i)
  }
  if (typingInput.value.length >= typingText.length) {
    typingComplete.value = true
    const elapsed = (Date.now() - typingStartTime.value) / 60000
    const words = typingText.split(' ').length
    typingWPM.value = Math.round(words / elapsed)
    typingAccuracy.value = Math.round(((typingText.length - typingErrors.value.length) / typingText.length) * 100)
  }
}

// 调色板
const paletteColors = ref([])
const copiedColor = ref(null)

const generatePalette = () => {
  const hue = Math.random() * 360
  paletteColors.value = Array.from({ length: 6 }, (_, i) => {
    const h = (hue + i * 30 + Math.random() * 20) % 360
    const s = 60 + Math.random() * 30
    const l = 40 + Math.random() * 30
    return `hsl(${Math.round(h)}, ${Math.round(s)}%, ${Math.round(l)}%)`
  })
}

const copyColor = (color) => {
  navigator.clipboard?.writeText(color)
  copiedColor.value = color
  setTimeout(() => { copiedColor.value = null }, 2000)
}

onMounted(() => {
  document.addEventListener('keydown', handleKonami)
  document.addEventListener('keydown', handleSnakeKeys)
  generatePalette()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKonami)
  document.removeEventListener('keydown', handleSnakeKeys)
  if (snakeInterval) clearInterval(snakeInterval)
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.help-key {
  padding: 1px 6px;
  border-radius: 3px;
  background: rgba(148, 163, 184, 0.08);
  border: 1px solid rgba(148, 163, 184, 0.12);
  font-family: monospace;
  font-size: 11px;
  color: var(--text-primary);
}

.animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
</style>
