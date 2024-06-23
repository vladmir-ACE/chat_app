import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// for toast notification
import ToastPlugin from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-bootstrap.css';

const app = createApp(App)

app.use(ToastPlugin);

app.use(router);

app.mount('#app')
