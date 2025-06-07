<template>
  <div class="app-container" :class="{ 'dark-mode': isDarkMode }">
    <Header />
    <div class="main-container">
      <Sidebar />
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { useAppStore } from './store';
import Header from './components/Header.vue';
import Sidebar from './components/Sidebar.vue';

const appStore = useAppStore();

const isDarkMode = computed(() => appStore.isDarkMode);

// 使用 ref 创建一个响应式变量来控制是否执行 onMounted 中的逻辑
const isMounted = ref(false);

onMounted(() => {
  isMounted.value = true;
  // 从localStorage恢复主题设置
  const savedTheme = localStorage.getItem('darkMode');
  if (savedTheme) {
    appStore.isDarkMode = JSON.parse(savedTheme);
  }
});
</script>

<style>
/* 全局样式已在 main.css 中定义 */
.main-container {
  display: flex;
  flex: 1;
  height: calc(100vh - var(--header-height));
}

.content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}
</style>
