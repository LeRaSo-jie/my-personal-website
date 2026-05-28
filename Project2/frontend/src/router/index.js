import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ResumeView from '../views/ResumeView.vue'
import PortfolioView from '../views/PortfolioView.vue'
import ToolsView from '../views/ToolsView.vue'
import LogsView from '../views/LogsView.vue'
import BlogView from '../views/BlogView.vue'
import CodeActivityView from '../views/CodeActivityView.vue'
import PlaygroundView from '../views/PlaygroundView.vue'
import NotFoundView from '../views/NotFoundView.vue'

// 路由配置
const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/resume', name: 'resume', component: ResumeView },
  { path: '/portfolio', name: 'portfolio', component: PortfolioView },
  { path: '/tools', name: 'tools', component: ToolsView },
  { path: '/downloads', redirect: '/tools?tab=downloads' },
  { path: '/logs', name: 'logs', component: LogsView },
  { path: '/blog', name: 'blog', component: BlogView },
  { path: '/code', name: 'code', component: CodeActivityView },
  { path: '/playground', name: 'playground', component: PlaygroundView },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
  // 滚动行为：切换页面时滚动到顶部
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

export default router