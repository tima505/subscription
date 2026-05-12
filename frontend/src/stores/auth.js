import { defineStore } from 'pinia'
import axios from 'axios'
import { API_URL } from '../config'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    role: (state) => state.user?.role || 'client'
  },
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post(`${API_URL}/auth/login/`, { username, password })
        this.token = response.data.access
        localStorage.setItem('token', this.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        await this.fetchUser()
        return true
      } catch (error) {
        console.error('Login failed', error)
        return false
      }
    },
    async fetchUser() {
      if (!this.token) return
      try {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        const response = await axios.get(`${API_URL}/users/me/`)
        this.user = response.data
      } catch (error) {
        this.logout()
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
