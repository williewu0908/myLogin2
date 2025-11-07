<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore'
import { ElMessage, ElForm, ElFormItem, ElButton, ElInput, ElCard, ElContainer, ElHeader } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import type { ResetForm } from '@/types'

const route = useRoute();

const isLoading = ref(false)
const authStore = useAuthStore()
const resetForm = reactive<ResetForm>({
    token: '',
    password: '',
    confirmPassword: '',
})
const isValidToken = ref(false);

const resetFormRef = ref<FormInstance>()
const rules = reactive<FormRules<ResetForm>>({
    password: [{ required: true, message: '請設定密碼', trigger: 'blur' }],
    confirmPassword: [{ required: true, message: '請再次輸入密碼', trigger: 'blur' }],
})

onMounted(() => {
    const tokenFromQuery = route.query.token;
    // 檢查 token 是否存在，且是否為單一字串
    if (tokenFromQuery && typeof tokenFromQuery === 'string') {
        resetForm.token = tokenFromQuery;
        isValidToken.value = true;
    } else {
        // Token 不存在或格式錯誤
        isValidToken.value = false;
        ElMessage.error('重設連結無效或已過期。');
    }
});

const handleReset = async () => {
    if (!resetFormRef.value) return

    await resetFormRef.value.validate(async (valid) => {
        if (!valid) {
            ElMessage.error('請確認所有欄位皆正確填寫');
            return
        }

        if (resetForm.password !== resetForm.confirmPassword) {
            ElMessage.error('兩次輸入的密碼不一致！')
            return
        }

        isLoading.value = true
        try {
            await authStore.reset(resetForm)
            ElMessage.success('重設成功！')
        } catch (error: any) {
            if (error.response && error.response.data && error.response.data.msg) {
                ElMessage.error(error.response.data.msg);
            } else {
                ElMessage.error('重設失敗，Token 無效或已過期。');
            }
        } finally {
            isLoading.value = false
        }
    })
}
</script>
<template>
    <el-container class="reset-container" v-if="isValidToken">
        <el-header style="height: 90px; position: relative; top: -30px;">
            <h2 class="reset-title">重設密碼</h2>
        </el-header>
        <el-card class="reset-card" shadow="hover">
            <el-form label-position="top" :model="resetForm" @submit.prevent="handleReset" :rules="rules"
                ref="resetFormRef">
                <el-form-item label="密碼" prop="password">
                    <el-input v-model="resetForm.password" type="password" placeholder="請輸入密碼" show-password
                        clearable />
                </el-form-item>
                <el-form-item label="確認密碼" prop="confirmPassword">
                    <el-input v-model="resetForm.confirmPassword" type="password" placeholder="請再次輸入密碼" show-password
                        clearable />
                </el-form-item>

                <el-form-item style="display: flex; align-items: center;">
                    <div class="reset-button-container">
                        <el-button class="reset-button" type="primary" size="large" round :loading="isLoading"
                            @click="handleReset">
                            {{ isLoading ? '重設中...' : '重設' }}
                        </el-button>
                    </div>
                </el-form-item>
            </el-form>
        </el-card>
    </el-container>
    <el-container class="reset-container" v-else>
        <el-header style="height: 90px; position: relative; top: -30px;">
            <h2 class="reset-title">重設密碼</h2>
        </el-header>
        <el-card class="reset-card" shadow="hover">
            <p>重設連結無效或已過期。</p>
        </el-card>
    </el-container>
</template>



<style scoped>
.reset-container {
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.reset-card {
    max-width: 400px;
    width: 90%;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
    position: relative;
    top: -30px;
}

.reset-title {
    text-align: center;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
    font-size: 50px;
}

.reset-button-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 5px 0 10px 0;

}

.reset-button {
    width: 50%;
}

.el-card:deep {
    padding: 20px 50px;
    padding-bottom: 0px;
}
</style>
