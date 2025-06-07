import { defineStore } from 'pinia'
import { ref } from 'vue'
import { searchUploaders, getUploaderInfo, getStickyUploaders, getUploaderNetwork } from '@/services/uploader'

const defaultNetworkData = {
  nodes: [{
    id: '',
    nickname: '',
    weight: 30
  }],
  edges: [{
    source: '',
    target: '',
    weight: 1
  }]
}

export const useUploaderStore = defineStore('uploader', () => {
  const searchResults = ref([])
  const selectedUploader = ref(null)
  const stickyUploaders = ref([])
  const networkData = ref(defaultNetworkData)
  const loading = ref(false)
  const error = ref(null)

  const search = async (params) => {
    try {
      loading.value = true
      error.value = null
      searchResults.value = await searchUploaders(params)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to search uploaders'
    } finally {
      loading.value = false
    }
  }

  const fetchUploaderInfo = async (uid) => {
    try {
      loading.value = true
      error.value = null
      selectedUploader.value = await getUploaderInfo(uid)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch uploader info'
    } finally {
      loading.value = false
    }
  }

  const fetchStickyUploaders = async () => {
    try {
      loading.value = true
      error.value = null
      stickyUploaders.value = await getStickyUploaders()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch sticky uploaders'
    } finally {
      loading.value = false
    }
  }

  const fetchNetworkData = async (uid) => {
    try {
      loading.value = true
      error.value = null
      networkData.value = await getUploaderNetwork(uid)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch network data'
    } finally {
      loading.value = false
    }
  }

  return {
    searchResults,
    selectedUploader,
    stickyUploaders,
    networkData,
    loading,
    error,
    search,
    fetchUploaderInfo,
    fetchStickyUploaders,
    fetchNetworkData
  }
}) 