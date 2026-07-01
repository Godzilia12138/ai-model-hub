<template>
  <div class="card">

    <h2>{{ title }}</h2>

    <pre>{{ content }}</pre>

  </div>
</template>

<script setup>

defineProps({

  title:String,

  content:String

})

</script>

<style scoped>

.card{

    background:white;

    padding:20px;

    border-radius:15px;

    margin-bottom:20px;

    box-shadow:0 10px 25px rgba(0,0,0,.08);

}

h2{

    margin-top:0;

}

pre{

    white-space:pre-wrap;

}

</style>