<template>
  <div>
    <div class="page-header">
      <h2>数据分析</h2>
      <div class="page-actions">
        <button class="refresh-button" @click="refreshData">
          <RefreshCwIcon />
          刷新数据
        </button>
      </div>
    </div>

    <!-- 分析指标 -->
    <div class="analytics-metrics">
      <div class="metric-card">
        <div class="metric-header">
          <h3>实时用户</h3>
          <TrendingUpIcon class="metric-icon" />
        </div>
        <div class="metric-value">1,234</div>
        <div class="metric-change positive">+5.2% 较昨日</div>
      </div>
      <div class="metric-card">
        <div class="metric-header">
          <h3>会话时长</h3>
          <ClockIcon class="metric-icon" />
        </div>
        <div class="metric-value">4:32</div>
        <div class="metric-change positive">+12.3% 较昨日</div>
      </div>
      <div class="metric-card">
        <div class="metric-header">
          <h3>跳出率</h3>
          <MousePointerIcon class="metric-icon" />
        </div>
        <div class="metric-value">23.4%</div>
        <div class="metric-change negative">-2.1% 较昨日</div>
      </div>
    </div>

    <!-- 详细分析图表 -->
    <div class="analytics-charts">
      <ChartCard title="用户行为分析" :isLarge="true">
        <div class="chart-placeholder">
          <p>用户行为分析图表</p>
        </div>
      </ChartCard>
      <ChartCard title="转化漏斗">
        <div class="chart-placeholder">
          <p>转化漏斗图表</p>
        </div>
      </ChartCard>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ChartCard from '../components/ChartCard.vue';
import { 
  RefreshCw as RefreshCwIcon,
  TrendingUp as TrendingUpIcon,
  Clock as ClockIcon,
  MousePointer as MousePointerIcon
} from 'lucide-vue-next';

const refreshData = () => {
  console.log('刷新分析数据...');
};
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
}

.page-actions {
  display: flex;
  gap: 1rem;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background-color 0.2s;
}

.refresh-button:hover {
  background-color: #e91e63;
}

.analytics-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  background-color: var(--card);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.metric-header h3 {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  font-weight: 500;
}

.metric-icon {
  color: var(--primary);
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.metric-change {
  font-size: 0.875rem;
}

.metric-change.positive {
  color: #10B981;
}

.metric-change.negative {
  color: #EF4444;
}

.analytics-charts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.chart-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--muted-foreground);
  font-style: italic;
}

@media (max-width: 1024px) {
  .analytics-charts {
    grid-template-columns: 1fr;
  }
}
</style>
