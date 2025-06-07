<template>
  <div class="uploader-analysis">
    <!-- 移动端导航 -->
    <div class="mobile-navigation">
      <!-- 顶部导航栏 -->
      <div class="nav-header">
        <button @click="toggleSidebar" class="menu-button">
          <Menu />
        </button>
        <div class="nav-title">{{ currentPage }}</div>
        <button @click="toggleSearch" class="search-button">
          <Search />
        </button>
      </div>

      <!-- 侧边栏 -->
      <Transition name="slide">
        <div v-if="isSidebarOpen">
          <div class="sidebar-overlay" @click="closeSidebar"></div>
          <div class="sidebar" @click.stop>
            <div class="sidebar-header">
              <div class="app-logo">
                <div class="logo-icon">B</div>
                <span>UP主分析平台</span>
              </div>
              <button @click="closeSidebar" class="close-button">
                <X />
              </button>
            </div>
            
            <div class="sidebar-content">
              <div class="user-info">
                <div class="user-avatar">
                  <img :src=userUrl alt="用户头像" class="avatar-image" />
                </div>
                <div class="user-details">
                  <div class="user-name">数据分析师</div>
                  <div class="user-role">管理员</div>
                </div>
              </div>
              
              <div class="nav-menu">
                <router-link 
                  v-for="item in navItems" 
                  :key="item.path" 
                  :to="item.path"
                  class="nav-item"
                  :class="{ active: currentRoute === item.path }"
                  @click="closeSidebar"
                >
                  <component :is="item.icon" class="nav-icon" />
                  <span>{{ item.name }}</span>
                </router-link>
              </div>
            </div>
            
            <div class="sidebar-footer">
              <div class="version">版本 v1.0.0</div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- 搜索面板 -->
      <Transition name="fade">
        <div v-if="isSearchOpen" class="search-overlay">
          <div class="search-panel">
            <div class="search-header">
              <Search class="search-icon" />
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="搜索UP主或视频..." 
                class="search-input"
                ref="searchInput"
                @keyup.enter="performSearch"
              />
              <button @click="closeSearch" class="close-search">
                <X />
              </button>
            </div>
            
            <div class="search-results" v-if="searchQuery.length > 0">
              <div class="result-section">
                <div class="result-title">UP主</div>
                <div class="result-list">
                  <div class="result-item" v-for="i in 3" :key="`up-${i}`">
                    <img :src=userUrl alt="用户头像" class="avatar-image" /> 
                    <div class="result-info">
                      <div class="result-name">UP主{{ i }}</div>
                      <div class="result-meta">{{ 10000 * i }} 粉丝</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="result-section">
                <div class="result-title">视频</div>
                <div class="result-list">
                  <div class="result-item" v-for="i in 2" :key="`video-${i}`">
                    <div class="result-thumbnail">
                      <img :src=videoUrl alt="视频缩略图" /> 
                    </div>
                    <div class="result-info">
                      <div class="result-name">视频标题{{ i }}</div>
                      <div class="result-meta">{{ 5000 * i }} 播放</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="search-empty" v-else>
              <div class="empty-icon">
                <Search size="48" class="empty-search-icon" />
              </div>
              <div class="empty-text">输入关键词搜索UP主或视频</div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- 底部导航栏 -->
      <div class="bottom-nav">
        <router-link 
          v-for="item in mainNavItems" 
          :key="item.path" 
          :to="item.path"
          class="bottom-nav-item"
          :class="{ active: currentRoute === item.path }"
        >
          <component :is="item.icon" class="bottom-nav-icon" />
          <span class="bottom-nav-label">{{ item.name }}</span>
        </router-link>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <div class="content-header">
        <h1>UP主分析</h1>
        <div class="header-actions">
          <button class="action-button">
            <Search />
            <span>搜索</span>
          </button>
          <button class="action-button">
            <Filter />
            <span>筛选</span>
          </button>
        </div>
      </div>

      <div class="content-body">
        <!-- 数据概览卡片 -->
        <div class="overview-cards">
          <div class="card">
            <div class="card-title">总UP主数</div>
            <div class="card-value">1,234</div>
            <div class="card-trend up">+12.5%</div>
          </div>
          <div class="card">
            <div class="card-title">活跃UP主</div>
            <div class="card-value">856</div>
            <div class="card-trend up">+8.3%</div>
          </div>
          <div class="card">
            <div class="card-title">平均粉丝数</div>
            <div class="card-value">45.2K</div>
            <div class="card-trend down">-2.1%</div>
          </div>
          <div class="card">
            <div class="card-title">平均互动率</div>
            <div class="card-value">12.8%</div>
            <div class="card-trend up">+5.4%</div>
          </div>
        </div>

        <!-- 图表区域 -->
        <div class="charts-container">
          <div class="chart-card">
            <div class="chart-header">
              <h3>UP主增长趋势</h3>
              <div class="chart-actions">
                <button class="chart-action">周</button>
                <button class="chart-action active">月</button>
                <button class="chart-action">年</button>
              </div>
            </div>
            <div class="chart-content">
              <!-- 这里放置图表组件 -->
              <div class="chart-placeholder">图表区域</div>
            </div>
          </div>

          <div class="chart-card">
            <div class="chart-header">
              <h3>UP主分类分布</h3>
              <div class="chart-actions">
                <button class="chart-action active">全部</button>
                <button class="chart-action">活跃</button>
              </div>
            </div>
            <div class="chart-content">
              <!-- 这里放置图表组件 -->
              <div class="chart-placeholder">图表区域</div>
            </div>
          </div>
        </div>

        <!-- UP主列表 -->
        <div class="uploader-list">
          <div class="list-header">
            <h3>UP主列表</h3>
            <div class="list-actions">
              <input type="text" placeholder="搜索UP主..." class="search-input" />
              <select class="filter-select">
                <option value="all">全部分类</option>
                <option value="active">活跃UP主</option>
                <option value="new">新晋UP主</option>
              </select>
            </div>
          </div>
          <div class="list-content">
            <div class="uploader-item" v-for="i in 5" :key="i">
              <div class="uploader-info">
                <img :src=userUrl alt="UP主头像" class="uploader-avatar" />
                <div class="uploader-details">
                  <div class="uploader-name">UP主{{ i }}</div>
                  <div class="uploader-meta">
                    <span>{{ 10000 * i }} 粉丝</span>
                    <span>{{ 500 * i }} 视频</span>
                  </div>
                </div>
              </div>
              <div class="uploader-stats">
                <div class="stat-item">
                  <div class="stat-value">{{ 1000 * i }}</div>
                  <div class="stat-label">播放量</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ 100 * i }}</div>
                  <div class="stat-label">互动量</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ 10 * i }}%</div>
                  <div class="stat-label">互动率</div>
                </div>
              </div>
              <button class="view-details">查看详情</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { Menu, X, Search, Home, Users, Video, BarChart2, Network, Filter } from 'lucide-vue-next'

const route = useRoute()
const currentRoute = computed(() => route.path)

const userUrl = 'https://i2.hdslb.com/bfs/face/7dbcfb5de033b1dd5409acd992b2a56900ab6d9d.jpg'
const videoUrl = 'http://i0.hdslb.com/bfs/archive/97dcac82485886f8e6288c41ec813b67f3c0e021.jpg'

// 导航项
const navItems = [
  { name: '平台概览', path: '/', icon: Home },
  { name: 'UP主分析', path: '/uploader-analysis', icon: Users },
  { name: '视频分析', path: '/video-analysis', icon: Video },
  { name: '数据报表', path: '/reports', icon: BarChart2 },
  { name: '社交图谱', path: '/social-network', icon: Network }
]

// 主要导航项（用于底部导航）
const mainNavItems = computed(() => navItems.slice(0, 4))

// 当前页面标题
const currentPage = computed(() => {
  const current = navItems.find(item => item.path === currentRoute.value)
  return current ? current.name : '平台概览'
})

// 侧边栏状态
const isSidebarOpen = ref(false)
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
  if (isSidebarOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}
const closeSidebar = () => {
  isSidebarOpen.value = false
  document.body.style.overflow = ''
}

// 搜索面板状态
const isSearchOpen = ref(false)
const searchQuery = ref('')
const searchInput = ref<HTMLInputElement | null>(null)

const toggleSearch = () => {
  isSearchOpen.value = !isSearchOpen.value
  if (isSearchOpen.value) {
    document.body.style.overflow = 'hidden'
    nextTick(() => {
      searchInput.value?.focus()
    })
  } else {
    document.body.style.overflow = ''
  }
}

const closeSearch = () => {
  isSearchOpen.value = false
  document.body.style.overflow = ''
}

const performSearch = () => {
  console.log('搜索:', searchQuery.value)
  // 实现搜索逻辑
}

// 监听路由变化关闭侧边栏和搜索
watch(currentRoute, () => {
  closeSidebar()
  closeSearch()
})
</script>

<style scoped>
.uploader-analysis {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  padding: 24px;
  color: #fff;
}

/* 移动端导航样式 */
.mobile-navigation {
  position: relative;
  z-index: 100;
  display: none;
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  padding: 24px;
  margin-left: 0;
  transition: margin-left 0.3s ease;
  min-height: 100vh;
  width: 100%;
}

@media (min-width: 1024px) {
  .mobile-navigation {
    display: none;
  }
  
  .main-content {
    margin-left: 240px;
    width: calc(100% - 240px);
  }
}

@media (max-width: 1023px) {
  .mobile-navigation {
    display: block;
  }
  
  .main-content {
    margin-left: 0;
    width: 100%;
  }
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.content-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background: rgba(255, 255, 255, 0.15);
}

/* 数据概览卡片 */
.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.card {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-title {
  font-size: 14px;
  color: #999;
  margin-bottom: 8px;
}

.card-value {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 8px;
}

.card-trend {
  font-size: 14px;
  font-weight: 500;
}

.card-trend.up {
  color: #00d4ff;
}

.card-trend.down {
  color: #ff3d00;
}

/* 图表区域 */
.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.chart-card {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.chart-actions {
  display: flex;
  gap: 8px;
}

.chart-action {
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 6px;
  color: #999;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chart-action.active {
  background: #00d4ff;
  color: #fff;
}

.chart-content {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.chart-placeholder {
  color: #666;
}

/* UP主列表 */
.uploader-list {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.list-actions {
  display: flex;
  gap: 12px;
}

.search-input {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  outline: none;
  color: #fff;
}

.search-input::placeholder {
  color: #666;
}

.filter-select {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  outline: none;
  color: #fff;
}

.filter-select option {
  background: #1a1a2e;
  color: #fff;
}

.uploader-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.uploader-item:last-child {
  border-bottom: none;
}

.uploader-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.uploader-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid #00d4ff;
}

.uploader-name {
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.uploader-meta {
  display: flex;
  gap: 12px;
  color: #999;
  font-size: 14px;
}

.uploader-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

.view-details {
  padding: 8px 16px;
  background: #00d4ff;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-details:hover {
  background: #00b8e6;
}

/* 保持原有的移动端导航样式 */
.nav-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: rgba(10, 10, 26, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 50;
}

.menu-button,
.search-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #fff;
  border-radius: 50%;
  cursor: pointer;
}

.menu-button:active,
.search-button:active {
  background: rgba(255, 255, 255, 0.1);
}

.nav-title {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 100;
  display: flex;
}

.sidebar {
  width: 280px;
  max-width: 80vw;
  height: 100%;
  background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.app-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #fff;
  font-weight: 600;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
}

.close-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #fff;
  border-radius: 50%;
  cursor: pointer;
}

.sidebar-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-bottom: 24px;
}

.user-avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #00d4ff;
}

.user-name {
  font-weight: 600;
  color: #fff;
  font-size: 14px;
}

.user-role {
  color: #00d4ff;
  font-size: 12px;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  color: #ccc;
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-item:active {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background: rgba(0, 212, 255, 0.1);
  color: #00d4ff;
}

.nav-icon {
  width: 20px;
  height: 20px;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.version {
  font-size: 12px;
  color: #666;
}

.search-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 10, 26, 0.98);
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.search-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.search-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.search-icon {
  color: #999;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #fff;
  font-size: 16px;
}

.close-search {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #fff;
  border-radius: 50%;
  cursor: pointer;
}

.search-results {
  padding: 16px;
}

.result-section {
  margin-bottom: 24px;
}

.result-title {
  font-size: 14px;
  font-weight: 600;
  color: #999;
  margin-bottom: 12px;
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
}

.result-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.result-thumbnail img {
  width: 72px;
  height: 40px;
  border-radius: 4px;
  object-fit: cover;
}

.result-name {
  font-size: 14px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 4px;
}

.result-meta {
  font-size: 12px;
  color: #999;
}

.search-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  color: #666;
}

.empty-icon {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-size: 14px;
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(10, 10, 26, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 50;
}

.bottom-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
  text-decoration: none;
  gap: 4px;
}

.bottom-nav-item.active {
  color: #00d4ff;
}

.bottom-nav-icon {
  width: 20px;
  height: 20px;
}

.bottom-nav-label {
  font-size: 12px;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>