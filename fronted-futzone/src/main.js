import { createApp } from 'vue'
import router from './router'
import FontAwesomeIcon from './plugins/fontawesome'
import './assets/tailwind.css'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config';
import App from './App.vue'
AOS.init()
const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia())
app.use(PrimeVue);
app.use(router)
app.mount('#app')