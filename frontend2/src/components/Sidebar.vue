<template>
  <aside class="sidebar" :class="{ 'collapsed': isSidebarCollapsed }">
    <button class="collapse-button" @click="toggleSidebar">
      <ChevronLeftIcon v-if="!isSidebarCollapsed" />
      <ChevronRightIcon v-else />
    </button>
    <nav class="sidebar-nav">
      <ul>
        <li 
          v-for="item in menuItems" 
          :key="item.path"
          :class="{ 'active': currentRoute === item.path }"
          @click="handleNavigation(item.path)"
        >
          <component :is="item.icon" />
          <span v-if="!isSidebarCollapsed">{{ item.name }}</span>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAppStore } from '../store';
import { 
  Home as HomeIcon,
  BarChart as BarChartIcon,
  Database as DatabaseIcon,
  Table as TableIcon,
  FileText as FileTextIcon,
  Video as VideoIcon,
  Users as UsersIcon,
  Settings as SettingsIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();
const appStore = useAppStore();

const menuItems = [
  { name: '仪表盘', path: '/', icon: HomeIcon },
  { name: '分析', path: '/analytics', icon: BarChartIcon },
  { name: '数据源', path: '/data-sources', icon: DatabaseIcon },
  { name: '表格', path: '/tables', icon: TableIcon },
  { name: '报表', path: '/reports', icon: FileTextIcon },
  { name: '媒体', path: '/media', icon: VideoIcon },
  { name: '热门视频', path: '/hot-videos', icon: VideoIcon },
  { name: '用户', path: '/users', icon: UsersIcon },
  { name: '设置', path: '/settings', icon: SettingsIcon }
];

const currentRoute = computed(() => route.path);
const isSidebarCollapsed = computed(() => appStore.isSidebarCollapsed);

const toggleSidebar = () => {
  appStore.toggleSidebar();
};

const navigateTo = (path) => {
  router.push(path);
};

const handleNavigation = (path) => {
  navigateTo(path);
}
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--card);
  border-right: 1px solid var(--border);
  transition: width 0.3s ease;
  position: relative;
  overflow-y: auto;
  height: 100%;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.collapse-button {
  position: absolute;
  top: 1rem;
  right: -12px;
  width: 24px;
  height: 24px;
  background-color: var(--primary);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  z-index: 10;
}

.sidebar-nav {
  padding: 1.5rem 0;
}

.sidebar-nav ul {
  list-style: none;
}

.sidebar-nav li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
  color: var(--muted-foreground);
}

.sidebar-nav li.active {
  background-color: var(--primary-light);
  color: var(--primary);
  font-weight: 500;
  position: relative;
}

.sidebar-nav li.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background-color: var(--primary);
}

.sidebar-nav li:hover:not(.active) {
  background-color: var(--muted);
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 50;
    height: 100vh;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.active {
    transform: translateX(0);
  }
}
</style>
