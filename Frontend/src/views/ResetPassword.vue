<script setup lang="ts">
import ResetPasswdForm from '@/components/ResetPasswdForm.vue'

</script>

<template>
      <div class="login-page">
            <div class="background"></div>
            <div class="form-wrapper">
                  <ResetPasswdForm />
            </div>
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
