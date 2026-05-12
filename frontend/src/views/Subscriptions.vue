<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight transition-colors">Абонементы</h1>
        <p class="text-sm md:text-base text-gray-500 dark:text-gray-400 mt-1 md:mt-2 transition-colors">Управление доступными абонементами</p>
      </div>
      <button v-if="authStore.role === 'admin'" @click="showAddModal = true" class="w-full md:w-auto flex justify-center items-center px-5 py-2.5 bg-blue-600 dark:bg-blue-500 text-white font-medium rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors shadow-sm">
        <PlusIcon class="w-5 h-5 mr-2" /> Создать тариф
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="sub in subscriptions" :key="sub.id" class="bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow relative overflow-hidden flex flex-col">
        <div class="absolute top-0 right-0 p-4 opacity-10 dark:opacity-5">
          <CreditCardIcon class="w-24 h-24" />
        </div>
        <div class="flex-1">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-1">{{ sub.name }}</h3>
          <p class="text-3xl font-extrabold text-blue-600 dark:text-blue-400 my-4">${{ sub.price }}</p>
          <div class="space-y-2 mt-4 text-gray-600 dark:text-gray-300 text-sm font-medium">
            <div class="flex items-center">
              <ClockIcon class="w-4 h-4 mr-2 text-gray-400 dark:text-gray-500" />
              Длительность: {{ sub.duration_days }} дней
            </div>
            <div class="flex items-center">
              <ActivityIcon class="w-4 h-4 mr-2 text-gray-400 dark:text-gray-500" />
              Визиты: {{ sub.visit_limit || 'Безлимит' }}
            </div>
          </div>
        </div>
        <div class="mt-6 pt-4 border-t border-gray-100 dark:border-gray-700 flex justify-end" v-if="authStore.role === 'admin' || authStore.role === 'manager'">
          <button @click="assignSub(sub)" class="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium text-sm flex items-center">
            Назначить клиенту <ChevronRightIcon class="w-4 h-4 ml-1" />
          </button>
        </div>
      </div>
    </div>
    <!-- Add Sub Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-900/50 dark:bg-gray-900/80 backdrop-blur-sm flex justify-center items-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-3xl p-8 max-w-md w-full shadow-2xl transform transition-all border border-transparent dark:border-gray-700">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Новый тариф</h2>
        <form @submit.prevent="createSub" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Компания</label>
            <select v-model="newSub.business" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100" required>
              <option disabled value="">Выберите компанию</option>
              <option v-for="biz in businesses" :key="biz.id" :value="biz.id">{{ biz.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Название тарифа</label>
            <input v-model="newSub.name" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100" required>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Дней</label>
              <input v-model="newSub.duration_days" type="number" min="1" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100" required>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Цена ($)</label>
              <input v-model="newSub.price" type="number" step="0.01" min="0" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100" required>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Лимит посещений (оставьте пустым для безлимита)</label>
            <input v-model="newSub.visit_limit" type="number" min="1" class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100">
          </div>
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="showAddModal = false" class="px-5 py-2.5 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors font-medium">Отмена</button>
            <button type="submit" class="px-5 py-2.5 bg-blue-600 dark:bg-blue-500 text-white rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors shadow-sm font-medium">Создать</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Assign Modal -->
    <div v-if="assignSubModal" class="fixed inset-0 bg-gray-900/50 dark:bg-gray-900/80 backdrop-blur-sm flex justify-center items-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-3xl p-8 max-w-md w-full shadow-2xl transform transition-all border border-transparent dark:border-gray-700">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Назначить абонемент</h2>
        <form @submit.prevent="confirmAssign" class="space-y-4">
          <p class="text-gray-600 dark:text-gray-400">Тариф: <strong class="text-gray-900 dark:text-white">{{ selectedSub?.name }}</strong></p>
          <div class="relative">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Выберите клиента</label>
            <div v-if="!assignClientId" class="relative">
              <input 
                v-model="clientSearchQuery" 
                @focus="showClientDropdown = true" 
                @blur="setTimeout(() => showClientDropdown = false, 200)"
                type="text" 
                placeholder="Поиск по имени или телефону..." 
                class="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100"
                required
              />
              <div v-if="showClientDropdown" class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-xl max-h-60 overflow-y-auto">
                <div v-if="filteredClientsDropdown.length === 0" class="p-3 text-sm text-gray-500 dark:text-gray-400 text-center">Ничего не найдено</div>
                <div v-for="client in filteredClientsDropdown" :key="client.id" @mousedown.prevent="selectClientForAssign(client)" class="p-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer flex items-center justify-between border-b border-gray-50 dark:border-gray-700 last:border-0">
                  <div>
                    <p class="font-bold text-gray-900 dark:text-gray-100 text-sm">{{ client.first_name }} {{ client.last_name }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">@{{ client.username }}</p>
                  </div>
                  <span class="text-xs text-gray-400 dark:text-gray-500">{{ client.phone }}</span>
                </div>
              </div>
            </div>
            <!-- When selected -->
            <div v-else class="w-full px-4 py-2 border border-blue-200 dark:border-blue-900/50 bg-blue-50 dark:bg-blue-900/20 rounded-xl flex items-center justify-between">
              <div>
                <p class="font-bold text-blue-900 dark:text-blue-300 text-sm">{{ selectedClientObj?.first_name }} {{ selectedClientObj?.last_name }} <span class="text-xs text-blue-500 dark:text-blue-400 font-normal">(@{{ selectedClientObj?.username }})</span></p>
              </div>
              <button type="button" @click="assignClientId = ''" class="text-blue-400 dark:text-blue-500 hover:text-blue-600 dark:hover:text-blue-300">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
              </button>
            </div>
          </div>
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="assignSubModal = false" class="px-5 py-2.5 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors font-medium">Отмена</button>
            <button type="submit" class="px-5 py-2.5 bg-green-600 dark:bg-green-500 text-white rounded-xl hover:bg-green-700 dark:hover:bg-green-600 transition-colors shadow-sm font-medium">Назначить</button>
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
import { PlusIcon, CreditCardIcon, ClockIcon, ActivityIcon, ChevronRightIcon } from 'lucide-vue-next'

const authStore = useAuthStore()
const subscriptions = ref([])
const businesses = ref([])
const clients = ref([])
const showAddModal = ref(false)
const assignSubModal = ref(false)
const selectedSub = ref(null)
const assignClientId = ref('')

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
  return clients.value.find(c => c.id === assignClientId.value)
})

const selectClientForAssign = (client) => {
  assignClientId.value = client.id
  clientSearchQuery.value = ''
  showClientDropdown.value = false
}

const newSub = ref({
  business: '',
  name: '',
  duration_days: 30,
  visit_limit: '',
  price: 0
})

const fetchSubscriptions = async () => {
  const res = await axios.get(`${API_URL}/subscriptions/`)
  subscriptions.value = res.data
}

const fetchData = async () => {
  if (authStore.role === 'admin') {
    const bizRes = await axios.get(`${API_URL}/businesses/`)
    businesses.value = bizRes.data
  }
  if (authStore.role !== 'client') {
    const clientsRes = await axios.get(`${API_URL}/users/clients/`)
    clients.value = clientsRes.data
  }
}

const createSub = async () => {
  try {
    const payload = { ...newSub.value }
    if (!payload.visit_limit) payload.visit_limit = null
    await axios.post(`${API_URL}/subscriptions/`, payload)
    showAddModal.value = false
    await fetchSubscriptions()
  } catch (err) {
    alert('Ошибка при создании тарифа')
  }
}

const assignSub = (sub) => {
  selectedSub.value = sub
  assignSubModal.value = true
}

const confirmAssign = async () => {
  try {
    await axios.post(`${API_URL}/client-subscriptions/`, {
      subscription: selectedSub.value.id,
      client: assignClientId.value
    })
    assignSubModal.value = false
    assignClientId.value = ''
    alert('Абонемент успешно назначен!')
  } catch(err) {
    alert(err.response?.data?.detail || 'Ошибка при назначении абонемента')
  }
}

onMounted(() => {
  fetchSubscriptions()
  fetchData()
})
</script>
