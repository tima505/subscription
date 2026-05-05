<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight transition-colors">Дашборд</h1>
      <p class="text-sm md:text-base text-gray-500 dark:text-gray-400 mt-1 md:mt-2 transition-colors">С возвращением, {{ authStore.user?.first_name || authStore.user?.username }}</p>
    </div>

    <!-- Client View -->
    <div v-if="authStore.role === 'client'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="sub in clientSubscriptions" :key="sub.id" class="bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow relative overflow-hidden group">
        <div class="absolute top-0 right-0 w-24 h-24 bg-blue-50 dark:bg-blue-900/20 rounded-bl-full -z-10 group-hover:scale-110 transition-transform"></div>
        <div class="flex items-center justify-between mb-4">
          <div class="p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-2xl">
            <CreditCardIcon class="w-6 h-6" />
          </div>
          <span v-if="sub.days_left <= 3 && sub.days_left > 0" class="px-3 py-1 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 text-xs font-bold rounded-full animate-pulse">Скоро истекает</span>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ sub.subscription_details?.name }}</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ sub.subscription_details?.business_name || 'Название компании' }}</p>
        
        <div class="mt-6 space-y-4">
          <div>
            <div class="flex justify-between text-sm mb-1">
              <span class="font-medium text-gray-700 dark:text-gray-300">Осталось дней</span>
              <span class="font-bold text-gray-900 dark:text-gray-100">{{ sub.days_left }} дней</span>
            </div>
            <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
              <div class="bg-blue-500 h-2 rounded-full" :style="`width: ${Math.min(100, (sub.days_left / sub.subscription_details?.duration_days) * 100)}%`"></div>
            </div>
          </div>
          
          <div v-if="sub.remaining_visits !== null">
            <div class="flex justify-between text-sm mb-1">
              <span class="font-medium text-gray-700 dark:text-gray-300">Осталось посещений</span>
              <span class="font-bold text-gray-900 dark:text-gray-100">{{ sub.remaining_visits }}</span>
            </div>
            <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
              <div class="bg-indigo-500 h-2 rounded-full" :style="`width: ${Math.min(100, (sub.remaining_visits / sub.subscription_details?.visit_limit) * 100)}%`"></div>
            </div>
          </div>
          <div v-else class="text-sm font-medium text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-3 py-2 rounded-lg inline-block border border-transparent dark:border-green-900/30">
            Безлимитно
          </div>
        </div>
      </div>
      
      <div v-if="clientSubscriptions.length === 0" class="col-span-full flex flex-col items-center justify-center p-12 bg-white dark:bg-gray-800 rounded-3xl border border-dashed border-gray-300 dark:border-gray-700">
        <CreditCardIcon class="w-12 h-12 text-gray-400 dark:text-gray-500 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Нет активных абонементов</h3>
        <p class="text-gray-500 dark:text-gray-400 mt-1 text-center max-w-sm">У вас пока нет активных абонементов. Приобретите один в филиале, чтобы начать работу.</p>
      </div>
    </div>

    <!-- Admin/Manager View -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 flex items-center transition-colors">
        <div class="p-4 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-2xl mr-4">
          <UsersIcon class="w-8 h-8" />
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Всего клиентов</p>
          <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ clients.length }}</p>
        </div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 flex items-center transition-colors">
        <div class="p-4 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-2xl mr-4">
          <ActivityIcon class="w-8 h-8" />
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Посещений (Сегодня)</p>
          <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ visits.length }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { CreditCardIcon, UsersIcon, ActivityIcon } from 'lucide-vue-next'

const authStore = useAuthStore()
const clientSubscriptions = ref([])
const clients = ref([])
const visits = ref([])

onMounted(async () => {
  if (authStore.role === 'client') {
    const res = await axios.get('http://localhost:8000/api/client-subscriptions/')
    clientSubscriptions.value = res.data
  } else {
    const clientsRes = await axios.get('http://localhost:8000/api/users/clients/')
    clients.value = clientsRes.data
    const visitsRes = await axios.get('http://localhost:8000/api/visits/')
    visits.value = visitsRes.data
  }
})
</script>
