<script setup>
let message = "Hello Vite + Vue!";
let num = 100;
let test = () => {
  return "你好";
};
</script>

<template>
  <div id="app">
    <div>{{ message }}</div>
    <div>{{ num > 100 }}</div>
    <div>{{ num > 10 ? "Yes" : "No" }}</div>
    <div>{{ test() }}</div>
    <input type="text" :value="message" />
  </div>
</template>
