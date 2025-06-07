import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getHotVideos, getHeatmapData, getKeywordData, getCategoryRanking, getModelMetrics, getModelComparison } from '@/services/video'

export const useVideoStore = defineStore('video', () => {
  const hotVideos = ref([])
  const heatmapData = ref([])
  const keywordData = ref([])
  const categoryRanking = ref([])
  const modelMetrics = ref(null)
  const modelComparison = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchHotVideos = async () => {
    try {
      loading.value = true
      error.value = null
      hotVideos.value = await getHotVideos()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch hot videos'
    } finally {
      loading.value = false
    }
  }

  const fetchHeatmapData = async (startDate, endDate) => {
    try {
      loading.value = true
      error.value = null
      heatmapData.value = await getHeatmapData({ startDate, endDate })
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch heatmap data'
    } finally {
      loading.value = false
    }
  }

  const fetchKeywordData = async (videoId) => {
    try {
      loading.value = true
      error.value = null
      keywordData.value = await getKeywordData(videoId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch keyword data'
    } finally {
      loading.value = false
    }
  }

  const fetchCategoryRanking = async () => {
    try {
      loading.value = true
      error.value = null
      categoryRanking.value = await getCategoryRanking()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch category ranking'
    } finally {
      loading.value = false
    }
  }

  const fetchModelMetrics = async () => {
    try {
      loading.value = true
      error.value = null
      modelMetrics.value = await getModelMetrics()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch model metrics'
    } finally {
      loading.value = false
    }
  }

  const fetchModelComparison = async () => {
    try {
      loading.value = true
      error.value = null
      modelComparison.value = await getModelComparison()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch model comparison'
    } finally {
      loading.value = false
    }
  }

  return {
    hotVideos,
    heatmapData,
    keywordData,
    categoryRanking,
    modelMetrics,
    modelComparison,
    loading,
    error,
    fetchHotVideos,
    fetchHeatmapData,
    fetchKeywordData,
    fetchCategoryRanking,
    fetchModelMetrics,
    fetchModelComparison
  }
}) 