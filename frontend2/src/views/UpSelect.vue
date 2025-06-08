<template>
  <div>
    <div class="page-header">
      <h2>UP主详细数据</h2>
      <div class="search-bar">
        <input v-model="searchName" placeholder="输入UP主昵称进行模糊搜索" @keyup.enter="searchUp" />
        <input v-model="searchUid" placeholder="输入UID精确搜索" @keyup.enter="searchUp" type="number" />
        <button @click="searchUp">搜索</button>
        <button @click="resetSearch">重置</button>
      </div>
    </div>
    <div class="up-gallery">
      <div class="up-card" v-for="item in pagedUps" :key="item.uid" @click="goToBiliSpace(item.uid)">
        <div class="up-thumb">
          <img :src="proxyImg(item.avatar_url)" :alt="item.name" />
        </div>
        <div class="up-info">
          <h3 class="up-title">
            {{ item.name }}
            <span v-if="item.cluster_label !== undefined && item.cluster_label !== null" class="up-cluster-label">
              [{{ clusterMap[item.cluster_label] || '未知' }}]
            </span>
            <span class="up-uid">(UID: {{ item.uid }})</span>
          </h3>
          <div class="up-meta">
            <span>粉丝：{{ formatNumber(item.followers) }}</span>
            <span>投稿：{{ item.total_videos }}</span>
            <span>总播放：{{ formatNumber(item.total_view) }}</span>
            <span>总点赞：{{ formatNumber(item.total_like) }}</span>
            <span>总硬币：{{ formatNumber(item.total_coin) }}</span>
            <span>总收藏：{{ formatNumber(item.total_favorite) }}</span>
            <span>总分享：{{ formatNumber(item.total_share) }}</span>
            <span>评论数：{{ formatNumber(item.total_comment) }}</span>
            <span>弹幕：{{ formatNumber(item.total_danmaku) }}</span>
            <span>视频总时长：{{ formatNumber(item.total_duration) }}</span>
            <span>充电数：{{ formatNumber(item.total_chargers) }}</span>
          </div>
        </div>
      </div>
      <div v-if="pagedUps.length === 0" class="no-result">暂无数据</div>
    </div>
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="prevPage">上一页</button>
      <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button :disabled="currentPage === totalPages" @click="nextPage">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

const upList = ref([]);
const searchName = ref('');
const searchUid = ref('');

const clusterMap = { 0: '大V', 1: '普通UP', 2: '潜力UP' };

const pageSize = 10;
const currentPage = ref(1);
const totalPages = computed(() => Math.ceil(upList.value.length / pageSize));
const pagedUps = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return upList.value.slice(start, start + pageSize);
});

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};
const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const formatNumber = n => n > 10000 ? (n/10000).toFixed(1) + '万' : n;

const proxyImg = url => `http://127.0.0.1:3000/proxy?url=${encodeURIComponent(url)}`;

const searchUp = async () => {
  let url = 'http://127.0.0.1:3000/api/up-profile';
  const params = {};
  if (searchUid.value) params.uid = searchUid.value;
  else if (searchName.value) params.name = searchName.value;
  try {
    const res = await axios.get(url, { params });
    if(res.data && res.data.data) {
      upList.value = Array.isArray(res.data.data) ? res.data.data : [res.data.data];
    } else {
      upList.value = [];
    }
    currentPage.value = 1; // 搜索后重置到第一页
  } catch (e) {
    upList.value = [];
    currentPage.value = 1;
  }
};

const resetSearch = () => {
  searchName.value = '';
  searchUid.value = '';
  searchUp();
};

const goToBiliSpace = (uid) => {
  window.open(`https://space.bilibili.com/${uid}`, '_blank');
};

// 初始加载全部UP主
searchUp();
</script>

<style scoped>
.page-header {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.search-bar {
  display: flex;
  gap: 0.75rem;
}
.search-bar input {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 1rem;
}
.search-bar button {
  padding: 0.5rem 1.2rem;
  border: none;
  border-radius: 6px;
  background: var(--primary);
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.search-bar button:hover {
  background: var(--primary-hover, #1890ff);
}
.up-gallery {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.up-card {
  width: 100%;
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  overflow: hidden;
  display: flex;
  flex-direction: row;
  align-items: center;
  transition: box-shadow 0.2s, transform 0.2s;
  cursor: pointer;
}
.up-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  transform: translateY(-2px) scale(1.02);
}
.up-thumb {
  flex: 0 0 90px;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--muted);
}
.up-thumb img {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border);
}
.up-info {
  flex: 1;
  padding: 1rem;
}
.up-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}
.up-uid {
  font-size: 0.95rem;
  color: var(--muted-foreground);
  margin-left: 0.5rem;
}
.up-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem 1.2rem;
  font-size: 0.97rem;
  color: var(--muted-foreground);
}
.no-result {
  text-align: center;
  color: var(--muted-foreground);
  font-size: 1.1rem;
  margin-top: 2rem;
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
.up-cluster-label {
  margin-left: 0.5rem;
  font-size: 0.98rem;
  color: #e74c3c;
  font-weight: bold;
}
</style> 