<template>
  <footer class="relative py-10" style="border-top: 1px solid var(--border-color); background: var(--bg-secondary);">
    <div class="absolute top-0 left-0 right-0 h-px" style="background: linear-gradient(90deg, transparent, rgba(14, 165, 233, 0.15), rgba(139, 92, 246, 0.15), transparent);"></div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 随机程序员名言 -->
      <div class="text-center mb-6">
        <Transition name="quote" mode="out-in">
          <p :key="currentQuoteIndex" class="text-sm font-mono italic max-w-2xl mx-auto" style="color: var(--text-tertiary);">
            <span class="text-neon opacity-40">"</span>
            {{ quotes[currentQuoteIndex].text }}
            <span class="text-neon opacity-40">"</span>
            <span class="block mt-1 text-xs opacity-60">— {{ quotes[currentQuoteIndex].author }}</span>
          </p>
        </Transition>
      </div>

      <div class="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
        <!-- 左侧：版权信息 -->
        <div class="text-center md:text-left">
          <p class="text-sm font-mono" style="color: var(--text-muted);">
            <span class="text-neon opacity-40">></span> © {{ currentYear }} DIGITAL NEXUS
            <span class="mx-2 opacity-30">|</span>
            <span>Built with Vue.js & Flask</span>
          </p>
        </div>

        <!-- 中间：访客计数器 -->
        <div class="flex items-center gap-3 px-4 py-2 rounded-lg font-mono text-xs" style="background: rgba(0, 240, 255, 0.04); border: 1px solid rgba(0, 240, 255, 0.1);">
          <svg class="w-4 h-4 text-neon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          <span style="color: var(--text-tertiary);">VISITORS:</span>
          <span class="text-neon font-bold tracking-wider">{{ formattedVisitorCount }}</span>
        </div>

        <!-- 右侧：状态和链接 -->
        <div class="flex items-center space-x-6">
          <div class="flex items-center gap-2 text-xs font-mono" style="color: var(--text-muted);">
            <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
            <span>SYSTEM ONLINE</span>
          </div>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer"
             class="transition-colors duration-300 text-neon" title="GitHub">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
          </a>
          <a href="https://gitee.com" target="_blank" rel="noopener noreferrer"
             class="transition-colors duration-300 hover:opacity-100 opacity-70" style="color: #c71d23;" title="Gitee">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M11.984 0C5.372 0 0 5.372 0 11.984c0 6.612 5.372 11.984 11.984 11.984 6.612 0 11.984-5.372 11.984-11.984C23.968 5.372 18.596 0 11.984 0zM9.062 18.628c-3.27 0-5.92-2.028-6.884-4.864h3.576c.712 1.44 2.184 2.424 3.88 2.424 2.388 0 4.32-1.932 4.32-4.32 0-2.388-1.932-4.32-4.32-4.32-1.696 0-3.168.984-3.88 2.424H2.178c.964-2.836 3.614-4.864 6.884-4.864 4.036 0 7.308 3.272 7.308 7.308 0 4.036-3.272 7.308-7.308 7.308z"/>
            </svg>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const currentYear = new Date().getFullYear()

// 随机程序员名言
const quotes = [
  { text: 'Talk is cheap. Show me the code.', author: 'Linus Torvalds' },
  { text: '任何足够先进的技术都与魔法无异。', author: 'Arthur C. Clarke' },
  { text: '先让它工作，再让它正确，最后让它快。', author: 'Kent Beck' },
  { text: '程序必须写给人看，其次才是让机器执行。', author: 'Abelson & Sussman' },
  { text: '过早优化是万恶之源。', author: 'Donald Knuth' },
  { text: '简单是可靠的先决条件。', author: 'Edsger Dijkstra' },
  { text: '好的程序员是那种过着平淡生活的人。', author: '陈皓' },
  { text: '代码是写给人看的，附带能在机器上运行。', author: 'Martin Fowler' },
  { text: '没有银弹。', author: 'Fred Brooks' },
  { text: '调试代码比写代码难两倍。所以，如果你写代码时尽可能聪明，那你就不够资格调试它。', author: 'Brian Kernighan' },
  { text: 'UNIX 是简单的，但需要天才才能理解它的简单。', author: 'Dennis Ritchie' },
  { text: '世界上只有两种语言：人们抱怨的语言和没人用的语言。', author: 'Bjarne Stroustrup' },
  { text: '软件就像熵一样：很难理解、无法度量，而且不会减少。', author: 'Norman Augustine' },
  { text: '最能误导人的就是那种「大部分正确」的代码。', author: 'Steve Maguire' },
  { text: '首先，解决好问题。然后，写好代码。', author: 'John Johnson' },
  { text: '如果你不能向一个六岁的孩子解释清楚，那你自己也没有真正理解它。', author: 'Albert Einstein' },
  { text: '测量不了的东西就无法改进。', author: 'Peter Drucker' },
  { text: '程序员和上帝打赌要写一个没有 Bug 的程序，上帝笑了。', author: '佚名' },
  { text: '不要重复你自己。', author: 'Andy Hunt & Dave Thomas' },
  { text: '好的代码本身就是最好的文档。', author: 'Steve McConnell' },
  { text: '唯一不变的就是变化本身。', author: 'Heraclitus' },
  { text: '软件设计的核心在于控制复杂度。', author: 'John Ousterhout' },
  { text: '编程不是关于你知道什么，而是关于你能想出什么。', author: 'Chris Pine' },
  { text: '在软件中，最容易被忽略的成本是认知成本。', author: 'Rich Hickey' },
  { text: '每一行代码都是一封写给未来的信。', author: 'Robert C. Martin' },
  { text: '完美不是「无可增添」，而是「无可删减」。', author: 'Antoine de Saint-Exupéry' },
  { text: 'Make it work, make it right, make it fast. In that order.', author: 'Kent Beck' },
  { text: '任何 Bug 都可以在一行代码里找到，只不过你需要看另外一千行来确定是哪行。', author: '佚名' },
  { text: '代码是给人读的，顺便给机器跑一下。', author: 'Harold Abelson' },
  { text: '给我六个小时砍一棵树，我会花前四个小时磨斧头。', author: 'Abraham Lincoln' },
  { text: '真正的程序员不用注释——代码本身就难以理解。', author: '佚名' },
  { text: '世界上最危险的一句话是：我们一直都是这样做的。', author: 'Grace Hopper' },
  { text: '不是所有的代码都需要写，最好的代码是不写的代码。', author: '佚名' },
  { text: '解决问题的能力，才是程序员最核心的竞争力。', author: '吴军' },
  { text: '把程序写好，就是把故事讲好。', author: 'Paul Graham' },
  { text: 'Simplicity is prerequisite for reliability.', author: 'Edsger Dijkstra' },
  { text: '最好的架构源于实践，最好的代码源于思考。', author: 'Martin Fowler' },
  { text: '有两种方式写没有 Bug 的程序，但只有第三种方式能让它运行。', author: 'C.A.R. Hoare' },
  { text: '软件开发中最难的部分不是写代码，而是理解需求。', author: 'Frederick Brooks' },
  { text: '一万小时定律没有捷径，但有方向。', author: 'Malcolm Gladwell' },
  { text: 'Not all those who wander are lost — but all who code do debug.', author: 'J.R.R. Tolkien (改编)' },
  { text: '测试能证明缺陷的存在，但不能证明缺陷的不存在。', author: 'Edsger Dijkstra' },
  { text: '优秀是一种习惯，代码是一种表达。', author: 'Aristotle (改编)' },
  { text: 'The best error message is the one that never shows up.', author: 'Thomas Fuchs' },
  { text: '代码之外，也要读诗、散步、发呆。', author: '佚名' },
]

const currentQuoteIndex = ref(Math.floor(Math.random() * quotes.length))
let quoteTimer = null

// 访客计数器
const visitorCount = ref(0)

const formattedVisitorCount = computed(() => {
  return visitorCount.value.toString().padStart(6, '0')
})

// 模拟访客计数（实际项目中可对接后端 API）
const initVisitorCount = () => {
  // 从 localStorage 读取
  const stored = localStorage.getItem('visitor_count')
  if (stored) {
    visitorCount.value = parseInt(stored)
  } else {
    // 初始值：模拟一个合理的基数
    visitorCount.value = 13847
  }

  // 检查是否是本次会话的首次访问
  const sessionVisited = sessionStorage.getItem('visited')
  if (!sessionVisited) {
    sessionStorage.setItem('visited', 'true')
    visitorCount.value++
    localStorage.setItem('visitor_count', visitorCount.value.toString())
  }
}

onMounted(() => {
  initVisitorCount()
  // 每 15 秒切换名言
  quoteTimer = setInterval(() => {
    currentQuoteIndex.value = (currentQuoteIndex.value + 1) % quotes.length
  }, 15000)
})

onUnmounted(() => {
  if (quoteTimer) clearInterval(quoteTimer)
})
</script>

<style scoped>
/* 名言切换动画 */
.quote-enter-active {
  transition: all 0.4s ease;
}
.quote-leave-active {
  transition: all 0.3s ease;
}
.quote-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.quote-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
