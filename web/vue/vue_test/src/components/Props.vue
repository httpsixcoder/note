<script setup>
import { ref } from 'vue'
let context = ref("12")
let song_to_fa = ref("000")
let func = (data) => {
    song_to_fa.value = data
}
let func_to_bor = (data) => {
    context.value = data
}
</script>

<template>
    <div>
        <h1>传值</h1>
        <router-link to="/props/1">显示两个子组件</router-link> &nbsp;
        <br>
        {{ context }}
        <input type="text" v-model="context">
        <!-- <input type="button" value="传给son1" @click="song_son1()"> -->
        <router-view name="one" :fat_mess="context"></router-view>
        {{ song_to_fa }}
        <router-view name="two" @song_fa_data="func" @func_to_bor="func_to_bor"> </router-view>

    </div>
</template>

<style scoped></style>