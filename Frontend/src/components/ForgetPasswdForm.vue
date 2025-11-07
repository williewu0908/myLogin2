<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { ElMessage, ElForm, ElFormItem, ElButton, ElInput, ElCard, ElContainer, ElHeader } from 'element-plus'
import type { ForgetForm } from '@/types'

const isLoading = ref(false)
const authStore = useAuthStore()
const forgetForm = reactive<ForgetForm>({
    userName: '',
    Email: '',
})

const handleForget = async () => {
    if (!forgetForm.userName || !forgetForm.Email) {
        ElMessage.error('請輸入帳號與Email')
        return
    }

    isLoading.value = true

    try {
        await authStore.forget(forgetForm)
        ElMessage.success('發送成功！')
        // 成功登入後可在外層 (forget.vue) 處理跳轉
    } catch (error) {
        isLoading.value = false
        if (error instanceof Error) {
            ElMessage.error('帳號或密碼Email錯誤')
        } else {
            ElMessage.error('發生未知錯誤')
        }
    }
}
</script>
<template>
    <el-container class="forget-container">
        <el-header style="height: 90px; position: relative; top: -30px;">
            <h2 class="forget-title">忘記密碼</h2>
        </el-header>
        <el-card class="forget-card" shadow="hover">
            <el-form label-position="top" :model="forgetForm" @submit.prevent="handleForget">
                <el-form-item label="帳號">
                    <el-input v-model="forgetForm.userName" placeholder="請輸入帳號" />
                </el-form-item>

                <el-form-item label="Email">
                    <el-input v-model="forgetForm.Email" type="email" placeholder="請輸入Email"
                        clearable />
                </el-form-item>

                <el-form-item style="display: flex; align-items: center;">
                    <div class="forget-button-container">
                        <el-button class="forget-button" type="primary" size="large" round :loading="isLoading"
                            @click="handleForget">
                            {{ isLoading ? '發送中...' : '發送重設郵件' }}
                        </el-button>
                    </div>
                </el-form-item>
            </el-form>
        </el-card>
    </el-container>
</template>



<style scoped>
.forget-container {
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.forget-card {
    max-width: 400px;
    width: 90%;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
    position: relative;
    top: -30px;
}

.forget-title {
    text-align: center;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
    font-size: 50px;
}

.forget-button-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 5px 0 10px 0;

}

.forget-button {
    width: 50%;
}

.el-card:deep {
    padding: 20px 50px;
    padding-bottom: 0px;
}
</style>
