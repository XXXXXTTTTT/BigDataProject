import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDashboardMetrics, getActivityData, getCategoryData } from '@/services/dashboard'

export const useDashboardStore = defineStore('dashboard', () => {
  const metrics = ref(null)
  const activityData = ref([])
  const categoryData = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchMetrics = async () => {
    try {
      loading.value = true
      error.value = null
      metrics.value = await getDashboardMetrics()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch metrics'
    } finally {
      loading.value = false
    }
  }

  const fetchActivityData = async (startDate, endDate) => {
    try {
      loading.value = true
      error.value = null
      activityData.value = await getActivityData({ startDate, endDate })
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch activity data'
    } finally {
      loading.value = false
    }
  }

  const fetchCategoryData = async () => {
    try {
      loading.value = true
      error.value = null
      categoryData.value = await getCategoryData()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch category data'
    } finally {
      loading.value = false
    }
  }

  return {
    metrics,
    activityData,
    categoryData,
    loading,
    error,
    fetchMetrics,
    fetchActivityData,
    fetchCategoryData
  }
}) 