<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 60 60'%3E%3Crect width='60' height='60' fill='%23FB7299'/%3E%3Ctext x='30' y='35' text-anchor='middle' fill='white' font-size='12'%3ELogo%3C/text%3E%3C/svg%3E" alt="Logo" class="logo" />
        <h1>DataBili</h1>
        <p>登录到您的大数据分析平台</p>
      </div>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="form.email" 
            required 
            placeholder="请输入您的邮箱"
          />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="form.password" 
            required 
            placeholder="请输入您的密码"
          />
        </div>
        <div class="form-options">
          <label class="checkbox-label">
            <input type="checkbox" v-model="form.remember" />
            <span>记住我</span>
          </label>
          <a href="#" class="forgot-password">忘记密码？</a>
        </div>
        <button type="submit" class="login-button" :disabled="isLoading">
          <span v-if="isLoading">登录中...</span>
          <span v-else>登录</span>
        </button>
      </form>
      <div class="login-footer">
        <p>还没有账户？ <a href="#" @click="showRegister = true">立即注册</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAppStore } from '../store';

const router = useRouter();
const appStore = useAppStore();

const form = ref({
  email: '',
  password: '',
  remember: false
});

const isLoading = ref(false);
const showRegister = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  
  try {
    // 模拟登录API调用
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 设置用户信息
    appStore.setUser({
      id: 1,
      name: '张三',
      email: form.value.email,
      avatar: '/placeholder.svg?height=40&width=40'
    });
    
    // 跳转到仪表盘
    router.push('/');
  } catch (error) {
    console.error('Login failed:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  padding: 1rem;
}

.login-card {
  background-color: var(--card);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  width: 60px;
  height: 60px;
  margin-bottom: 1rem;
}

.login-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.login-header p {
  color: var(--muted-foreground);
  font-size: 0.875rem;
}

.login-form {
  space-y: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--foreground);
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background-color: var(--background);
  color: var(--foreground);
  font-size: 0.875rem;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(251, 114, 153, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--foreground);
}

.checkbox-label input {
  width: auto;
}

.forgot-password {
  font-size: 0.875rem;
  color: var(--primary);
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover:not(:disabled) {
  background-color: #e91e63;
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}

.login-footer p {
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

.login-footer a {
  color: var(--primary);
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>
