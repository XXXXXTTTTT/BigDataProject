<template>
  <div class="hot-videos">
    <!-- 顶部切换按钮 -->
    <div class="tab-switcher">
      <button 
        class="tab-button" 
        :class="{ active: activeTab === 'overview' }"
        @click="activeTab = 'overview'"
      >
        总体特征
      </button>
      <button 
        class="tab-button" 
        :class="{ active: activeTab === 'videos' }"
        @click="activeTab = 'videos'"
      >
        热门视频
      </button>
    </div>

    <!-- 总体特征内容 -->
    <div v-if="activeTab === 'overview'" class="overview-content">
      <div class="page-header">
        <h2>热门视频总体特征分析</h2>
        <button class="refresh-button" @click="refreshAllData" :disabled="isLoading">
          <RefreshCwIcon :class="{ spinning: isLoading }" />
          {{ isLoading ? '加载中...' : '刷新数据' }}
        </button>
      </div>

      <!-- 在线人数分析 -->
      <div class="analysis-section">
        <div class="section-header">
          <h3><UsersIcon /> 在线人数分析</h3>
          <span class="section-desc">24小时用户活跃度趋势</span>
        </div>
        <div class="chart-container">
          <div v-if="dataLoaded" ref="onlineChart" class="chart"></div>
          <div v-else class="loading-placeholder">
            <LoaderIcon class="spinning" />
            <span>加载中...</span>
          </div>
        </div>
      </div>

      <!-- 热门标签分析 -->
      <div class="analysis-section">
        <div class="section-header">
          <h3><TagIcon /> 热门标签分析</h3>
          <span class="section-desc">当前最热门的标签词云与排行</span>
        </div>
        
        <!-- 标签词云 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">标签词云</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="tagChart" class="chart wordcloud-chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>

        <!-- 热门标签排行 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">热门标签排行榜</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="tagRankChart" class="chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 视频分区分析 -->
      <div class="analysis-section">
        <div class="section-header">
          <h3><GridIcon /> 视频分区分析</h3>
          <span class="section-desc">各分区多维度数据对比</span>
        </div>
        
        <!-- 分区播放数据对比 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">分区播放与互动数据对比</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="categoryChart" class="chart large-chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>

        <!-- 分区详细指标 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">分区详细指标表现</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="categoryDetailChart" class="chart large-chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 热门UP分析 -->
      <div class="analysis-section">
        <div class="section-header">
          <h3><StarIcon /> 热门UP主分析</h3>
          <span class="section-desc">UP主多维度表现分析</span>
        </div>
        
        <!-- UP主播放量排行 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">UP主播放量增长排行</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="upViewChart" class="chart upview-chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>

        <!-- UP主综合数据对比 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">UP主综合数据表现</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="upMetricsChart" class="chart large-chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 视频类型分析 -->
      <div class="analysis-section">
        <div class="section-header">
          <h3><VideoIcon /> 视频类型分析</h3>
          <span class="section-desc">不同时长视频的全方位表现对比</span>
        </div>
        
        <!-- 视频数量分布 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">视频数量分布</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="videoTypePieChart" class="chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>

        <!-- 视频类型表现指标 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">各类型视频表现指标对比</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="videoTypeMetricsChart" class="chart large-chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>

        <!-- 视频类型详细数据 -->
        <div class="chart-wrapper">
          <h4 class="chart-title">视频类型详细数据分析</h4>
          <div class="chart-container">
            <div v-if="dataLoaded" ref="videoTypeDetailChart" class="chart large-chart"></div>
            <div v-else class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>加载中...</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门视频内容 -->
    <div v-if="activeTab === 'videos'" class="videos-content">
      <div class="page-header">
        <h2>热门B站视频</h2>
      </div>
      <div class="video-gallery">
        <div class="video-card" v-for="item in pagedVideos" :key="item.aid">
          <div class="video-thumb">
            <div class="video-link" @click="showAnalysisCard(item)">
              <img :src="proxyImg(item.pic)" :alt="item.title" />
            </div>
          </div>
          <div class="video-info">
            <h3 class="video-title">
              <div class="video-link" @click="showAnalysisCard(item)">{{ item.title }}</div>
            </h3>
            <div class="video-meta">
              <img class="up-face" :src="proxyImg(item.owner_face)" :alt="item.owner_name" />
              <span class="up-name">{{ item.owner_name }}</span>
              <span class="video-tname">{{ item.tname }}</span>
            </div>
            <div class="video-stats">
              <span class="stat-item"><PlayIcon class="stat-icon" />{{ formatNumber(item.stat_view) }}</span>
              <span class="stat-item"><LikeIcon class="stat-icon" />{{ formatNumber(item.stat_like) }}</span>
              <span class="stat-item"><CommentIcon class="stat-icon" />{{ formatNumber(item.stat_reply) }}</span>
              <span class="stat-item"><TimeIcon class="stat-icon" />{{ formatTime(item.pubdate) }}</span>
            </div>
          </div>
        </div>
      </div>
        <div class="pagination">
          <button :disabled="currentPage === 1" @click="prevPage">上一页</button>
          <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
          
          <!-- 快速页码跳转 -->
          <template v-for="page in visiblePages" :key="page">
            <button
              v-if="page !== currentPage"
              class="page-jump-btn"
              @click="goToPage(page)"
            >{{ page }}</button>
            <span v-else class="current-page">{{ page }}</span>
          </template>
          
          <!-- 输入跳转 -->
          <input
            v-model="inputPage"
            type="number"
            min="1"
            :max="totalPages"
            class="page-input"
            @keyup.enter="jumpToInputPage"
            style="width: 60px; margin: 0 0.5rem;"
          />
          <button @click="jumpToInputPage">跳转</button>
          
          <button :disabled="currentPage === totalPages" @click="nextPage">下一页</button>
        </div>
      <!-- 浮动分析卡片 -->
      <div v-if="showCard" class="analysis-card-overlay" @click="closeAnalysisCard">
        <div class="analysis-card" @click.stop>
          <button class="close-button" @click="closeAnalysisCard">×</button>
          <div class="analysis-card-content">
            <div class="video-analysis-header">
              <h3>{{ selectedVideo?.title }}</h3>
              <p class="video-meta-info">
                UP主: {{ selectedVideo?.owner_name }} | 
                分区: {{ selectedVideo?.tname }} | 
                发布时间: {{ formatTime(selectedVideo?.pubdate) }}
              </p>
            </div>
            
            <!-- 修复：始终渲染图表容器，通过CSS控制显示 -->
            <div ref="analysisChartRef" class="analysis-chart" :style="{ display: analysisLoading || analysisChartData.length === 0 ? 'none' : 'block' }"></div>
            
            <div v-if="analysisLoading" class="loading-placeholder">
              <LoaderIcon class="spinning" />
              <span>正在加载视频分析数据...</span>
            </div>
            
            <div v-else-if="analysisChartData.length === 0" class="no-data-placeholder">
              <p>暂无分析数据</p>
            </div>
            <div style="text-align:center; margin-top:0.5rem;">
              <a
                v-if="selectedVideo && selectedVideo.aid"
                :href="`https://www.bilibili.com/video/av${selectedVideo.aid}`"
                target="_blank"
                rel="noopener noreferrer"
                class="open-video-btn"
              >
                打开视频
              </a>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="videos.length === 0" class="empty-state">
        <div class="empty-icon">
          <VideoIcon />
        </div>
        <h3>暂无热门视频</h3>
        <p>请稍后再试或检查网络连接。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import 'echarts-wordcloud';
import axios from 'axios';
import { 
  RefreshCw as RefreshCwIcon,
  Loader as LoaderIcon,
  Users as UsersIcon,
  Tag as TagIcon,
  Grid as GridIcon,
  Star as StarIcon,
  Video as VideoIcon,
  Play as PlayIcon,
  ThumbsUp as LikeIcon,
  MessageCircle as CommentIcon,
  Clock as TimeIcon
} from 'lucide-vue-next';

const inputPage = ref('');
const activeTab = ref('overview');
const isLoading = ref(false);
const dataLoaded = ref(false);

// 数据存储
const onlineData = ref([]);
const tagData = ref([]);
const categoryData = ref([]);
const upData = ref([]);
const videoTypeData = ref([]);

// 图表引用
const onlineChart = ref(null);
const tagChart = ref(null);
const tagRankChart = ref(null);
const categoryChart = ref(null);
const categoryDetailChart = ref(null);
const upViewChart = ref(null);
const upMetricsChart = ref(null);
const videoTypePieChart = ref(null);
const videoTypeMetricsChart = ref(null);
const videoTypeDetailChart = ref(null);

// 图表实例
let chartInstances = {};

// 视频分析相关
const analysisChartRef = ref(null);
let analysisChartInstance = null;
const analysisChartData = ref([]);
const analysisLoading = ref(false);

// 热门视频相关
const videos = ref([]);
const pageSize = 48;
const currentPage = ref(1);
const showCard = ref(false);
const selectedVideo = ref(null);

const totalPages = computed(() => Math.ceil(videos.value.length / pageSize));
const pagedVideos = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return videos.value.slice(start, start + pageSize);
});

// 监听activeTab变化，重新渲染图表
watch(activeTab, async (newTab) => {
  if (newTab === 'overview' && dataLoaded.value) {
    await nextTick();
    renderAllCharts();
  } else if (newTab === 'videos' && videos.value.length === 0) {
    try {
      const res = await axios.get('http://127.0.0.1:3000/api/hot-videos');
      if(res.data && res.data.data) {
        videos.value = res.data.data;
      }
    } catch (error) {
      console.error('获取热门视频数据失败:', error);
    }
  }
});

// 监听分析数据变化，自动渲染图表
watch(analysisChartData, async (newData) => {
  if (newData.length > 0 && analysisChartRef.value) {
    await nextTick();
    renderAnalysisChart();
  }
}, { deep: true });





// API调用函数
const fetchOnlineData = async () => {
  try {
    const response = await fetch('http://localhost:3000/api/hot-videos/analyze/online-people');
    const result = await response.json();
    if (result.code === 0) {
      onlineData.value = result.data;
    }
  } catch (error) {
    console.error('获取在线人数数据失败:', error);
    onlineData.value = generateMockOnlineData();
  }
};


const fetchTagData = async () => {
  try {
    const response = await fetch('http://localhost:3000/api/hot-videos/analyze/hot-tags');
    const result = await response.json();
    if (result.code === 0) {
      tagData.value = result.data;
    }
  } catch (error) {
    console.error('获取热门标签数据失败:', error);
    tagData.value = generateMockTagData();
  }
};

const fetchCategoryData = async () => {
  try {
    const response = await fetch('http://localhost:3000/api/hot-videos/analyze/category');
    const result = await response.json();
    if (result.code === 0) {
      categoryData.value = result.data;
    }
  } catch (error) {
    console.error('获取分区数据失败:', error);
    categoryData.value = generateMockCategoryData();
  }
};

const fetchUpData = async () => {
  try {
    const response = await fetch('http://localhost:3000/api/hot-videos/analyze/up-growth');
    const result = await response.json();
    if (result.code === 0) {
      upData.value = result.data;
    }
  } catch (error) {
    console.error('获取UP主数据失败:', error);
    upData.value = generateMockUpData();
  }
};

const fetchVideoTypeData = async () => {
  try {
    const response = await fetch('http://localhost:3000/api/hot-videos/analyze/video-types');
    const result = await response.json();
    if (result.code === 0) {
      videoTypeData.value = result.data;
    }
  } catch (error) {
    console.error('获取视频类型数据失败:', error);
    videoTypeData.value = generateMockVideoTypeData();
  }
};

// 获取单个视频分析数据
const fetchVideoAnalysisData = async (aid) => {
  try {
    const response = await axios.get(`http://localhost:3000/api/hot-videos/analyze/video-info?aid=${aid}`);
    if (response.data && response.data.code === 0 && Array.isArray(response.data.data)) {
      // 按timestamp升序排序
      const sortedData = response.data.data.slice().sort((a, b) => a.timestamp - b.timestamp);
      return sortedData;
    }
    return [];
  } catch (error) {
    console.error('获取视频分析数据失败:', error);
    return [];
  }
};

// 计算动态Y轴范围
const calculateDynamicYAxisRange = (data, padding = 0.1) => {
  if (!data || data.length === 0) return { min: 0, max: 100 };
  
  const validData = data.filter(val => val !== null && val !== undefined && !isNaN(val));
  if (validData.length === 0) return { min: 0, max: 100 };
  
  const min = Math.min(...validData);
  const max = Math.max(...validData);
  
  // 如果最大值和最小值相同，设置一个默认范围
  if (min === max) {
    return {
      min: Math.max(0, min - Math.abs(min) * 0.1),
      max: max + Math.abs(max) * 0.1 + 1
    };
  }
  
  const range = max - min;
  const paddingValue = range * padding;
  
  return {
    min: Math.max(0, min - paddingValue),
    max: max + paddingValue
  };
};

// 渲染视频分析图表
const renderAnalysisChart = () => {
  console.log('renderAnalysisChart called, ref:', analysisChartRef.value, 'data length:', analysisChartData.value.length);
  
  if (!analysisChartRef.value || !analysisChartData.value.length) {
    console.warn('图表容器或数据未准备好，跳过渲染');
    return;
  }

  if (analysisChartInstance) {
    analysisChartInstance.dispose();
  }
  
  analysisChartInstance = echarts.init(analysisChartRef.value);
  
  const data = analysisChartData.value;
  
  // 格式化时间轴数据
  const timeLabels = data.map(item => {
    const date = new Date(item.timestamp * 1000);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  });
  
  // 定义要显示的指标（忽略growth字段）
  const metrics = [
    { key: 'stat_view', name: '播放量', color: '#FB7299' },
    { key: 'stat_danmaku', name: '弹幕数', color: '#23ADE5' },
    { key: 'stat_reply', name: '评论数', color: '#10B981' },
    { key: 'stat_favorite', name: '收藏数', color: '#F59E0B' },
    { key: 'stat_coin', name: '投币数', color: '#8B5CF6' },
    { key: 'stat_share', name: '分享数', color: '#EF4444' },
    { key: 'stat_like', name: '点赞数', color: '#06B6D4' }
  ];
  
  // 创建系列数据
  const series = metrics.map(metric => {
    const seriesData = data.map(item => item[metric.key]);
    return {
      name: metric.name,
      type: 'line',
      data: seriesData,
      smooth: true,
      showSymbol: false,
      lineStyle: {
        color: metric.color,
        width: 2
      },
      itemStyle: {
        color: metric.color
      }
    };
  });

  // legend默认选中配置
  const legendSelected = {
    '播放量': true,
    '弹幕数': false,
    '评论数': false,
    '收藏数': false,
    '投币数': false,
    '分享数': false,
    '点赞数': false
  };
  // 只用初始选中的那一条线的数据算y轴范围
  const defaultSelectedMetric = metrics.find(m => legendSelected[m.name]);
  const defaultMetricData = data.map(item => item[defaultSelectedMetric.key]).filter(val => val !== null && val !== undefined);
  const yAxisRange = calculateDynamicYAxisRange(defaultMetricData);

  const option = {
    title: {
      text: '视频数据变化趋势分析',
      left: 'center',
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#333'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      },
      formatter: function(params) {
        let result = `<div style="font-weight: bold; margin-bottom: 5px;">${params[0].axisValue}</div>`;
        params.forEach(param => {
          if (param.value !== null && param.value !== undefined) {
            result += `<div style="color: ${param.color};">
              ${param.seriesName}: ${param.value.toLocaleString()}
            </div>`;
          }
        });
        return result;
      }
    },
    legend: {
      data: metrics.map(m => m.name),
      selectedMode: 'single', // 设置为单选模式
      selected: legendSelected,
      top: 40,
      textStyle: {
        fontSize: 12
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: timeLabels,
      axisLabel: {
        rotate: 30,
        fontSize: 10,
        color: '#666'
      },
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      }
    },
    yAxis: {
      type: 'value',
      min: Math.floor(yAxisRange.min),
      max: Math.ceil(yAxisRange.max),
      axisLabel: {
        formatter: function(value) {
          if (value >= 10000) {
            return (value / 10000).toFixed(1) + '万';
          }
          return value.toLocaleString();
        },
        color: '#666'
      },
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      },
      splitLine: {
        lineStyle: {
          color: '#f0f0f0'
        }
      }
    },
    series: series,
    animation: true,
    animationDuration: 1000
  };
  
  analysisChartInstance.setOption(option);
  
  // 监听图例选择变化，动态调整Y轴范围
  analysisChartInstance.on('legendselectchanged', function(params) {
    const selectedMetric = Object.keys(params.selected).find(key => params.selected[key]);
    if (selectedMetric) {
      const metric = metrics.find(m => m.name === selectedMetric);
      if (metric) {
        const metricData = data.map(item => item[metric.key]).filter(val => val !== null && val !== undefined);
        const metricRange = calculateDynamicYAxisRange(metricData);
        
        analysisChartInstance.setOption({
          yAxis: {
            min: Math.floor(metricRange.min),
            max: Math.ceil(metricRange.max)
          }
        });
      }
    }
  });
  
  console.log('图表渲染完成');
};

// 显示分析卡片
const showAnalysisCard = async (video) => {
  console.log('显示分析卡片:', video.title);
  selectedVideo.value = video;
  showCard.value = true;
  analysisLoading.value = true;
  analysisChartData.value = [];
  document.body.style.overflow = 'hidden';
  
  // 等待DOM更新
  await nextTick();
  console.log('DOM更新后，analysisChartRef:', analysisChartRef.value);
  
  try {
    const data = await fetchVideoAnalysisData(video.aid);
    console.log('获取到数据:', data.length, '条记录');
    analysisChartData.value = data;
    // 数据更新后，watch会自动触发图表渲染
  } catch (error) {
    console.error('加载视频分析数据失败:', error);
  } finally {
    analysisLoading.value = false;
  }
};

// 关闭分析卡片
const closeAnalysisCard = () => {
  showCard.value = false;
  selectedVideo.value = null;
  analysisChartData.value = [];
  document.body.style.overflow = 'auto';
  
  if (analysisChartInstance) {
    analysisChartInstance.dispose();
    analysisChartInstance = null;
  }
};

// 模拟数据生成函数
const generateMockOnlineData = () => {
  const data = [];
  for (let i = 0; i < 24; i++) {
    data.push({
      timestamp: Date.now() + i * 3600000,
      video_count: Math.floor(Math.random() * 1000) + 500,
      total_people: Math.floor(Math.random() * 100000) + 50000,
      total_people_web: Math.floor(Math.random() * 50000) + 25000,
      avg_people: Math.floor(Math.random() * 5000) + 2000,
      avg_people_web: Math.floor(Math.random() * 2500) + 1000
    });
  }
  return data;
};

const generateMockTagData = () => {
  const tags = ['搞笑', '高考', 'UP小剧场', '游戏', '动漫', '音乐', '舞蹈', '科技', '美食', '旅游', '教育', '体育', '时尚', '生活', '娱乐', '电影', '综艺', '知识', '汽车', '数码'];
  return tags.map(tag => ({
    tag,
    count: Math.floor(Math.random() * 500) + 100
  })).sort((a, b) => b.count - a.count);
};

const generateMockCategoryData = () => {
  return [
    {
      category: "国产动画",
      unique_videos_with_growth: 4,
      avg_observation_hours: "8.38",
      avg_view_growth_per_hour: "114455.1",
      avg_like_growth_per_hour: "1748.5",
      avg_coin_growth_per_hour: "2067.8",
      avg_favorite_growth_per_hour: "368.8",
      avg_share_growth_per_hour: "33.3",
      avg_reply_growth_per_hour: "191.6",
      avg_danmaku_growth_per_hour: "1375.5"
    },
    {
      category: "游戏",
      unique_videos_with_growth: 8,
      avg_observation_hours: "12.25",
      avg_view_growth_per_hour: "95432.7",
      avg_like_growth_per_hour: "1892.3",
      avg_coin_growth_per_hour: "1543.6",
      avg_favorite_growth_per_hour: "456.2",
      avg_share_growth_per_hour: "78.9",
      avg_reply_growth_per_hour: "234.1",
      avg_danmaku_growth_per_hour: "987.3"
    },
    {
      category: "科技",
      unique_videos_with_growth: 6,
      avg_observation_hours: "9.67",
      avg_view_growth_per_hour: "76543.2",
      avg_like_growth_per_hour: "1234.8",
      avg_coin_growth_per_hour: "987.4",
      avg_favorite_growth_per_hour: "321.5",
      avg_share_growth_per_hour: "45.6",
      avg_reply_growth_per_hour: "156.7",
      avg_danmaku_growth_per_hour: "654.2"
    },
    {
      category: "音乐",
      unique_videos_with_growth: 5,
      avg_observation_hours: "11.34",
      avg_view_growth_per_hour: "89765.4",
      avg_like_growth_per_hour: "2134.6",
      avg_coin_growth_per_hour: "1876.3",
      avg_favorite_growth_per_hour: "543.7",
      avg_share_growth_per_hour: "89.2",
      avg_reply_growth_per_hour: "198.4",
      avg_danmaku_growth_per_hour: "1123.8"
    },
    {
      category: "生活",
      unique_videos_with_growth: 7,
      avg_observation_hours: "14.56",
      avg_view_growth_per_hour: "67890.3",
      avg_like_growth_per_hour: "1567.9",
      avg_coin_growth_per_hour: "1234.5",
      avg_favorite_growth_per_hour: "432.1",
      avg_share_growth_per_hour: "56.7",
      avg_reply_growth_per_hour: "178.3",
      avg_danmaku_growth_per_hour: "789.6"
    },
    {
      category: "美食",
      unique_videos_with_growth: 3,
      avg_observation_hours: "16.78",
      avg_view_growth_per_hour: "54321.8",
      avg_like_growth_per_hour: "1345.2",
      avg_coin_growth_per_hour: "876.9",
      avg_favorite_growth_per_hour: "298.4",
      avg_share_growth_per_hour: "41.2",
      avg_reply_growth_per_hour: "134.7",
      avg_danmaku_growth_per_hour: "567.8"
    }
  ];
};

const generateMockUpData = () => {
  return [
    {
      owner_name: "大象新闻",
      video_count: 7,
      avg_observation_hours: "12.57",
      avg_view_growth_per_hour: "16158.8",
      avg_like_growth_per_hour: "1610.4",
      avg_coin_growth_per_hour: "63.8",
      avg_favorite_growth_per_hour: "83.3",
      avg_share_growth_per_hour: "127.3",
      avg_reply_growth_per_hour: "52.6"
    },
    {
      owner_name: "磊哥游戏",
      video_count: 5,
      avg_observation_hours: "20.74",
      avg_view_growth_per_hour: "18246.1",
      avg_like_growth_per_hour: "1191.1",
      avg_coin_growth_per_hour: "37.0",
      avg_favorite_growth_per_hour: "39.0",
      avg_share_growth_per_hour: "20.5",
      avg_reply_growth_per_hour: "55.7"
    },
    {
      owner_name: "科技UP主",
      video_count: 3,
      avg_observation_hours: "15.32",
      avg_view_growth_per_hour: "14567.9",
      avg_like_growth_per_hour: "987.6",
      avg_coin_growth_per_hour: "45.2",
      avg_favorite_growth_per_hour: "67.8",
      avg_share_growth_per_hour: "23.4",
      avg_reply_growth_per_hour: "43.1"
    },
    {
      owner_name: "音乐达人",
      video_count: 4,
      avg_observation_hours: "18.45",
      avg_view_growth_per_hour: "13245.7",
      avg_like_growth_per_hour: "1456.8",
      avg_coin_growth_per_hour: "89.3",
      avg_favorite_growth_per_hour: "123.4",
      avg_share_growth_per_hour: "34.6",
      avg_reply_growth_per_hour: "78.9"
    },
    {
      owner_name: "生活博主",
      video_count: 6,
      avg_observation_hours: "13.67",
      avg_view_growth_per_hour: "12890.4",
      avg_like_growth_per_hour: "1234.5",
      avg_coin_growth_per_hour: "67.8",
      avg_favorite_growth_per_hour: "98.7",
      avg_share_growth_per_hour: "28.9",
      avg_reply_growth_per_hour: "56.3"
    },
    {
      owner_name: "美食探店",
      video_count: 2,
      avg_observation_hours: "19.23",
      avg_view_growth_per_hour: "11567.2",
      avg_like_growth_per_hour: "1098.7",
      avg_coin_growth_per_hour: "54.3",
      avg_favorite_growth_per_hour: "76.5",
      avg_share_growth_per_hour: "19.8",
      avg_reply_growth_per_hour: "41.2"
    }
  ];
};

const generateMockVideoTypeData = () => {
  return [
    {
      duration_category: "短视频(<1分钟)",
      video_count: 80,
      avg_observation_hours: "15.72",
      view_hour: "22086.4",
      like_hour: "2006.7",
      coin_hour: "135.4",
      favorite_hour: "242.7",
      share_hour: "85.8",
      reply_hour: "25.4",
      danmaku_hour: "50.7"
    },
    {
      duration_category: "短中视频(1-5分钟)",
      video_count: 475,
      avg_observation_hours: "17.87",
      view_hour: "15440.9",
      like_hour: "908.6",
      coin_hour: "111.7",
      favorite_hour: "230.3",
      share_hour: "40.0",
      reply_hour: "17.7",
      danmaku_hour: "24.8"
    },
    {
      duration_category: "中等视频(5-10分钟)",
      video_count: 184,
      avg_observation_hours: "17.33",
      view_hour: "14630.8",
      like_hour: "705.2",
      coin_hour: "119.9",
      favorite_hour: "207.8",
      share_hour: "29.8",
      reply_hour: "25.2",
      danmaku_hour: "43.9"
    },
    {
      duration_category: "长视频(10-30分钟)",
      video_count: 234,
      avg_observation_hours: "17.60",
      view_hour: "14945.2",
      like_hour: "536.6",
      coin_hour: "160.3",
      favorite_hour: "174.4",
      share_hour: "25.3",
      reply_hour: "28.6",
      danmaku_hour: "74.9"
    },
    {
      duration_category: "超长视频(>30分钟)",
      video_count: 87,
      avg_observation_hours: "16.25",
      view_hour: "15456.8",
      like_hour: "484.5",
      coin_hour: "281.5",
      favorite_hour: "350.8",
      share_hour: "32.8",
      reply_hour: "39.8",
      danmaku_hour: "257.5"
    }
  ];
};

// 图表渲染函数
const renderOnlineChart = () => {
  if (!onlineChart.value || !onlineData.value || onlineData.value.length === 0) {
    console.warn("图表容器或数据未准备好，跳过渲染。");
    return;
  }
  
  if (chartInstances.online) {
    chartInstances.online.dispose();
  }
  
  chartInstances.online = echarts.init(onlineChart.value);

  console.log("--- 开始处理24小时在线数据 ---");
  const hourMap = {};

  onlineData.value.forEach(item => {
    let ts = item.timestamp;
    const ts_raw = ts; 

    if (typeof ts === 'string') ts = Number(ts);
    if (ts < 1e12) ts = ts * 1000; 

    const d = new Date(ts);
    const year = d.getFullYear();
    const month = (d.getMonth() + 1).toString().padStart(2, '0');
    const day = d.getDate().toString().padStart(2, '0');
    const h = d.getHours().toString().padStart(2, '0');
    const m = d.getMinutes().toString().padStart(2, '0');
    const s = d.getSeconds().toString().padStart(2, '0');
    const formattedDate = `${year}-${month}-${day} ${h}:${m}:${s}`;

    let originalHour = d.getHours();
    const min = d.getMinutes();
    
    let targetHour = originalHour;
    if (min >= 30) {
      targetHour = (originalHour + 1) % 24;
    }

    console.log(`[数据分组] 时间戳: ${ts_raw} -> ${formattedDate} | 分钟数: ${min} | 原小时: ${originalHour}点 -> 计入: ${targetHour}点`);

    if (!hourMap[targetHour]) {
      hourMap[targetHour] = [];
    }
    hourMap[targetHour].push(item);
  });

  const totalPeople = [];
  const webPeople = [];
  const hourlyAverages = []; 

  for (let i = 0; i < 24; i++) {
    const arr = hourMap[i] || [];
    let avgTotal, avgWeb;

    if (arr.length === 0) {
      avgTotal = null;
      avgWeb = null;
    } else {
      const sumTotal = arr.reduce((sum, x) => sum + parseFloat(x.total_people || 0), 0);
      const sumWeb = arr.reduce((sum, x) => sum + parseFloat(x.total_people_web || 0), 0);
      
      avgTotal = Math.round(sumTotal / arr.length);
      avgWeb = Math.round(sumWeb / arr.length);
    }
    
    totalPeople.push(avgTotal);
    webPeople.push(avgWeb);
    
    hourlyAverages.push({
        '小时 (Hour)': `${i}:00`,
        '原始数据条数 (Count)': arr.length,
        '平均总在线 (Avg Total)': avgTotal,
        '平均Web端在线 (Avg Web)': avgWeb
    });
  }
  
  console.log("--- 每小时统计结果 (已修正) ---");
  console.table(hourlyAverages);
  
  const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`);

  const option = {
    title: { text: '24小时在线人数趋势', left: 'center', textStyle: { color: '#333', fontSize: 18, fontWeight: 'bold' }},
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' }},
    legend: { data: ['总在线人数', 'Web端在线人数'], top: 40 },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '20%', containLabel: true },
    xAxis: { type: 'category', data: hours, axisLabel: { color: '#666' }},
    yAxis: { type: 'value', axisLabel: { color: '#666' }},
    series: [
      { name: '总在线人数', type: 'line', data: totalPeople, smooth: true, connectNulls: false, lineStyle: { color: '#FB7299', width: 3 }, areaStyle: { color: 'rgba(251, 114, 153, 0.1)' }},
      { name: 'Web端在线人数', type: 'line', data: webPeople, smooth: true, connectNulls: false, lineStyle: { color: '#23ADE5', width: 3 }, areaStyle: { color: 'rgba(35, 173, 229, 0.1)' }}
    ]
  };
  
  chartInstances.online.setOption(option);
};

const renderTagChart = () => {
  if (!tagChart.value || tagData.value.length === 0) return;
  
  if (chartInstances.tagCloud) {
    chartInstances.tagCloud.dispose();
  }
  
  chartInstances.tagCloud = echarts.init(tagChart.value);
  
  const wordCloudData = tagData.value.map(item => ({
    name: item.tag,
    value: item.count
  }));
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: function (params) {
        return `${params.name}: ${params.value} 次`;
      }
    },
    series: [{
      type: 'wordCloud',
      gridSize: 8,
      sizeRange: [12, 80],
      rotationRange: [-45, 45],
      shape: 'circle',
      width: '100%',
      height: '90%',
      textStyle: {
        fontFamily: 'Inter, sans-serif',
        color: function () {
          const colors = ['#FB7299', '#23ADE5', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444'];
          return colors[Math.floor(Math.random() * colors.length)];
        }
      },
      data: wordCloudData
    }]
  };
  
  chartInstances.tagCloud.setOption(option);
};

const renderTagRankChart = () => {
  if (!tagRankChart.value || tagData.value.length === 0) return;
  
  if (chartInstances.tagRank) {
    chartInstances.tagRank.dispose();
  }
  
  chartInstances.tagRank = echarts.init(tagRankChart.value);
  
  const topTags = tagData.value.slice(0, 15);
  
  const option = {
    title: {
      text: 'TOP15 热门标签排行',
      left: 'center',
      textStyle: { color: '#333', fontSize: 16, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: topTags.map(item => item.tag),
      axisLabel: { 
        color: '#666',
        rotate: 45,
        interval: 0
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#666' }
    },
    series: [{
      type: 'bar',
      data: topTags.map(item => item.count),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
          { offset: 0, color: '#FB7299' },
          { offset: 1, color: '#23ADE5' }
        ])
      },
      label: {
        show: true,
        position: 'top',
        color: '#666',
        fontSize: 12
      }
    }]
  };
  
  chartInstances.tagRank.setOption(option);
};

const renderCategoryChart = () => {
  if (!categoryChart.value || categoryData.value.length === 0) return;

  if (chartInstances.category) {
    chartInstances.category.dispose();
  }

  chartInstances.category = echarts.init(categoryChart.value);

  const categories = categoryData.value.map(item => item.category);
  const viewData = categoryData.value.map(item => parseFloat(item.avg_view_growth_per_hour));
  const likeData = categoryData.value.map(item => parseFloat(item.avg_like_growth_per_hour));
  const coinData = categoryData.value.map(item => parseFloat(item.avg_coin_growth_per_hour));
  const favoriteData = categoryData.value.map(item => parseFloat(item.avg_favorite_growth_per_hour));

  const option = {
    title: {
      text: '分区播放与互动数据对比',
      left: 'center',
      textStyle: { color: '#333', fontSize: 24, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      selectedMode: 'single',
      data: ['播放增长/小时', '点赞增长/小时', '投币增长/小时', '收藏增长/小时'],
      selected: {
        '播放增长/小时': true,
        '点赞增长/小时': false,
        '投币增长/小时': false,
        '收藏增长/小时': false
      },
      top: 40
    },
    grid: {
      left: '0%',
      right: '4%',
      bottom: '3%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        color: '#666'
      }
    },
    series: [
      {
        name: '播放增长/小时',
        type: 'bar',
        data: viewData,
        itemStyle: { color: '#FB7299' }
      },
      {
        name: '点赞增长/小时',
        type: 'bar',
        data: likeData,
        itemStyle: { color: '#23ADE5' }
      },
      {
        name: '投币增长/小时',
        type: 'bar',
        data: coinData,
        itemStyle: { color: '#10B981' }
      },
      {
        name: '收藏增长/小时',
        type: 'bar',
        data: favoriteData,
        itemStyle: { color: '#F59E0B' }
      }
    ]
  };

  chartInstances.category.setOption(option);
};

const renderCategoryDetailChart = () => {
  if (!categoryDetailChart.value || categoryData.value.length === 0) return;

  if (chartInstances.categoryDetail) {
    chartInstances.categoryDetail.dispose();
  }

  chartInstances.categoryDetail = echarts.init(categoryDetailChart.value);

  const categories = categoryData.value.map(item => item.category);
  const shareData = categoryData.value.map(item => parseFloat(item.avg_share_growth_per_hour));
  const replyData = categoryData.value.map(item => parseFloat(item.avg_reply_growth_per_hour));
  const danmakuData = categoryData.value.map(item => parseFloat(item.avg_danmaku_growth_per_hour));

  const option = {
    title: {
      text: '分区详细指标表现',
      left: 'center',
      textStyle: { color: '#333', fontSize: 16, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      selectedMode: 'single',
      data: ['转发增长/小时', '评论增长/小时', '弹幕增长/小时'],
      selected: {
        '转发增长/小时': false,
        '评论增长/小时': true,
        '弹幕增长/小时': false,
      },
      top: 40
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        color: '#666',
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#666' }
    },
    series: [
      {
        name: '转发增长/小时',
        type: 'bar',
        data: shareData,
        itemStyle: { color: '#8B5CF6' }
      },
      {
        name: '评论增长/小时',
        type: 'bar',
        data: replyData,
        itemStyle: { color: '#EF4444' }
      },
      {
        name: '弹幕增长/小时',
        type: 'bar',
        data: danmakuData,
        itemStyle: { color: '#06B6D4' }
      }
    ]
  };
  
  chartInstances.categoryDetail.setOption(option);
};

const renderUpViewChart = () => {
  if (!upViewChart.value || upData.value.length === 0) return;
  
  if (chartInstances.upView) {
    chartInstances.upView.dispose();
  }
  
  chartInstances.upView = echarts.init(upViewChart.value);
  
  const sorted = upData.value.slice().sort((b, a) => parseFloat(b.avg_view_growth_per_hour) - parseFloat(a.avg_view_growth_per_hour));
  const upNames = sorted.map(item => item.owner_name);
  const viewGrowth = sorted.map(item => parseFloat(item.avg_view_growth_per_hour));
  
  const option = {
    title: {
      text: 'UP主播放量增长排行',
      left: 'center',
      textStyle: { color: '#333', fontSize: 20, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'category',
      data: upNames,
      axisLabel: { color: '#666' }
    },
    series: [{
      type: 'bar',
      data: viewGrowth,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#FB7299' },
          { offset: 1, color: '#23ADE5' }
        ])
      },
      label: {
        show: false
      }
    }]
  };
  
  chartInstances.upView.setOption(option);
};

const renderUpMetricsChart = () => {
  if (!upMetricsChart.value || upData.value.length === 0) return;
  
  if (chartInstances.upMetrics) {
    chartInstances.upMetrics.dispose();
  }
  
  chartInstances.upMetrics = echarts.init(upMetricsChart.value);
  
  const upNames = upData.value.map(item => item.owner_name);
  const likeData = upData.value.map(item => parseFloat(item.avg_like_growth_per_hour));
  const coinData = upData.value.map(item => parseFloat(item.avg_coin_growth_per_hour));
  const favoriteData = upData.value.map(item => parseFloat(item.avg_favorite_growth_per_hour));
  const shareData = upData.value.map(item => parseFloat(item.avg_share_growth_per_hour));
  const replyData = upData.value.map(item => parseFloat(item.avg_reply_growth_per_hour));
  
  const option = {
    title: {
      text: 'UP主综合数据表现',
      left: 'center',
      textStyle: { color: '#333', fontSize: 16, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      selectedMode: 'single',
      data: ['点赞增长', '投币增长', '收藏增长', '转发增长', '评论增长'],
      selected : {
        '点赞增长': true, 
        '投币增长': false, 
        '收藏增长': false, 
        '转发增长': false,
        '评论增长':false
      },
      top: 40
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: upNames,
      axisLabel: { 
        color: '#666',
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#666' }
    },
    series: [
      {
        name: '点赞增长',
        type: 'bar',
        data: likeData,
        itemStyle: { color: '#FB7299' }
      },
      {
        name: '投币增长',
        type: 'bar',
        data: coinData,
        itemStyle: { color: '#23ADE5' }
      },
      {
        name: '收藏增长',
        type: 'bar',
        data: favoriteData,
        itemStyle: { color: '#10B981' }
      },
      {
        name: '转发增长',
        type: 'bar',
        data: shareData,
        itemStyle: { color: '#F59E0B' }
      },
      {
        name: '评论增长',
        type: 'bar',
        data: replyData,
        itemStyle: { color: '#8B5CF6' }
      }
    ]
  };
  
  chartInstances.upMetrics.setOption(option);
};

const renderVideoTypePieChart = () => {
  if (!videoTypePieChart.value || videoTypeData.value.length === 0) return;
  
  if (chartInstances.videoTypePie) {
    chartInstances.videoTypePie.dispose();
  }
  
  chartInstances.videoTypePie = echarts.init(videoTypePieChart.value);
  
  const pieData = videoTypeData.value.map(item => ({
    name: item.duration_category,
    value: item.video_count
  }));
  
  const option = {
    title: {
      text: '视频数量分布',
      left: 'center',
      textStyle: { color: '#333', fontSize: 16, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'middle'
    },
    series: [{
      name: '视频数量',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['60%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        position: 'outside',
        formatter: '{b}: {c}'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '16',
          fontWeight: 'bold'
        }
      },
      data: pieData,
      color: ['#FB7299', '#23ADE5', '#10B981', '#F59E0B', '#8B5CF6']
    }]
  };
  
  chartInstances.videoTypePie.setOption(option);
};

const renderVideoTypeMetricsChart = () => {
  if (!videoTypeMetricsChart.value || videoTypeData.value.length === 0) return;
  
  if (chartInstances.videoTypeMetrics) {
    chartInstances.videoTypeMetrics.dispose();
  }
  
  chartInstances.videoTypeMetrics = echarts.init(videoTypeMetricsChart.value);
  
  const categories = videoTypeData.value.map(item => item.duration_category);
  const viewData = videoTypeData.value.map(item => parseFloat(item.view_hour));
  const likeData = videoTypeData.value.map(item => parseFloat(item.like_hour));
  const coinData = videoTypeData.value.map(item => parseFloat(item.coin_hour));
  const favoriteData = videoTypeData.value.map(item => parseFloat(item.favorite_hour));
  
  const option = {
    title: {
      text: '各类型视频表现指标对比',
      left: 'center',
      textStyle: { color: '#333', fontSize: 16, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['播放量/小时', '点赞/小时', '投币/小时', '收藏/小时'],
      selected: {
        '播放量/小时': false, '点赞/小时': true, '投币/小时': true, '收藏/小时': true
      },
      top: 40
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: { 
        color: '#666',
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#666' }
    },
    series: [
      {
        name: '播放量/小时',
        type: 'bar',
        data: viewData,
        itemStyle: { color: '#FB7299' }
      },
      {
        name: '点赞/小时',
        type: 'bar',
        data: likeData,
        itemStyle: { color: '#23ADE5' }
      },
      {
        name: '投币/小时',
        type: 'bar',
        data: coinData,
        itemStyle: { color: '#10B981' }
      },
      {
        name: '收藏/小时',
        type: 'bar',
        data: favoriteData,
        itemStyle: { color: '#F59E0B' }
      }
    ]
  };
  
  chartInstances.videoTypeMetrics.setOption(option);
};

const renderVideoTypeDetailChart = () => {
  if (!videoTypeDetailChart.value || videoTypeData.value.length === 0) return;
  
  if (chartInstances.videoTypeDetail) {
    chartInstances.videoTypeDetail.dispose();
  }
  
  chartInstances.videoTypeDetail = echarts.init(videoTypeDetailChart.value);
  
  const categories = videoTypeData.value.map(item => item.duration_category);
  const shareData = videoTypeData.value.map(item => parseFloat(item.share_hour));
  const replyData = videoTypeData.value.map(item => parseFloat(item.reply_hour));
  const danmakuData = videoTypeData.value.map(item => parseFloat(item.danmaku_hour));
  
  const option = {
    title: {
      text: '视频类型详细数据分析',
      left: 'center',
      textStyle: { color: '#333', fontSize: 16, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['转发/小时', '评论/小时', '弹幕/小时'],
      top: 40
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: { 
        color: '#666',
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#666' }
    },
    series: [
      {
        name: '转发/小时',
        type: 'bar',
        data: shareData,
        itemStyle: { color: '#8B5CF6' }
      },
      {
        name: '评论/小时',
        type: 'bar',
        data: replyData,
        itemStyle: { color: '#EF4444' }
      },
      {
        name: '弹幕/小时',
        type: 'bar',
        data: danmakuData,
        itemStyle: { color: '#06B6D4' }
      }
    ]
  };
  
  chartInstances.videoTypeDetail.setOption(option);
};

// 渲染所有图表
const renderAllCharts = async () => {
  await nextTick();
  renderOnlineChart();
  renderTagChart();
  renderTagRankChart();
  renderCategoryChart();
  renderCategoryDetailChart();
  renderUpViewChart();
  renderUpMetricsChart();
  renderVideoTypePieChart();
  renderVideoTypeMetricsChart();
  renderVideoTypeDetailChart();
};

// 刷新所有数据
const refreshAllData = async () => {
  isLoading.value = true;
  try {
    await Promise.all([
      fetchOnlineData(),
      fetchTagData(),
      fetchCategoryData(),
      fetchUpData(),
      fetchVideoTypeData()
    ]);
    dataLoaded.value = true;
    if (activeTab.value === 'overview') {
      await renderAllCharts();
    }
  } finally {
    isLoading.value = false;
  }
};

// 工具函数
//--------------------------
const visiblePages = computed(() => {
  const pages = [];
  const total = totalPages.value;
  const current = currentPage.value;
  let start = Math.max(1, current - 2);
  let end = Math.min(total, current + 2);
  // 保证显示5个页码（如果有足够页数）
  if (end - start < 4) {
    if (start === 1) {
      end = Math.min(total, start + 4);
    } else if (end === total) {
      start = Math.max(1, end - 4);
    }
  }
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

// 跳转到指定页
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    inputPage.value = '';
  }
};

// 输入跳转
const jumpToInputPage = () => {
  const page = Number(inputPage.value);
  if (!isNaN(page) && page >= 1 && page <= totalPages.value) {
    goToPage(page);
  } else {
    inputPage.value = '';
    alert('请输入有效的页码');
  }
};
//--------------------------

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

// 组件挂载时加载数据
onMounted(() => {
  refreshAllData();
});

// 组件卸载时清理图表实例
onUnmounted(() => {
  Object.values(chartInstances).forEach(instance => {
    if (instance) instance.dispose();
  });
  if (analysisChartInstance) {
    analysisChartInstance.dispose();
  }
});
</script>

<style scoped>
.page-input {
  width: 60px;
  padding: 0.3rem 0.5rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 1rem;
  margin: 0 0.5rem;
  text-align: center;
}

.page-jump-btn {
  background: var(--muted);
  color: var(--foreground);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}
.page-jump-btn:hover {
  background: var(--primary);
  color: #fff;
}
.current-page {
  font-weight: bold;
  color: var(--primary);
  margin: 0 0.2rem;
}




.hot-videos {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background-color: var(--background);
}

.tab-switcher {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
  background-color: var(--muted);
  border-radius: 12px;
  padding: 0.5rem;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
}

.tab-button {
  padding: 1rem 2rem;
  border: none;
  background: transparent;
  color: var(--muted-foreground);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
}

.tab-button.active {
  background-color: var(--card);
  color: var(--primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tab-button:hover:not(.active) {
  color: var(--foreground);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
}

.page-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--foreground);
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, var(--primary), #e91e63);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.refresh-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(251, 114, 153, 0.3);
}

.refresh-button:disabled {
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

.analysis-section {
  padding: 2.5rem;
  margin-bottom: 4rem;
  background-color: var(--card);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border);
}

.section-header {
  margin-bottom: 2rem;
  text-align: center;
}

.section-header h3 {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--foreground);
  margin-bottom: 0.5rem;
}

.section-desc {
  color: var(--muted-foreground);
  font-size: 1.1rem;
}

.chart-wrapper {
  padding: 2rem;
  margin-bottom: 3rem;
  background-color: var(--background);
  border-radius: 12px;
  border: 1px solid var(--border);
}

.chart-wrapper:last-child {
  margin-bottom: 0;
}

.chart-title {
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--foreground);
  text-align: center;
  border-bottom: 2px solid var(--primary);
}

.chart-container {
  position: relative;
  min-height: 400px;
}

.chart {
  width: 100%;
  height: 400px;
}

.large-chart {
  height: 500px;
}

.wordcloud-chart {
  height: 450px;
}

.upview-chart {
  height: 500px;
}

.loading-placeholder {
  display: flex;
  gap: 1rem;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: var(--muted-foreground);
}

.loading-placeholder span {
  font-size: 1.1rem;
}

.videos-content {
  padding: 2rem 0;
}

.video-gallery {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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
  height: 160px;
  object-fit: cover;
  display: block;
}

.video-info {
  padding: 1rem;
}

.video-title {
  font-size: 1.08rem;
  font-family: 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  font-weight: 500;
  margin-bottom: 0.5rem;
  line-height: 1.5;
  /* color: #222; */
  transition: color 0.2s;
}

.video-link {
  text-decoration: none;
  color: inherit;
  transition: color 0.2s;
  cursor: pointer;
}

.video-link:hover {
  text-decoration: none;
  color: var(--primary, #e91e63);
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
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.stat-icon {
  width: 1.1em;
  height: 1.1em;
  margin-right: 0.1em;
  color: var(--muted-foreground);
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

.analysis-card-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

.analysis-card {
  position: relative;
  width: 90%;
  max-width: 1200px;
  height: 90vh;
  background-color: var(--background);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  overflow-y: auto;
  padding: 2rem;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background-color: var(--muted);
  color: var(--foreground);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: var(--primary);
  color: white;
}

.analysis-card-content {
  width: 100%;
  height: 100%;
}

.video-analysis-header {
  margin-bottom: 2rem;
  text-align: center;
}

.video-analysis-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--foreground);
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.video-meta-info {
  color: var(--muted-foreground);
  font-size: 0.95rem;
}

.analysis-chart {
  width: 100%;
  height: 500px;
  margin-top: 1rem;
}

.no-data-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: var(--muted-foreground);
  font-size: 1.1rem;
}

.empty-state {
  padding: 6rem 2rem;
  text-align: center;
  color: var(--muted-foreground);
}

.empty-icon {
  display: flex;
  margin: 0 auto 2rem;
  width: 100px;
  height: 100px;
  font-size: 2.5rem;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  color: var(--muted-foreground);
  background-color: var(--muted);
}

.empty-state h3 {
  margin-bottom: 1rem;
  font-size: 2rem;
  color: var(--foreground);
}

.empty-state p {
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .hot-videos {
    padding: 1rem;
  }
  
  .page-header {
    gap: 1rem;
    flex-direction: column;
    text-align: center;
  }
  
  .analysis-section {
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .chart-wrapper {
    padding: 1.5rem;
  }
  
  .chart {
    height: 300px;
  }
  
  .large-chart {
    height: 400px;
  }
  
  .wordcloud-chart {
    height: 350px;
  }
  
  .tab-switcher {
    width: 100%;
  }
  
  .tab-button {
    flex: 1;
    padding: 0.75rem 1rem;
  }
  
  .video-gallery {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .analysis-card {
    width: 95%;
    height: 95vh;
    padding: 1rem;
  }
  
  .analysis-chart {
    height: 400px;
  }
}

/* 打开视频按钮样式 */
.open-video-btn {
  display: inline-block;
  padding: 0.75rem 2.2rem;
  background: linear-gradient(90deg, var(--primary), #fb7299);
  color: #fff;
  font-size: 1.15rem;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(251, 114, 153, 0.10);
  text-decoration: none;
  transition: background 0.2s, box-shadow 0.2s, transform 0.2s;
  margin-top: 1.5rem;
}
.open-video-btn:hover {
  background: linear-gradient(90deg, #fb7299, var(--primary));
  color: #fff;
  box-shadow: 0 6px 24px rgba(251, 114, 153, 0.18);
  transform: translateY(-2px) scale(1.04);
}
</style>
