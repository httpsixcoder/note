<script setup>
import { ref } from "vue";

let user = ref({
  username: "admin",
  password: 123456
})
</script>

<template>
  <div>
    {{ user }}
    <hr>
    username:<input type="text" :value="user.username" /><br>
    password:<input type="text" :value="user.password">
    <hr>
    username:<input type="text" v-model="user.username" /><br>
    password:<input type="text" v-model="user.password">

  </div>
</template>

<style scoped></style>