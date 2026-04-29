import { createPinia } from "pinia";
import App from "./App.vue";

// #ifndef VUE3
import Vue from "vue";

Vue.config.productionTip = false;
App.mpType = "app";

const pinia = createPinia();
const app = new Vue({
  ...App,
});

Vue.use(pinia);
app.$mount();
// #endif

// #ifdef VUE3
import { createSSRApp } from "vue";

export function createApp() {
  const app = createSSRApp(App);
  const pinia = createPinia();
  app.use(pinia);
  return {
    app,
    pinia,
  };
}
// #endif
