<template>
  <div>
    <div class="page-header">
      <h2>热门B站视频</h2>
    </div>
    <div class="video-gallery">
      <div class="video-card" v-for="item in pagedVideos" :key="item.aid">
        <div class="video-thumb">
          <a :href="item.short_link_v2" target="_blank">
            <img :src="proxyImg(item.pic)" :alt="item.title" />
          </a>
        </div>
        <div class="video-info">
          <h3 class="video-title">
            <a :href="item.short_link_v2" target="_blank">{{ item.title }}</a>
          </h3>
          <div class="video-meta">
            <img class="up-face" :src="proxyImg(item.owner_face)" :alt="item.owner_name" />
            <span class="up-name">{{ item.owner_name }}</span>
            <span class="video-tname">{{ item.tname }}</span>
          </div>
          <div class="video-stats">
            <span>播放：{{ formatNumber(item.stat_view) }}</span>
            <span>点赞：{{ formatNumber(item.stat_like) }}</span>
            <span>发布时间：{{ formatTime(item.pubdate) }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="prevPage">上一页</button>
      <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button :disabled="currentPage === totalPages" @click="nextPage">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const videos = ref([]);
const pageSize = 48;
const currentPage = ref(1);

const totalPages = computed(() => Math.ceil(videos.value.length / pageSize));
const pagedVideos = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return videos.value.slice(start, start + pageSize);
});

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};
const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const formatNumber = n => n > 10000 ? (n/10000).toFixed(1) + '万' : n;
const formatTime = ts => {
  const date = new Date(ts * 1000);
  return date.toLocaleDateString();
};
const proxyImg = url => `http://127.0.0.1:3000/proxy?url=${encodeURIComponent(url)}`;

onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:3000/api/hot-videos');
  if(res.data && res.data.data) {
    videos.value = res.data.data;
  }
});
</script>

<style scoped>
.page-header {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.video-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}
.video-card {
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.2s;
}
.video-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}
.video-thumb img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}
.video-info {
  padding: 1rem;
}
.video-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}
.video-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.up-face {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--border);
}
.up-name {
  font-size: 0.95rem;
  color: var(--muted-foreground);
}
.video-tname {
  background: var(--muted);
  color: var(--muted-foreground);
  border-radius: 8px;
  padding: 0 8px;
  font-size: 0.85rem;
  margin-left: 0.5rem;
}
.video-stats {
  font-size: 0.92rem;
  color: var(--muted-foreground);
  display: flex;
  gap: 1.2rem;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin: 2rem 0 1rem 0;
}
.pagination button {
  padding: 0.5rem 1.2rem;
  border: none;
  border-radius: 6px;
  background: var(--primary);
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.pagination button:disabled {
  background: var(--muted);
  color: var(--muted-foreground);
  cursor: not-allowed;
}
</style> 