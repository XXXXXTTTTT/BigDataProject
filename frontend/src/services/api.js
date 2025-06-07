import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，跳转到登录页
          break
        case 403:
          // 权限不足
          break
        case 404:
          // 资源不存在
          break
        case 500:
          // 服务器错误
          break
        default:
          break
      }
    }
    return Promise.reject(error)
  }
)

export default api 