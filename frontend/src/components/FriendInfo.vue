<template>
	<div>
		<b> Username : </b> {{username}}
		<br>
		<b> Name : </b> {{userdata.fullname}} ({{userdata.band}})
		<br>
		<b> City : </b> {{userdata.city.name}}
		<br>
		<b> State : </b> {{userdata.state.name}}
		<br>
		<b> Country : </b> {{userdata.country.name}}
		<br>
		<b> Organization : </b> {{userdata.organization}}
		<br>
		<b> ProblemStats : </b> {{userdata.problemStats}}
		<br>
		<b> Ratings : </b> {{userdata.ratings}}
		<br>
		<b> Rankings : </b> {{userdata.rankings}}
		<br>
		<b> SubmissionStats : </b> {{userdata.submissionStats}}
	</div>
</template>
<script>
export default {
	data(){
		return {
			username:null,
			userdata:null
		}
	},
	mounted(){
		this.username = this.$route.params.username;
		this.$http.get(`api/following/${this.username}`).then(resp=>{
			this.userdata = resp.data;
		});
	}
}
</script>
