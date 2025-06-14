//顶端页面
<template>
  <header class="header">
    <div class="logo-container">
      <img src="../assets/logo.png" alt= "Logo" class="logo" />
      <h1 class="site-title">DataBili</h1>
    </div>
    <div class="header-actions">
      <button class="theme-toggle" @click="toggleDarkMode">
        <SunIcon v-if="isDarkMode" />
        <MoonIcon v-else />
      </button>
      <div class="notification-icon" @click="toggleNotifications">
        <BellIcon />
        <span class="notification-badge" v-if="unreadNotificationsCount">{{ unreadNotificationsCount }}</span>
        <div class="notifications-dropdown" v-if="showNotifications">
          <div class="notifications-header">
            <h3>通知</h3>
            <button @click="markAllAsRead">全部已读</button>
          </div>
          <div class="notifications-list">
            <div 
              v-for="notification in notifications" 
              :key="notification.id" 
              class="notification-item"
              :class="{ 'unread': !notification.read }"
              @click="markAsRead(notification.id)"
            >
              <div class="notification-content">
                <h4>{{ notification.title }}</h4>
                <p>{{ notification.message }}</p>
                <span class="notification-time">{{ notification.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="user-profile" @click="toggleUserMenu">
        <img src="../assets/2233.png" alt="User Avatar" class="avatar" />
        <div class="user-menu" v-if="isUserMenuOpen">
          <ul>
            <li @click="navigateTo('/profile')"><UserIcon /> 个人资料</li>
            <li @click="navigateTo('/settings')"><SettingsIcon /> 设置</li>
            <li @click="logout"><LogOutIcon /> 退出登录</li>
          </ul>
        </div>
      </div>
      <button class="collapse-button" @click="toggleSidebar">
        <ChevronLeft v-if="!isSidebarCollapsed" :class="{ 'dark-icon': isDarkMode }" />
        <ChevronRight v-else :class="{ 'dark-icon': isDarkMode }" />
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAppStore } from '../store';
import { 
  Search as SearchIcon, 
  Bell as BellIcon, 
  User as UserIcon, 
  Settings as SettingsIcon, 
  LogOut as LogOutIcon,
  Sun as SunIcon,
  Moon as MoonIcon,
  ChevronLeft,
  ChevronRight,
} from 'lucide-vue-next';

const router = useRouter();
const appStore = useAppStore();

const isUserMenuOpen = ref(false);
const showNotifications = ref(false);

const notifications = computed(() => appStore.notifications);
const unreadNotificationsCount = computed(() => appStore.unreadNotificationsCount);
const isSidebarCollapsed = computed(() => appStore.isSidebarCollapsed);
const isDarkMode = computed(() => appStore.isDarkMode);

const toggleDarkMode = () => {
  appStore.toggleDarkMode();
};

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value;
  if (isUserMenuOpen.value) {
    showNotifications.value = false;
  }
};

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value;
  if (showNotifications.value) {
    isUserMenuOpen.value = false;
  }
};

const navigateTo = (path) => {
  router.push(path);
  isUserMenuOpen.value = false;
};

const logout = () => {
  appStore.logout();
  router.push('/login');
};

const markAsRead = (id) => {
  appStore.markNotificationAsRead(id);
};

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    appStore.markNotificationAsRead(notification.id);
  });
};

const toggleSidebar = () => {
  appStore.toggleSidebar();
};
</script>

<style scoped>
.header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  background-color: var(--card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo {
  height: 2rem;
  width: 2rem;
}

.site-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-left: auto;
}

.theme-toggle,
.collapse-button,
.notification-icon,
.user-profile {
  background: none;
  border: none;
  color: var(--foreground);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  min-width: 2.5rem;
  min-height: 2.5rem;
  box-sizing: border-box;
  transition: background-color 0.2s, color 0.2s;
}
.theme-toggle:hover,
.collapse-button:hover,
.notification-icon:hover,
.user-profile:hover {
  background-color: var(--muted);
}
.theme-toggle svg,
.collapse-button svg,
.notification-icon svg {
  width: 1.5rem;
  height: 1.5rem;
  display: block;
}
.avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--primary);
}

.notification-icon {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background-color: var(--primary);
  color: white;
  border-radius: 50%;
  width: 1.1em;
  height: 1.1em;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  box-shadow: 0 0 0 2px var(--card);
}

.notifications-dropdown {
  position: absolute;
  top: 100%;
  right: -100px;
  margin-top: 0.5rem;
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 300px;
  z-index: 10;
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
}

.notifications-header h3 {
  font-size: 1rem;
  font-weight: 600;
}

.notifications-header button {
  background: none;
  border: none;
  color: var(--primary);
  cursor: pointer;
  font-size: 0.875rem;
}

.notifications-list {
  max-height: 300px;
  overflow-y: auto;
}

.notification-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: var(--muted);
}

.notification-item.unread {
  background-color: var(--primary-light);
}

.notification-content h4 {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.notification-content p {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin-bottom: 0.25rem;
}

.notification-time {
  font-size: 0.75rem;
  color: var(--muted-foreground);
}

.user-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 200px;
  z-index: 10;
}

.user-menu ul {
  list-style: none;
  padding: 0.5rem 0;
}

.user-menu li {
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-menu li:hover {
  background-color: var(--muted);
}

@media (max-width: 640px) {
  .search-container {
    display: none;
  }
}

.sidebar {
  width: 200px;
  min-width: 60px;
  max-width: 240px;
  overflow-x: hidden;
  overflow-y: auto;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.sidebar.collapsed {
  width: 60px;
}

.dark-icon {
  color: #222;
  transition: color 0.2s;
}

.dark-mode .dark-icon {
  color: #f3f3f3;
}

body.dark .collapse-button svg {
  color: #fff;
}
</style>
