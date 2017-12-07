<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      msg: 'The Daily Bark',
    };
  },
};
</script>

<style scoped>
 h1, h2 {
     font-weight: bold;
     color: #ffc857;
 }
</style>
