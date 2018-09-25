<template>
	<v-container>
		<v-form @submit.prevent="addFriend" >
			<v-layout row>
				<v-flex xs11 >
					<v-text-field placeholder="Add new friend" v-model="newFriendName" ></v-text-field>
				</v-flex>
			<v-flex>
				<v-btn type="submit" icon>
					<v-icon @click="addFriend" >add</v-icon>
				</v-btn>
			</v-flex>
			</v-layout>
		</v-form>
		<v-list>
			<v-list-tile :to="'friend/'+f.username" v-for="f in friends" :key="f.username" >
				<v-list-tile-title>{{f.username}}</v-list-tile-title> 
				<v-list-tile-action>
					<v-btn @click.prevent="removeFriend(f.username)" icon>
						<v-icon color="red">delete</v-icon>
					</v-btn>
				</v-list-tile-action>
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
			newFriendName:""
		}
	},
	methods:{
		loadFriends(){
			this.$http.get("api/friends").then(res=>{
				this.friends = res.body;
			});
		},
		addFriend(){
			this.$http.put("api/friends",{username:this.newFriendName})
				.then(resp=>{
					this.friends = resp.body;
				});
		},
		removeFriend(username){
			this.$http.delete(`api/friends/${username}`)
				.then(resp=>{
					this.friends = resp.body;
				});
		}
	},
	mounted(){
		this.loadFriends();
	}
}
</script>
