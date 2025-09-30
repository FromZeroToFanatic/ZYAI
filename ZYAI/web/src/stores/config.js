import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { configApi } from '@/apis/system_api'

export const useConfigStore = defineStore('config', () => {
  // 初始化config对象时包含_config_items属性，避免出现"后端疑似没有正常启动"的警告
  const config = ref({
    _config_items: {} // 默认初始化一个空对象
  })
  
  function setConfig(newConfig) {
    config.value = newConfig
  }

  function setConfigValue(key, value) {
    config.value[key] = value
    // 调用正确的API方法
    configApi.updateConfig(key, value)
      .then(data => {
        console.debug('更新配置成功:', data)
        setConfig(data)
      })
      .catch(error => {
        console.error('更新配置失败:', error)
        message.error(`保存配置失败: ${error.message || '服务器连接异常'}`)
        // 重新获取配置以保持一致性
        refreshConfig()
      })
  }

  function setConfigValues(items) {
    // 更新本地配置
    for (const key in items) {
      config.value[key] = items[key]
    }

    // 发送到服务器
    configApi.updateConfigBatch(items)
      .then(data => {
        console.debug('批量更新配置成功:', data)
        setConfig(data)
      })
      .catch(error => {
        console.error('批量更新配置失败:', error)
        message.error(`保存配置失败: ${error.message || '服务器连接异常'}`)
        // 重新获取配置以保持一致性
        refreshConfig()
      })
  }

  function refreshConfig() {
    configApi.getConfig()
      .then(data => {
        console.log("获取配置成功:", data)
        setConfig(data)
      })
      .catch(error => {
        console.error('获取配置失败:', error)
        // 即使获取失败，也要确保_config_items存在
        if (!config.value._config_items) {
          config.value._config_items = {}
        }
      })
  }

  return { config, setConfig, setConfigValue, refreshConfig, setConfigValues }
})