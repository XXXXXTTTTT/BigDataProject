import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '数据概览',
      keepAlive: true
    }
  },
  {
    path: '/uploader',
    name: 'UploaderAnalysis',
    component: () => import('@/views/UploaderAnalysis.vue'),
    meta: {
      title: 'UP主分析',
      keepAlive: true
    }
  },
  {
    path: '/video',
    name: 'VideoAnalysis',
    component: () => import('@/views/VideoAnalysis.vue'),
    meta: {
      title: '视频分析',
      keepAlive: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} - B站数据分析平台`
  next()
})

export default router 