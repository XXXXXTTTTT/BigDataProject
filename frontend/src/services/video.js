import api from './api'

export const getHotVideos = async () => {
  const response = await api.get('/videos/hot')
  return response.data
}

export const getHeatmapData = async (params) => {
  const response = await api.get('/videos/heatmap', { params })
  return response.data
}

export const getKeywordData = async (videoId) => {
  const response = await api.get(`/videos/${videoId}/keywords`)
  return response.data
}

export const getCategoryRanking = async () => {
  const response = await api.get('/videos/categories/ranking')
  return response.data
}

export const getModelMetrics = async () => {
  const response = await api.get('/videos/model/metrics')
  return response.data
}

export const getModelComparison = async () => {
  const response = await api.get('/videos/model/comparison')
  return response.data
} 