<script setup>
import { ref } from "vue";
let flag= ref(true)
let func=()=>{
  flag.value=!flag.value
}

</script>

<template>
  <div>
    <h1 v-if="flag">{{ flag }}11111</h1>
    <h1 v-else>{{ flag }}6666666</h1>
    <h1 v-show="flag">{{ flag }}123123131</h1>
    <h1 v-show="!flag">{{ flag }}45645646564564</h1>

    <input type="button" value="按钮" @click="func" />
  </div>
</template>

<style scoped>

</style>