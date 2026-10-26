<script setup>
// import axios from 'axios'
// 导入自己定义的axios.js文件,而不是导入axios依赖  
import axios from '../axios/axios'
import { onMounted, ref } from 'vue';

const jsonData = ref("666")

const getLoveMessage1 = async () => {
    try {
        const res = await axios.get('http://127.0.0.1:8000/hello')
        // axios 返回的对象中，真正的数据在 res.data 里
        // Object.assign(jsonData, res.data)
        jsonData.value = res.data.content
    } catch (error) {
        console.error("请求失败：", error)
    }
}

const getLoveMessage2 = async () => {
    try {
        const res = await axios.post(
            'http://127.0.0.1:8000/hello',
            { content: "qian_axios" }
        )
        jsonData.value = res.data.content
    } catch (error) {
        console.error("请求失败：", error)
    }
}


</script>

<template>
    <div>
        {{ jsonData }}
        <button @click="getLoveMessage1">axios_get</button>
        <button @click="getLoveMessage2">axios_post</button>
    </div>
</template>

<style scoped></style>