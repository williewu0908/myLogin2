<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { ElMessage, ElForm, ElMain, ElButton, ElAffix, ElCard, ElContainer, ElHeader, ElCol, ElRow, ElImage } from 'element-plus'
import { useRouter } from 'vue-router';
import backgroundImage from '@/assets/bg.jpg'

// 獲取 router 實例，用於內部跳轉
const router = useRouter();

// 定義卡片資料的型別
interface FeatureCard {
  id: number;
  title: string;
  description: string;
  imageUrl: string;
  targetUrl: string; // 點擊後要跳轉的 URL
}

// 卡片的靜態資料
const cardData = ref<FeatureCard[]>([
  {
    id: 1,
    title: '功能一：數據分析',
    description: '深入了解您的數據，提供視覺化報表。',
    imageUrl: 'https://picsum.photos/400/250?random=2',
    targetUrl: '/analytics' // 內部路由
  },
  {
    id: 2,
    title: '功能二：用戶管理',
    description: '輕鬆管理所有使用者的資料與權限。',
    imageUrl: 'https://picsum.photos/400/250?random=3',
    targetUrl: '/users' // 內部路由
  },
  {
    id: 3,
    title: '功能三：專案設定',
    description: '設定您的專案參數與喜好設定。',
    imageUrl: 'https://picsum.photos/400/250?random=4',
    targetUrl: '/settings' // 內部路由
  },
  {
    id: 4,
    title: '功能四：外部連結',
    description: '點擊這裡查看我們的官方文件。',
    imageUrl: 'https://picsum.photos/400/250?random=5',
    targetUrl: 'https://example.com' // 外部 URL
  },
  {
    id: 5,
    title: '功能一：數據分析',
    description: '深入了解您的數據，提供視覺化報表。',
    imageUrl: 'https://picsum.photos/400/250?random=2',
    targetUrl: '/analytics' // 內部路由
  },
  {
    id: 6,
    title: '功能二：用戶管理',
    description: '輕鬆管理所有使用者的資料與權限。',
    imageUrl: 'https://picsum.photos/400/250?random=3',
    targetUrl: '/users' // 內部路由
  },
  {
    id: 7,
    title: '功能三：專案設定',
    description: '設定您的專案參數與喜好設定。',
    imageUrl: 'https://picsum.photos/400/250?random=4',
    targetUrl: '/settings' // 內部路由
  },
  {
    id: 8,
    title: '功能四：外部連結',
    description: '點擊這裡查看我們的官方文件。',
    imageUrl: 'https://picsum.photos/400/250?random=5',
    targetUrl: 'https://example.com' // 外部 URL
  },
  {
    id: 9,
    title: '功能一：數據分析',
    description: '深入了解您的數據，提供視覺化報表。',
    imageUrl: 'https://picsum.photos/400/250?random=2',
    targetUrl: '/analytics' // 內部路由
  },
  {
    id: 10,
    title: '功能二：用戶管理',
    description: '輕鬆管理所有使用者的資料與權限。',
    imageUrl: 'https://picsum.photos/400/250?random=3',
    targetUrl: '/users' // 內部路由
  }
]);

// 點擊卡片時的處理函式
const handleCardClick = (url: string) => {
  if (!url) return;

  // 檢查 URL 是外部連結還是內部路由
  if (url.startsWith('http')) {
    // 外部連結 (例如 https://...)，在新分頁開啟
    window.open(url, '_blank', 'noopener,noreferrer');
  } else {
    // 內部路由 (例如 /analytics)，使用 vue-router 跳轉
    router.push(url);
  }
};


</script>

<template>
  <el-container direction="vertical" class="home-container">
    <el-header height="300px" class="home-header">
      <div class="home-button-container">
        <el-button class="signOut" size="large" round plain>
          登出
        </el-button>
      </div>
      <el-image class="home-image" :src="backgroundImage" fit="cover" alt="首頁橫幅圖片" />
      <div class="home-text">
        <h2>Online Learning system</h2>
        <p>Codes & Games & Tools</p>
      </div>
    </el-header>

    <el-main class="features-section">
      <el-row :gutter="20">

        <el-col v-for="card in cardData" :key="card.id" :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" :body-style="{ padding: '0px' }" class="feature-card"
            @click="handleCardClick(card.targetUrl)">
            <el-image :src="card.imageUrl" fit="cover" class="card-image" alt="功能圖片" />

            <div class="card-content">
              <h3>{{ card.title }}</h3>
              <p>{{ card.description }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>

  </el-container>
</template>

<style scoped>
.home-container {
  width: 100%;
  align-items: center;
}

/* 1. 頂端 Hero 圖片區塊 (el-header) */
.home-header {
  position: relative;
  width: 100%;
  padding: 0;
  margin-bottom: 24px;
}

.home-button-container {
  position: fixed;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 100%;
  height: 60px;
  padding: 10px 30px;
  backdrop-filter: blur(2px);
  background-color: #1313138e;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.274);
  z-index: 10000;
}

.signOut {
      background-color: rgba(12, 12, 12, 0.164);
      color: white;
}

.signOut:hover {
      color: rgb(63, 63, 63);
      background-color: white;
      border: transparent;
}

.home-image {
  width: 100%;
  height: 100%;
  background-color: #c2c1c16e;
  /* (可選) 圓角 */
  display: block;
  /* 確保圖片正確填滿 */
}

/* (可選) 圖片上的疊加文字 (保持不變) */
.home-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.home-text h2 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

/* 2. 功能卡片區塊 (el-main) */
.features-section {
  width: 80%;

}

/* --- 卡片樣式 (保持不變) --- */
.feature-card {
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-image {
  width: 100%;
  height: 180px;
  display: block;
}

.card-content {
  padding: 14px;
}

.card-content h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.card-content p {
  font-size: 0.9rem;
  color: #606266;
  line-height: 1.4;
}
</style>