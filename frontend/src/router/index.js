import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
      { path: 'businesses', name: 'Businesses', component: () => import('../views/Businesses.vue') },
      { path: 'subscriptions', name: 'Subscriptions', component: () => import('../views/Subscriptions.vue') },
      { path: 'clients', name: 'Clients', component: () => import('../views/Clients.vue') },
      { path: 'bookings', name: 'Bookings', component: () => import('../views/Bookings.vue') },
      { path: 'profile', name: 'Profile', component: () => import('../views/Profile.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
