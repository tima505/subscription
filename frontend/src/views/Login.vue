<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
    <div class="max-w-md w-full bg-white rounded-3xl shadow-xl p-8 relative overflow-hidden transform transition-all hover:scale-[1.01]">
      <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-500 to-indigo-500"></div>
      
      <div class="text-center mb-8">
        <h1 class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">SubSaaS</h1>
        <p class="text-gray-500 mt-2 text-sm">Войдите для управления абонементами</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя пользователя (Логин)</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <UserIcon class="h-5 w-5 text-gray-400" />
            </div>
            <input v-model="username" type="text" class="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-xl leading-5 bg-gray-50 placeholder-gray-400 focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors" placeholder="Введите логин" required />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <LockIcon class="h-5 w-5 text-gray-400" />
            </div>
            <input v-model="password" type="password" class="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-xl leading-5 bg-gray-50 placeholder-gray-400 focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors" placeholder="Введите пароль" required />
          </div>
        </div>
        
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input id="remember-me" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
            <label for="remember-me" class="ml-2 block text-sm text-gray-700">Запомнить меня</label>
          </div>
          <div class="text-sm">
            <a href="#" class="font-medium text-blue-600 hover:text-blue-500">Забыли пароль?</a>
          </div>
        </div>
        
        <button type="submit" :disabled="loading" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-md text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-all transform active:scale-95">
          <span v-if="!loading">Войти</span>
          <LoaderIcon v-else class="h-5 w-5 animate-spin" />
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { UserIcon, LockIcon, LoaderIcon } from 'lucide-vue-next'

const username = ref('')
const password = ref('')
const loading = ref(false)
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  loading.value = true
  const success = await authStore.login(username.value, password.value)
  loading.value = false
  if (success) {
    router.push('/')
  } else {
    alert('Ошибка входа. Проверьте логин и пароль.')
  }
}
</script>
