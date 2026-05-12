<template>
  <div class="space-y-6 md:space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight transition-colors">Записи</h1>
        <p class="text-sm md:text-base text-gray-500 dark:text-gray-400 mt-1 md:mt-2 transition-colors">Управление записями клиентов</p>
      </div>
      <button v-if="authStore.role !== 'client'" @click="showAddModal = true" class="w-full md:w-auto flex justify-center items-center px-5 py-2.5 bg-blue-600 dark:bg-blue-500 text-white font-medium rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors shadow-sm">
        <PlusIcon class="w-5 h-5 mr-2" /> Новая запись
      </button>
    </div>

    <!-- Tabs for admin/manager -->
    <div v-if="authStore.role !== 'client'" class="flex flex-wrap gap-1 bg-gray-100 dark:bg-gray-800 rounded-xl p-1 w-full md:w-fit transition-colors">
      <button @click="activeTab = 'all'" :class="activeTab === 'all' ? 'bg-white dark:bg-gray-700 shadow-sm text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'" class="flex-1 md:flex-none text-center px-3 md:px-4 py-2 rounded-lg text-xs md:text-sm font-medium transition-all">
        Все записи
      </button>
      <button @click="activeTab = 'pending'" :class="activeTab === 'pending' ? 'bg-white dark:bg-gray-700 shadow-sm text-yellow-600 dark:text-yellow-400' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'" class="flex-1 md:flex-none text-center px-3 md:px-4 py-2 rounded-lg text-xs md:text-sm font-medium transition-all">
        Ожидают ({{ pendingCount }})
      </button>
      <button @click="activeTab = 'confirmed'" :class="activeTab === 'confirmed' ? 'bg-white dark:bg-gray-700 shadow-sm text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'" class="flex-1 md:flex-none text-center px-3 md:px-4 py-2 rounded-lg text-xs md:text-sm font-medium transition-all">
        Подтверждённые
      </button>
    </div>

    <!-- Empty state -->
    <div v-if="filteredBookings.length === 0" class="bg-white dark:bg-gray-800 rounded-2xl md:rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 p-12 text-center transition-colors">
      <CalendarIcon class="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
      <p class="text-gray-500 dark:text-gray-400">Записи не найдены.</p>
    </div>

    <!-- Mobile card layout -->
    <div v-else class="space-y-3 md:hidden">
      <div v-for="booking in filteredBookings" :key="booking.id" class="bg-white dark:bg-gray-800 rounded-2xl p-4 shadow-sm border border-gray-100 dark:border-gray-700 transition-colors">
        <div class="flex items-start gap-3">
          <div class="p-2.5 rounded-xl shrink-0" :class="statusIconBg(booking.status)">
            <CalendarIcon class="w-5 h-5" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-2">
              <p class="font-bold text-gray-900 dark:text-white text-sm leading-snug">{{ formatDate(booking.datetime) }}</p>
              <span class="px-2.5 py-0.5 text-xs font-bold rounded-full shrink-0 whitespace-nowrap" :class="statusBadge(booking.status)">
                {{ statusLabel(booking.status) }}
              </span>
            </div>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {{ booking.business_name || 'Компания' }}
            </p>
            <p v-if="authStore.role !== 'client'" class="text-xs text-gray-400 dark:text-gray-500 mt-0.5">
              {{ booking.client_name }}
            </p>
          </div>
        </div>
        <!-- Pending actions for client (mobile) -->
        <div v-if="booking.status === 'pending' && authStore.role === 'client'" class="flex gap-2 mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
          <button @click="confirmBooking(booking.id)" class="flex-1 py-2 bg-green-500 text-white text-sm font-medium rounded-xl hover:bg-green-600 transition-colors shadow-sm text-center">
            Подтвердить
          </button>
          <button @click="rejectBooking(booking.id)" class="flex-1 py-2 bg-red-500 text-white text-sm font-medium rounded-xl hover:bg-red-600 transition-colors shadow-sm text-center">
            Отклонить
          </button>
        </div>
      </div>
    </div>

    <!-- Desktop table layout -->
    <div class="hidden md:block bg-white dark:bg-gray-800 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden transition-colors">
      <div class="divide-y divide-gray-100 dark:divide-gray-700">
        <div v-for="booking in filteredBookings" :key="booking.id" class="p-6 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
          <div class="flex items-center">
            <div class="p-3 rounded-2xl mr-4" :class="statusIconBg(booking.status)">
              <CalendarIcon class="w-6 h-6" />
            </div>
            <div>
              <p class="font-bold text-gray-900 dark:text-white">{{ formatDate(booking.datetime) }}</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ booking.business_name || 'Компания' }}
                <span v-if="authStore.role !== 'client'" class="ml-2 text-gray-400 dark:text-gray-500">• {{ booking.client_name }}</span>
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <!-- Pending actions for client -->
            <template v-if="booking.status === 'pending' && authStore.role === 'client'">
              <button @click="confirmBooking(booking.id)" class="px-4 py-2 bg-green-500 text-white text-sm font-medium rounded-xl hover:bg-green-600 transition-colors shadow-sm">
                Подтвердить
              </button>
              <button @click="rejectBooking(booking.id)" class="px-4 py-2 bg-red-500 text-white text-sm font-medium rounded-xl hover:bg-red-600 transition-colors shadow-sm">
                Отклонить
              </button>
            </template>
            <!-- Status badge -->
            <span class="px-3 py-1 text-xs font-bold rounded-full" :class="statusBadge(booking.status)">
              {{ statusLabel(booking.status) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Booking Modal (only for admin/manager) -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-900/50 dark:bg-gray-900/80 backdrop-blur-sm flex justify-center items-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-2xl md:rounded-3xl p-6 md:p-8 max-w-md w-full shadow-2xl transform transition-all border border-transparent dark:border-gray-700 max-h-[90vh] overflow-y-auto">
        <h2 class="text-xl md:text-2xl font-bold mb-5 md:mb-6 text-gray-900 dark:text-white">Создать запись</h2>
        <form @submit.prevent="createBooking" class="space-y-4">
          <div class="relative">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Клиент</label>
            <div v-if="!newBooking.client" class="relative">
              <input 
                v-model="clientSearchQuery" 
                @focus="showClientDropdown = true" 
                @blur="setTimeout(() => showClientDropdown = false, 200)"
                type="text" 
                placeholder="Поиск по имени или телефону..." 
                class="w-full px-4 py-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100"
                required
              />
              <div v-if="showClientDropdown" class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-xl max-h-60 overflow-y-auto">
                <div v-if="filteredClientsDropdown.length === 0" class="p-3 text-sm text-gray-500 dark:text-gray-400 text-center">Ничего не найдено</div>
                <div v-for="client in filteredClientsDropdown" :key="client.id" @mousedown.prevent="selectClientForBooking(client)" class="p-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer flex items-center justify-between border-b border-gray-50 dark:border-gray-700 last:border-0">
                  <div>
                    <p class="font-bold text-gray-900 dark:text-gray-100 text-sm">{{ client.first_name }} {{ client.last_name }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">@{{ client.username }}</p>
                  </div>
                  <span class="text-xs text-gray-400 dark:text-gray-500">{{ client.phone }}</span>
                </div>
              </div>
            </div>
            <!-- When selected -->
            <div v-else class="w-full px-4 py-3 border border-blue-200 dark:border-blue-900/50 bg-blue-50 dark:bg-blue-900/20 rounded-xl flex items-center justify-between">
              <div class="min-w-0 mr-2">
                <p class="font-bold text-blue-900 dark:text-blue-300 text-sm truncate">{{ selectedClientObj?.first_name }} {{ selectedClientObj?.last_name }} <span class="text-xs text-blue-500 dark:text-blue-400 font-normal">(@{{ selectedClientObj?.username }})</span></p>
              </div>
              <button type="button" @click="newBooking.client = ''" class="text-blue-400 dark:text-blue-500 hover:text-blue-600 dark:hover:text-blue-300 shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Компания</label>
            <select v-model="newBooking.business" class="w-full px-4 py-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100" required>
              <option disabled value="">Выберите компанию</option>
              <option v-for="biz in businesses" :key="biz.id" :value="biz.id">{{ biz.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Дата и Время</label>
            <input v-model="newBooking.datetime" type="datetime-local" class="w-full px-4 py-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100 [color-scheme:light] dark:[color-scheme:dark]" required>
          </div>
          
          <!-- Error message -->
          <div v-if="createError" class="p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-900/50 rounded-xl text-red-700 dark:text-red-400 text-sm font-medium">
            {{ createError }}
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="showAddModal = false; createError = ''" class="px-5 py-2.5 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors font-medium">Отмена</button>
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
import { useAuthStore } from '../stores/auth'
import { PlusIcon, CalendarIcon } from 'lucide-vue-next'

const authStore = useAuthStore()
const bookings = ref([])
const businesses = ref([])
const clients = ref([])
const showAddModal = ref(false)
const createError = ref('')
const activeTab = ref('all')
const newBooking = ref({ business: '', datetime: '', client: '' })

// Custom select state
const clientSearchQuery = ref('')
const showClientDropdown = ref(false)

const filteredClientsDropdown = computed(() => {
  if (!clientSearchQuery.value) return clients.value
  const q = clientSearchQuery.value.toLowerCase()
  return clients.value.filter(c => 
    c.username.toLowerCase().includes(q) || 
    (c.first_name && c.first_name.toLowerCase().includes(q)) || 
    (c.last_name && c.last_name.toLowerCase().includes(q)) ||
    (c.phone && c.phone.includes(q))
  )
})

const selectedClientObj = computed(() => {
  return clients.value.find(c => c.id === newBooking.value.client)
})

const selectClientForBooking = (client) => {
  newBooking.value.client = client.id
  clientSearchQuery.value = ''
  showClientDropdown.value = false
}

const filteredBookings = computed(() => {
  if (authStore.role === 'client' || activeTab.value === 'all') return bookings.value
  return bookings.value.filter(b => b.status === activeTab.value)
})

const pendingCount = computed(() => bookings.value.filter(b => b.status === 'pending').length)

const fetchBookings = async () => {
  const res = await axios.get(`${API_URL}/bookings/`)
  bookings.value = res.data
}

const fetchData = async () => {
  const bizRes = await axios.get(`${API_URL}/businesses/`)
  businesses.value = bizRes.data

  if (authStore.role !== 'client') {
    const clientsRes = await axios.get(`${API_URL}/users/clients/`)
    clients.value = clientsRes.data
  }
}

const createBooking = async () => {
  try {
    createError.value = ''
    await axios.post(`${API_URL}/bookings/`, newBooking.value)
    showAddModal.value = false
    newBooking.value = { business: '', datetime: '', client: '' }
    await fetchBookings()
  } catch (err) {
    createError.value = err.response?.data?.detail || 'Не удалось создать запись'
  }
}

const confirmBooking = async (id) => {
  try {
    const res = await axios.post(`${API_URL}/bookings/${id}/confirm/`)
    alert(res.data.detail || 'Запись подтверждена')
    await fetchBookings()
  } catch (err) {
    alert(err.response?.data?.detail || 'Ошибка подтверждения')
  }
}

const rejectBooking = async (id) => {
  try {
    await axios.post(`${API_URL}/bookings/${id}/reject/`)
    await fetchBookings()
  } catch (err) {
    alert(err.response?.data?.detail || 'Ошибка отклонения')
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('ru-RU')
}

const statusLabel = (status) => {
  const map = { pending: 'Ожидает', confirmed: 'Подтверждено', rejected: 'Отклонено' }
  return map[status] || status
}

const statusBadge = (status) => {
  const map = {
    pending: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400',
    confirmed: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
    rejected: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400',
  }
  return map[status] || 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
}

const statusIconBg = (status) => {
  const map = {
    pending: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-500',
    confirmed: 'bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400',
    rejected: 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400',
  }
  return map[status] || 'bg-gray-50 dark:bg-gray-900 text-gray-600 dark:text-gray-400'
}

onMounted(() => {
  fetchBookings()
  fetchData()
})
</script>
