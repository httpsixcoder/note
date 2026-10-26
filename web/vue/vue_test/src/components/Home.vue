<script setup>
 import {ref} from 'vue'
 import {useRoute,useRouter} from 'vue-router'
 let route =useRoute()
 let router = useRouter()
 //  并不是每次进入home页时,都有用户名参数传入
 //let username = route.query.username
 let username =window.localStorage.getItem('username'); 
 let logout= ()=>{
    // 清除localStorge中的username
    //window.sessionStorage.removeItem('username')
    window.localStorage.removeItem('username')
    // 动态路由到登录页
    router.push("/login")
 }
</script>
<template>
    <div>
        <h1>Home页面</h1>
        <h3>欢迎{{username}}登录</h3>
        <button @click="logout">退出登录</button>
    </div>
</template>
<style scoped>
</style>