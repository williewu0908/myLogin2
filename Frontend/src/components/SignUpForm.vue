<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { ElMessage, ElForm, ElFormItem, ElButton, ElInput, ElCard, ElContainer, ElHeader, ElDivider } from 'element-plus'
import type { SignUpForm } from '@/types'

const isLoading = ref(false)
const authStore = useAuthStore()
const signUpForm = reactive<SignUpForm>({
    userName: '',
    userTrueName: '',
    email: '',
    password: '',
    confirmPassword: '',
})

const handleSignUp = async () => {
}
</script>
<template>
    <el-container class="signup-container">
        <el-header style="height: 90px; position: relative; top: -20px;">
            <h2 class="signup-title">註冊</h2>
        </el-header>
        <el-card class="signup-card" shadow="hover">
            <el-form label-position="top" :model="signUpForm" @submit.prevent="handleSignUp">
                <el-form-item label="名字">
                    <el-input v-model="signUpForm.userTrueName" placeholder="請輸入名字" />
                </el-form-item>
                <el-form-item label="帳號">
                    <el-input v-model="signUpForm.userName" placeholder="請輸入帳號" />
                </el-form-item>
                <el-form-item label="密碼">
                    <el-input v-model="signUpForm.password" type="password" placeholder="請輸入密碼" show-password
                        clearable />
                </el-form-item>
                <el-form-item label="確認密碼">
                    <el-input v-model="signUpForm.confirmPassword" type="password" placeholder="請再次輸入密碼" show-password
                        clearable />
                </el-form-item>
                <el-form-item style="display: flex; align-items: center;">
                    <div class="signup-button-container">
                        <el-button class="signup-button" type="primary" size="large" round :loading="isLoading"
                            @click="handleSignUp">
                            {{ isLoading ? '註冊中...' : '註冊' }}
                        </el-button>
                    </div>
                </el-form-item>
            </el-form>
        </el-card>
    </el-container>
</template>



<style scoped>
.signup-container {
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.signup-card {
    max-width: 450px;
    width: 90%;
    padding: 30px 40px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
    position: relative;
    top: -20px;
}

.signup-title {
    text-align: center;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
    font-size: 50px;
}

.signup-button-container {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 10px;
    position: relative;
}

.signup-button {
    width: 35%;
    position: relative;
    top: 10px;
}

.el-card:deep {
    padding: 10px 50px;
    padding-bottom: 0px;
}
</style>
