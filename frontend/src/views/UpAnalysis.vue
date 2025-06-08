<template>
  <div>
    <div class="page-header">
      <h2>UP主聚类分析</h2>
    </div>
    <div class="scatter-charts">
      <div v-for="(cluster, idx) in clusters" :key="idx" class="scatter-chart" style="position:relative;">
        <div v-if="activeIdx === idx && tooltipData" class="up-tooltip up-tooltip-float">
          <img :src="proxyImg(tooltipData.avatar_url)" :alt="tooltipData.name" />
          <div>{{ tooltipData.name }}</div>
          <div>UID: {{ tooltipData.uid }}</div>
          <div>标签: {{ clusterMap[tooltipData.cluster_label] }}</div>
        </div>
        <div :ref="el => scatterRefs[idx] = el" class="up-scatter-chart"></div>
        <div style="text-align:center;font-weight:bold;margin-top:8px;">{{ clusterMap[idx] }}</div>
      </div>
    </div>
    <div ref="barChartRef" class="bar-chart"></div>
    <div ref="pieChartRef" class="pie-chart"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';

const upList = ref([]);
const clusters = ref([[], [], []]);
const clusterMap = { 0: '大V', 1: '普通UP', 2: '潜力UP' };
const scatterRefs = ref([null, null, null]);
const scatterCharts = ref([null, null, null]);
const barChartRef = ref(null);
const barChartInstance = ref(null);
const pieChartRef = ref(null);
const pieChartInstance = ref(null);
const tooltipData = ref(null);
const tooltipStyle = ref({});
const activeIdx = ref(null);

const proxyImg = url => `http://127.0.0.1:3000/proxy?url=${encodeURIComponent(url)}`;

const fetchUps = async () => {
  const res = await axios.get('http://127.0.0.1:3000/api/up-profile/analysis');
  if (res.data && res.data.data) {
    upList.value = res.data.data;
    // 分组
    const arr = [[], [], []];
    upList.value.forEach(up => {
      arr[up.cluster_label]?.push(up);
    });
    clusters.value = arr;
  }
};

const renderScatterCharts = () => {
  const colorMap = ['#e74c3c', '#27ae60', '#2980b9'];
  clusters.value.forEach((cluster, idx) => {
    if (!scatterRefs.value[idx]) return;
    if (!scatterCharts.value[idx]) {
      scatterCharts.value[idx] = echarts.init(scatterRefs.value[idx]);
    }
    const data = cluster.map(up => [
      Math.random(),
      Math.random(),
      up.avatar_url,
      up.name,
      up.uid,
      up.cluster_label
    ]);
    scatterCharts.value[idx].setOption({
      tooltip: { show: false },
      xAxis: {
        show: false,
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false }
      },
      yAxis: {
        show: false,
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false }
      },
      series: [{
        symbolSize: 24,
        type: 'scatter',
        data,
        itemStyle: {
          color: colorMap[idx]
        }
      }]
    });
    scatterCharts.value[idx].off('click');
    scatterCharts.value[idx].on('click', params => {
      const [x, y, avatar_url, name, uid, cluster_label] = params.data;
      tooltipData.value = { avatar_url, name, uid, cluster_label };
      activeIdx.value = idx;
    });
    scatterCharts.value[idx].off('globalout');
    scatterCharts.value[idx].on('globalout', () => {
      tooltipData.value = null;
      activeIdx.value = null;
    });
  });
};

const renderBarChart = () => {
  if (!barChartRef.value) return;
  if (!barChartInstance.value) {
    barChartInstance.value = echarts.init(barChartRef.value);
  }
  // 计算每组的平均特征值（显示特征数值，带单位，保留合适小数）
  const features = [
    { key: 'log_followers', name: '对数粉丝数'},
    { key: 'log_view', name: '对数播放量'},
    { key: 'like_rate', name: '点赞率', unit: '%' },
    { key: 'engagement_rate', name: '互动率', unit: '%' },
  ];
  // 需要up_profile表的原始数据，假设后端已返回
  const avgData = features.map(f => ({
    name: f.name,
    大V: getAvg(clusters.value[0], f.key, f.unit),
    普通UP: getAvg(clusters.value[1], f.key, f.unit),
    潜力UP: getAvg(clusters.value[2], f.key, f.unit)
  }));
  barChartInstance.value.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: Object.values(clusterMap) },
    xAxis: { type: 'category', data: features.map(f => f.name) },
    yAxis: { type: 'value' },
    series: [
      {
        name: '大V',
        type: 'bar',
        data: avgData.map(d => d.大V.value),
        itemStyle: { color: '#e74c3c' },
        label: { show: true, position: 'top', formatter: p => dUnit(p.value, avgData[p.dataIndex].大V.unit) }
      },
      {
        name: '普通UP',
        type: 'bar',
        data: avgData.map(d => d.普通UP.value),
        itemStyle: { color: '#27ae60' },
        label: { show: true, position: 'top', formatter: p => dUnit(p.value, avgData[p.dataIndex].普通UP.unit) }
      },
      {
        name: '潜力UP',
        type: 'bar',
        data: avgData.map(d => d.潜力UP.value),
        itemStyle: { color: '#2980b9' },
        label: { show: true, position: 'top', formatter: p => dUnit(p.value, avgData[p.dataIndex].潜力UP.unit) }
      }
    ]
  });
};

const renderPieChart = () => {
  if (!pieChartRef.value) return;
  if (!pieChartInstance.value) {
    pieChartInstance.value = echarts.init(pieChartRef.value);
  }

  
  const pieData = [
    { value: clusters.value[0].length, name: '大V' },
    { value: clusters.value[1].length, name: '普通UP' },
    { value: clusters.value[2].length, name: '潜力UP' }
  ];
  pieChartInstance.value.setOption({
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [
      {
        name: 'UP主分布',
        type: 'pie',
        radius: '60%',
        data: pieData,
        emphasis: {
          itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
        },
        color: ['#e74c3c', '#27ae60', '#2980b9']
      }
    ]
  });
};

function getAvg(arr, key, unit) {
  if (!arr.length) return { value: 0, unit };
  let avg = arr.reduce((sum, up) => sum + (up[key] || 0), 0) / arr.length;
  if (unit === '%') avg = (avg * 100).toFixed(2);
  else if (avg > 10000 && unit === '人') avg = (avg / 10000).toFixed(2); // 万人
  else avg = avg.toFixed(2);
  return { value: avg, unit };
}

function dUnit(val, unit) {
  if (unit === '人' && val > 10000) return val + '万';
  if (unit === '%') return val + '%';
  if (unit) return val + unit;
  return val;
}

function resizeAllCharts() {
  scatterCharts.value.forEach(chart => chart && chart.resize());
  barChartInstance.value && barChartInstance.value.resize();
  pieChartInstance.value && pieChartInstance.value.resize();
}

onMounted(async () => {
  await fetchUps();
  await nextTick();
  renderScatterCharts();
  renderBarChart();
  renderPieChart();
  window.addEventListener('resize', resizeAllCharts);
});

onBeforeUnmount(() => {
  scatterCharts.value.forEach(chart => chart && chart.dispose());
  barChartInstance.value && barChartInstance.value.dispose();
  pieChartInstance.value && pieChartInstance.value.dispose();
  window.removeEventListener('resize', resizeAllCharts);
});
</script>

<style scoped>
.page-header {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.up-scatter-chart {
  width: 100%;
  height: 400px;
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  margin-bottom: 1rem;
  position: relative;
}
.up-tooltip {
  position: fixed;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  padding: 12px 18px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
}
.up-tooltip img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-bottom: 8px;
  object-fit: cover;
}
.scatter-charts {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
}
.scatter-chart {
  flex: 1;
  margin-right: 1rem;
}
.scatter-chart:last-child {
  margin-right: 0;
}
.bar-chart {
  width: 100%;
  height: 300px;
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  margin-bottom: 2rem;
  position: relative;
}
.pie-chart {
  width: 100%;
  height: 300px;
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  margin-bottom: 2rem;
  position: relative;
}
.up-tooltip-float {
  position: absolute;
  left: 50%;
  top: -70px;
  transform: translateX(-50%);
  background: rgba(255,255,255,0.92);
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  padding: 12px 18px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
  pointer-events: none;
  transition: opacity 0.2s;
}
</style> 