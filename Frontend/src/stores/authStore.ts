import { defineStore } from 'pinia';
import { ref, type Ref } from 'vue';
import { authService } from '@/services/authService';
import router from '@/router';
import type { User } from '@/types';

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

  return {
    isAuthenticated,
    user,
    login,
    logout,
    checkAuthStatus,
  };
});