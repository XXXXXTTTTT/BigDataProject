<template>
  <div class="table-section">
    <div class="card-header">
      <h3>{{ title }}</h3>
      <div class="table-actions">
        <div class="search-filter">
          <input type="text" v-model="searchQuery" placeholder="搜索条目..." />
          <SearchIcon />
        </div>
        <button class="filter-button" @click="toggleFilters">
          <FilterIcon />
          筛选
        </button>
        <button class="export-button" @click="exportData">
          <DownloadIcon />
          导出
        </button>
      </div>
    </div>
    <div class="data-table">
      <table>
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key" @click="sortBy(column.key)">
              {{ column.label }}
              <span v-if="sortKey === column.key" class="sort-indicator">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in sortedAndFilteredData" :key="item.id">
            <td v-for="column in columns" :key="column.key">
              <slot :name="column.key" :item="item">
                {{ item[column.key] }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button class="pagination-button" @click="prevPage" :disabled="currentPage === 1">
          <ChevronLeftIcon />
        </button>
        <button 
          v-for="page in totalPages" 
          :key="page" 
          class="pagination-number" 
          :class="{ 'active': currentPage === page }"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
        <button class="pagination-button" @click="nextPage" :disabled="currentPage === totalPages">
          <ChevronRightIcon />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { 
  Search as SearchIcon,
  Filter as FilterIcon,
  Download as DownloadIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon
} from 'lucide-vue-next';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  data: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
  itemsPerPage: {
    type: Number,
    default: 5
  }
});

const emit = defineEmits(['export', 'filter']);

const searchQuery = ref('');
const sortKey = ref('');
const sortOrder = ref('asc');
const currentPage = ref(1);

const filteredData = computed(() => {
  if (!searchQuery.value) return props.data;
  
  return props.data.filter(item => {
    return props.columns.some(column => {
      const value = item[column.key];
      return value && value.toString().toLowerCase().includes(searchQuery.value.toLowerCase());
    });
  });
});

const sortedData = computed(() => {
  if (!sortKey.value) return filteredData.value;
  
  return [...filteredData.value].sort((a, b) => {
    const aValue = a[sortKey.value];
    const bValue = b[sortKey.value];
    
    if (aValue === bValue) return 0;
    
    const result = aValue > bValue ? 1 : -1;
    return sortOrder.value === 'asc' ? result : -result;
  });
});

const totalPages = computed(() => {
  return Math.ceil(filteredData.value.length / props.itemsPerPage);
});

const sortedAndFilteredData = computed(() => {
  const start = (currentPage.value - 1) * props.itemsPerPage;
  const end = start + props.itemsPerPage;
  return sortedData.value.slice(start, end);
});

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const goToPage = (page) => {
  currentPage.value = page;
};

const toggleFilters = () => {
  emit('filter');
};

const exportData = () => {
  emit('export', sortedData.value);
};
</script>

<style scoped>
.table-section {
  background-color: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.table-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-filter {
  position: relative;
}

.search-filter input {
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border-radius: var(--radius);
  border: 1px solid var(--input);
  background-color: var(--muted);
  color: var(--foreground);
}

.search-filter svg {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--muted-foreground);
}

.filter-button, .export-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: var(--muted);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--foreground);
}

.export-button {
  background-color: var(--primary);
  color: white;
  border: none;
}

.data-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: var(--muted);
}

th, td {
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

th {
  font-weight: 600;
  color: var(--muted-foreground);
  cursor: pointer;
}

th:hover {
  background-color: var(--border);
}

.sort-indicator {
  margin-left: 0.25rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid var(--border);
}

.pagination-button, .pagination-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background-color: var(--card);
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-number.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
}

.pagination-button:hover, .pagination-number:hover:not(.active) {
  background-color: var(--muted);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .table-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .search-filter {
    width: 100%;
  }
  
  .search-filter input {
    width: 100%;
  }
}
</style>
