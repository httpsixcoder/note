<script setup>
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue';
// 获取当前的route对象
let route = useRoute()
let languageName = ref('')
//  借助更新时生命周期,将数据更新进入响应式对象
onMounted(() => {
    // 获取对象中的参数
    languageName.value = route.params.mse
})    
</script>

<template>
    <div>
        <p>路径参数</p>
        <h3>{{ languageName }}是世界上最好的语言</h3>
    </div>
</template>

<style scoped></style>