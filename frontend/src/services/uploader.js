import api from './api'

export const searchUploaders = async (params) => {
  const response = await api.get('/uploaders/search', { params })
  return response
}

export const getUploaderInfo = async (uid) => {
  const response = await api.get(`/uploaders/${uid}`)
  return response
}

export const getStickyUploaders = async () => {
  const response = await api.get('/uploaders/sticky')
  return response
}

export const getUploaderNetwork = async (uid) => {
  const response = await api.get(`/uploaders/${uid}/network`)
  return response
} 