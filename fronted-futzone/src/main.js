import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";

import "./assets/tailwind.css";
import "aos/dist/aos.css";
import "sweetalert2/dist/sweetalert2.min.css";


import "vue3-toastify/dist/index.css";
import Vue3Toastify from 'vue3-toastify'
import AOS from "aos";
import VueSweetalert2 from "vue-sweetalert2";
import FontAwesomeIcon from "./plugins/fontawesome";

AOS.init();

const app = createApp(App);

app.component("font-awesome-icon", FontAwesomeIcon);

app.use(createPinia());
app.use(router);
app.use(Vue3Toastify, {
  autoClose: 3000,
  position: "top-right",
  theme: "light",
  hideProgressBar: false,
  pauseOnHover: true,
  transition: "slide",
});
app.use(VueSweetalert2);

app.mount("#app");
