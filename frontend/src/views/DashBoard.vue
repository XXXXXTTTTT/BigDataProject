<template>
  <div>
    <!-- 项目介绍 -->
    <div class="intro-card">
      <h2>B站数据分析平台</h2>
      <p>
        本项目基于B站UP主与热门视频，用户评论等数据，分析Up主类别标签，热门视频趋势特征，用户特征
      </p>
    </div>
    <!-- 汇总数据卡片 -->
    <div class="summary-cards">
      <div class="summary-card" v-for="item in summaryList" :key="item.key">
        <div class="summary-title">{{ item.title }}</div>
        <div class="summary-value">{{ item.value }}</div>
      </div>
    </div>
    <!-- 聚类分布 -->
    <div class="cluster-summary" v-if="clusterSummary.length">
      <h3>UP主聚类分布</h3>
      <div class="cluster-list">
        <div class="cluster-item" v-for="c in clusterSummary" :key="c.label">
          <span class="cluster-label" :style="{color: clusterColors[c.label]}" >{{ clusterMap[c.label] }}</span>
          <span class="cluster-count">{{ c.count }} 人</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated } from 'vue';
import axios from 'axios';

const summary = ref({});
const summaryList = ref([]);
const clusterSummary = ref([]);
const clusterMap = { 0: '大V', 1: '普通UP', 2: '潜力UP' };
const clusterColors = { 0: '#e74c3c', 1: '#27ae60', 2: '#2980b9' };

const formatNumber = n => n > 10000 ? (n/10000).toFixed(1) + '万' : n;

async function fetchSummary() {
  const res = await axios.get('http://127.0.0.1:3000/api/up-profile/summary');
  if(res.data && res.data.data) {
    summary.value = res.data.data;
    summaryList.value = [
      { key: 'up_count', title: '抓取UP主数', value: formatNumber(summary.value.up_count) },
      { key: 'total_videos', title: '视频总数', value: formatNumber(summary.value.total_videos) },
      { key: 'total_view', title: '总播放量', value: formatNumber(summary.value.total_view) },
      { key: 'total_followers', title: '总粉丝数', value: formatNumber(summary.value.total_followers) },
      { key: 'total_like', title: '总点赞数', value: formatNumber(summary.value.total_like) },
      { key: 'total_coin', title: '总硬币数', value: formatNumber(summary.value.total_coin) },
      { key: 'total_favorite', title: '总收藏数', value: formatNumber(summary.value.total_favorite) },
      { key: 'total_share', title: '总分享数', value: formatNumber(summary.value.total_share) },
      { key: 'total_comment', title: '总评论数', value: formatNumber(summary.value.total_comment) },
      { key: 'total_danmaku', title: '总弹幕数', value: formatNumber(summary.value.total_danmaku) },
      { key: 'total_duration', title: '视频总时长', value: formatNumber(summary.value.total_duration) },
      { key: 'analysis_count', title: '聚类分析UP主数', value: formatNumber(summary.value.analysis_count) },
    ];
    clusterSummary.value = (summary.value.cluster_counts || []).map(c => ({
      label: c.cluster_label,
      count: c.count
    }));
  }
}

onMounted(fetchSummary);
onActivated(fetchSummary);
</script>

<style scoped>
.intro-card {
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  padding: 2rem 2.5rem 1.5rem 2.5rem;
  margin-bottom: 2.5rem;
  text-align: left;
}
.intro-card h2 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}
.intro-card p {
  font-size: 1.15rem;
  color: var(--muted-foreground);
  line-height: 1.8;
}
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}
.summary-card {
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.summary-title {
  font-size: 1.1rem;
  color: var(--muted-foreground);
  margin-bottom: 0.7rem;
}
.summary-value {
  font-size: 2.1rem;
  font-weight: bold;
  color: var(--primary);
}
.cluster-summary {
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
}
.cluster-summary h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}
.cluster-list {
  display: flex;
  gap: 2.5rem;
  flex-wrap: wrap;
}
.cluster-item {
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 1.2rem;
}
.cluster-label {
  font-weight: bold;
  font-size: 1.1rem;
}
.cluster-count {
  color: var(--primary);
  font-size: 1.1rem;
}
</style>
