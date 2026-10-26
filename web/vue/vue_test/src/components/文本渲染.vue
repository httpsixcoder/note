<script setup>
let message = "Hello Vite + Vue!";
let num = 100;
let test = () => {
  return "你好";
};
let tag="<h1>你好</h1>";
</script>

<template>
  <div id="app">
    <div>{{ message }}</div>
    <div v-text="message"></div>
    <div v-html="message"></div>
    <hr />
    <div>{{ message }}666</div>
    <div v-text="message + '6666666'"></div>
    <div v-html="message + '6666666666666'"></div>
    <hr />
    <div>{{ message }}666</div>
    <div v-text="message > 10 ? 'Yes' : 'No'"></div>
    <div v-text="test()"></div>
    <hr />
    <div>{{ tag }}</div>
    <div v-html="tag"></div>
    <div v-text="tag"></div>
  </div>
</template>
