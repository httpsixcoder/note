<script setup type="module">
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue';
// 获取当前的route对象
let route = useRoute()
let languageName = ref('')
//  借助更新时生命周期,将数据更新进入响应式对象
onMounted(() => {

    languageName.value = route.query.mse
})    
</script>
<template>
    <div>
        <h1>ShowDetail2页面</h1>
        <h3>{{ languageName }}是世界上最好的语言</h3>
    </div>
</template>
<style scoped></style>