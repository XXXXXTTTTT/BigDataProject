<template>
  <div class="video-analysis-container">
    <a-row :gutter="[16, 16]">
      <!-- 实时视频监控 -->
      <a-col :span="24">
        <a-card class="monitor-card" title="实时视频监控">
          <a-row :gutter="[16, 16]">
            <a-col :span="6" v-for="video in hotVideos" :key="video.id">
              <a-card hoverable class="video-card">
                <template #cover>
                  <img :src="video.cover" :alt="video.title" />
                </template>
                <a-card-meta :title="video.title">
                  <template #description>
                    <div class="video-info">
                      <p class="uploader">
                        <user-outlined />
                        {{ video.uploader }}
                      </p>
                      <div class="metrics">
                        <span>
                          <eye-outlined />
                          {{ formatNumber(video.views) }}
                        </span>
                        <span>
                          <message-outlined />
                          {{ formatNumber(video.comments) }}
                        </span>
                      </div>
                    </div>
                  </template>
                </a-card-meta>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </a-col>

      <!-- 视频热度分析 -->
      <a-col :span="16">
        <a-card class="heat-card" title="视频热度分析">
          <a-tabs v-model:activeKey="activeTab">
            <a-tab-pane key="heatmap" tab="热度热力图">
              <div ref="heatmapChartRef" class="chart-container"></div>
            </a-tab-pane>
            <a-tab-pane key="wordcloud" tab="关键词词云">
              <div ref="wordcloudChartRef" class="chart-container"></div>
            </a-tab-pane>
          </a-tabs>
        </a-card>
      </a-col>

      <!-- 分区热度排行 -->
      <a-col :span="8">
        <a-card class="category-card" title="分区热度排行">
          <div ref="categoryChartRef" class="chart-container"></div>
        </a-card>
      </a-col>

      <!-- 模型性能分析 -->
      <a-col :span="24">
        <a-card class="model-card" title="模型性能分析">
          <a-row :gutter="[16, 16]">
            <a-col :span="8" v-for="metric in modelMetrics" :key="metric.title">
              <a-card class="metric-card">
                <template #title>
                  <div class="card-title">
                    <component :is="metric.icon" />
                    <span>{{ metric.title }}</span>
                  </div>
                </template>
                <div class="metric-value">
                  <span class="number">{{ metric.value }}</span>
                  <span class="unit">{{ metric.unit }}</span>
                </div>
                <div class="metric-trend" :class="metric.trend">
                  <component :is="metric.trendIcon" />
                  <span>{{ metric.trendValue }}</span>
                </div>
              </a-card>
            </a-col>
          </a-row>
          <div class="model-comparison">
            <div ref="modelComparisonChartRef" class="chart-container"></div>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import {
  HeatmapChart,
  BarChart,
  LineChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CalendarComponent
} from 'echarts/components'
import * as echarts from 'echarts'
import 'echarts-wordcloud/dist/echarts-wordcloud.min.js'
import {
  UserOutlined,
  EyeOutlined,
  MessageOutlined,
  RocketOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined
} from '@ant-design/icons-vue'

// Register ECharts components
use([
  CanvasRenderer,
  HeatmapChart,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CalendarComponent
])

const activeTab = ref('heatmap')
const heatmapChartRef = ref()
const wordcloudChartRef = ref()
const categoryChartRef = ref()
const modelComparisonChartRef = ref()
let heatmapChart = null
let wordcloudChart = null
let categoryChart = null
let modelComparisonChart = null

const hotVideos = ref([
  {
    id: '1',
    title: '【游戏实况】最新游戏实况视频',
    cover: 'https://picsum.photos/300/200?random=1',
    uploader: '游戏UP主',
    views: 123456,
    comments: 1234
  },
  {
    id: '2',
    title: '【动画】新番动画解说',
    cover: 'https://picsum.photos/300/200?random=2',
    uploader: '动画UP主',
    views: 98765,
    comments: 987
  },
  {
    id: '3',
    title: '【音乐】原创音乐作品',
    cover: 'https://picsum.photos/300/200?random=3',
    uploader: '音乐UP主',
    views: 56789,
    comments: 567
  },
  {
    id: '4',
    title: '【舞蹈】舞蹈教学视频',
    cover: 'https://picsum.photos/300/200?random=4',
    uploader: '舞蹈UP主',
    views: 34567,
    comments: 345
  }
])

const modelMetrics = ref([
  {
    title: '准确率',
    value: '85.6',
    unit: '%',
    icon: RocketOutlined,
    trend: 'up',
    trendIcon: ArrowUpOutlined,
    trendValue: '2.3%'
  },
  {
    title: '召回率',
    value: '82.1',
    unit: '%',
    icon: RocketOutlined,
    trend: 'up',
    trendIcon: ArrowUpOutlined,
    trendValue: '1.8%'
  },
  {
    title: 'F1分数',
    value: '83.8',
    unit: '%',
    icon: RocketOutlined,
    trend: 'up',
    trendIcon: ArrowUpOutlined,
    trendValue: '2.1%'
  }
])

const formatNumber = (num) => {
  return num >= 10000
    ? (num / 10000).toFixed(1) + '万'
    : num.toString()
}

const initCharts = () => {
  if (heatmapChartRef.value) {
    heatmapChart = echarts.init(heatmapChartRef.value)
    heatmapChart.setOption({
      tooltip: {
        position: 'top'
      },
      grid: {
        top: '60',
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        splitArea: {
          show: true
        }
      },
      yAxis: {
        type: 'category',
        data: ['0-6时', '6-12时', '12-18时', '18-24时'],
        splitArea: {
          show: true
        }
      },
      visualMap: {
        min: 0,
        max: 100,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '0%'
      },
      series: [
        {
          name: '热度',
          type: 'heatmap',
          data: [
            [0, 0, 10], [1, 0, 20], [2, 0, 30], [3, 0, 40], [4, 0, 50], [5, 0, 60], [6, 0, 70],
            [0, 1, 20], [1, 1, 30], [2, 1, 40], [3, 1, 50], [4, 1, 60], [5, 1, 70], [6, 1, 80],
            [0, 2, 30], [1, 2, 40], [2, 2, 50], [3, 2, 60], [4, 2, 70], [5, 2, 80], [6, 2, 90],
            [0, 3, 40], [1, 3, 50], [2, 3, 60], [3, 3, 70], [4, 3, 80], [5, 3, 90], [6, 3, 100]
          ],
          label: {
            show: true
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    })
  }

  if (wordcloudChartRef.value) {
    wordcloudChart = echarts.init(wordcloudChartRef.value)
    wordcloudChart.setOption({
      tooltip: {
        show: true
      },
      series: [
        {
          type: 'wordCloud',
          shape: 'circle',
          left: 'center',
          top: 'center',
          width: '70%',
          height: '80%',
          right: null,
          bottom: null,
          sizeRange: [12, 60],
          rotationRange: [-90, 90],
          rotationStep: 45,
          gridSize: 8,
          drawOutOfBound: false,
          textStyle: {
            fontFamily: 'sans-serif',
            fontWeight: 'bold',
            color: function () {
              return 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
              ].join(',') + ')'
            }
          },
          emphasis: {
            focus: 'self',
            textStyle: {
              shadowBlur: 10,
              shadowColor: '#333'
            }
          },
          data: [
            { name: '游戏', value: 100 },
            { name: '动画', value: 80 },
            { name: '音乐', value: 60 },
            { name: '舞蹈', value: 40 },
            { name: '知识', value: 30 }
          ]
        }
      ]
    })
  }

  if (categoryChartRef.value) {
    categoryChart = echarts.init(categoryChartRef.value)
    categoryChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value'
      },
      yAxis: {
        type: 'category',
        data: ['游戏', '动画', '音乐', '舞蹈', '知识']
      },
      series: [
        {
          name: '热度',
          type: 'bar',
          data: [100, 80, 60, 40, 30],
          itemStyle: {
            color: '#1890ff'
          }
        }
      ]
    })
  }

  if (modelComparisonChartRef.value) {
    modelComparisonChart = echarts.init(modelComparisonChartRef.value)
    modelComparisonChart.setOption({
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['XGBoost', 'Random Forest', 'LSTM']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['1月', '2月', '3月', '4月', '5月', '6月']
      },
      yAxis: {
        type: 'value',
        name: '准确率(%)'
      },
      series: [
        {
          name: 'XGBoost',
          type: 'line',
          data: [80, 82, 84, 85, 86, 87]
        },
        {
          name: 'Random Forest',
          type: 'line',
          data: [78, 79, 81, 82, 83, 84]
        },
        {
          name: 'LSTM',
          type: 'line',
          data: [75, 77, 79, 80, 81, 82]
        }
      ]
    })
  }
}

const handleResize = () => {
  heatmapChart?.resize()
  wordcloudChart?.resize()
  categoryChart?.resize()
  modelComparisonChart?.resize()
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  heatmapChart?.dispose()
  wordcloudChart?.dispose()
  categoryChart?.dispose()
  modelComparisonChart?.dispose()
})
</script>

<style lang="scss" scoped>

.video-analysis-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 24px;
  color: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  
  
  .monitor-card {
    background: rgba(255, 255, 255, 0.05);;


    .video-card {
      .ant-card-cover {
        img {
          height: 200px;
          object-fit: cover;
        }
      }

      .video-info {
        .uploader {
          margin: 8px 0;
          color: #8c8c8c;
        }

        .metrics {
          display: flex;
          gap: 16px;
          color: #8c8c8c;

          span {
            display: flex;
            align-items: center;
            gap: 4px;
          }
        }
      }
    }
  }

  .heat-card,
  .category-card {
    .chart-container {
      height: 400px;
    }
  }

  .model-card {
    .metric-card {
      .card-title {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .metric-value {
        margin: 16px 0;
        
        .number {
          font-size: 24px;
          font-weight: bold;
          color: #1890ff;
        }

        .unit {
          margin-left: 4px;
          color: #8c8c8c;
        }
      }

      .metric-trend {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 12px;

        &.up {
          color: #52c41a;
        }

        &.down {
          color: #ff4d4f;
        }
      }
    }

    .model-comparison {
      margin-top: 24px;
      
      .chart-container {
        height: 300px;
      }
    }
  }
}
</style> 