import type { RouteRecordRaw } from 'vue-router';

const authRoutes: Array<RouteRecordRaw>= [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/Register.vue')
    }
  ];


  export default authRoutes;