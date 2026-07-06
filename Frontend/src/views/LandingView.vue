<template>
<div>
  <div @click="$router.push('/admin')">Go to Admin</div>
  <div @click="$router.push('/student')">Go to Student</div>
  <div @click="$router.push('/company')">Go to Company</div>
</div>
</template>


<script>
  export default {
  name: 'LandingView'
}
</script>