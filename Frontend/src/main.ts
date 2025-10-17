import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from '@/stores/authStore';

import App from './App.vue'
import router from './router'
import 'element-plus/dist/index.css'

const app = createApp(App)

const pinia = createPinia();
app.use(pinia);
const authStore = useAuthStore(pinia);
await authStore.checkAuthStatus();
app.use(router)

app.mount('#app')
