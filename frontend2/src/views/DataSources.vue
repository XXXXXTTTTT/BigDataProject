<template>
  <div>
    <div class="page-header">
      <h2>数据源管理</h2>
      <button class="add-button" @click="showAddDialog = true">
        <PlusIcon />
        添加数据源
      </button>
    </div>

    <!-- 数据源列表 -->
    <div class="datasources-grid">
      <div 
        v-for="source in dataSources" 
        :key="source.id" 
        class="datasource-card"
        :class="{ 'connected': source.status === 'connected' }"
      >
        <div class="datasource-header">
          <div class="datasource-icon" :class="source.type">
            <component :is="getIcon(source.type)" />
          </div>
          <div class="datasource-status">
            <span class="status-dot" :class="source.status"></span>
            {{ source.status === 'connected' ? '已连接' : '未连接' }}
          </div>
        </div>
        <div class="datasource-info">
          <h3>{{ source.name }}</h3>
          <p>{{ source.description }}</p>
          <div class="datasource-meta">
            <span><DatabaseIcon /> {{ source.type }}</span>
            <span><CalendarIcon /> {{ source.lastSync }}</span>
          </div>
        </div>
        <div class="datasource-actions">
          <button @click="testConnection(source)">
            <WifiIcon />
            测试连接
          </button>
          <button @click="editSource(source)">
            <SettingsIcon />
            配置
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
  Database as DatabaseIcon,
  Calendar as CalendarIcon,
  Wifi as WifiIcon,
  Settings as SettingsIcon,
  Server as ServerIcon,
  Cloud as CloudIcon,
  FileText as FileTextIcon
} from 'lucide-vue-next';

const showAddDialog = ref(false);

const dataSources = ref([
  {
    id: 1,
    name: 'MySQL 主数据库',
    type: 'mysql',
    description: '用户数据和业务数据的主要存储',
    status: 'connected',
    lastSync: '2023-11-15 10:30'
  },
  {
    id: 2,
    name: 'Redis 缓存',
    type: 'redis',
    description: '实时数据缓存和会话存储',
    status: 'connected',
    lastSync: '2023-11-15 10:25'
  },
  {
    id: 3,
    name: 'Elasticsearch 日志',
    type: 'elasticsearch',
    description: '应用日志和搜索数据',
    status: 'disconnected',
    lastSync: '2023-11-14 15:20'
  },
  {
    id: 4,
    name: 'MongoDB 文档库',
    type: 'mongodb',
    description: '非结构化数据存储',
    status: 'connected',
    lastSync: '2023-11-15 09:45'
  }
]);

const getIcon = (type) => {
  const icons = {
    mysql: ServerIcon,
    redis: CloudIcon,
    elasticsearch: FileTextIcon,
    mongodb: DatabaseIcon
  };
  return icons[type] || DatabaseIcon;
};

const testConnection = (source) => {
  console.log('测试连接:', source.name);
};

const editSource = (source) => {
  console.log('编辑数据源:', source.name);
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

.add-button {
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

.add-button:hover {
  background-color: #e91e63;
}

.datasources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.datasource-card {
  background-color: var(--card);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-left: 4px solid var(--border);
  transition: all 0.2s;
}

.datasource-card.connected {
  border-left-color: #10B981;
}

.datasource-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.datasource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.datasource-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.datasource-icon.mysql {
  background-color: #4479A1;
}

.datasource-icon.redis {
  background-color: #DC382D;
}

.datasource-icon.elasticsearch {
  background-color: #005571;
}

.datasource-icon.mongodb {
  background-color: #47A248;
}

.datasource-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.connected {
  background-color: #10B981;
}

.status-dot.disconnected {
  background-color: #EF4444;
}

.datasource-info h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.datasource-info p {
  color: var(--muted-foreground);
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.datasource-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: var(--muted-foreground);
  margin-bottom: 1rem;
}

.datasource-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.datasource-actions {
  display: flex;
  gap: 0.5rem;
}

.datasource-actions button {
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

.datasource-actions button:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}
</style>
