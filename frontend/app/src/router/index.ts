import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Gomoku Game'
      }
    },
    {
      path: '/rules',
      name: 'rules',
      component: () => import('../views/Rules.vue')
    },
    {
      path: '/game',
      name: 'game',
      component: () => import('../views/Game.vue')
    },
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.title && typeof to.meta.title === "string") {
    document.title = to.meta.title;
  }
  next();
})

export default router
