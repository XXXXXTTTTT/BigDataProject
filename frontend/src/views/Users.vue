<template>
  <div>
    <div class="page-header">
      <h2>用户管理</h2>
      <button class="invite-button" @click="showInviteDialog = true">
        <UserPlusIcon />
        邀请用户
      </button>
    </div>

    <!-- 用户表格 -->
    <DataTable 
      title="用户列表" 
      :data="users" 
      :columns="userColumns"
      @export="exportUsers"
      @filter="showFilterDialog = true"
    >
      <template #user="{ item }">
        <div class="user-cell">
          <img :src="item.avatar" :alt="item.name" class="user-avatar" />
          <div>
            <div class="user-name">{{ item.name }}</div>
            <div class="user-email">{{ item.email }}</div>
          </div>
        </div>
      </template>
      <template #role="{ item }">
        <span class="role-badge" :class="item.role">
          {{ getRoleText(item.role) }}
        </span>
      </template>
      <template #status="{ item }">
        <span class="status-badge" :class="item.status">
          {{ item.status === 'active' ? '活跃' : '非活跃' }}
        </span>
      </template>
      <template #actions="{ item }">
        <div class="action-buttons">
          <button @click="editUser(item)" title="编辑">
            <EditIcon />
          </button>
          <button @click="toggleUserStatus(item)" title="切换状态">
            <ShieldIcon />
          </button>
          <button @click="deleteUser(item)" title="删除">
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
  UserPlus as UserPlusIcon,
  Edit as EditIcon,
  Shield as ShieldIcon,
  Trash as TrashIcon
} from 'lucide-vue-next';

const showInviteDialog = ref(false);
const showFilterDialog = ref(false);

const userColumns = [
  { key: 'user', label: '用户' },
  { key: 'role', label: '角色' },
  { key: 'department', label: '部门' },
  { key: 'status', label: '状态' },
  { key: 'lastLogin', label: '最后登录' },
  { key: 'actions', label: '操作' }
];

const users = ref([
  {
    id: 1,
    name: '张三',
    email: 'zhangsan@company.com',
    avatar: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40"%3E%3Ccircle cx="20" cy="20" r="20" fill="%23FB7299"/%3E%3Ctext x="20" y="25" text-anchor="middle" fill="white" font-size="12"%3E头%3C/text%3E%3C/svg%3E',
    role: 'admin',
    department: '技术部',
    status: 'active',
    lastLogin: '2023-11-15 10:30'
  },
  {
    id: 2,
    name: '李四',
    email: 'lisi@company.com',
    avatar: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40"%3E%3Ccircle cx="20" cy="20" r="20" fill="%23FB7299"/%3E%3Ctext x="20" y="25" text-anchor="middle" fill="white" font-size="12"%3E头%3C/text%3E%3C/svg%3E',
    role: 'user',
    department: '市场部',
    status: 'active',
    lastLogin: '2023-11-15 09:45'
  },
  {
    id: 3,
    name: '王五',
    email: 'wangwu@company.com',
    avatar: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40"%3E%3Ccircle cx="20" cy="20" r="20" fill="%23FB7299"/%3E%3Ctext x="20" y="25" text-anchor="middle" fill="white" font-size="12"%3E头%3C/text%3E%3C/svg%3E',
    role: 'editor',
    department: '产品部',
    status: 'inactive',
    lastLogin: '2023-11-10 16:20'
  }
]);

const getRoleText = (role) => {
  const roleMap = {
    admin: '管理员',
    editor: '编辑者',
    user: '普通用户'
  };
  return roleMap[role] || '未知';
};

const editUser = (user) => {
  console.log('编辑用户:', user.name);
};

const toggleUserStatus = (user) => {
  console.log('切换用户状态:', user.name);
};

const deleteUser = (user) => {
  console.log('删除用户:', user.name);
};

const exportUsers = (data) => {
  console.log('导出用户数据:', data);
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

.invite-button {
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

.invite-button:hover {
  background-color: #e91e63;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-weight: 500;
}

.user-email {
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

.role-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.role-badge.admin {
  background-color: rgba(239, 68, 68, 0.1);
  color: #EF4444;
}

.role-badge.editor {
  background-color: rgba(251, 114, 153, 0.1);
  color: var(--primary);
}

.role-badge.user {
  background-color: rgba(107, 114, 128, 0.1);
  color: #6B7280;
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
