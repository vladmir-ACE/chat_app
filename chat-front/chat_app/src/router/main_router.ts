

import type { RouteRecordRaw } from 'vue-router';

const mainRoutes: Array<RouteRecordRaw>= [
    {
      path: '/main',
      name: 'main',
      component: () => import('../views/main/MainView.vue'),
      children: [
        {
          path: '',
          name: 'main',
          component: () => import("../views/main/ChatView.vue")
        },
        {
            path: '/chat',
            name: 'chat',
            component: () => import("../views/main/ChatView.vue")
          }
    
    ]
    }
    
  ];

  export default mainRoutes;