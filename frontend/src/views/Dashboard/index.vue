<template>
  <div class="dashboard-container">
    <a-row :gutter="[16, 16]">
      <!-- 项目介绍卡片 -->
      <a-col :span="24">
        <a-card class="intro-card">
          <template #title>
            <div class="card-title">
              <rocket-outlined />
              <span>项目介绍</span>
            </div>
          </template>
          <p class="intro-text">
            基于大数据分析的B站UP主成长规律与视频热度预测系统，帮助内容创作者和运营人员洞察平台趋势，优化内容策略。
          </p>
        </a-card>
      </a-col>

      <!-- Core Metrics Cards -->
      <a-col :span="6" v-for="metric in coreMetrics" :key="metric.title">
        <a-card class="metric-card" :loading="loading">
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

      <!-- Charts Row -->
      <a-col :span="16">
        <a-card class="chart-card" title="平台活跃度趋势">
          <div ref="activityChartRef" class="chart-container"></div>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card class="chart-card" title="内容分区分布">
          <div ref="categoryChartRef" class="chart-container"></div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import * as echarts from 'echarts'
import {
  RocketOutlined,
  UserOutlined,
  VideoCameraOutlined,
  FireOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined
} from '@ant-design/icons-vue'

// Register ECharts components
use([
  CanvasRenderer,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const loading = ref(true)
const activityChartRef = ref()
const categoryChartRef = ref()
let activityChart = null
let categoryChart = null

const coreMetrics = ref([
  {
    title: '总UP主数',
    value: '1,234,567',
    unit: '位',
    icon: UserOutlined,
    trend: 'up',
    trendIcon: ArrowUpOutlined,
    trendValue: '12.5%'
  },
  {
    title: '平均互动率',
    value: '8.76',
    unit: '%',
    icon: FireOutlined,
    trend: 'up',
    trendIcon: ArrowUpOutlined,
    trendValue: '3.2%'
  },
  {
    title: '活跃用户数',
    value: '89.5',
    unit: '万',
    icon: UserOutlined,
    trend: 'down',
    trendIcon: ArrowDownOutlined,
    trendValue: '1.8%'
  },
  {
    title: '视频总数',
    value: '5,678',
    unit: '个',
    icon: VideoCameraOutlined,
    trend: 'up',
    trendIcon: ArrowUpOutlined,
    trendValue: '5.6%'
  }
])

const initCharts = () => {
  if (activityChartRef.value) {
    activityChart = echarts.init(activityChartRef.value)
    activityChart.setOption({
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['活跃UP主', '视频发布量', '互动量']
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
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '活跃UP主',
          type: 'line',
          data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
          name: '视频发布量',
          type: 'line',
          data: [220, 182, 191, 234, 290, 330, 310]
        },
        {
          name: '互动量',
          type: 'line',
          data: [150, 232, 201, 154, 190, 330, 410]
        }
      ]
    })
  }

  if (categoryChartRef.value) {
    categoryChart = echarts.init(categoryChartRef.value)
    categoryChart.setOption({
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '内容分区',
          type: 'pie',
          radius: '50%',
          data: [
            { value: 1048, name: '游戏' },
            { value: 735, name: '动画' },
            { value: 580, name: '音乐' },
            { value: 484, name: '舞蹈' },
            { value: 300, name: '知识' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    })
  }
}

const handleResize = () => {
  activityChart?.resize()
  categoryChart?.resize()
}

onMounted(() => {
  setTimeout(() => {
    loading.value = false
    initCharts()
  }, 1000)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  activityChart?.dispose()
  categoryChart?.dispose()
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  .intro-card {
    background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
    color: white;

    .card-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 16px;
    }

    .intro-text {
      margin: 0;
      font-size: 14px;
      line-height: 1.6;
    }
  }

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

  .chart-card {
    .chart-container {
      height: 300px;
    }
  }
}
</style>
