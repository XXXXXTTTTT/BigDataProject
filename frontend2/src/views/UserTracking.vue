<template>
  <div class="user-tracking">
    <!-- 搜索栏 -->
    <div class="search-section">
      <div class="search-container">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchUid" 
            placeholder="请输入用户UID进行分析..."
            @keyup.enter="startAnalysis"
            :disabled="isLoading"
          />
          <button 
            class="analyze-button" 
            @click="startAnalysis"
            :disabled="isLoading || !searchUid.trim()"
          >
            <SearchIcon v-if="!isLoading" />
            <LoaderIcon v-else class="spinning" />
            {{ isLoading ? '分析中...' : '开始分析' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error-message">
      <AlertCircleIcon />
      <span>{{ error }}</span>
    </div>

    <!-- 分析结果 -->
    <div v-if="analysisData && !error" class="analysis-results">
      <!-- 用户信息 -->
      <div class="user-info" :class="{ 'animate-in': showResults }">
        <div class="user-header">
          <div class="user-avatar">
            <img v-if="analysisData.face" :src="proxyImg(analysisData.face)" alt="用户头像" style="width:80px;height:80px;border-radius:20px;object-fit:cover;" />
            <UserIcon v-else />
          </div>
          <div class="user-details">
            <h2>用户：{{ analysisData.name || analysisData.uid }}</h2>
            <p>数据分析报告</p>
          </div>
        </div>
      </div>

      <!-- 分析内容 - 垂直布局 -->
      <div class="analysis-content" :class="{ 'animate-in': showResults }">
        
        <!-- 1. 用户活跃程度曲线 -->
        <div class="analysis-section activity-section">
          <h3 class="section-title">
            <ActivityIcon /> 用户活跃程度
          </h3>
          <div class="comment-total">
            <span>评论总数：</span><b>{{ analysisData.replies?.length || 0 }}</b>
          </div>
          <div class="chart-wrapper">
            <Line 
              :data="activityChartData" 
              :options="activityChartOptions"
              :height="120"
            />
          </div>

        </div>

        <!-- 2. 词云 -->
        <div class="analysis-section wordcloud-section">
          <h3 class="section-title">
            <CloudIcon /> 词云分析
          </h3>
          <div class="wordcloud-wrapper">
            <div ref="echartsWordcloud" class="wordcloud-container"></div>
          </div>
        </div>

        <!-- 3. 词频分布 -->
        <div class="analysis-section frequency-section">
          <h3 class="section-title">
            <BarChartIcon /> 词频分布
          </h3>
          <div class="chart-wrapper">
            <Bar 
              :data="frequencyChartData" 
              :options="frequencyChartOptions"
              :height="120"
            />
          </div>
        </div>

        <!-- 4. 用户关键字 -->
        <div class="analysis-section keywords-section">
          <h3 class="section-title">
            <TagIcon /> 用户关键字
          </h3>
          <div class="keywords-display">
            <div 
              v-for="(keyword, index) in analysisData.user_keyword" 
              :key="keyword"
              class="keyword-item"
              :style="{ animationDelay: (index * 0.2) + 's' }"
            >
              {{ keyword }}
            </div>
          </div>
        </div>

        <!-- 5. 友好程度 -->
        <div class="analysis-section friendly-section">
          <h3 class="section-title">
            <HeartIcon /> 评论评分
          </h3>
          <div class="friendly-display">
            <div class="score-main">
              <span class="score-number">{{ analysisData.friendly_score.score }}</span>
              <span class="score-total">/10</span>
            </div>
            <p class="score-description">{{ analysisData.friendly_score.comment }}</p>
          </div>
        </div>

        <!-- 6. 兴趣推测 -->
        <div class="analysis-section interest-section">
          <h3 class="section-title">
            <StarIcon /> 兴趣推测
          </h3>
          <div class="interest-display">
            <p class="interest-text">{{ analysisData.interest }}</p>
          </div>
        </div>

        <!-- 7. 评论列表（分页） -->
        <div class="analysis-section commentlist-section">
          <h3 class="section-title">
            <BarChartIcon /> 评论列表
          </h3>
          <div class="commentlist-wrapper">
            <div v-if="pagedComments.length === 0" class="no-comments">暂无评论</div>
            <div v-else>
              <div v-for="(item, idx) in pagedComments" :key="item.timestamp + idx" class="comment-item">
                <div class="comment-time">{{ formatTime(item.timestamp) }}</div>
                <div class="comment-content">{{ item.comment }}</div>
              </div>
            </div>
            <div v-if="totalPages > 1" class="pagination-bar">
              <button :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">上一页</button>
              <span>第 <input type="number" v-model.number="inputPage" min="1" :max="totalPages" @keyup.enter="jumpToPage" style="width: 3em; text-align: center;"/> / {{ totalPages }} 页</span>
              <button :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">下一页</button>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!analysisData && !isLoading && !error" class="empty-state">
      <div class="empty-icon">
        <SearchIcon />
      </div>
      <h3>开始用户分析</h3>
      <p>请输入用户UID开始分析用户行为数据</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted, watch } from 'vue';
import { Line, Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import * as echarts from 'echarts';
import 'echarts-wordcloud';
import axios from 'axios';
import { 
  Search as SearchIcon,
  Loader as LoaderIcon,
  AlertCircle as AlertCircleIcon,
  User as UserIcon,
  Activity as ActivityIcon,
  Cloud as CloudIcon,
  BarChart as BarChartIcon,
  Tag as TagIcon,
  Heart as HeartIcon,
  Star as StarIcon
} from 'lucide-vue-next';

// 注册 Chart.js 组件
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const searchUid = ref('');
const isLoading = ref(false);
const error = ref('');
const analysisData = ref(null);
const showResults = ref(false);
const echartsWordcloud = ref(null);
let wordcloudInstance = null;

// Chart.js 配置
const activityChartData = computed(() => {
  if (!analysisData.value?.replies) return { labels: [], datasets: [] };
  
  // 处理数据 - 按小时统计
  const hourlyData = new Array(24).fill(0);
  analysisData.value.replies.forEach(reply => {
    const hour = new Date(reply.timestamp).getHours();
    hourlyData[hour]++;
  });
  
  return {
    labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
    datasets: [
      {
        label: '评论数量',
        data: hourlyData,
        borderColor: '#FB7299',
        backgroundColor: 'rgba(251, 114, 153, 0.1)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#FB7299',
        pointBorderColor: '#FB7299',
        pointRadius: 4,
        pointHoverRadius: 6,
      }
    ]
  };
});

const activityChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: '#FB7299',
      borderWidth: 1,
      callbacks: {
        afterBody: function(context) {
          const hour = context[0].dataIndex;
          const comments = analysisData.value?.replies?.filter(reply => 
            new Date(reply.timestamp).getHours() === hour
          ) || [];
          
          if (comments.length > 0) {
            return comments.slice(0, 3).map(comment => 
              `"${comment.comment.substring(0, 30)}..."`
            );
          }
          return [];
        }
      }
    }
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(0, 0, 0, 0.1)'
      },
      ticks: {
        color: '#6B7280'
      }
    },
    y: {
      grid: {
        color: 'rgba(0, 0, 0, 0.1)'
      },
      ticks: {
        color: '#6B7280'
      },
      beginAtZero: true
    }
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false
  }
};

const frequencyChartData = computed(() => {
  if (!analysisData.value?.word_count) return { labels: [], datasets: [] };
  
  const topWords = analysisData.value.word_count
    .sort((a, b) => b.value - a.value)
    .slice(0, 10);
  
  return {
    labels: topWords.map(w => w.word),
    datasets: [
      {
        label: '词频',
        data: topWords.map(w => w.value),
        backgroundColor: [
          '#FB7299', '#23ADE5', '#10B981', '#F59E0B', '#8B5CF6',
          '#EF4444', '#06B6D4', '#84CC16', '#F97316', '#EC4899'
        ],
        borderWidth: 0,
        borderRadius: 4,
      }
    ]
  };
});

const frequencyChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y',
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: '#FB7299',
      borderWidth: 1,
    }
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(0, 0, 0, 0.1)'
      },
      ticks: {
        color: '#6B7280'
      },
      beginAtZero: true
    },
    y: {
      grid: {
        display: false
      },
      ticks: {
        color: '#6B7280'
      }
    }
  }
};

// 方法
const proxyImg = url => `http://127.0.0.1:3000/proxy?url=${encodeURIComponent(url)}`;

const startAnalysis = async () => {
  if (!searchUid.value.trim() || isLoading.value) return;
  isLoading.value = true;
  error.value = '';
  analysisData.value = null;
  showResults.value = false;

  // 测试数据
  const mockData = {
    code: 0,
    uid: searchUid.value,
    replies: generateMockReplies(),
    word_count: generateMockWordCount(),
    user_keyword: ["技术爱好者", "游戏玩家", "二次元"],
    friendly_score: {
      score: Math.floor(Math.random() * 4) + 7, // 7-10分
      comment: "该用户表现出较高的友好程度，评论内容积极正面，经常与其他用户进行友善互动"
    },
    interest: "该用户对科技、游戏和动漫内容表现出浓厚兴趣，经常参与相关话题讨论，活跃时间主要集中在晚间，具有较强的社区参与意识。喜欢分享技术心得，对新兴科技保持高度关注，同时也是资深游戏玩家，对各类游戏都有涉猎。"
  };

  try {
    // 请求后端接口
    const res = await axios.get(`http://localhost:3000/api/user-track?uid=${searchUid.value}`);
    const data = res.data;
    if (data && data.code === 0) {
      analysisData.value = data;
    } else if (data && data.code === -1) {
      error.value = '未找到该用户，请检查UID是否正确';
      return;
    } else {
      error.value = '分析失败，请稍后重试';
      return;
    }
  } catch (err) {
    // 请求失败，使用 mockData
    analysisData.value = mockData;
  } finally {
    if (analysisData.value) {
      await nextTick();
      showResults.value = true;
      setTimeout(() => {
        renderEchartsWordCloud();
      }, 500);
    }
    isLoading.value = false;
  }
};

const generateMockReplies = () => {
  const replies = [];
  const now = Date.now();
  const oneDay = 24 * 60 * 60 * 1000;
  
  for (let i = 0; i < 100; i++) {
    replies.push({
      comment: `这是第${i + 1}条评论内容，包含了用户的真实想法和观点`,
      timestamp: now - Math.random() * 30 * oneDay
    });
  }
  
  return replies.sort((a, b) => a.timestamp - b.timestamp);
};

const generateMockWordCount = () => {
  const words = [
    '好看', '有趣', '不错', '喜欢', '支持', '厉害', '牛逼', '666',
    '哈哈', '笑死', '太棒了', '赞', '优秀', '精彩', '感谢', '学习',
    '技术', '游戏', '动漫', '音乐', '视频', 'up主', '弹幕', '关注',
    '科技', '编程', '代码', '算法', '数据', '人工智能', '机器学习'
  ];
  
  return words.map(word => ({
    word,
    value: Math.floor(Math.random() * 100) + 10
  })).sort((a, b) => b.value - a.value);
};

const renderEchartsWordCloud = () => {
  if (!echartsWordcloud.value || !analysisData.value?.word_count) return;
  if (wordcloudInstance) {
    wordcloudInstance.dispose();
  }
  wordcloudInstance = echarts.init(echartsWordcloud.value);
  const wordList = analysisData.value.word_count
    .slice(0, 30)
    .map(item => ({ name: item.word, value: item.value }));
  const option = {
    tooltip: {},
    series: [{
      type: 'wordCloud',
      gridSize: 8,
      sizeRange: [28, 80],
      rotationRange: [-45, 90],
      shape: 'circle',
      width: '100%',
      height: '100%',
      textStyle: {
        color: () => {
          const colors = ['#FB7299', '#23ADE5', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444'];
          return colors[Math.floor(Math.random() * colors.length)];
        }
      },
      data: wordList
    }]
  };
  wordcloudInstance.setOption(option);
  window.addEventListener('resize', () => wordcloudInstance && wordcloudInstance.resize());
};

// 评论分页相关
const currentPage = ref(1);
const inputPage = ref(1);
const pageSize = 50;
const pagedComments = computed(() => {
  if (!analysisData.value?.replies) return [];
  const start = (currentPage.value - 1) * pageSize;
  return analysisData.value.replies.slice(start, start + pageSize);
});
const totalPages = computed(() => {
  if (!analysisData.value?.replies) return 1;
  return Math.ceil(analysisData.value.replies.length / pageSize) || 1;
});
function goToPage(page) {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  inputPage.value = page;
  nextTick(() => {
    const el = document.querySelector('.commentlist-section');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}
function jumpToPage() {
  goToPage(inputPage.value);
}
watch(analysisData, () => {
  currentPage.value = 1;
  inputPage.value = 1;
});
function formatTime(ts) {
  // 兼容秒和毫秒
  if (typeof ts === 'string') ts = Number(ts);
  if (ts < 1e11) ts = ts * 1000; // 10位时间戳，转为毫秒
  const d = new Date(ts);
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const h = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  const s = String(d.getSeconds()).padStart(2, '0');
  return `${y}-${m}-${day} ${h}:${min}:${s}`;
}

onMounted(() => {
  // 组件挂载后的初始化
});

onUnmounted(() => {
  if (wordcloudInstance) {
    wordcloudInstance.dispose();
  }
});
</script>

<style scoped>
.user-tracking {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  background-color: var(--background);
}

.search-section {
  margin-bottom: 3rem;
}

.search-container {
  max-width: 600px;
  margin: 0 auto;
}

.search-box {
  display: flex;
  gap: 1rem;
  background-color: var(--card);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.search-box input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: 2px solid var(--border);
  border-radius: 8px;
  background-color: var(--background);
  color: var(--foreground);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(251, 114, 153, 0.1);
}

.analyze-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, var(--primary), #e91e63);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.analyze-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(251, 114, 153, 0.3);
}

.analyze-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem;
  background-color: rgba(239, 68, 68, 0.1);
  color: #EF4444;
  border-radius: 12px;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.user-info {
  margin-bottom: 3rem;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease;
}

.user-info.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.user-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem 0;
}

.user-avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.user-details h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--foreground);
}

.user-details p {
  color: var(--muted-foreground);
  font-size: 1.1rem;
}

.analysis-content {
  opacity: 0;
  transform: translateY(30px);
  transition: all 1s ease 0.3s;
}

.analysis-content.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.analysis-section {
  margin-bottom: 4rem;
  padding: 2rem 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--foreground);
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--primary);
}

.chart-wrapper {
  height: 300px;
  margin: 1rem 0;
}

.wordcloud-wrapper {
  margin: 2rem 0;
}

.wordcloud-container {
  width: 100%;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.keywords-display {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin: 2rem 0;
}

.keyword-item {
  font-size: 2rem;
  font-weight: 800;
  color: var(--primary);
  padding: 1rem 2rem;
  background: linear-gradient(135deg, rgba(251, 114, 153, 0.1), rgba(35, 173, 229, 0.1));
  border-radius: 16px;
  border: 2px solid var(--primary);
  opacity: 0;
  animation: slideInKeyword 0.8s ease forwards;
  transition: all 0.3s ease;
}

.keyword-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(251, 114, 153, 0.2);
}

@keyframes slideInKeyword {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.friendly-display {
  margin: 2rem 0;
}

.score-main {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.score-number {
  font-size: 4rem;
  font-weight: 900;
  color: var(--primary);
  line-height: 1;
}

.score-total {
  font-size: 2rem;
  color: var(--muted-foreground);
  font-weight: 600;
}

.score-description {
  font-size: 1.2rem;
  line-height: 1.6;
  color: var(--foreground);
  margin: 0;
}

.interest-display {
  margin: 2rem 0;
}

.interest-text {
  font-size: 1.3rem;
  line-height: 1.8;
  color: var(--foreground);
  margin: 0;
  text-align: justify;
}

.empty-state {
  text-align: center;
  padding: 6rem 2rem;
  color: var(--muted-foreground);
}

.empty-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 2rem;
  background-color: var(--muted);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--muted-foreground);
  font-size: 2.5rem;
}

.empty-state h3 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--foreground);
}

.empty-state p {
  font-size: 1.1rem;
}

.comment-total {
  text-align: right;
  color: var(--muted-foreground);
  font-size: 1.1rem;
  margin-top: -1.5rem;
  margin-bottom: 1.5rem;
  margin-right: 0.5rem;
}

.commentlist-section {
  position: relative;
  background: var(--card);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  padding: 2rem 1rem 4.5rem 1rem;
  margin-bottom: 3rem;
}

.commentlist-wrapper {
  max-height: 400px;
  overflow-y: auto;
  padding: 0.5rem 0.5rem 2.5rem 0.5rem;
}

.comment-item {
  border-bottom: 1px solid var(--border);
  padding: 0.5rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.comment-time {
  color: var(--muted-foreground);
  font-size: 0.95rem;
}

.comment-content {
  color: var(--foreground);
  font-size: 1.1rem;
  word-break: break-all;
}

.no-comments {
  color: var(--muted-foreground);
  text-align: center;
  padding: 2rem 0;
}

.pagination-bar {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  background: rgba(255,255,255,0.85);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  z-index: 10;
}

.pagination-bar button {
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.3rem 1.2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.pagination-bar button:disabled {
  background: #eee;
  color: #aaa;
  cursor: not-allowed;
}

.pagination-bar input[type="number"] {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.1rem 0.3rem;
  font-size: 1rem;
  width: 2.5em;
}

@media (max-width: 768px) {
  .user-tracking {
    padding: 1rem;
  }
  
  .search-box {
    flex-direction: column;
    padding: 1rem;
  }
  
  .user-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .keywords-display {
    justify-content: center;
  }
  
  .keyword-item {
    font-size: 1.5rem;
    padding: 0.75rem 1.5rem;
  }
  
  .score-number {
    font-size: 3rem;
  }
  
  .interest-text {
    font-size: 1.1rem;
  }
}
</style>
