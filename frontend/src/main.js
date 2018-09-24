import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import Home from './components/Home.vue'
import RecvToken from './components/RecvToken.vue'
import Friends from './components/Friends.vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import store from './store.js'

Vue.config.productionTip = false

Vue.use(VueRouter);
Vue.use(VueResource);

Vue.http.options.root = "http://localhost:8080";
Vue.http.interceptors.push(function(request) {
	// return response callback
	store.loading = true;
	return function(response) {
		store.loading = false;
		if (response.status != 200) {
			this.store.alert = {
				enabled: true,
				color: "red",
				message: response.body.detail
			};
		}
	};
 });

const routes = [
	{ path: '/', component: Home },
	{ path: '/token/:token', component: RecvToken },
	{ path: '/friends', component: Friends },
];

const token = window.localStorage.getItem("token");
if(token){
	Vue.http.headers.common['Authorization'] = `Token ${token}`;
	store.loggedIn = true;
}

new Vue({
  render: h => h(App),
	router:new VueRouter({routes}),
}).$mount('#app')
