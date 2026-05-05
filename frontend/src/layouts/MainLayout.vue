<template>
  <div class="flex h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 font-sans transition-colors duration-300 overflow-hidden">
    <!-- Mobile Sidebar Backdrop -->
    <div v-if="isMobileMenuOpen" @click="isMobileMenuOpen = false" class="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-40 md:hidden transition-opacity"></div>
    
    <!-- Sidebar -->
    <aside :class="isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'" class="fixed md:relative z-50 w-64 h-full bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-transform duration-300">
      <div class="h-16 flex items-center px-6 border-b border-gray-100 dark:border-gray-700">
        <span class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">SubSaaS</span>
      </div>
      <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <router-link to="/" class="flex items-center px-4 py-3 rounded-xl hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" active-class="bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-400 font-semibold shadow-sm">
          <HomeIcon class="w-5 h-5 mr-3" /> Главная
        </router-link>
        <router-link v-if="authStore.role === 'admin'" to="/businesses" class="flex items-center px-4 py-3 rounded-xl hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" active-class="bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-400 font-semibold shadow-sm">
          <BriefcaseIcon class="w-5 h-5 mr-3" /> Компании
        </router-link>
        <router-link v-if="authStore.role === 'admin' || authStore.role === 'manager'" to="/subscriptions" class="flex items-center px-4 py-3 rounded-xl hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" active-class="bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-400 font-semibold shadow-sm">
          <CreditCardIcon class="w-5 h-5 mr-3" /> Абонементы
        </router-link>
        <router-link v-if="authStore.role === 'admin' || authStore.role === 'manager'" to="/clients" class="flex items-center px-4 py-3 rounded-xl hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" active-class="bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-400 font-semibold shadow-sm">
          <UsersIcon class="w-5 h-5 mr-3" /> Клиенты
        </router-link>
        <router-link to="/bookings" class="flex items-center px-4 py-3 rounded-xl hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" active-class="bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-400 font-semibold shadow-sm">
          <CalendarIcon class="w-5 h-5 mr-3" /> Записи
        </router-link>
        <router-link to="/profile" class="flex items-center px-4 py-3 rounded-xl hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" active-class="bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-400 font-semibold shadow-sm">
          <UserIcon class="w-5 h-5 mr-3" /> Профиль
        </router-link>
      </nav>
      <div class="p-4 border-t border-gray-100 dark:border-gray-700">
        <button @click="logout" class="flex items-center w-full px-4 py-3 text-red-500 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-colors font-medium">
          <LogOutIcon class="w-5 h-5 mr-3" /> Выйти
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6 z-10 shadow-sm backdrop-blur-md bg-white/80 dark:bg-gray-800/80 transition-colors duration-300">
        <div class="flex items-center md:hidden">
          <button @click="isMobileMenuOpen = true" class="mr-3 p-2 -ml-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700 transition-colors">
            <MenuIcon class="w-6 h-6" />
          </button>
          <span class="text-xl font-bold text-blue-600 dark:text-blue-400">SubSaaS</span>
        </div>
        <div class="flex items-center space-x-4 ml-auto">
          <button @click="toggleTheme" class="p-2 rounded-full text-gray-500 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-700 transition-colors">
            <SunIcon v-if="isDark" class="w-5 h-5" />
            <MoonIcon v-else class="w-5 h-5" />
          </button>
          
          <div class="flex flex-col text-right hidden sm:flex">
            <span class="text-sm font-semibold text-gray-800 dark:text-gray-200">{{ authStore.user?.first_name }} {{ authStore.user?.last_name }}</span>
            <span class="text-xs text-gray-500 dark:text-gray-400 capitalize">{{ authStore.role }}</span>
          </div>
          <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold shadow-md ring-2 ring-white dark:ring-gray-800 cursor-pointer hover:scale-105 transition-transform">
            {{ authStore.user?.username.charAt(0).toUpperCase() }}
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <div class="flex-1 overflow-y-auto p-6 md:p-8 bg-[#f8fafc] dark:bg-[#0f172a] transition-colors duration-300">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRoute, useRouter } from 'vue-router'
import { HomeIcon, BriefcaseIcon, CreditCardIcon, UsersIcon, CalendarIcon, UserIcon, LogOutIcon, MoonIcon, SunIcon, MenuIcon } from 'lucide-vue-next'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const isDark = ref(false)
const isMobileMenuOpen = ref(false)

// Close mobile menu on route change
watch(route, () => {
  isMobileMenuOpen.value = false
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  // Check local storage or system preference
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
