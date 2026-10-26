<script setup>
import { ref,reactive } from "vue";
// 推荐ref，
let num = ref(2026)
let data=reactive({
  name:"张三",
  age:18
})
let refData=ref({
  name:"张三6",
  age:16
})
let func = () => {
  num.value++
  data.age++
  refData.value.age++

}
</script>

<template>
  <div>
    <h1>{{ num }}</h1>
    <h1>{{ data }}</h1>
    <h1>{{ refData }}</h1>

    <input type="button" value="按钮" @click="func" />
  </div>
</template>

<style scoped></style>