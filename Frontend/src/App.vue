<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/authStore' // 導入 Auth Store

// 獲取 store 實例
const authStore = useAuthStore()

// 準備登出方法
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