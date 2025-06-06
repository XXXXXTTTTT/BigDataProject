import api from './api'

export const getDashboardMetrics = async () => {
  const response = await api.get('/dashboard/metrics')
  return response.data
}

export const getActivityData = async (params) => {
  const response = await api.get('/dashboard/activity', { params })
  return response.data
}

export const getCategoryData = async () => {
  const response = await api.get('/dashboard/categories')
  return response.data
} 