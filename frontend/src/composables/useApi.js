import axios from 'axios'

// 创建 axios 实例，设置基础路径
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 管理员状态管理
let adminPassword = null
let isAdminMode = false

/**
 * 获取管理员登录状态
 * @returns {boolean} 是否为管理员模式
 */
export const getAdminStatus = () => isAdminMode

/**
 * 管理员登录
 * @param {string} password - 管理员密码
 */
export const loginAsAdmin = (password) => {
  adminPassword = password
  isAdminMode = true
  setAdminHeader(password)
  // 保存到 sessionStorage，刷新后保持登录状态
  sessionStorage.setItem('adminPassword', password)
}

/**
 * 管理员登出
 */
export const logoutAdmin = () => {
  adminPassword = null
  isAdminMode = false
  setAdminHeader(null)
  sessionStorage.removeItem('adminPassword')
}

/**
 * 页面加载时检查管理员状态
 * @returns {boolean} 是否已登录
 */
export const checkAdminOnLoad = () => {
  const saved = sessionStorage.getItem('adminPassword')
  if (saved) {
    loginAsAdmin(saved)
    return true
  }
  return false
}

/**
 * 验证管理员密码
 * @param {string} password - 管理员密码
 * @returns {boolean} 验证是否成功
 */
export const verifyAdmin = async (password) => {
  try {
    const response = await apiClient.post('/auth/verify', { password })
    return response.data.success
  } catch (error) {
    console.error('验证失败', error)
    return false
  }
}

/**
 * 设置管理员密码请求头
 * @param {string|null} password - 管理员密码，null 表示清除
 */
export const setAdminHeader = (password) => {
  if (password) {
    apiClient.defaults.headers.common['X-Admin-Password'] = password
  } else {
    delete apiClient.defaults.headers.common['X-Admin-Password']
  }
}

/**
 * 获取作品集列表
 * @returns {Array} 作品列表
 */
export const getPortfolio = async () => {
  const response = await apiClient.get('/portfolio')
  return response.data
}

/**
 * 添加新作品（管理员）
 * @param {Object} data - 作品数据
 * @returns {Object} 创建的作品对象
 */
export const addPortfolio = async (data) => {
  const response = await apiClient.post('/portfolio', data)
  return response.data
}

/**
 * 删除作品（管理员）
 * @param {number} id - 作品 ID
 * @returns {Object} 删除结果
 */
export const deletePortfolio = async (id) => {
  const response = await apiClient.delete(`/portfolio/${id}`)
  return response.data
}

/**
 * 获取工具列表（支持分页和搜索）
 * @param {number} page - 页码
 * @param {number} perPage - 每页数量
 * @param {string} search - 搜索关键词
 * @returns {Object} 包含 items, total, page, per_page, pages 的对象
 */
export const getTools = async (page = 1, perPage = 12, search = '') => {
  const response = await apiClient.get('/tools', {
    params: { page, per_page: perPage, search }
  })
  return response.data
}

/**
 * 下载工具文件
 * @param {number} id - 工具 ID
 * @returns {Object} axios 响应对象（blob 格式）
 */
export const downloadTool = async (id) => {
  const response = await apiClient.get(`/tools/download/${id}`, {
    responseType: 'blob'
  })
  return response.data
}

/**
 * 上传工具文件（管理员）
 * @param {FormData} formData - 包含文件和元数据的 FormData
 * @param {Function} onProgress - 上传进度回调
 * @returns {Object} 创建的工具对象
 */
export const uploadTool = async (formData, onProgress) => {
  const response = await apiClient.post('/tools/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: onProgress
  })
  return response.data
}

/**
 * 删除工具（管理员）
 * @param {number} id - 工具 ID
 * @returns {Object} 删除结果
 */
export const deleteTool = async (id) => {
  const response = await apiClient.delete(`/tools/${id}`)
  return response.data
}

/**
 * 获取访问统计（管理员）
 * @returns {Object} 统计数据
 */
export const getStats = async () => {
  const response = await apiClient.get('/stats/visits')
  return response.data
}

/**
 * 获取简历数据
 * @returns {Object} 简历数据
 */
export const getResume = async () => {
  const response = await apiClient.get('/resume')
  return response.data
}

/**
 * 更新简历数据（管理员）
 * @param {Object} data - 简历数据
 * @returns {Object} 更新结果
 */
export const updateResume = async (data) => {
  const response = await apiClient.put('/resume', data)
  return response.data
}

/**
 * 获取活动日志（管理员）
 * @param {number} page - 页码
 * @param {number} perPage - 每页数量
 * @param {string} logType - 日志类型筛选
 * @param {string} search - 搜索关键词
 * @param {number} days - 最近几天
 * @returns {Object} 日志列表
 */
export const getLogs = async (page = 1, perPage = 20, logType = '', search = '', days = 30) => {
  const response = await apiClient.get('/logs', {
    params: { page, per_page: perPage, log_type: logType, search, days }
  })
  return response.data
}

/**
 * 获取日志统计（管理员）
 * @returns {Object} 统计数据
 */
export const getLogStats = async () => {
  const response = await apiClient.get('/logs/stats')
  return response.data
}

// ============================================================
//  博客 API
// ============================================================

/**
 * 获取博客文章列表
 * @param {number} page - 页码
 * @param {number} perPage - 每页数量
 * @param {string} tag - 标签筛选
 * @param {string} search - 搜索关键词
 * @returns {Object} 文章列表
 */
export const getBlogPosts = async (page = 1, perPage = 12, tag = '', search = '', status = 'published', sort = 'desc') => {
  const response = await apiClient.get('/blog', {
    params: { page, per_page: perPage, tag, search, status, sort }
  })
  return response.data
}

/**
 * 获取单篇博客文章详情
 * @param {number} id - 文章 ID
 * @returns {Object} 文章详情
 */
export const getBlogPost = async (id) => {
  const response = await apiClient.get(`/blog/${id}`)
  return response.data
}

/**
 * 创建博客文章（管理员）
 * @param {Object} data - 文章数据
 * @returns {Object} 创建的文章
 */
export const createBlogPost = async (data) => {
  const response = await apiClient.post('/blog', data)
  return response.data
}

/**
 * 更新博客文章（管理员）
 * @param {number} id - 文章 ID
 * @param {Object} data - 更新数据
 * @returns {Object} 更新后的文章
 */
export const updateBlogPost = async (id, data) => {
  const response = await apiClient.put(`/blog/${id}`, data)
  return response.data
}

/**
 * 删除博客文章（管理员）
 * @param {number} id - 文章 ID
 */
export const deleteBlogPost = async (id) => {
  const response = await apiClient.delete(`/blog/${id}`)
  return response.data
}

/**
 * 点赞博客文章
 * @param {number} id - 文章 ID
 * @returns {Object} { likes }
 */
export const likeBlogPost = async (id) => {
  const response = await apiClient.post(`/blog/${id}/like`)
  return response.data
}

/**
 * 获取博客标签列表
 * @returns {string[]} 标签列表
 */
export const getBlogTags = async () => {
  const response = await apiClient.get('/blog/tags')
  return response.data
}

// ============================================================
//  照片墙 API
// ============================================================

/**
 * 获取照片列表
 * @returns {Array} 照片列表
 */
export const getPhotos = async () => {
  const response = await apiClient.get('/photos')
  return response.data
}

/**
 * 创建照片（管理员）
 * @param {FormData|Object} data - 照片数据（FormData 用于文件上传，Object 用于 JSON）
 * @returns {Object} 创建的照片
 */
export const createPhoto = async (data) => {
  const isFormData = data instanceof FormData
  const response = await apiClient.post('/photos', data, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {}
  })
  return response.data
}

/**
 * 更新照片（管理员）
 * @param {number} id - 照片 ID
 * @param {FormData|Object} data - 更新数据
 * @returns {Object} 更新后的照片
 */
export const updatePhoto = async (id, data) => {
  const isFormData = data instanceof FormData
  const response = await apiClient.put(`/photos/${id}`, data, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {}
  })
  return response.data
}

/**
 * 删除照片（管理员）
 * @param {number} id - 照片 ID
 * @returns {Object} 删除结果
 */
export const deletePhoto = async (id) => {
  const response = await apiClient.delete(`/photos/${id}`)
  return response.data
}

// ============================================================
//  GitHub & Gitee 数据
// ============================================================
export const getGitHubData = async () => {
  const response = await apiClient.get('/code-activity/github')
  return response.data
}

export const getGiteeData = async () => {
  const response = await apiClient.get('/code-activity/gitee')
  return response.data
}

export default {
  getAdminStatus,
  loginAsAdmin,
  logoutAdmin,
  checkAdminOnLoad,
  verifyAdmin,
  setAdminHeader,
  getPortfolio,
  addPortfolio,
  deletePortfolio,
  getTools,
  downloadTool,
  uploadTool,
  deleteTool,
  getStats,
  getResume,
  updateResume,
  getLogs,
  getLogStats,
  getPhotos,
  createPhoto,
  updatePhoto,
  deletePhoto
}