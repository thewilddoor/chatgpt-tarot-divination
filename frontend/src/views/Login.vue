<script setup>
import { NButton } from 'naive-ui'
import { useRouter } from 'vue-router'

const router = useRouter();
</script>

<template>
    <div class="login-container">
        <div class="login-content">
            <h2>占卜系统</h2>
            <p>欢迎使用塔罗牌、梅花易数等占卜功能</p>
            <n-button type="primary" size="large" @click="router.push('/')">
                进入应用
            </n-button>
        </div>
    </div>
</template>

<style scoped>
.side {
    height: 100vh;
}

.main {
    height: 100vh;
    text-align: center;
}

.n-grid {
    height: 100%;
}

.n-gi {
    height: 100%;
}

.n-space {
    height: 100%;
}

.n-alert {
    text-align: center;
}

.button-container {
    display: flex;
    justify-content: center;
}

.n-button {
    margin-top: 12px;
    text-align: center;
    margin-bottom: 12px;
}

.result {
    text-align: left;
}
</style>
