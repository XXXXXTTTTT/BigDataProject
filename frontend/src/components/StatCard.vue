<template>
  <div class="stat-card">
    <div class="stat-icon" :class="iconClass">
      <component :is="icon" />
    </div>
    <div class="stat-info">
      <h3>{{ title }}</h3>
      <p class="stat-value">{{ value }}</p>
      <p class="stat-change" :class="changeClass">
        {{ change }}
        <component :is="changeIcon" />
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { 
  ArrowUp as ArrowUpIcon,
  ArrowDown as ArrowDownIcon
} from 'lucide-vue-next';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: String,
    required: true
  },
  change: {
    type: String,
    required: true
  },
  icon: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    default: 'users',
    validator: (value) => ['users', 'views', 'revenue', 'engagement'].includes(value)
  },
  isPositive: {
    type: Boolean,
    default: true
  }
});

const iconClass = computed(() => props.type);
const changeClass = computed(() => props.isPositive ? 'positive' : 'negative');
const changeIcon = computed(() => props.isPositive ? ArrowUpIcon : ArrowDownIcon);
</script>

<style scoped>
.stat-card {
  background-color: var(--card);
  border-radius: var(--radius);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon.users {
  background-color: var(--primary);
}

.stat-icon.views {
  background-color: var(--secondary);
}

.stat-icon.revenue {
  background-color: #10B981;
}

.stat-icon.engagement {
  background-color: #F59E0B;
}

.stat-info h3 {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-change {
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-change.positive {
  color: #10B981;
}

.stat-change.negative {
  color: #EF4444;
}
</style>
