import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import Login from '@/views/Login.vue';
import Home from '@/views/Home.vue';
import SignUp from '@/views/SignUp.vue';

// 明確定義 routes 的型別
const routes: Array<RouteRecordRaw> = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'SignUp', component: SignUp },
  { 
    path: '/Home', 
    name: 'Home', 
    component: Home, 
    meta: { requiresAuth: true }
  },
  { path: '/', redirect: '/Home' }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  // Pinia store 必須在 'beforeEach' 內部獲取
  const authStore = useAuthStore();
  const loggedIn = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !loggedIn) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;