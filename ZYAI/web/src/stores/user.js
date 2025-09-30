import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('user_token') || '')
  const userId = ref(parseInt(localStorage.getItem('user_id') || '0') || null)
  const username = ref(localStorage.getItem('username') || '')
  const userRole = ref(localStorage.getItem('user_role') || 'user') // 从本地存储获取用户角色，默认为user

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isSuperAdmin = computed(() => userRole.value === 'superadmin')
  const isAdmin = computed(() => userRole.value === 'admin' || userRole.value === 'superadmin')

  // 动作
  async function login(credentials) {
    try {
      const formData = new FormData()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await fetch('/api/auth/token', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '登录失败')
      }

      const data = await response.json()

      // 更新状态
      token.value = data.access_token
      userId.value = data.user_id
      username.value = data.username
      userRole.value = data.role || 'user' // 保存用户角色

      // 保存到本地存储
      localStorage.setItem('user_token', data.access_token)
      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('username', data.username)
      localStorage.setItem('user_role', data.role || 'user') // 保存角色到本地存储

      return true
    } catch (error) {
      console.error('登录错误:', error)
      throw error
    }
  }

  function logout() {
    // 清除状态
    token.value = ''
    userId.value = null
    username.value = ''
    userRole.value = 'user'

    // 清除本地存储
    localStorage.removeItem('user_token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('username')
    localStorage.removeItem('user_role')
  }

  async function initialize(admin) {
    try {
      const response = await fetch('/api/auth/initialize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(admin)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '初始化管理员失败')
      }

      const data = await response.json()

      // 更新状态
      token.value = data.access_token
      userId.value = data.user_id
      username.value = data.username

      // 保存到本地存储
      localStorage.setItem('user_token', data.access_token)
      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('username', data.username)

      return true
    } catch (error) {
      console.error('初始化管理员错误:', error)
      throw error
    }
  }

  async function checkFirstRun() {
    try {
      const response = await fetch('/api/auth/check-first-run')
      const data = await response.json()
      return data.first_run
    } catch (error) {
      console.error('检查首次运行状态错误:', error)
      return false
    }
  }

  // 用于API请求的授权头
  function getAuthHeaders() {
    return {
      'Authorization': `Bearer ${token.value}`
    }
  }



  return {
    // 状态
    token,
    userId,
    username,
    userRole,

    // 计算属性
    isLoggedIn,
    isSuperAdmin,
    isAdmin,

    // 方法
    login,
    logout,
    initialize,
    checkFirstRun,
    getAuthHeaders
  }
})

// 权限检查函数
export function checkAdminPermission() {
  const store = useUserStore();
  return store.isAdmin;
}

export function checkSuperAdminPermission() {
  const store = useUserStore();
  return store.isSuperAdmin;
}