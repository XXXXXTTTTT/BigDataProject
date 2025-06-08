<template>
  <div>
    <div class="page-header">
      <h2>报表管理</h2>
      <button class="create-button" @click="showCreateDialog = true">
        <PlusIcon />
        创建报表
      </button>
    </div>

    <!-- 报表网格 -->
    <div class="reports-grid">
      <div 
        v-for="report in reports" 
        :key="report.id" 
        class="report-card"
        @click="openReport(report)"
      >
        <div class="report-header">
          <div class="report-icon">
            <FileTextIcon />
          </div>
          <div class="report-menu">
            <button @click.stop="showReportMenu(report)">
              <MoreVerticalIcon />
            </button>
          </div>
        </div>
        <div class="report-content">
          <h3>{{ report.title }}</h3>
          <p>{{ report.description }}</p>
          <div class="report-meta">
            <span><CalendarIcon /> {{ report.lastRun }}</span>
            <span><ClockIcon /> {{ report.schedule }}</span>
          </div>
        </div>
        <div class="report-footer">
          <div class="report-status" :class="report.status">
            <span class="status-dot"></span>
            {{ getStatusText(report.status) }}
          </div>
          <button class="run-button" @click.stop="runReport(report)">
            <PlayIcon />
            运行
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { 
  Plus as PlusIcon,
  FileText as FileTextIcon,
  MoreVertical as MoreVerticalIcon,
  Calendar as CalendarIcon,
  Clock as ClockIcon,
  Play as PlayIcon
} from 'lucide-vue-next';

const showCreateDialog = ref(false);

const reports = ref([
  {
    id: 1,
    title: '每日用户活跃报表',
    description: '统计每日活跃用户数据和趋势分析',
    lastRun: '2023-11-15 06:00',
    schedule: '每日 06:00',
    status: 'success'
  },
  {
    id: 2,
    title: '销售业绩周报',
    description: '周度销售数据汇总和分析',
    lastRun: '2023-11-13 08:00',
    schedule: '每周一 08:00',
    status: 'success'
  },
  {
    id: 3,
    title: '系统性能监控',
    description: '服务器性能和应用响应时间监控',
    lastRun: '2023-11-15 11:45',
    schedule: '每小时',
    status: 'running'
  },
  {
    id: 4,
    title: '用户行为分析月报',
    description: '月度用户行为深度分析报告',
    lastRun: '2023-11-01 09:00',
    schedule: '每月1日 09:00',
    status: 'failed'
  }
]);

const getStatusText = (status) => {
  const statusMap = {
    success: '成功',
    running: '运行中',
    failed: '失败',
    pending: '等待中'
  };
  return statusMap[status] || '未知';
};

const openReport = (report) => {
  console.log('打开报表:', report.title);
};

const showReportMenu = (report) => {
  console.log('显示报表菜单:', report.title);
};

const runReport = (report) => {
  console.log('运行报表:', report.title);
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

.create-button {
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

.create-button:hover {
  background-color: #e91e63;
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.report-card {
  background-color: var(--card);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s;
}

.report-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.report-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background-color: var(--primary-light);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.report-menu button {
  background: none;
  border: none;
  color: var(--muted-foreground);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.report-menu button:hover {
  background-color: var(--muted);
}

.report-content h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.report-content p {
  color: var(--muted-foreground);
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.report-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: var(--muted-foreground);
  margin-bottom: 1rem;
}

.report-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.report-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.report-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.report-status.success .status-dot {
  background-color: #10B981;
}

.report-status.running .status-dot {
  background-color: #F59E0B;
}

.report-status.failed .status-dot {
  background-color: #EF4444;
}

.report-status.pending .status-dot {
  background-color: #6B7280;
}

.run-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--muted);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 0.875rem;
  color: var(--foreground);
  transition: all 0.2s;
}

.run-button:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}
</style>
