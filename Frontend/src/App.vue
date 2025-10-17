<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/authStore' // 1. 導入 Auth Store

// 2. 獲取 store 實例
const authStore = useAuthStore()

// 3. 準備登出方法 (可選，也可以直接在模板中呼叫)
const handleLogout = () => {
  authStore.logout()
}
</script>

<template>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>

</style>