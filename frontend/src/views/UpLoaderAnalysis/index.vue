<template>
    <div class="uploader-analysis-container">
      <!-- Search Section -->
      <a-card class="search-card">
        <template #title>
          <div class="card-title">
            <span>UP主搜索</span>
            <a-button type="primary" @click="handleSearch">
              搜索
            </a-button>
          </div>
        </template>

        <a-form :model="searchForm" layout="vertical">
          <a-row :gutter="16">
            <a-col :span="8">
              <a-form-item label="关键词">
                <a-input
                  v-model:value="searchForm.keyword"
                  placeholder="UP主昵称/UID"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="粉丝数范围">
                <a-range-picker
                  v-model:value="searchForm.followerRange"
                  :ranges="followerRanges"
                  :format="'YYYY-MM-DD'"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="等级">
                <a-select
                  v-model:value="searchForm.level"
                  placeholder="选择等级"
                  allow-clear
                >
                  <a-select-option v-for="level in levels" :key="level" :value="level">
                    {{ level }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
      </a-card>
  
      <a-row :gutter="[16, 16]" class="content-row">
        <!-- UP主详情卡片 -->
        <a-col :span="8">
          <a-card class="detail-card" :loading="loading">
            <template #title>
              <div class="card-title">
                <user-outlined />
                <span>UP主详情</span>
              </div>
            </template>
            <div v-if="selectedUploader" class="uploader-info">
              <div class="avatar-section">
                <a-avatar :size="64" :src="selectedUploader.avatar" />
                <div class="basic-info">
                  <h3>{{ selectedUploader.nickname }}</h3>
                  <p>UID: {{ selectedUploader.uid }}</p>
                  <p>等级: Lv.{{ selectedUploader.level }}</p>
                </div>
              </div>
              <a-divider />
              <div class="metrics-grid">
                <div class="metric-item">
                  <span class="label">粉丝数</span>
                  <span class="value">{{ formatNumber(selectedUploader.followers) }}</span>
                </div>
                <div class="metric-item">
                  <span class="label">播放/粉丝比</span>
                  <span class="value">{{ selectedUploader.playFollowerRatio }}%</span>
                </div>
                <div class="metric-item">
                  <span class="label">互动率</span>
                  <span class="value">{{ selectedUploader.interactionRate }}%</span>
                </div>
                <div class="metric-item">
                  <span class="label">投稿频率</span>
                  <span class="value">{{ selectedUploader.postFrequency }}/周</span>
                </div>
              </div>
            </div>
            <a-empty v-else description="请选择UP主查看详情" />
          </a-card>
        </a-col>
  
        <!-- 粘性UP主分析 -->
        <a-col :span="16">
          <a-card class="sticky-card" title="粘性UP主分析">
            <a-tabs v-model:activeKey="activeTab">
              <a-tab-pane key="table" tab="数据表格">
                <a-table
                  :columns="stickyColumns"
                  :data-source="stickyUploaders"
                  :loading="loading"
                  :pagination="{ pageSize: 5 }"
                >
                  <template #bodyCell="{ column, record }">
                    <template v-if="column.key === 'interactionRate'">
                      <a-progress
                        :percent="record.interactionRate"
                        :stroke-color="getProgressColor(record.interactionRate)"
                      />
                    </template>
                  </template>
                </a-table>
              </a-tab-pane>
              <a-tab-pane key="scatter" tab="散点图">
                <div ref="scatterChartRef" class="chart-container"></div>
              </a-tab-pane>
            </a-tabs>
          </a-card>
        </a-col>
  
        <!-- 社交网络图 -->
        <a-col :span="24">
          <a-card class="network-card" title="UP主社交网络">
            <div ref="networkChartRef" class="network-container"></div>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, reactive } from 'vue'
  import { use } from 'echarts/core'
  import { CanvasRenderer } from 'echarts/renderers'
  import { ScatterChart } from 'echarts/charts'
  import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent
  } from 'echarts/components'
  import * as echarts from 'echarts'
  import G6, { Graph } from '@antv/g6'
  import { useUploaderStore } from '../../stores/uploader.js'
  import {
    SearchOutlined,
    UserOutlined
  } from '@ant-design/icons-vue'
  
  // Register ECharts components
  use([
    CanvasRenderer,
    ScatterChart,
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent
  ])
  
  const uploaderStore = useUploaderStore()
  const loading = ref(false)
  const activeTab = ref('table')
  const scatterChartRef = ref()
  const networkChartRef = ref()
  const detailVisible = ref(false)
  const networkVisible = ref(false)
  let scatterChart = null
  let networkGraph = null
  
  const searchForm = reactive({
    keyword: '',
    followerRange: [null, null],
    level: undefined
  })
  
  const selectedUploader = ref(null)
  
  const pagination = reactive({
    current: 1,
    pageSize: 10,
    total: 0
  })
  
  const followerRanges = {
    '最近一周': [new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), new Date()],
    '最近一月': [new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), new Date()],
    '最近三月': [new Date(Date.now() - 90 * 24 * 60 * 60 * 1000), new Date()]
  }
  
  const levels = ['1', '2', '3', '4', '5', '6']
  
  const stickyColumns = [
    {
      title: 'UP主',
      dataIndex: 'nickname',
      key: 'nickname'
    },
    {
      title: '粉丝数',
      dataIndex: 'followers',
      key: 'followers',
      sorter: (a, b) => a.followers - b.followers
    },
    {
      title: '互动率',
      dataIndex: 'interactionRate',
      key: 'interactionRate',
      sorter: (a, b) => a.interactionRate - b.interactionRate
    },
    {
      title: '播放/粉丝比',
      dataIndex: 'playFollowerRatio',
      key: 'playFollowerRatio',
      sorter: (a, b) => a.playFollowerRatio - b.playFollowerRatio
    }
  ]
  
  const stickyUploaders = ref([
    {
      key: '1',
      nickname: 'UP主1',
      followers: 50000,
      interactionRate: 12.5,
      playFollowerRatio: 18.2
    },
    {
      key: '2',
      nickname: 'UP主2',
      followers: 30000,
      interactionRate: 15.8,
      playFollowerRatio: 22.5
    },
    {
      key: '3',
      nickname: 'UP主3',
      followers: 80000,
      interactionRate: 9.2,
      playFollowerRatio: 15.8
    }
  ])
  
  const formatNumber = (num) => {
    return num >= 10000
      ? (num / 10000).toFixed(1) + '万'
      : num.toString()
  }
  
  const getProgressColor = (value) => {
    if (value >= 15) return '#52c41a'
    if (value >= 10) return '#1890ff'
    if (value >= 5) return '#faad14'
    return '#ff4d4f'
  }
  
  const handleSearch = async () => {
    loading.value = true
    try {
      await uploaderStore.search({
        keyword: searchForm.keyword,
        startDate: searchForm.followerRange[0] ? new Date(searchForm.followerRange[0]).toISOString() : undefined,
        endDate: searchForm.followerRange[1] ? new Date(searchForm.followerRange[1]).toISOString() : undefined,
        level: searchForm.level
      })
      pagination.total = uploaderStore.searchResults.length
    } finally {
      loading.value = false
    }
  }
  
  const handleRefresh = () => {
    handleSearch()
  }
  
  const handleTableChange = (pag) => {
    pagination.current = pag.current
    pagination.pageSize = pag.pageSize
  }
  
  const handleViewDetail = async (record) => {
    selectedUploader.value = record
    detailVisible.value = true
    try {
      await uploaderStore.fetchUploaderInfo(record.uid)
      selectedUploader.value = uploaderStore.selectedUploader
    } catch (error) {
      console.error('Failed to fetch uploader info:', error)
    }
  }
  
  const handleViewNetwork = async (record) => {
    networkVisible.value = true
    try {
      await uploaderStore.fetchNetworkData(record.uid)
      initNetworkGraph()
    } catch (error) {
      console.error('Failed to fetch network data:', error)
    }
  }
  
  const initNetworkGraph = () => {
    if (!networkChartRef.value || !uploaderStore.networkData?.nodes || !uploaderStore.networkData?.edges) return

    if (networkGraph) {
      networkGraph.destroy()
    }

    const data = {
      nodes: uploaderStore.networkData.nodes.map(node => ({
        id: node.id,
        label: node.nickname || node.id,
        size: node.weight || 30
      })),
      edges: uploaderStore.networkData.edges.map(edge => ({
        source: edge.source,
        target: edge.target,
        weight: edge.weight || 1
      }))
    }

    networkGraph = new G6.Graph({
      container: networkChartRef.value,
      width: networkChartRef.value.clientWidth,
      height: 600,
      layout: {
        type: 'force',
        preventOverlap: true
      },
      modes: {
        default: ['drag-node', 'zoom-canvas', 'drag-canvas']
      },
      defaultNode: {
        type: 'circle',
        size: 30,
        style: {
          fill: '#91d5ff',
          stroke: '#40a9ff'
        },
        labelCfg: {
          style: {
            fill: '#000',
            fontSize: 12
          }
        }
      },
      defaultEdge: {
        type: 'line',
        style: {
          stroke: '#91d5ff'
        }
      }
    })

    networkGraph.data(data)
    networkGraph.render()
  }
  
  const handleResize = () => {
    if (scatterChart) {
      scatterChart.resize()
    }
    if (networkGraph && networkChartRef.value) {
      networkGraph.changeSize(
        networkChartRef.value.clientWidth,
        600
      )
    }
  }
  
  onMounted(() => {
    handleSearch()
    window.addEventListener('resize', handleResize)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    if (scatterChart) {
      scatterChart.dispose()
    }
    if (networkGraph) {
      networkGraph.destroy()
    }
  })
  </script>
  
  <style lang="scss" scoped>
  .uploader-analysis-container {
    .search-card {
      margin-bottom: 16px;
    }
  
    .content-row {
      .detail-card {
        .uploader-info {
          .avatar-section {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 16px;
  
            .basic-info {
              h3 {
                margin: 0 0 8px;
              }
  
              p {
                margin: 0;
                color: #8c8c8c;
              }
            }
          }
  
          .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
  
            .metric-item {
              display: flex;
              flex-direction: column;
              align-items: center;
              padding: 8px;
              background: #f5f5f5;
              border-radius: 4px;
  
              .label {
                font-size: 12px;
                color: #8c8c8c;
              }
  
              .value {
                font-size: 18px;
                font-weight: bold;
                color: #1890ff;
              }
            }
          }
        }
      }
  
      .sticky-card {
        .chart-container {
          height: 400px;
        }
      }
  
      .network-card {
        .network-container {
          height: 600px;
        }
      }
    }
  }
  </style>