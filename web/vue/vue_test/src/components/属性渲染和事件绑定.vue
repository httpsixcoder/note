<script setup>

let func = () => {
  alert("按钮被点击了")

}
let testPrevent = (e) => {
  alert("按钮被点击了")
  if(!confirm("是否跳转到尚硅谷")) {
    e.preventDefault();
  }
}
</script>

<template>
  <div>
    <input type="button" value="按钮" v-on:click="func" />
    <hr>
    <input type="button" value="按钮" @:click="func" />
    <hr>
    <input type="button" value="按钮" @:click.once="func" />

    <a href="https://www.aiguigu.com" >尚硅谷</a>
    <hr>
    <a href="https://www.aiguigu.com" @click.prevent="">尚硅谷</a>
    <hr>
    <a href="https://www.aiguigu.com" @click="testPrevent">注销</a>
    <hr>
    

  </div>
</template>

<style scoped></style>