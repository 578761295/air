import Vue from "vue";
import VueCompositionApi from '@vue/composition-api';
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

// cnpm i -S vue-baidu-map
import BaiduMap from 'vue-baidu-map'
Vue.use(BaiduMap, {
	ak: "29GwADE1baTUR0tGmIUgA1p2FrUiEDcG"
})

Vue.use(ElementUI);
Vue.use(VueCompositionApi);

new Vue({
	router,
	store,
	render: h => h(App)
}).$mount("#app");

Vue.config.productionTip = false;
