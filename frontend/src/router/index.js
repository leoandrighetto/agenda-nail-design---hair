/**
 * router/index.js
 *
 * Manual routes for ./src/pages/*.vue
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import Index from '@/pages/index.vue'
import Agenda from '@/pages/agenda.vue'
import Clientes from '@/pages/clientes.vue'
import Servicos from '@/pages/servicos.vue'
import Cursos from '@/pages/cursos.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Index,
    },
    {
      path: '/agenda',
      component: Agenda,
    },
    {
      path: '/clientes',
      component: Clientes,
    },
    {
      path: '/servicos',
      component: Servicos,
    },
    {
      path: '/cursos',
      component: Cursos,
    },
  ],
})

export default router
