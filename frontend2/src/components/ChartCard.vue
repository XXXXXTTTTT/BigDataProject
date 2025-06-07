<template>
  <div class="chart-card" :class="{ 'large': isLarge }">
    <div class="card-header">
      <h3>{{ title }}</h3>
      <div class="card-actions">
        <button @click="refreshData"><RefreshCwIcon /></button>
        <button><MoreVerticalIcon /></button>
      </div>
    </div>
    <div class="chart-area">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { 
  RefreshCw as RefreshCwIcon,
  MoreVertical as MoreVerticalIcon
} from 'lucide-vue-next';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  isLarge: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['refresh']);

const refreshData = () => {
  emit('refresh');
};
</script>

<style scoped>
.chart-card {
  background-color: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chart-card.large {
  grid-column: span 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
}

.card-header h3 {
  font-size: 1rem;
  font-weight: 600;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.card-actions button {
  background: none;
  border: none;
  color: var(--muted-foreground);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.card-actions button:hover {
  background-color: var(--muted);
  color: var(--foreground);
}

.chart-area {
  padding: 1.5rem;
  height: 300px;
}

@media (max-width: 1024px) {
  .chart-card.large {
    grid-column: span 1;
  }
}
</style>
