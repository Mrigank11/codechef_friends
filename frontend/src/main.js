import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import Home from './components/Home.vue'
import RecvToken from './components/RecvToken.vue'
import Friends from './components/Friends.vue'
import FriendInfo from './components/FriendInfo.vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import store from './store.js'

Vue.config.productionTip = false

Vue.use(VueRouter);
Vue.use(VueResource);

if (process.env.NODE_ENV == "development") {
	Vue.http.options.root = "http://localhost:8080";
} 

Vue.http.interceptors.push(function() {
	// return response callback
	store.loading = true;
	return function(response) {
		store.loading = false;
		if (response.status != 200) {
			store.alert = {
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
	{ path: '/friend/:username', component: FriendInfo },
];

let token = window.localStorage.getItem("token");
if(!token){
	//try to fetch token from API
	Vue.http.get("api/token").then(res=>{
		token = res.data.token;
	});
}

if(token){
	Vue.http.headers.common['Authorization'] = `Token ${token}`;
	store.loggedIn = true;
}

new Vue({
  render: h => h(App),
	router:new VueRouter({routes}),
}).$mount('#app')
