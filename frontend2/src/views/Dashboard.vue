<template>
  <div>
    <div class="page-header">
      <h2>仪表盘概览</h2>
      <div class="date-filter">
        <button class="date-button" @click="toggleDatePicker">
          <CalendarIcon />
          {{ selectedDateRange }}
          <ChevronDownIcon />
        </button>
        <div class="date-picker" v-if="showDatePicker">
          <div 
            v-for="range in dateRanges" 
            :key="range.value" 
            class="date-option"
            :class="{ 'active': selectedRange === range.value }"
            @click="selectDateRange(range.value)"
          >
            {{ range.label }}
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-container">
      <StatCard 
        title="总用户数" 
        value="2.4M" 
        change="+12.5%" 
        :icon="UsersIcon" 
        type="users" 
        :isPositive="true" 
      />
      <StatCard 
        title="页面浏览量" 
        value="18.6M" 
        change="+8.2%" 
        :icon="EyeIcon" 
        type="views" 
        :isPositive="true" 
      />
      <StatCard 
        title="收入" 
        value="$842K" 
        change="+5.3%" 
        :icon="DollarSignIcon" 
        type="revenue" 
        :isPositive="true" 
      />
      <StatCard 
        title="参与度" 
        value="64.7%" 
        change="-2.1%" 
        :icon="ActivityIcon" 
        type="engagement" 
        :isPositive="false" 
      />
    </div>

    <!-- Charts Section -->
    <div class="charts-container">
      <ChartCard title="用户活动趋势" :isLarge="true" @refresh="refreshCharts">
        <LineChart :chartData="lineChartData" />
      </ChartCard>
      <ChartCard title="流量来源" @refresh="refreshCharts">
        <DoughnutChart :chartData="doughnutChartData" />
      </ChartCard>
      <ChartCard title="内容分类" @refresh="refreshCharts">
        <BarChart :chartData="barChartData" />
      </ChartCard>
    </div>

    <!-- Data Table Section -->
    <DataTable 
      title="最近数据条目" 
      :data="tableData" 
      :columns="tableColumns"
      @export="exportTableData"
      @filter="showFilterDialog = true"
    >
      <template #title="{ item }">
        <div class="title-cell">
          <img :src="item.thumbnail" :alt="item.title" class="thumbnail" />
          <span>{{ item.title }}</span>
        </div>
      </template>
      <template #category="{ item }">
        <span class="category-tag" :class="item.category.toLowerCase()">
          {{ item.category }}
        </span>
      </template>
      <template #actions="{ item }">
        <div class="action-buttons">
          <button @click="editItem(item)"><EditIcon /></button>
          <button @click="deleteItem(item)"><TrashIcon /></button>
        </div>
      </template>
    </DataTable>

    <!-- Media Gallery Section -->
    <MediaGallery 
      title="媒体库" 
      :items="mediaData" 
      :hasMore="true"
      @select="openMediaItem"
      @load-more="loadMoreMedia"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useDataStore } from '../store';
import StatCard from '../components/StatCard.vue';
import ChartCard from '../components/ChartCard.vue';
import DataTable from '../components/DataTable.vue';
import MediaGallery from '../components/MediaGallery.vue';
import { 
  Users as UsersIcon,
  Eye as EyeIcon,
  DollarSign as DollarSignIcon,
  Activity as ActivityIcon,
  Calendar as CalendarIcon,
  ChevronDown as ChevronDownIcon,
  Edit as EditIcon,
  Trash as TrashIcon
} from 'lucide-vue-next';

// Chart components (simplified for this example)
const LineChart = {
  props: ['chartData'],
  template: `
    <div class="chart-container">
      <!-- This would be a real chart in production -->
      <div class="chart-placeholder line-chart">
        <div class="chart-lines">
          <div class="chart-line" v-for="(_, i) in 5" :key="i" :style="{ height: (20 + i * 20) + '%' }"></div>
        </div>
      </div>
    </div>
  `
};

const DoughnutChart = {
  props: ['chartData'],
  template: `
    <div class="chart-container">
      <!-- This would be a real chart in production -->
      <div class="chart-placeholder doughnut-chart">
        <div class="doughnut-segments">
          <div class="doughnut-segment" 
               v-for="(data, i) in chartData.datasets[0].data" 
               :key="i"
               :style="{ 
                 backgroundColor: chartData.datasets[0].backgroundColor[i],
                 transform: \`rotate(\${i * 72}deg)\`,
                 clipPath: 'polygon(50% 50%, 100% 0, 100% 100%, 50% 100%)'
               }">
          </div>
        </div>
      </div>
    </div>
  `
};

const BarChart = {
  props: ['chartData'],
  template: `
    <div class="chart-container">
      <!-- This would be a real chart in production -->
      <div class="chart-placeholder bar-chart">
        <div class="bar-container">
          <div class="chart-bar" 
               v-for="(data, i) in chartData.datasets[0].data" 
               :key="i"
               :style="{ 
                 height: (data / 5 * 100) + '%',
                 backgroundColor: chartData.datasets[0].backgroundColor
               }">
          </div>
        </div>
      </div>
    </div>
  `
};

const dataStore = useDataStore();

// Date filter
const showDatePicker = ref(false);
const selectedRange = ref('7d');
const dateRanges = [
  { label: '今天', value: '1d' },
  { label: '昨天', value: 'yesterday' },
  { label: '过去7天', value: '7d' },
  { label: '过去30天', value: '30d' },
  { label: '本月', value: 'month' },
  { label: '上个月', value: 'last-month' },
  { label: '今年', value: 'year' }
];

const selectedDateRange = computed(() => {
  const range = dateRanges.find(r => r.value === selectedRange.value);
  return range ? range.label : '过去7天';
});

const toggleDatePicker = () => {
  showDatePicker.value = !showDatePicker.value;
};

const selectDateRange = (range) => {
  selectedRange.value = range;
  showDatePicker.value = false;
  // 在实际应用中，这里会触发数据重新加载
};

// Table configuration
const tableColumns = [
  { key: 'id', label: 'ID' },
  { key: 'title', label: '标题' },
  { key: 'category', label: '分类' },
  { key: 'views', label: '浏览量' },
  { key: 'likes', label: '点赞' },
  { key: 'comments', label: '评论' },
  { key: 'date', label: '日期' },
  { key: 'actions', label: '操作' }
];

const showFilterDialog = ref(false);

// Data from store
const lineChartData = computed(() => dataStore.lineChartData);
const doughnutChartData = computed(() => dataStore.doughnutChartData);
const barChartData = computed(() => dataStore.barChartData);
const tableData = computed(() => dataStore.tableData);
const mediaData = computed(() => dataStore.mediaData);

// Methods
const refreshCharts = () => {
  console.log('Refreshing charts...');
  // 在实际应用中，这里会重新获取数据
};

const exportTableData = (data) => {
  console.log('Exporting data:', data);
  // 在实际应用中，这里会导出数据到CSV或Excel
};

const editItem = (item) => {
  console.log('Editing item:', item);
  // 在实际应用中，这里会打开编辑对话框
};

const deleteItem = (item) => {
  console.log('Deleting item:', item);
  // 在实际应用中，这里会显示确认对话框并删除项目
};

const openMediaItem = (item) => {
  console.log('Opening media item:', item);
  // 在实际应用中，这里会打开媒体查看器
};

const loadMoreMedia = () => {
  console.log('Loading more media...');
  // 在实际应用中，这里会加载更多媒体项目
};

onMounted(async () => {
  await dataStore.fetchData();
});
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

.date-filter {
  position: relative;
}

.date-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--foreground);
}

.date-picker {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 200px;
  z-index: 10;
}

.date-option {
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.date-option:hover {
  background-color: var(--muted);
}

.date-option.active {
  background-color: var(--primary-light);
  color: var(--primary);
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.thumbnail {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
}

.category-tag {
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.category-tag.technology {
  background-color: var(--primary-light);
  color: var(--primary);
}

.category-tag.education {
  background-color: var(--secondary-light);
  color: var(--secondary);
}

.category-tag.design {
  background-color: rgba(124, 58, 237, 0.1);
  color: #7C3AED;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-buttons button {
  background: none;
  border: none;
  color: var(--muted-foreground);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.action-buttons button:hover {
  background-color: var(--muted);
  color: var(--foreground);
}

/* Chart placeholders for demo */
.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  position: relative;
}

.chart-lines {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.chart-line {
  width: 100%;
  height: 1px;
  background-color: var(--border);
}

.line-chart::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60%;
  background: linear-gradient(to top, var(--primary-light), transparent);
  z-index: 1;
}

.line-chart::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--primary);
  z-index: 2;
  clip-path: polygon(
    0% 0%, 
    15% 50%, 
    30% 20%, 
    45% 60%, 
    60% 40%, 
    75% 60%, 
    90% 10%, 
    100% 30%, 
    100% 100%, 
    0% 100%
  );
}

.doughnut-chart {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
}

.doughnut-segments {
  width: 100%;
  height: 100%;
  position: relative;
}

.doughnut-segment {
  position: absolute;
  width: 100%;
  height: 100%;
  transform-origin: center;
}

.doughnut-chart::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60%;
  height: 60%;
  background-color: var(--card);
  border-radius: 50%;
}

.bar-chart {
  align-items: flex-end;
}

.bar-container {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  width: 100%;
  height: 100%;
  padding-top: 20px;
}

.chart-bar {
  width: 40px;
  background-color: var(--primary);
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

@media (max-width: 1024px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
}
</style>
