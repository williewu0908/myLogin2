<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { ElMessage, ElForm, ElFormItem, ElButton, ElInput, ElCard, ElContainer, ElHeader, ElDivider } from 'element-plus'
import type { LoginForm } from '@/types'

const isLoading = ref(false)
const authStore = useAuthStore()
const loginForm = reactive<LoginForm>({
    userName: 'Willie',
    password: 'Willie',
})

const handleLogin = async () => {
    if (!loginForm.userName || !loginForm.password) {
        ElMessage.error('請輸入帳號與密碼')
        return
    }

    isLoading.value = true

    try {
        await authStore.login(loginForm.userName, loginForm.password)
        ElMessage.success('登入成功！')
        // 成功登入後可在外層 (Login.vue) 處理跳轉
    } catch (error) {
        isLoading.value = false
        if (error instanceof Error) {
            ElMessage.error('帳號或密碼錯誤')
        } else {
            ElMessage.error('發生未知錯誤')
        }
    }
}
</script>
<template>
    <el-container class="login-container">
        <el-header style="height: 90px;">
            <h2 class="login-title">EduTools</h2>
        </el-header>
        <el-card class="login-card" shadow="hover">
            <el-form label-position="top" :model="loginForm" @submit.prevent="handleLogin">
                <el-form-item label="帳號">
                    <el-input v-model="loginForm.userName" placeholder="請輸入帳號" />
                </el-form-item>

                <el-form-item label="密碼">
                    <el-input v-model="loginForm.password" type="password" placeholder="請輸入密碼" show-password
                        clearable />
                </el-form-item>

                <el-form-item style="display: flex; align-items: center;">
                    <div class="login-button-container">
                        <el-button class="login-button" type="primary" size="large" round :loading="isLoading"
                            @click="handleLogin">
                            {{ isLoading ? '登入中...' : '登入' }}
                        </el-button>
                    </div>
                </el-form-item>
            </el-form>
            <el-divider>
                <span style="color: var(--el-text-color-regular);">快捷登入</span>
            </el-divider>
            <div class="fast-login-container">
                <el-button circle>
                    <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="16" height="16"
                        viewBox="0 0 48 48">
                        <path fill="#FFC107"
                            d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z">
                        </path>
                        <path fill="#FF3D00"
                            d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z">
                        </path>
                        <path fill="#4CAF50"
                            d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z">
                        </path>
                        <path fill="#1976D2"
                            d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z">
                        </path>
                    </svg>
                </el-button>
            </div>
        </el-card>
    </el-container>
</template>



<style scoped>
.login-container {
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-card {
    max-width: 380px;
    width: 90%;
    padding: 30px 40px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
}

.login-title {
    text-align: center;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
    font-size: 50px;
}

.login-button-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
}

.login-button {
    width: 50%;
}

.el-card:deep {
    padding: 20px 40px;
    padding-bottom: 0px;
}

.fast-login-container {
    width: 100%;
    display: flex;
    justify-content: center;
}
</style>
