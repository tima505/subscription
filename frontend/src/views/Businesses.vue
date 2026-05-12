<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight transition-colors">Компании</h1>
        <p class="text-sm md:text-base text-gray-500 dark:text-gray-400 mt-1 md:mt-2 transition-colors">Управление зарегистрированми филиалами / бизнесами</p>
      </div>
      <button @click="showAddModal = true" class="w-full md:w-auto flex justify-center items-center px-5 py-2.5 bg-blue-600 dark:bg-blue-500 text-white font-medium rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors shadow-sm">
        <PlusIcon class="w-5 h-5 mr-2" /> Добавить
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="biz in businesses" :key="biz.id" class="bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-all relative overflow-hidden group">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-400 to-indigo-500 dark:from-blue-500 dark:to-indigo-600"></div>
        <div class="flex items-center justify-between mb-4 mt-2">
          <div class="p-3 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-2xl">
            <BriefcaseIcon class="w-6 h-6" />
          </div>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ biz.name }}</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">{{ biz.description || 'Описание отсутствует.' }}</p>
      </div>
      
      <div v-if="businesses.length === 0" class="col-span-full p-12 text-center bg-white dark:bg-gray-800 rounded-3xl border border-dashed border-gray-300 dark:border-gray-700">
        <BriefcaseIcon class="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Компании не найдены</h3>
        <p class="text-gray-500 dark:text-gray-400 mt-1">Добавьте первый бизнес, чтобы начать.</p>
      </div>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-900/50 dark:bg-gray-900/80 backdrop-blur-sm flex justify-center items-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-3xl p-8 max-w-md w-full shadow-2xl transform transition-all border border-transparent dark:border-gray-700">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Новая компания</h2>
        <form @submit.prevent="addBusiness" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Название</label>
            <input v-model="newBiz.name" type="text" class="w-full px-4 py-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100" required>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Описание</label>
            <textarea v-model="newBiz.description" rows="3" class="w-full px-4 py-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none transition-colors text-gray-900 dark:text-gray-100"></textarea>
          </div>
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="showAddModal = false" class="px-5 py-2.5 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors font-medium">Отмена</button>
            <button type="submit" class="px-5 py-2.5 bg-blue-600 dark:bg-blue-500 text-white rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors shadow-sm font-medium">Сохранить</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { API_URL } from '../config'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { PlusIcon, BriefcaseIcon } from 'lucide-vue-next'

const businesses = ref([])
const showAddModal = ref(false)
const newBiz = ref({ name: '', description: '' })

const fetchBusinesses = async () => {
  const res = await axios.get(`${API_URL}/businesses/`)
  businesses.value = res.data
}

const addBusiness = async () => {
  try {
    await axios.post(`${API_URL}/businesses/`, newBiz.value)
    showAddModal.value = false
    newBiz.value = { name: '', description: '' }
    await fetchBusinesses()
  } catch (err) {
    alert('Не удалось добавить компанию')
  }
}

onMounted(fetchBusinesses)
</script>
