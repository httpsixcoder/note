<script setup>



import AxiosTest from './components/AxiosTest.vue'
import { useRouter } from 'vue-router'
import { definedPerson } from './store/store';
//创建动态路由对象
let router = useRouter()
let showList = () => {
  router.push({ path: '/base' })
}
let showDetail = (mse) => {
  router.push({ name: "Router_pro1", params: { mse: mse } })
}
let showDetail2 = (mse) => {
  /*uri键值对参数,需要使用query */
  router.push({ path: "/router2", query: { mse: mse } })
}
//import  definedPerson  from '../store/store';//如果采用默认导出，请使用该行导入
// 读取存储的数据
let person = definedPerson()


</script>

<template>

  <div>
    <h1>App页面</h1>
    <h1>Axios</h1>
    <AxiosTest />

    <h1>pinia</h1>
    读取姓名:{{ person.username }} <br>
    读取年龄:{{ person.age }} <br>
    <hr />
    <!-- 路由的连接 -->
    <h1>声明式路由：</h1>
    <router-link to="/base">基础</router-link> &nbsp;
    <router-link to="/666">666重定向</router-link> &nbsp;

    <router-link to="/props">传值</router-link>

    <!-- <hr> Base视图展示:<router-view name="homeView"></router-view> -->
    <!-- 动态输入路径,点击按钮,触发单击事件的函数,在函数中通过编程是路由切换页面 -->
    <hr>
    <h1>编程式路由</h1>
    <button @click="showList()">showBase</button> <br>
    <hr>
    <!-- 路由连接对应视图的展示位置 -->
    默认展示位置:<router-view></router-view>
    <hr>
    <h1>路由守卫，路由传参</h1>
    <!-- 路径参数   -->
    <router-link to="/router/Web1">路径传参</router-link>
    <button @click="showDetail('Web2')">编程式路由路径传参显示</button>
    <hr />
    <!-- 键值对参数 -->
    <router-link v-bind:to="{ path: '/router2', query: { mse: 'Py1' } }">键值对传参JAVA</router-link>
    <button @click="showDetail2('Py2')">编程式路由键值对传参JAVA</button>
    <hr> showDetail视图展示:<router-view name="showDetailView"></router-view>
    <hr> showDetail2视图展示:<router-view name="showDetailView2"></router-view>
    <hr>
    <hr>


  </div>
</template>
