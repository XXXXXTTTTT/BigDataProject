<template>
  <div>
    <div class="page-header">
      <h2>媒体管理</h2>
      <div class="page-actions">
        <button class="upload-button" @click="showUploadDialog = true">
          <UploadIcon />
          上传文件
        </button>
        <button class="folder-button" @click="showFolderDialog = true">
          <FolderPlusIcon />
          新建文件夹
        </button>
      </div>
    </div>

    <!-- 媒体库 -->
    <MediaGallery 
      title="媒体文件" 
      :items="mediaItems" 
      :hasMore="true"
      @select="selectMedia"
      @load-more="loadMore"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import MediaGallery from '../components/MediaGallery.vue';
import { 
  Upload as UploadIcon,
  FolderPlus as FolderPlusIcon
} from 'lucide-vue-next';

const showUploadDialog = ref(false);
const showFolderDialog = ref(false);

const mediaItems = ref([
  {
    id: 1,
    type: 'video',
    title: '产品介绍视频',
    thumbnail: '/placeholder.svg?height=160&width=280',
    duration: '5:42',
    views: '12.5K',
    likes: '892',
    comments: '156'
  },
  {
    id: 2,
    type: 'image',
    title: '用户界面设计图',
    thumbnail: '/placeholder.svg?height=160&width=280',
    views: '8.9K',
    likes: '567',
    comments: '89'
  },
  {
    id: 3,
    type: 'video',
    title: '数据分析演示',
    thumbnail: '/placeholder.svg?height=160&width=280',
    duration: '12:18',
    views: '25.3K',
    likes: '1.2K',
    comments: '234'
  },
  {
    id: 4,
    type: 'image',
    title: '营销海报设计',
    thumbnail: '/placeholder.svg?height=160&width=280',
    views: '6.7K',
    likes: '445',
    comments: '67'
  }
]);

const selectMedia = (item) => {
  console.log('选择媒体文件:', item.title);
};

const loadMore = () => {
  console.log('加载更多媒体文件...');
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

.upload-button, .folder-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background-color 0.2s;
}

.upload-button {
  background-color: var(--primary);
  color: white;
}

.folder-button {
  background-color: var(--muted);
  color: var(--foreground);
  border: 1px solid var(--border);
}

.upload-button:hover {
  background-color: #e91e63;
}

.folder-button:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}
</style>
