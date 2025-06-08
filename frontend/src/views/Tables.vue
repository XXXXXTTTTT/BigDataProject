<template>
  <div>
    <div class="page-header">
      <h2>数据表管理</h2>
      <div class="page-actions">
        <button class="create-button" @click="showCreateDialog = true">
          <PlusIcon />
          创建表
        </button>
        <button class="import-button" @click="showImportDialog = true">
          <UploadIcon />
          导入数据
        </button>
      </div>
    </div>

    <!-- 表格列表 -->
    <DataTable 
      title="数据表" 
      :data="tables" 
      :columns="tableColumns"
      @export="exportTable"
      @filter="showFilterDialog = true"
    >
      <template #name="{ item }">
        <div class="table-name">
          <TableIcon class="table-icon" />
          <div>
            <div class="name">{{ item.name }}</div>
            <div class="schema">{{ item.schema }}</div>
          </div>
        </div>
      </template>
      <template #status="{ item }">
        <span class="status-badge" :class="item.status">
          {{ item.status === 'active' ? '活跃' : '非活跃' }}
        </span>
      </template>
      <template #actions="{ item }">
        <div class="action-buttons">
          <button @click="viewTable(item)" title="查看">
            <EyeIcon />
          </button>
          <button @click="editTable(item)" title="编辑">
            <EditIcon />
          </button>
          <button @click="deleteTable(item)" title="删除">
            <TrashIcon />
          </button>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DataTable from '../components/DataTable.vue';
import { 
  Plus as PlusIcon,
  Upload as UploadIcon,
  Table as TableIcon,
  Eye as EyeIcon,
  Edit as EditIcon,
  Trash as TrashIcon
} from 'lucide-vue-next';

const showCreateDialog = ref(false);
const showImportDialog = ref(false);
const showFilterDialog = ref(false);

const tableColumns = [
  { key: 'name', label: '表名' },
  { key: 'records', label: '记录数' },
  { key: 'size', label: '大小' },
  { key: 'status', label: '状态' },
  { key: 'lastModified', label: '最后修改' },
  { key: 'actions', label: '操作' }
];

const tables = ref([
  {
    id: 1,
    name: 'users',
    schema: 'public',
    records: '1,234,567',
    size: '45.2 MB',
    status: 'active',
    lastModified: '2023-11-15 10:30'
  },
  {
    id: 2,
    name: 'orders',
    schema: 'public',
    records: '567,890',
    size: '78.9 MB',
    status: 'active',
    lastModified: '2023-11-15 09:45'
  },
  {
    id: 3,
    name: 'products',
    schema: 'public',
    records: '12,345',
    size: '5.6 MB',
    status: 'active',
    lastModified: '2023-11-14 16:20'
  },
  {
    id: 4,
    name: 'logs_archive',
    schema: 'archive',
    records: '9,876,543',
    size: '2.3 GB',
    status: 'inactive',
    lastModified: '2023-11-10 14:15'
  }
]);

const viewTable = (table) => {
  console.log('查看表:', table.name);
};

const editTable = (table) => {
  console.log('编辑表:', table.name);
};

const deleteTable = (table) => {
  console.log('删除表:', table.name);
};

const exportTable = (data) => {
  console.log('导出表数据:', data);
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

.create-button, .import-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background-color 0.2s;
}

.create-button {
  background-color: var(--primary);
  color: white;
}

.import-button {
  background-color: var(--muted);
  color: var(--foreground);
  border: 1px solid var(--border);
}

.create-button:hover {
  background-color: #e91e63;
}

.import-button:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}

.table-name {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.table-icon {
  color: var(--primary);
  flex-shrink: 0;
}

.name {
  font-weight: 500;
}

.schema {
  font-size: 0.75rem;
  color: var(--muted-foreground);
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.active {
  background-color: rgba(16, 185, 129, 0.1);
  color: #10B981;
}

.status-badge.inactive {
  background-color: rgba(107, 114, 128, 0.1);
  color: #6B7280;
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
</style>
