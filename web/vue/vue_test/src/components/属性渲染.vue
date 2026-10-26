<script setup>
let username="admin"

</script>

<template>
  <div>
    <input type="text" value="username" />
    <br>
    <input type="text" v-bind:value="username" />
    <br>
    <input type="text" :value="username" />
  </div>
</template>
