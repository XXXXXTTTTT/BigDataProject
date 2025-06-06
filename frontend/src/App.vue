<template>
  <div class="app-container">
    <header class="header">
      <!-- 顶端左侧 -->
      <div class="header-left">
        <div class="logo">
          <img src="@/assets/logo.png" alt="Logo" />
          <h1>Bilibili 数据分析平台</h1>
        </div>
      </div>
      <!-- 顶端右侧 -->
      <div class="header-right">
        <a-dropdown>
          <a class="user-dropdown" @click.prevent>
            <a-avatar :size="32" icon="user" />
            <span class="username">管理员</span>
          </a>
          <template #overlay>
            <a-menu>
              <a-menu-item key="profile">
                <user-outlined />
                个人信息
              </a-menu-item>
              <a-menu-item key="settings">
                <setting-outlined />
                系统设置
              </a-menu-item>
              <a-menu-divider />
              <a-menu-item key="logout">
                <logout-outlined />
                退出登录
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
      </div>
    </header>

    <!-- 左侧菜单栏 -->
    <div class="app-content">
      <aside class="sidebar" :class="{ collapsed }">
        <!-- 伸缩开关，放到顶部 -->
        <div class="sidebar-toggle" @click="collapsed = !collapsed">
          <menu-unfold-outlined v-if="collapsed" />
          <menu-fold-outlined v-else />
        </div>

        <!-- 菜单项 -->
         <!-- 只在侧边栏展开时显示菜单 -->
        <a-menu
          mode="inline"
          :selectedKeys="[route.path]"
          @click="handleMenuClick"
          v-show="!collapsed"  
        >
          <a-menu-item v-for="item in menuItems" :key="item.key">
            <template #icon>
              <component :is="item.icon" />
            </template>
            {{ item.label }}
          </a-menu-item>
        </a-menu>
      </aside>

      <!-- 主面板 -->
      <main class="main-content" :class="{ collapsed }">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DashboardOutlined,
  UserOutlined,
  VideoCameraOutlined,
  SettingOutlined,
  LogoutOutlined
} from '@ant-design/icons-vue'

const collapsed = ref(false)
const router = useRouter()
const route = useRoute()

const menuItems = [
  {
    key: '/dashboard',
    icon: DashboardOutlined,
    label: '数据概览',
    path: '/dashboard'
  },
  {
    key: '/uploader',
    icon: UserOutlined,
    label: 'UP主分析',
    path: '/uploader'
  },
  {
    key: '/video',
    icon: VideoCameraOutlined,
    label: '视频分析',
    path: '/video'
  }
]

const handleMenuClick = ({ key }) => {
  router.push(key)
}

onMounted(() => {
  if (route.path === '/') {
    router.push('/dashboard')
  }
})
</script>

<style lang="scss">
@use "@/assets/styles/variables.scss" as *;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  height: 100%;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.5);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.7);
}

/* 响应式工具类 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

@media (min-width: 768px) {
  .container {
    padding: 0 24px;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 32px;
  }
}

/* 动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-leave-to {
  transform: translateX(100%);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-content {
  flex: 1;
  display: flex;
  margin-top: 64px;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 64px;
  bottom: 0;
  width: 160px;  /* 初始宽度更小 */
  height: calc(100vh - 64px);
  background: #001529;
  border-right: 1px solid #f0f0f0;
  transition: all 0.3s;
  z-index: 10;
  overflow-y: auto;

  &.collapsed {
    width: 60px;  /* 收起后仅剩开关 */
  }

  :deep(.ant-menu) {
    height: 100%;
    border-right: none;
  }
}


/* 侧边栏折叠时功能菜单隐藏 */
.sidebar.collapsed .main-content {
  padding-left: 80px;
}

.main-content {
  flex: 1;
  margin-left: 200px;
  padding: 24px;
  transition: all 0.3s;
  min-height: calc(100vh - 64px);
  &.collapsed {
    margin-left: 80px;
  }
}

/* 顶部 header 位置 */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background-color: #001529;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;

  .header-left {
    display: flex;
    align-items: center;
    gap: 16px;

    .logo {
      display: flex;
      align-items: center;
      gap: 12px;

      img {
        height: 32px;
        width: auto;
      }

      h1 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        color: #fff;
      }
    }
  }

  .header-right {
    display: flex;
    align-items: center;

    .user-dropdown {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      color: #fff;

      .username {
        font-size: 14px;
      }
    }
  }

  .trigger {
  font-size: 22px;  
  cursor: pointer;
  transition: color 0.3s;

  &:hover {
    color: #1890ff;  
  }
}

}

.sidebar-toggle {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #001529;
  padding: 10px;
  cursor: pointer;
  color: #fff;
  border-bottom: 1px solid #333;
  font-size: 20px;
}

.ant-menu {
  background-color: #1e1e1e !important;  
  border-right: none !important;          
}

.ant-menu-item {
  font-size: 16px;  
  color: #d4d4d4 !important; 
  transition: all 0.3s ease; 
}

.ant-menu-item:hover {
  background-color: #00d4ff !important; 
  color: #fff !important;  
}

.ant-menu-item-selected {
  background-color: #00d4ff !important;  
  color: #fff !important; 
}


</style>
