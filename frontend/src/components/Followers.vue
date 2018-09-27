<template>
	<v-container>
		<v-list>
			<v-list-tile :to="'userinfo/'+f.username" v-for="f in friends" :key="f.username" >
				<v-list-tile-title>{{f.username}}</v-list-tile-title> 
			</v-list-tile>	
		</v-list>
	</v-container>
</template>

<script>
import store from '../store.js'

export default {
	data(){
		return {
			store:store,
			friends:[],
		}
	},
	methods:{
		loadFriends(){
			this.$http.get("api/followers").then(res=>{
				this.friends = res.body;
			});
		},
	},
	mounted(){
		this.loadFriends();
	}
}
</script>
