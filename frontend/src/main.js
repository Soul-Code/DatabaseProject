// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import router from "./router";
import axios from "axios";
axios.defaults.withCredentials=true;
Vue.prototype.$axios = axios;
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";

Vue.use(ElementUI, { size: "large", zIndex: 3000 });

Vue.config.productionTip = false;

Vue.prototype.$url = "http://127.0.0.1:5000/api/";

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  components: { App },
  template: "<App/>"
});
