<template>
  <div class="media-section">
    <div class="card-header">
      <h3>{{ title }}</h3>
      <div class="view-options">
        <button :class="{ 'active': viewMode === 'grid' }" @click="viewMode = 'grid'">
          <GridIcon />
        </button>
        <button :class="{ 'active': viewMode === 'list' }" @click="viewMode = 'list'">
          <ListIcon />
        </button>
      </div>
    </div>
    <div class="media-gallery" :class="viewMode">
      <div class="media-card" v-for="item in items" :key="item.id" @click="selectItem(item)">
        <div class="media-thumbnail">
          <img :src="item.thumbnail" :alt="item.title" />
          <div class="media-overlay">
            <button class="play-button" v-if="item.type === 'video'">
              <PlayIcon />
            </button>
            <button class="expand-button" v-else>
              <MaximizeIcon />
            </button>
          </div>
          <span class="media-duration" v-if="item.duration">{{ item.duration }}</span>
        </div>
        <div class="media-info">
          <h4>{{ item.title }}</h4>
          <div class="media-meta">
            <span><EyeIcon /> {{ item.views }}</span>
            <span><ThumbsUpIcon /> {{ item.likes }}</span>
            <span><MessageSquareIcon /> {{ item.comments }}</span>
          </div>
        </div>
      </div>
    </div>
    <button class="load-more" v-if="hasMore" @click="loadMore">加载更多</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { 
  Grid as GridIcon,
  List as ListIcon,
  Play as PlayIcon,
  Maximize as MaximizeIcon,
  Eye as EyeIcon,
  ThumbsUp as ThumbsUpIcon,
  MessageSquare as MessageSquareIcon
} from 'lucide-vue-next';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    required: true
  },
  hasMore: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['select', 'load-more']);

const viewMode = ref('grid');

const selectItem = (item) => {
  emit('select', item);
};

const loadMore = () => {
  emit('load-more');
};
</script>

<style scoped>
.media-section {
  background-color: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.view-options {
  display: flex;
  gap: 0.5rem;
}

.view-options button {
  background: none;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.25rem;
  cursor: pointer;
  color: var(--muted-foreground);
}

.view-options button.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
}

.media-gallery {
  padding: 1.5rem;
}

.media-gallery.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.media-gallery.list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.media-gallery.list .media-card {
  display: flex;
  align-items: center;
}

.media-gallery.list .media-thumbnail {
  width: 200px;
  flex-shrink: 0;
}

.media-gallery.list .media-info {
  flex: 1;
}

.media-card {
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
}

.media-card:hover {
  transform: translateY(-5px);
}

.media-thumbnail {
  position: relative;
  height: 160px;
}

.media-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.media-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.media-thumbnail:hover .media-overlay {
  opacity: 1;
}

.play-button, .expand-button {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  border: 2px solid white;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.play-button:hover, .expand-button:hover {
  background-color: var(--primary);
  border-color: var(--primary);
  transform: scale(1.1);
}

.media-duration {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.media-info {
  padding: 1rem;
  background-color: var(--card);
}

.media-info h4 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.media-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

.media-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.load-more {
  display: block;
  margin: 0 auto 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: var(--muted);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--foreground);
  font-weight: 500;
  transition: all 0.2s;
}

.load-more:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}

@media (max-width: 768px) {
  .media-gallery.grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
  
  .media-gallery.list .media-card {
    flex-direction: column;
  }
  
  .media-gallery.list .media-thumbnail {
    width: 100%;
  }
}
</style>
