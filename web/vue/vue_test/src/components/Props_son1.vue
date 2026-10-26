<script setup>
import { defineProps } from 'vue'
//声明父组件传递属性值
defineProps({
    fat_mess: String,
})
</script>

<template>
    <div>
        <h1>son1</h1>
        <div>{{ fat_mess }}</div>
    </div>
</template>

<style scoped></style>