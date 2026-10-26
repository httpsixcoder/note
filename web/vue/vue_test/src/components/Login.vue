<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
let username = ref('')
let password = ref('')
let router = useRouter();
let login = () => {
    console.log(username.value, password.value)
    if (username.value == 'root' & password.value == '123456') {
        router.push({ path: '/home', query: { 'username': username.value } })
        //登录成功利用前端存储机制，存储账号！
        localStorage.setItem('username', username.value)
        //sessionStorage.setItem('username',username)
    } else {
        alert('登录失败，账号或者密码错误！');
    }
}
import { definedPerson } from '../store/store';
//import  definedPerson  from '../store/store';//如果采用默认导出，请使用该行导入
// 读取存储的数据
let person = definedPerson()

</script>
<template>
    <div>
        账号： <input type="text" v-model="username" placeholder="请输入账号！"><br>
        密码： <input type="password" v-model="password" placeholder="请输入密码！"><br>
        <button @click="login()">登录</button>
        <button @click="person.doubleAge()">年龄加倍</button> <br>
    </div>
</template>
<style scoped></style>