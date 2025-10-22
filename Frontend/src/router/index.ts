import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import Login from '@/views/Login.vue';
import Home from '@/views/Home.vue';
import SignUp from '@/views/SignUp.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true } // 受保護的路由
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guestOnly: true } // 僅限訪客
  },
  {
    path: '/register',
    name: 'Register',
    component: SignUp,
    meta: { guestOnly: true } // 僅限訪客
  },
  // 根目錄重定向
  {
    path: '/',
    redirect: '/home'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const loggedIn = authStore.isAuthenticated;

  // 情況一：如果目標是「僅限訪客」的頁面
  if (to.meta.guestOnly) {
    if (loggedIn) {
      // 如果用戶已經登入，重定向到 Home
      next({ name: 'Home' });
    } else {
      // 如果用戶未登入，允許訪問
      next();
    }
  }
  // 情況二：如果目標是「需要認證」的頁面 (例如 /home)
  else if (to.meta.requiresAuth) {
    if (loggedIn) {
      // 如果用戶已經登入，允許訪問
      next();
    } else {
      // 如果用戶未登入，重定向到 Login
      next({ name: 'Login' });
    }
  }
  // 情況三：其他所有頁面
  else {
    next();
  }
});

export default router;