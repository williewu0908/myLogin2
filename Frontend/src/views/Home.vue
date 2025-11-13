<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { ElAnchor, ElAnchorLink, ElMessage, ElDialog, ElAvatar, ElMain, ElButton, ElCard, ElContainer, ElHeader, ElFooter, ElCol, ElRow, ElImage } from 'element-plus'
import { useRouter } from 'vue-router';
import backgroundImage from '@/assets/bg.jpg'
import { UserFilled } from '@element-plus/icons-vue'

const router = useRouter();
const authStore = useAuthStore();

interface FeatureCard {
  id: number;
  title: string;
  description: string;
  author: string;
  imageUrl: string;
  targetUrl: string; // 點擊後要跳轉的 URL
}

interface CardGroup {
  year: number | string;
  cards: FeatureCard[];
}

const groupedCardData = ref<CardGroup[]>([]);
// 🚀 載入外部 JSON
onMounted(async () => {
  try {
    const response = await fetch('/app.json')
    if (!response.ok) throw new Error('載入失敗')
    groupedCardData.value = await response.json()
  } catch (error) {
    console.error('無法載入 app.json：', error)
    ElMessage.error('無法載入功能資料')
  }
})

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


const dialogVisible = ref(false);

const handleLogout = async () => {
  try {
    await authStore.logout();
    ElMessage.success('已成功登出！');
    router.push('/login');
  } catch (error) {
    ElMessage.error('登出失敗，請稍後再試。');
  }
};

</script>

<template>
  <el-container direction="vertical" class="home-container">
    <el-header height="300px" class="home-header">
      <div class="home-header-button-container">
        <!-- <h1>Edu<span>Tools</span></h1> -->
        <el-button class="signOut" size="large" round plain @click="dialogVisible = true">
          登出
        </el-button>
        <el-avatar class="home-avatar" :size="40" :icon="UserFilled"></el-avatar>
      </div>
      <el-image class="home-image" :src="backgroundImage" fit="cover" alt="首頁橫幅圖片" />
      <div class="home-text">
        <h2>Online Learning system</h2>
        <p>Codes & Games & Tools</p>
      </div>
    </el-header>
    <el-dialog v-model="dialogVisible" title="確認" width="300" align-center>
      <span>確定要登出嗎？</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleLogout">
            確定
          </el-button>
        </div>
      </template>
    </el-dialog>

    <el-main class="features-section">
      <el-row>
        <el-col :lg="2" :md="2" :sm="2" :xs="3">
          <div class="fixed-anchor-container">
            <el-anchor class="home-anchor" direction="vertical" :offset="50">
              <el-anchor-link v-for="group in groupedCardData" :key="group.year" :href="`#year-${group.year}`"
                :title="String(group.year)" />
            </el-anchor>
          </div>
        </el-col>
        <el-col :lg="22" :md="20" :sm="20" :xs="18">
          <div v-for="group in groupedCardData" :key="group.year" class="year-section">
            <h2 :id="`year-${group.year}`" class="year-title">
              {{ group.year }}
            </h2>

            <el-row :gutter="20">
              <el-col v-for="card in group.cards" :key="card.id" :xs="24" :sm="12" :md="8" :lg="6">
                <el-card shadow="hover" :body-style="{ padding: '0px' }" class="feature-card"
                  @click="handleCardClick(card.targetUrl)">
                  <div class="card-image-container">
                    <el-image :src="card.imageUrl" fit="cover" class="card-image" alt="功能圖片" />
                  </div>
                  <div class="card-content">
                    <h3>{{ card.title }}</h3>
                    <p>{{ card.description }}</p>
                    <p>作者：{{ card.author }}</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-col>

      </el-row>
    </el-main>
    <el-footer class="footer-text">
      <p>©2008-2025 Host by Prof. Po-Hsun Cheng(鄭伯壎) & Prof. Li-Wei Chen(陳立偉)</p>
      <p>Software Engineering and Management, National Kaohsiung Normal University, Taiwan.</p>
      <p>Information Education Center, National Kaohsiung Normal University, Taiwan.</p>
      <p>[Source] Wei-Ting Wu(吳威廷)</p>
    </el-footer>
  </el-container>

</template>

<style scoped>
.home-container {
  width: 100%;
  align-items: center;
}

.home-header {
  position: relative;
  width: 100%;
  padding: 0;
  margin-bottom: 24px;
  display: flex;
}

.home-header-button-container {
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
  z-index: 999;
}

.home-header-button-container h1 {
  color: white;
  font-size: 40px;
  margin-right: auto;
  font-weight: bold;
}

.home-header-button-container h1 span {
  color: orange;
  font-weight: bold;
}

.home-avatar {
  margin-left: 20px;
}

.signOut {
  background-color: rgba(12, 12, 12, 0.164);
  color: white;
  border: 2px solid white;
}

.signOut:hover {
  color: rgb(63, 63, 63);
  background-color: white;
  border: 2px solid white;
}

.home-image {
  width: 100%;
  height: 100%;
  background-color: #c2c1c16e;
  display: block;
}

.home-text {
  position: absolute;
  text-align: center;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.home-text h2 {
  font-size: 7vmin;
  font-weight: bold;
  color: white;
  margin-bottom: 10px;
}

.home-text p {
  font-size: 4vmin;
  font-weight: bold;
  margin-bottom: 10px;
  color: orange;
}

/* 功能卡片區塊 (el-main) */
.features-section {
  max-width: 1500px;
  width: 95%;
}

@media (max-width: 768px) {
  .features-section {
    width: 100%;
  }
}

.feature-card {
  cursor: pointer;
  transition: all 0.3s ease;
  max-width: 288px;
  margin: 0 auto 20px auto;
  height: 280px;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-image-container {
  width: 100%;
  height: 162px;
  display: flex;
  align-items: center;
  background-color: #fafafa;
}

.card-image {
  height: 100%;
  margin: 0 auto;
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
  margin-bottom: 6px;
  color: #606266;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  /* 超出顯示省略號 */
  max-width: 100%;
  display: block;
}

.year-section {
  margin-bottom: 30px;
}

.year-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--el-text-color-primary);
}

.fixed-anchor-container {
  height: 100%;
  top: 80px;
  display: block;
  overflow: hidden;
}

.home-anchor {
  position: fixed;
}

.footer-text {
  width: 100%;
  height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: #333;
  text-align: center;
  color: white;
  font-size: 12px;
  line-height: 1.5;
  z-index: 3;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

.el-message:deep() {
  z-index: 1000;
}
</style>