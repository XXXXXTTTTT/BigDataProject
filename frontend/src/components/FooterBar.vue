<template>
  <footer class="footer-bar">
    <div class="footer-content">
      <div class="footer-creators">
        <span>创作者：</span>
        <a
          v-for="creator in creators"
          :key="creator.username"
          :href="creator.link"
          class="creator-link"
          target="_blank"
          rel="noopener"
        >
          <img :src="`https://github.com/${creator.username}.png`" :alt="creator.name" class="creator-avatar" />
          <span class="creator-name">{{ creator.name }}</span>
        </a>
      </div>
      <div class="footer-info">
        <span>© 2025 DataBili 项目 | 仅供学习与交流 | 联系方式：2937746306@qq.com</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
const creators = [
  { name: 'XXXXXTTTTT', username: 'XXXXXTTTTT', link: 'https://github.com/XXXXXTTTTT' },
  { name: 'winelve', username: 'winelve', link: 'https://github.com/winelve' }
];
</script>

<style scoped>
.footer-bar {
  width: 100%;
  background: var(--card);
  border-top: 1px solid var(--border);
  padding: 0.7rem 0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.98rem;
  color: var(--muted-foreground);
  margin-top: auto;
}
.footer-content {
  width: 100%;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}
.footer-creators {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  margin-bottom: 0.2rem;
}
.creator-link {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  text-decoration: none;
  color: var(--primary);
  font-weight: 500;
}
.creator-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--border);
}
.creator-name {
  font-size: 1rem;
}
.footer-info {
  font-size: 0.95rem;
  color: var(--muted-foreground);
}
</style> 