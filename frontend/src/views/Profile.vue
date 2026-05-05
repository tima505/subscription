<template>
  <div class="max-w-3xl mx-auto space-y-8">
    <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight transition-colors">Профиль</h1>
    
    <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden transition-colors">
      <div class="p-8 border-b border-gray-100 dark:border-gray-700 flex items-center transition-colors">
        <div class="w-20 h-20 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center text-white text-3xl font-bold shadow-lg ring-4 ring-blue-50 dark:ring-blue-900/20 mr-6">
          {{ authStore.user?.username.charAt(0).toUpperCase() }}
        </div>
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ authStore.user?.first_name }} {{ authStore.user?.last_name || 'Администратор' }}</h2>
          <p class="text-gray-500 dark:text-gray-400">@{{ authStore.user?.username }}</p>
          <span class="inline-block mt-2 px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 text-xs font-bold rounded-full uppercase tracking-wide">{{ authStore.role }}</span>
        </div>
      </div>
      <div class="p-8 space-y-6">
        <div>
          <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">Контактная информация</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-2xl border border-gray-100 dark:border-gray-700 transition-colors">
              <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Email</p>
              <p class="font-medium text-gray-900 dark:text-gray-100">{{ authStore.user?.email || 'Не указан' }}</p>
            </div>
            <div class="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-2xl border border-gray-100 dark:border-gray-700 transition-colors">
              <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Телефон</p>
              <p class="font-medium text-gray-900 dark:text-gray-100">{{ authStore.user?.phone || 'Не указан' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>
