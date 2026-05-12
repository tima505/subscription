<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight transition-colors">Клиенты и Персонал</h1>
        <p class="text-sm md:text-base text-gray-500 dark:text-gray-400 mt-1 md:mt-2 transition-colors">Управление пользователями системы</p>
      </div>
      <button v-if="authStore.role === 'admin'" @click="showAddUserModal = true" class="w-full md:w-auto flex justify-center items-center px-5 py-2.5 bg-blue-600 dark:bg-blue-500 text-white font-medium rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors shadow-sm">
        <PlusIcon class="w-5 h-5 mr-2" /> Добавить пользователя
      </button>
    </div>

    <!-- Search -->
    <div class="relative">
      <SearchIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 dark:text-gray-500" />
      <input v-model="searchQuery" type="text" placeholder="Поиск по имени, логину или телефону..." class="w-full pl-12 pr-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 outline-none transition-colors text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500" />
    </div>

    <!-- Mobile card layout -->
    <div class="space-y-3 md:hidden">
      <div v-if="filteredClients.length === 0" class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-12 text-center transition-colors">
        <p class="text-gray-500 dark:text-gray-400">Клиенты не найдены</p>
      </div>
      <div v-for="client in filteredClients" :key="client.id" class="bg-white dark:bg-gray-800 rounded-2xl p-4 shadow-sm border border-gray-100 dark:border-gray-700 transition-colors">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold shrink-0 text-sm">
            {{ client.username.charAt(0).toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-bold text-gray-900 dark:text-gray-100 text-sm truncate">{{ client.first_name }} {{ client.last_name }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">@{{ client.username }}</p>
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-2 mb-3">
          <span v-if="client.phone" class="text-xs text-gray-500 dark:text-gray-400">📞 {{ client.phone }}</span>
          <span v-else class="text-xs text-gray-400 dark:text-gray-500">📞 Нет</span>
          <span class="text-gray-300 dark:text-gray-600">•</span>
          <span v-if="clientSubsMap[client.id]?.length" class="px-2.5 py-0.5 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 text-xs font-bold rounded-full">
            {{ clientSubsMap[client.id].length }} абон.
          </span>
          <span v-else class="px-2.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-xs font-bold rounded-full">Нет абон.</span>
        </div>
        <div class="flex items-center justify-between pt-3 border-t border-gray-100 dark:border-gray-700">
          <span v-if="clientSubsMap[client.id]?.length" class="px-2.5 py-0.5 bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-400 text-xs font-bold rounded-full">Активен</span>
          <span v-else class="px-2.5 py-0.5 bg-yellow-100 dark:bg-yellow-900/40 text-yellow-700 dark:text-yellow-500 text-xs font-bold rounded-full">Без абонемента</span>
          <button @click="openClient(client)" class="px-4 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/40 font-medium text-sm rounded-xl transition-colors">
            Управлять
          </button>
        </div>
      </div>
    </div>

    <!-- Desktop table layout -->
    <div class="hidden md:block bg-white dark:bg-gray-800 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden transition-colors w-full">
      <div class="overflow-x-auto w-full">
        <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 dark:bg-gray-900/50 text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider transition-colors">
            <th class="p-4 font-semibold">Пользователь</th>
            <th class="p-4 font-semibold">Телефон</th>
            <th class="p-4 font-semibold">Абонемент</th>
            <th class="p-4 font-semibold">Статус</th>
            <th class="p-4 font-semibold text-right">Действия</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
          <tr v-for="client in filteredClients" :key="client.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
            <td class="p-4">
              <div class="flex items-center">
                <div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold mr-3">
                  {{ client.username.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <p class="font-bold text-gray-900 dark:text-gray-100">{{ client.first_name }} {{ client.last_name }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">@{{ client.username }}</p>
                </div>
              </div>
            </td>
            <td class="p-4 text-sm text-gray-600 dark:text-gray-300">{{ client.phone || 'Нет' }}</td>
            <td class="p-4">
              <span v-if="clientSubsMap[client.id]?.length" class="px-3 py-1 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 text-xs font-bold rounded-full border border-blue-200 dark:border-blue-800">
                {{ clientSubsMap[client.id].length }} шт.
              </span>
              <span v-else class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-xs font-bold rounded-full">Нет</span>
            </td>
            <td class="p-4">
              <span v-if="clientSubsMap[client.id]?.length" class="px-3 py-1 bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-400 text-xs font-bold rounded-full border border-green-200 dark:border-green-800">Активен</span>
              <span v-else class="px-3 py-1 bg-yellow-100 dark:bg-yellow-900/40 text-yellow-700 dark:text-yellow-500 text-xs font-bold rounded-full border border-yellow-200 dark:border-yellow-800/50">Без абонемента</span>
            </td>
            <td class="p-4 text-right">
              <button @click="openClient(client)" class="px-4 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/40 font-medium text-sm rounded-xl transition-colors">
                Управлять
              </button>
            </td>
          </tr>
          <tr v-if="filteredClients.length === 0">
            <td colspan="5" class="p-12 text-center text-gray-500 dark:text-gray-400">Клиенты не найдены</td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>

    <!-- Client Detail Modal -->
    <div v-if="selectedClient" class="fixed inset-0 bg-gray-900/50 dark:bg-gray-900/80 backdrop-blur-sm flex justify-center items-center z-50 p-3 md:p-4">
      <div class="bg-white dark:bg-gray-800 rounded-2xl md:rounded-3xl p-5 md:p-8 max-w-3xl w-full shadow-2xl transform transition-all max-h-[90vh] overflow-y-auto border border-transparent dark:border-gray-700">
        <!-- Header -->
        <div class="flex justify-between items-start mb-6 md:mb-8">
          <div class="flex items-center min-w-0">
            <div class="w-12 h-12 md:w-16 md:h-16 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-500 dark:from-blue-600 dark:to-indigo-600 flex items-center justify-center text-white text-xl md:text-2xl font-bold mr-3 md:mr-4 shadow-lg shrink-0">
              {{ selectedClient.username.charAt(0).toUpperCase() }}
            </div>
            <div class="min-w-0">
              <h2 class="text-lg md:text-2xl font-bold text-gray-900 dark:text-white truncate">{{ selectedClient.first_name }} {{ selectedClient.last_name }}</h2>
              <p class="text-sm text-gray-500 dark:text-gray-400">@{{ selectedClient.username }}</p>
              <div class="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1 text-xs md:text-sm text-gray-500 dark:text-gray-400">
                <span v-if="selectedClient.phone" class="flex items-center"><PhoneIcon class="w-3.5 h-3.5 mr-1" /> {{ selectedClient.phone }}</span>
                <span v-if="selectedClient.email" class="flex items-center"><MailIcon class="w-3.5 h-3.5 mr-1" /> {{ selectedClient.email }}</span>
              </div>
            </div>
          </div>
          <button @click="selectedClient = null" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-1 shrink-0 ml-2"><XIcon class="w-6 h-6" /></button>
        </div>

        <!-- Stats cards -->
        <div class="grid grid-cols-3 gap-2 md:gap-4 mb-6 md:mb-8">
          <div class="bg-blue-50 dark:bg-blue-900/20 rounded-xl md:rounded-2xl p-3 md:p-4 text-center border border-transparent dark:border-blue-900/30">
            <p class="text-xl md:text-2xl font-bold text-blue-600 dark:text-blue-400">{{ clientSubs.length }}</p>
            <p class="text-[10px] md:text-xs font-medium text-blue-500 dark:text-blue-400 mt-1">Абонементов</p>
          </div>
          <div class="bg-green-50 dark:bg-green-900/20 rounded-xl md:rounded-2xl p-3 md:p-4 text-center border border-transparent dark:border-green-900/30">
            <p class="text-xl md:text-2xl font-bold text-green-600 dark:text-green-400">{{ totalVisitsLeft }}</p>
            <p class="text-[10px] md:text-xs font-medium text-green-500 dark:text-green-400 mt-1">Посещений осталось</p>
          </div>
          <div class="bg-indigo-50 dark:bg-indigo-900/20 rounded-xl md:rounded-2xl p-3 md:p-4 text-center border border-transparent dark:border-indigo-900/30">
            <p class="text-xl md:text-2xl font-bold text-indigo-600 dark:text-indigo-400">{{ clientVisits.length }}</p>
            <p class="text-[10px] md:text-xs font-medium text-indigo-500 dark:text-indigo-400 mt-1">Всего визитов</p>
          </div>
        </div>
        
        <!-- Active Subscriptions -->
        <h3 class="text-lg font-semibold mb-4 flex items-center text-gray-900 dark:text-gray-100">
          <CreditCardIcon class="w-5 h-5 mr-2 text-blue-500 dark:text-blue-400" /> Активные абонементы
        </h3>
        <div class="space-y-4 mb-8">
          <div v-for="sub in clientSubs" :key="sub.id" class="p-5 border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 rounded-2xl hover:border-blue-200 dark:hover:border-blue-500 transition-colors">
            <div class="flex justify-between items-start mb-3">
              <div>
                <p class="font-bold text-gray-900 dark:text-white text-lg">{{ sub.subscription_details?.name }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ sub.subscription_details?.business_name || 'Компания' }}</p>
              </div>
              <button @click="deductVisit(sub.id)" class="px-4 py-2 bg-indigo-600 dark:bg-indigo-500 text-white font-medium text-sm rounded-xl hover:bg-indigo-700 dark:hover:bg-indigo-600 shadow-sm transition-colors flex items-center">
                <MinusCircleIcon class="w-4 h-4 mr-1.5" /> Списать
              </button>
            </div>
            <!-- Days progress -->
            <div class="mb-3">
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-600 dark:text-gray-400">Дней осталось</span>
                <span class="font-bold" :class="sub.days_left <= 3 ? 'text-red-600 dark:text-red-400' : 'text-gray-900 dark:text-gray-200'">{{ sub.days_left }} дн.</span>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
                <div class="h-2 rounded-full transition-all" :class="sub.days_left <= 3 ? 'bg-red-500' : 'bg-blue-500'" :style="`width: ${Math.min(100, (sub.days_left / (sub.subscription_details?.duration_days || 30)) * 100)}%`"></div>
              </div>
            </div>
            <!-- Visits progress -->
            <div v-if="sub.remaining_visits !== null">
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-600 dark:text-gray-400">Посещений осталось</span>
                <span class="font-bold" :class="sub.remaining_visits <= 2 ? 'text-red-600 dark:text-red-400' : 'text-gray-900 dark:text-gray-200'">{{ sub.remaining_visits }} / {{ sub.subscription_details?.visit_limit }}</span>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
                <div class="h-2 rounded-full transition-all" :class="sub.remaining_visits <= 2 ? 'bg-red-500' : 'bg-indigo-500'" :style="`width: ${Math.min(100, (sub.remaining_visits / (sub.subscription_details?.visit_limit || 1)) * 100)}%`"></div>
              </div>
            </div>
            <div v-else class="text-sm font-medium text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-3 py-1.5 rounded-lg inline-block border border-green-100 dark:border-green-900/30">
              ∞ Безлимитно
            </div>
          </div>
          <div v-if="clientSubs.length === 0" class="text-center py-6 bg-gray-50 dark:bg-gray-800/50 rounded-2xl border border-dashed border-gray-300 dark:border-gray-600">
            <CreditCardIcon class="w-8 h-8 text-gray-400 dark:text-gray-500 mx-auto mb-2" />
            <p class="text-gray-500 dark:text-gray-400 text-sm">Нет активных абонементов</p>
          </div>
        </div>

        <!-- Recent Visits -->
        <h3 class="text-lg font-semibold mb-4 flex items-center text-gray-900 dark:text-gray-100">
          <ClockIcon class="w-5 h-5 mr-2 text-indigo-500 dark:text-indigo-400" /> Последние посещения
        </h3>
        <div class="space-y-2 mb-8">
          <div v-for="visit in clientVisits.slice(0, 5)" :key="visit.id" class="flex items-center justify-between py-3 px-4 bg-gray-50 dark:bg-gray-700/30 rounded-xl border border-transparent dark:border-gray-700/50">
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">{{ visit.business_name || 'Визит' }}</span>
            </div>
            <span class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(visit.date) }}</span>
          </div>
          <div v-if="clientVisits.length === 0" class="text-center py-4 text-gray-500 dark:text-gray-400 text-sm">
            Нет посещений
          </div>
        </div>

        <!-- Recent Bookings -->
        <h3 class="text-lg font-semibold mb-4 flex items-center text-gray-900 dark:text-gray-100">
          <CalendarIcon class="w-5 h-5 mr-2 text-yellow-500 dark:text-yellow-400" /> Записи
        </h3>
        <div class="space-y-2">
          <div v-for="booking in clientBookings" :key="booking.id" class="flex items-center justify-between py-3 px-4 bg-gray-50 dark:bg-gray-700/30 rounded-xl border border-transparent dark:border-gray-700/50">
            <div class="flex items-center">
              <div class="w-2 h-2 rounded-full mr-3" :class="{'bg-yellow-500': booking.status === 'pending', 'bg-green-500': booking.status === 'confirmed', 'bg-red-500': booking.status === 'rejected'}"></div>
              <div>
                <span class="text-sm text-gray-700 dark:text-gray-300">{{ booking.business_name || 'Запись' }}</span>
                <span class="text-xs text-gray-400 dark:text-gray-500 ml-2">{{ formatDate(booking.datetime) }}</span>
              </div>
            </div>
            <span class="px-2.5 py-1 text-xs font-bold rounded-full" :class="{'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400': booking.status === 'pending', 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400': booking.status === 'confirmed', 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400': booking.status === 'rejected'}">
              {{ { pending: 'Ожидает', confirmed: 'Подтверждено', rejected: 'Отклонено' }[booking.status] }}
            </span>
          </div>
          <div v-if="clientBookings.length === 0" class="text-center py-4 text-gray-500 dark:text-gray-400 text-sm">
            Нет записей
          </div>
        </div>
      </div>
    </div>

    <!-- Add User Modal -->
    <div v-if="showAddUserModal" class="fixed inset-0 bg-gray-900/50 dark:bg-gray-900/80 backdrop-blur-sm flex justify-center items-center z-50 p-3 md:p-4">
      <div class="bg-white dark:bg-gray-800 rounded-2xl md:rounded-3xl p-5 md:p-8 max-w-md w-full shadow-2xl transform transition-all border border-transparent dark:border-gray-700 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Новый пользователь</h2>
        <form @submit.prevent="createUser" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Роль</label>
            <select v-model="newUser.role" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none text-gray-900 dark:text-gray-100" required>
              <option value="client">Клиент</option>
              <option value="manager">Менеджер</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Логин</label>
            <input v-model="newUser.username" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none text-gray-900 dark:text-gray-100" required>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Пароль</label>
            <input v-model="newUser.password" type="password" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none text-gray-900 dark:text-gray-100" required>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Имя</label>
              <input v-model="newUser.first_name" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none text-gray-900 dark:text-gray-100">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Фамилия</label>
              <input v-model="newUser.last_name" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none text-gray-900 dark:text-gray-100">
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Телефон</label>
            <input v-model="newUser.phone" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none text-gray-900 dark:text-gray-100">
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="showAddUserModal = false" class="px-5 py-2.5 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors font-medium">Отмена</button>
            <button type="submit" class="px-5 py-2.5 bg-blue-600 dark:bg-blue-500 text-white rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors shadow-sm font-medium">Создать</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { API_URL } from '../config'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { XIcon, PlusIcon, SearchIcon, PhoneIcon, MailIcon, CreditCardIcon, ClockIcon, CalendarIcon, MinusCircleIcon } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const clients = ref([])
const allSubs = ref([])
const selectedClient = ref(null)
const clientSubs = ref([])
const clientVisits = ref([])
const clientBookings = ref([])
const searchQuery = ref('')

const showAddUserModal = ref(false)
const newUser = ref({
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  phone: '',
  role: 'client'
})

// Map of client ID -> their subscriptions (for table display)
const clientSubsMap = computed(() => {
  const map = {}
  for (const sub of allSubs.value) {
    if (!map[sub.client]) map[sub.client] = []
    map[sub.client].push(sub)
  }
  return map
})

const filteredClients = computed(() => {
  if (!searchQuery.value) return clients.value
  const q = searchQuery.value.toLowerCase()
  return clients.value.filter(c =>
    c.username.toLowerCase().includes(q) ||
    c.first_name?.toLowerCase().includes(q) ||
    c.last_name?.toLowerCase().includes(q) ||
    c.phone?.includes(q)
  )
})

const totalVisitsLeft = computed(() => {
  let total = 0
  let hasUnlimited = false
  for (const sub of clientSubs.value) {
    if (sub.remaining_visits === null) {
      hasUnlimited = true
    } else {
      total += sub.remaining_visits
    }
  }
  if (hasUnlimited) return '∞'
  return total
})

const fetchClients = async () => {
  const res = await axios.get(`${API_URL}/users/clients/`)
  clients.value = res.data
}

const fetchAllSubs = async () => {
  const res = await axios.get(`${API_URL}/client-subscriptions/`)
  allSubs.value = res.data
}

const openClient = async (client) => {
  selectedClient.value = client
  // Fetch subscriptions
  const subRes = await axios.get(`${API_URL}/client-subscriptions/`)
  clientSubs.value = subRes.data.filter(s => s.client === client.id)
  // Fetch visits
  const visitRes = await axios.get(`${API_URL}/visits/`)
  clientVisits.value = visitRes.data.filter(v => v.client === client.id)
  // Fetch bookings
  const bookingRes = await axios.get(`${API_URL}/bookings/`)
  clientBookings.value = bookingRes.data.filter(b => b.client === client.id)
}

const deductVisit = async (subId) => {
  try {
    const res = await axios.post(`${API_URL}/client-subscriptions/${subId}/deduct_visit/`)
    alert(`Посещение списано. Осталось: ${res.data.remaining !== null ? res.data.remaining : 'Безлимит'}`)
    await openClient(selectedClient.value)
    await fetchAllSubs()
  } catch (err) {
    alert(err.response?.data?.detail || 'Ошибка списания')
  }
}

const createUser = async () => {
  try {
    await axios.post(`${API_URL}/users/`, newUser.value)
    showAddUserModal.value = false
    newUser.value = { username: '', password: '', first_name: '', last_name: '', phone: '', role: 'client' }
    alert('Пользователь успешно создан!')
    await fetchClients()
  } catch(err) {
    alert('Ошибка при создании пользователя. Проверьте логин.')
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('ru-RU')
}

onMounted(() => {
  fetchClients()
  fetchAllSubs()
})
</script>
