<script setup lang="ts">
import LoginForm from '@/components/LoginForm.vue'
import { ElButton } from 'element-plus';
import { useRouter } from 'vue-router';

const router = useRouter();
const handleNavigateToSignUp = () => {
    router.push({name: 'SignUp'});
};

const handleNavigateToForgetPassword = () => {
    router.push({name: 'ForgetPassword'});
};
</script>

<template>
      <div class="login-page">
            <div class="background"></div>
            <div class="button-container">
                  <el-button class="signUp" size="large" round text @click="handleNavigateToForgetPassword">
                        忘記密碼？
                  </el-button>
                  <el-button class="signUp" size="large" round plain @click="handleNavigateToSignUp">
                        註冊
                  </el-button>
            </div>
            <div class="form-wrapper">
                  <LoginForm />
            </div>
            <!-- 版權資訊 -->
            <footer class="footer-text">
                  <p>©2008-2025 Host by Prof. Po-Hsun Cheng(鄭伯壎) & Prof. Li-Wei Chen(陳立偉)</p>
                  <p>Software Engineering & Management, NKNU, Taiwan</p>
                  <p>Information Education Center, NKNU, Taiwan</p>
                  <p>[Source] Wei-Ting Wu(吳威廷)</p>
            </footer>
      </div>
</template>

<style scoped>
.login-page {
      position: relative;
      width: 100%;
      overflow: hidden;
}

.background {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100vh;
      background-image: url('@/assets/bg-index.jpg');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      filter: brightness(0.8);
      z-index: 0;
}

/* 顏色蒙版 */
.background::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: -webkit-linear-gradient(left, rgba(0, 168, 255, 0.5), rgba(185, 0, 255, 0.5));
      z-index: 1;
}

/* 表單置中 */
.form-wrapper {
      position: relative;
      z-index: 1;
}

.button-container {
      position: absolute;
      top: 2%;
      right: 5%;
      z-index: 2;
}

.signUp {
      background-color: transparent;
      color: white;
}

.signUp.is-text {
      color: white;
}

.signUp:hover {
      color: purple;
      background-color: white;
      border: transparent;
}
.footer-text {
  position: absolute;
  bottom: 20px;
  width: 100%;
  text-align: center;
  color: white;
  font-size: 10px;
  line-height: 1.4;
  z-index: 3;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}
</style>
