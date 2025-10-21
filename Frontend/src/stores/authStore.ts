import { defineStore } from 'pinia';
import { ref, type Ref } from 'vue';
import { authService } from '@/services/authService';
import router from '@/router';
import type { User } from '@/types';
import type { SignUpForm } from '@/types'

export const useAuthStore = defineStore('authStore', () => {
  // State
  // 明確指定 user 的型別是 User 或 null
  const user: Ref<User | null> = ref(null);
  const isAuthenticated = ref(false);

  // Actions
  async function login(username: string, password: string): Promise<void> {
    try {
      const response = await authService.login(username, password);
      isAuthenticated.value = true;
      user.value = response.data.user; 
      
      router.push({ name: 'Home' });
    } catch (error) {
      console.error("Login failed:", error);
      isAuthenticated.value = false;
      user.value = null;
      throw error;
    }
  }

  async function logout(): Promise<void> {
    try {
      await authService.logout();
    } catch (error) {
      console.error("Logout API failed:", error);
    }
    
    isAuthenticated.value = false;
    user.value = null;
    router.push({ name: 'Login' });
  }

  async function checkAuthStatus(): Promise<void> {
    try {
      const response = await authService.checkSession();
      if (response.data.is_logged_in && response.data.user) {
        isAuthenticated.value = true;
        user.value = response.data.user;
      } else {
        isAuthenticated.value = false;
        user.value = null;
      }
    } catch (error) {
      isAuthenticated.value = false;
      user.value = null;
    }
  }

  async function register(formData: SignUpForm): Promise<void> {
    try {
      // 呼叫 service
      await authService.signUp(formData);
      
      // 註冊成功後，引導使用者去登入
      // (注意：這裡的 'Login' 必須是您 router/index.ts 中定義的 name)
      router.push({ name: 'Login' });
      
    } catch (error) {
      // 拋出錯誤，讓 Vue 組件可以捕獲並顯示
      console.error("Registration failed:", error);
      throw error;
    }
  }

  return {
    isAuthenticated,
    user,
    login,
    logout,
    checkAuthStatus,
    register
  };
});