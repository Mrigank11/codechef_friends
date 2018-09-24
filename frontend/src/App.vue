<template>
<v-app>
  <v-navigation-drawer clipped app v-model="drawer" >
		<v-list>
			<v-list-tile to="/friends" >
				Friends
			</v-list-tile>
		</v-list>
	</v-navigation-drawer>
  <v-toolbar :clipped-left="true" app dark color="primary">
		<v-toolbar-side-icon @click.stop="drawer = !drawer" ></v-toolbar-side-icon>
		<v-toolbar-title >CodeChef-Friends</v-toolbar-title>
	</v-toolbar>
  <v-content>
    <v-container fluid>
      <router-view></router-view>
			<v-dialog v-model="store.loading" persistent width="300" >
				<v-card color="primary" dark >
					<v-card-text>
						Please stand by
						<v-progress-linear indeterminate color="white" class="mb-0" ></v-progress-linear>
					</v-card-text>
				</v-card>
			</v-dialog>
			<v-dialog v-model="store.alert.enabled" persistent width="300" >
				<v-card :color="store.alert.color" dark>
					<v-card-text>
						{{store.alert.message}}
					</v-card-text>
					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn flat @click="store.alert.enabled=false" >Okay</v-btn>
					</v-card-actions>
				</v-card>
			</v-dialog>
			<div v-if="!store.loading && !store.loggedIn">
				<p> Please login to continue. </p>
				<a href="/oauth/redirect"><v-btn color="primary"  > Login In</v-btn></a>
			</div>
    </v-container>
  </v-content>
  <v-footer app></v-footer>
</v-app>
</template>

<script>
import store from "./store.js";
import Vue from "vue";

export default {
  data() {
    return {
      store: store,
      drawer: null
    };
  }
};
</script>
