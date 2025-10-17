<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { ElMessage, ElForm, ElFormItem, ElButton, ElInput, ElCard, ElContainer, ElHeader } from 'element-plus'

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const isLoading = ref(false)
const authStore = useAuthStore()

const handleLogin = async () => {
    if (!username.value || !password.value) {
        errorMsg.value = '請輸入帳號與密碼。'
        return
    }

    isLoading.value = true
    errorMsg.value = ''

    try {
        await authStore.login(username.value, password.value)
        ElMessage.success('登入成功！')
        // 成功登入後可在外層 (Login.vue) 處理跳轉
    } catch (error) {
        isLoading.value = false
        if (error instanceof Error) {
            errorMsg.value = '帳號或密碼錯誤。'
        } else {
            errorMsg.value = '發生未知錯誤。'
        }
    }
}
</script>
<template>
    <el-container class="login-container">
        <el-header class="login-title">登入系統</el-header>
        <el-card class="login-card" shadow="hover">
            <el-form ref="formRef" label-position="top" :model="{ username, password }" @submit.prevent="handleLogin">
                <el-form-item label="帳號">
                    <el-input v-model="username" placeholder="請輸入帳號" />
                </el-form-item>

                <el-form-item label="密碼">
                    <el-input v-model="password" type="password" placeholder="請輸入密碼" prefix-icon="Lock" show-password
                        clearable />
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" round style="width: 100%" :loading="isLoading" @click="handleLogin">
                        {{ isLoading ? '登入中...' : '登入' }}
                    </el-button>
                </el-form-item>
                <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
            </el-form>
        </el-card>
    </el-container>
</template>



<style scoped>
.error-msg {
    color: #f56c6c;
    text-align: center;
    font-size: 14px;
    margin-top: -10px;
}
.login-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f56c6c;
}

.login-card {
  width: 380px;
  padding: 30px 40px;
  border-radius: 18px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
  background-color: #333;
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 600;
  color: #333;
  letter-spacing: 1px;
  font-size: 50px;
}
</style>
