<template>
    <div class="dashboard-container">
      <!-- 项目介绍卡片 -->
      <div class="project-intro-card">
        <div class="intro-content">
          <h1 class="project-title">B站UP主与热门视频数据可视化平台</h1>
          <p class="project-desc">
            基于B站数据爬取，分析UP主性质， 预测视频热度趋势
          </p>
          <div class="project-tags">
            <span class="tag">UP主展示</span>
            <span class="tag">B站热门展示</span>
            <span class="tag">B站热门标签</span>
            <span class="tag">热门视频热度预测</span>
          </div>
        </div>
        <div class="intro-visual">
          <div class="pulse-circle"></div>
        </div>
      </div>
  
      <!-- 核心指标卡片 -->
      <div class="metrics-grid">
        <div class="metric-card" v-for="metric in coreMetrics" :key="metric.key">
          <div class="metric-icon">
            <component :is="metric.icon" />
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ formatNumber(metric.value) }}</div>
            <div class="metric-label">{{ metric.label }}</div>
            <div class="metric-trend" :class="metric.trend > 0 ? 'positive' : 'negative'">
              <TrendingUp v-if="metric.trend > 0" class="trend-icon" />
              <TrendingDown v-else class="trend-icon" />
              {{ Math.abs(metric.trend) }}%
            </div>
          </div>
        </div>
      </div>
  
      <!-- 实时数据概览 -->
      <div class="overview-charts">
        <div class="chart-container">
          <h3 class="chart-title">UP主活跃度分布</h3>
          <div ref="uploaderActivityChart" class="chart-content"></div>
        </div>
        <div class="chart-container">
          <h3 class="chart-title">视频热度趋势</h3>
          <div ref="videoTrendChart" class="chart-content"></div>
        </div>
      </div>
  
      <!-- 快速导航 -->
      <div class="quick-nav">
        <div class="nav-card" @click="navigateTo('/uploader-analysis')">
          <Users class="nav-icon" />
          <h4>UP主分析</h4>
          <p>深度分析UP主成长轨迹</p>
        </div>
        <div class="nav-card" @click="navigateTo('/video-analysis')">
          <Video class="nav-icon" />
          <h4>视频分析</h4>
          <p>热门视频趋势预测</p>
        </div>
        <div class="nav-card" @click="navigateTo('/social-network')">
          <Network class="nav-icon" />
          <h4>社交图谱</h4>
          <p>UP主关系网络分析</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, nextTick } from 'vue'
  import { useRouter } from 'vue-router'
  import { Users, Video, Network, TrendingUp, TrendingDown, Activity, Eye, Heart, MessageCircle } from 'lucide-vue-next'
  import * as echarts from 'echarts'
  
  const router = useRouter()
  
  // 响应式数据
  const uploaderActivityChart = ref<HTMLElement>()
  const videoTrendChart = ref<HTMLElement>()
  
  // 核心指标数据
  const coreMetrics = ref([
    {
      key: 'totalUploaders',
      label: '总UP主数',
      value: 125680,
      trend: 12.5,
      icon: Users
    },
    {
      key: 'avgInteractionRate',
      label: '平均互动率',
      value: 8.7,
      trend: 5.2,
      icon: Heart
    },
    {
      key: 'activeUsers',
      label: '活跃用户数',
      value: 2456789,
      trend: -2.1,
      icon: Activity
    },
    {
      key: 'totalViews',
      label: '总播放量',
      value: 98765432,
      trend: 18.9,
      icon: Eye
    }
  ])
  
  // 格式化数字
  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M'
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K'
    }
    return num.toString()
  }
  
  // 导航函数
  const navigateTo = (path: string) => {
    router.push(path)
  }
  
  // 初始化图表
  const initCharts = () => {
    // UP主活跃度分布图
    if (uploaderActivityChart.value) {
      const chart1 = echarts.init(uploaderActivityChart.value)
      const option1 = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          borderColor: '#00d4ff',
          textStyle: { color: '#fff' }
        },
        series: [{
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['50%', '50%'],
          data: [
            { value: 35, name: '高活跃', itemStyle: { color: '#00d4ff' } },
            { value: 45, name: '中活跃', itemStyle: { color: '#0099cc' } },
            { value: 20, name: '低活跃', itemStyle: { color: '#006699' } }
          ],
          label: {
            color: '#fff',
            fontSize: 12
          },
          labelLine: {
            lineStyle: { color: '#fff' }
          }
        }]
      }
      chart1.setOption(option1)
    }
  
    // 视频热度趋势图
    if (videoTrendChart.value) {
      const chart2 = echarts.init(videoTrendChart.value)
      const option2 = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          borderColor: '#00d4ff',
          textStyle: { color: '#fff' }
        },
        xAxis: {
          type: 'category',
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
          axisLine: { lineStyle: { color: '#333' } },
          axisLabel: { color: '#999' }
        },
        yAxis: {
          type: 'value',
          axisLine: { lineStyle: { color: '#333' } },
          axisLabel: { color: '#999' },
          splitLine: { lineStyle: { color: '#333' } }
        },
        series: [{
          data: [820, 932, 901, 934, 1290, 1330, 1320],
          type: 'line',
          smooth: true,
          lineStyle: { color: '#00d4ff', width: 3 },
          itemStyle: { color: '#00d4ff' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(0, 212, 255, 0.3)' },
                { offset: 1, color: 'rgba(0, 212, 255, 0)' }
              ]
            }
          }
        }]
      }
      chart2.setOption(option2)
    }
  }
  
  onMounted(async () => {
    await nextTick()
    initCharts()
  })
  </script>
  
  <style scoped>
  .dashboard-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    padding: 24px;
    color: #fff;
  }
  
  .project-intro-card {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 204, 0.1) 100%);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(10px);
  }
  
  .intro-content {
    flex: 1;
  }
  
  .project-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #00d4ff, #0099cc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .project-desc {
    font-size: 16px;
    color: #ccc;
    margin-bottom: 16px;
    line-height: 1.6;
  }
  
  .project-tags {
    display: flex;
    gap: 12px;
  }
  
  .tag {
    background: rgba(0, 212, 255, 0.2);
    border: 1px solid rgba(0, 212, 255, 0.5);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    color: #00d4ff;
  }
  
  .intro-visual {
    width: 120px;
    height: 120px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .pulse-circle {
    width: 80px;
    height: 80px;
    border: 2px solid #00d4ff;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }
  
  @keyframes pulse {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.1);
      opacity: 0.7;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }
  
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    margin-bottom: 32px;
  }
  
  .metric-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
  }
  
  .metric-card:hover {
    border-color: rgba(0, 212, 255, 0.5);
    transform: translateY(-2px);
  }
  
  .metric-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #00d4ff, #0099cc);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
  }
  
  .metric-content {
    flex: 1;
  }
  
  .metric-value {
    font-size: 24px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 4px;
  }
  
  .metric-label {
    font-size: 14px;
    color: #999;
    margin-bottom: 8px;
  }
  
  .metric-trend {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 600;
  }
  
  .metric-trend.positive {
    color: #00ff88;
  }
  
  .metric-trend.negative {
    color: #ff4757;
  }
  
  .trend-icon {
    width: 14px;
    height: 14px;
  }
  
  .overview-charts {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 32px;
  }
  
  .chart-container {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 24px;
    backdrop-filter: blur(10px);
  }
  
  .chart-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 16px;
    color: #fff;
  }
  
  .chart-content {
    height: 300px;
  }
  
  .quick-nav {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
  }
  
  .nav-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 32px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
  }
  
  .nav-card:hover {
    border-color: rgba(0, 212, 255, 0.5);
    transform: translateY(-4px);
    background: rgba(0, 212, 255, 0.1);
  }
  
  .nav-icon {
    width: 48px;
    height: 48px;
    color: #00d4ff;
    margin: 0 auto 16px;
  }
  
  .nav-card h4 {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
    color: #fff;
  }
  
  .nav-card p {
    font-size: 14px;
    color: #999;
  }
  
  @media (max-width: 768px) {
    .project-intro-card {
      flex-direction: column;
      text-align: center;
      gap: 24px;
    }
    
    .overview-charts {
      grid-template-columns: 1fr;
    }
    
    .metrics-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>