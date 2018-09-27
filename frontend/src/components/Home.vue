<template>
	<v-container>
		Use sidebar for navigation. 
		<br>
		You can follow people and see your followers.
	</v-container>
</template>

<script>
import store from '../store.js'

export default {
	data(){
		return {
			store:store
		}
	}
}
</script>
