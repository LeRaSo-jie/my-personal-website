<template>
  <div class="not-found-container">
    <!-- 动态背景粒子 -->
    <div class="particles">
      <div v-for="i in 20" :key="i" class="particle" :style="particleStyle(i)" />
    </div>

    <!-- 主内容 -->
    <div class="content-wrapper">
      <!-- 404 大字 -->
      <div class="glitch-wrapper">
        <h1 class="glitch-text" data-text="404">404</h1>
      </div>

      <!-- 终端风格错误信息 -->
      <div class="terminal-box">
        <div class="terminal-header">
          <span class="dot red" />
          <span class="dot yellow" />
          <span class="dot green" />
          <span class="terminal-title">error.log</span>
        </div>
        <div class="terminal-body">
          <p class="terminal-line">
            <span class="prompt">system@portfolio</span>:<span class="path">~</span>$ 
            <span class="cmd">navigate {{ $route.path }}</span>
          </p>
          <p class="terminal-line error">
            <span class="prefix">ERROR</span> 404: 页面未找到
          </p>
          <p class="terminal-line warn">
            <span class="prefix">WARN</span> 该路径不存在于已知维度中
          </p>
          <p class="terminal-line info">
            <span class="prefix">INFO</span> 建议返回首页重新导航
          </p>
          <p class="terminal-line">
            <span class="prompt">system@portfolio</span>:<span class="path">~</span>$ 
            <span class="cursor">_</span>
          </p>
        </div>
      </div>

      <!-- ASCII Art -->
      <pre class="ascii-art">
   ╔══════════════════════════════════╗
   ║  迷路了吗？这里什么都没有...     ║
   ║  也许你可以试试以下操作：        ║
   ╚══════════════════════════════════╝
      </pre>

      <!-- 操作按钮 -->
      <div class="actions">
        <router-link to="/" class="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
            <polyline points="9,22 9,12 15,12 15,22" />
          </svg>
          返回首页
        </router-link>
        <button class="btn btn-secondary" @click="goBack">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15,18 9,12 15,6" />
          </svg>
          返回上一页
        </button>
        <router-link to="/playground" class="btn btn-accent">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5,3 19,12 5,21" />
          </svg>
          去探索彩蛋
        </router-link>
      </div>

      <!-- 随机程序员名言 -->
      <div class="quote-box">
        <p class="quote-text">"{{ randomQuote.text }}"</p>
        <p class="quote-author">— {{ randomQuote.author }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const quotes = [
  { text: '在代码的世界里，404 只是另一个待解决的 bug。', author: '匿名程序员' },
  { text: '不是迷路了，只是发现了一条没人走过的路。', author: '探险家程序员' },
  { text: '每一个 404 背后，都藏着一个未被发现的功能。', author: '乐观主义者' },
  { text: 'Life is like a box of chocolates. You never know what URL you gonna get.', author: '阿甘·程序员' },
  { text: '404: 生活的意义暂时无法找到，请稍后再试。', author: '哲学家程序员' },
  { text: '最好的代码是不需要写的代码，最好的页面是不存在的页面。', author: '禅师' },
  { text: '这页就像我的头发一样——不见了。', author: '秃头程序员' },
]

const randomQuote = ref(quotes[Math.floor(Math.random() * quotes.length)])

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}

const particleStyle = (i) => {
  const x = Math.random() * 100
  const y = Math.random() * 100
  const size = Math.random() * 4 + 2
  const duration = Math.random() * 10 + 10
  const delay = Math.random() * 5
  const colors = ['#00f0ff', '#ff00e5', '#39ff14', '#ff6600', '#f0f']
  const color = colors[i % colors.length]
  return {
    left: `${x}%`,
    top: `${y}%`,
    width: `${size}px`,
    height: `${size}px`,
    background: color,
    boxShadow: `0 0 ${size * 2}px ${color}`,
    animationDuration: `${duration}s`,
    animationDelay: `${delay}s`,
  }
}
</script>

<style scoped>
.not-found-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 2rem;
  background: var(--bg-primary, #0a0a0f);
}

/* 粒子 */
.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.particle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.6;
  animation: float-particle linear infinite;
}
@keyframes float-particle {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.6; }
  25% { transform: translate(20px, -30px) scale(1.2); opacity: 1; }
  50% { transform: translate(-10px, -60px) scale(0.8); opacity: 0.4; }
  75% { transform: translate(30px, -20px) scale(1.1); opacity: 0.8; }
}

.content-wrapper {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 600px;
  width: 100%;
}

/* Glitch 404 */
.glitch-wrapper {
  margin-bottom: 2rem;
}
.glitch-text {
  font-size: 8rem;
  font-weight: 900;
  font-family: 'Courier New', monospace;
  color: var(--text-primary, #e0e0e0);
  position: relative;
  animation: glitch-skew 4s infinite linear alternate-reverse;
  text-shadow:
    0 0 20px rgba(0, 240, 255, 0.5),
    0 0 40px rgba(0, 240, 255, 0.3);
}
.glitch-text::before,
.glitch-text::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.glitch-text::before {
  color: #ff00e5;
  animation: glitch-1 2s infinite linear alternate-reverse;
  clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
}
.glitch-text::after {
  color: #00f0ff;
  animation: glitch-2 2s infinite linear alternate-reverse;
  clip-path: polygon(0 66%, 100% 66%, 100% 100%, 0 100%);
}
@keyframes glitch-1 {
  0%, 90%, 100% { transform: translate(0); }
  92% { transform: translate(-5px, 2px); }
  94% { transform: translate(5px, -2px); }
  96% { transform: translate(-3px, 1px); }
  98% { transform: translate(3px, -1px); }
}
@keyframes glitch-2 {
  0%, 90%, 100% { transform: translate(0); }
  91% { transform: translate(4px, -2px); }
  93% { transform: translate(-4px, 2px); }
  95% { transform: translate(2px, 1px); }
  97% { transform: translate(-2px, -1px); }
}
@keyframes glitch-skew {
  0%, 95%, 100% { transform: skew(0deg); }
  96% { transform: skew(2deg); }
  97% { transform: skew(-1deg); }
  98% { transform: skew(1deg); }
}

/* 终端 */
.terminal-box {
  border: 1px solid rgba(0, 240, 255, 0.2);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  text-align: left;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
}
.terminal-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.dot.red { background: #ff5f57; }
.dot.yellow { background: #febc2e; }
.dot.green { background: #28c840; }
.terminal-title {
  margin-left: auto;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  font-family: 'Courier New', monospace;
}
.terminal-body {
  padding: 1rem;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.8;
}
.terminal-line {
  color: var(--text-secondary, #aaa);
  margin: 0;
}
.prompt {
  color: #39ff14;
}
.path {
  color: #00f0ff;
}
.cmd {
  color: #ff00e5;
}
.terminal-line.error .prefix {
  color: #ff5f57;
  font-weight: bold;
}
.terminal-line.warn .prefix {
  color: #febc2e;
  font-weight: bold;
}
.terminal-line.info .prefix {
  color: #00f0ff;
  font-weight: bold;
}
.cursor {
  animation: blink 1s step-end infinite;
  color: #39ff14;
}
@keyframes blink {
  50% { opacity: 0; }
}

/* ASCII Art */
.ascii-art {
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: var(--text-secondary, #888);
  margin-bottom: 2rem;
  white-space: pre;
  line-height: 1.5;
}

/* 按钮 */
.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
  border: 1px solid transparent;
}
.btn-primary {
  background: linear-gradient(135deg, #00f0ff, #0080ff);
  color: #000;
  border-color: #00f0ff;
}
.btn-primary:hover {
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.5);
  transform: translateY(-2px);
}
.btn-secondary {
  background: transparent;
  color: var(--text-primary, #e0e0e0);
  border-color: rgba(255, 255, 255, 0.2);
}
.btn-secondary:hover {
  border-color: #ff00e5;
  color: #ff00e5;
  box-shadow: 0 0 15px rgba(255, 0, 229, 0.3);
}
.btn-accent {
  background: linear-gradient(135deg, #ff00e5, #ff6600);
  color: #fff;
  border-color: #ff00e5;
}
.btn-accent:hover {
  box-shadow: 0 0 20px rgba(255, 0, 229, 0.5);
  transform: translateY(-2px);
}

/* 名言 */
.quote-box {
  padding: 1.5rem;
  border-left: 3px solid #00f0ff;
  background: rgba(0, 240, 255, 0.05);
  border-radius: 0 8px 8px 0;
  text-align: left;
}
.quote-text {
  font-style: italic;
  color: var(--text-primary, #e0e0e0);
  margin: 0 0 0.5rem;
  font-size: 0.95rem;
  line-height: 1.6;
}
.quote-author {
  color: var(--text-secondary, #888);
  margin: 0;
  font-size: 0.8rem;
}

/* 响应式 */
@media (max-width: 640px) {
  .glitch-text {
    font-size: 5rem;
  }
  .actions {
    flex-direction: column;
    align-items: center;
  }
  .btn {
    width: 100%;
    max-width: 250px;
    justify-content: center;
  }
}
</style>