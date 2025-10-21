<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { ElMessage, ElForm, ElFormItem, ElButton, ElInput, ElCard, ElContainer, ElHeader } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import type { SignUpForm } from '@/types'

const isLoading = ref(false)
const authStore = useAuthStore()
const signUpFormRef = ref<FormInstance>()
const signUpForm = reactive<SignUpForm>({
    userName: '',
    userTrueName: '',
    email: '',
    password: '',
    confirmPassword: '',
})

const rules = reactive<FormRules<SignUpForm>>({
    userName: [{ required: true, message: '請輸入帳號名稱', trigger: 'blur' }],
    userTrueName: [{ required: true, message: '請輸入你的名字', trigger: 'blur' }],
    email: [
        { required: true, message: '請輸入電子郵件', trigger: 'blur' },
        { type: 'email', message: '請輸入正確的電子郵件格式', trigger: ['blur', 'change'] },
    ],
    password: [{ required: true, message: '請設定密碼', trigger: 'blur' }],
    confirmPassword: [{ required: true, message: '請再次輸入密碼', trigger: 'blur' }],
})

const handleSignUp = async () => {
    if (!signUpFormRef.value) return

    await signUpFormRef.value.validate(async (valid) => {
        if (!valid) {
            ElMessage.error('請確認所有欄位皆正確填寫');
            return
        }

        if (signUpForm.password !== signUpForm.confirmPassword) {
            ElMessage.error('兩次輸入的密碼不一致！')
            return
        }

        isLoading.value = true
        try {
            await authStore.register(signUpForm)
            ElMessage.success('註冊成功！將跳轉至登入頁面。')
            // TODO: 這裡可以加 router.push('/login')
        } catch (error: any) {
            if (error.response?.data?.msg) {
                ElMessage.error(error.response.data.msg)
            } else {
                ElMessage.error('註冊失敗，請稍後再試。')
            }
        } finally {
            isLoading.value = false
        }
    })
}

</script>
<template>
    <el-container class="signup-container">
        <el-header style="height: 80px; position: relative; top: -30px;">
            <h2 class="signup-title">註冊</h2>
        </el-header>

        <el-card class="signup-card" shadow="hover">
            <el-form label-position="top" :model="signUpForm" :rules="rules" ref="signUpFormRef"
                @submit.prevent="handleSignUp" hide-required-asterisk>
                <el-form-item label="帳號" prop="userName">
                    <el-input v-model="signUpForm.userName" placeholder="請輸入帳號" />
                </el-form-item>
                <el-form-item label="名字" prop="userTrueName">
                    <el-input v-model="signUpForm.userTrueName" placeholder="請輸入名字" />
                </el-form-item>
                <el-form-item label="電子郵件" prop="email">
                    <el-input v-model="signUpForm.email" placeholder="請輸入電子郵件" />
                </el-form-item>
                <el-form-item label="密碼" prop="password">
                    <el-input v-model="signUpForm.password" type="password" placeholder="請輸入密碼" show-password
                        clearable />
                </el-form-item>
                <el-form-item label="確認密碼" prop="confirmPassword">
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
    top: -30px;
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
