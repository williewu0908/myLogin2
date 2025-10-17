<script setup lang="ts"> // <-- 關鍵改變
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';

// ref('') 會被 TypeScript 自動推導為 Ref<string>
const username = ref('');
const password = ref('');
const errorMsg = ref('');
const isLoading = ref(false);

const authStore = useAuthStore();

const handleLogin = async () => {
  isLoading.value = true;
  errorMsg.value = '';
  try {
    await authStore.login(username.value, password.value);
  } catch (error) {
    isLoading.value = false;
    // 我們可以更精確地檢查錯誤型別
    if (error instanceof Error) {
      errorMsg.value = '帳號或密碼錯誤。';
    } else {
      errorMsg.value = '發生未知錯誤。';
    }
  }
  // 成功時 isLoading 不需設回 false，因為頁面會跳轉
};
</script>

<template>
  <div>
    <h2>登入</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">用戶名:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="password">密碼:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '登入中...' : '登入' }}
      </button>
    </form>
    <p v-if="errorMsg" style="color: red;">{{ errorMsg }}</p>
  </div>
</template>