<script setup>
import { ref, defineEmits } from 'vue'
let emites = defineEmits(['add', 'sub']);
let song_fa = ref(1);
let func = () => {
    //2.触发父组件对应的方法，调用defineEmites对应的属性
    emites('song_fa_data', song_fa.value)
}
let func_to_bor = () => {
    emites('func_to_bor', song_fa.value)
}
</script>

<template>
    <div>
        <h1>son2</h1>
        <input type="text" v-model="song_fa">{{ song_fa }}
        <input type="button" value="传值给父组件" @click="func()">
        <input type="button" value="传值给兄各组件" @click="func_to_bor()">
    </div>
</template>

<style scoped></style>