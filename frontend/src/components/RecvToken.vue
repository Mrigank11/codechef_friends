<template>
	<div></div>
</template>
<script>
export default {
	mounted(){
		window.localStorage.setItem("token",this.$route.params.token);
		this.$router.push({path:'/'});
	}
}
</script>
