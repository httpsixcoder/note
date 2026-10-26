<script setup>
import { ref } from 'vue'
let num = ref(1)
let message = "message"
let but_click = () => {
    num.value++
}
let ul_test = ref([
    { name: "张三", age: 18 },
    { name: "李四", age: 20 },
    { name: "王五", age: 22 }
])
let omdel_test = ref("123")
let slot_test = ref("slot_test")

</script>

<template>
    <div>
        <h1>插值表达式：</h1>
        {{ message }}
        <hr>
        <h1>事件点击</h1>
        <input type="button" value="事件" @click="but_click()">
        <br>
        <input type="button" value="事件once" @click.once="but_click()">
        <br>
        <input type="button" value="事件prevent(防止事件冒泡)" @click.prevent="but_click()">
        <hr>
        <h1>响应式 ref</h1>
        {{ num }}
        <hr>
        <h1>条件渲染</h1>
        <div v-if="num < 5">小于5</div>
        <div v-else-if="num > 5">大于5 整个div是否存在</div>
        <div v-else>等于5</div>
        <div v-show="num == 3">等于3 dispaly 属性修改</div>
        <hr>
        <h1>列表渲染</h1>
        <ul>
            <li v-for="item in ul_test" :key="item.name">
                {{ item.name }} - {{ item.age }}
            </li>
        </ul>
        <hr>
        <h1>双向绑定 v-model</h1>
        {{ omdel_test }}
        <input type="text" v-model="omdel_test">

        <hr>
        <h1>生命周期</h1>
        <p>初始化前：beforeCreate，初始化后：created</p>
        <p>挂载前：beforeMount，挂载后：mounted</p>
        <p>更新前：beforeUpdate，更新后：updated</p>
        <p>销毁前：beforeUnmount，销毁后：unmounted</p>
        <hr>
        <hr>
    </div>
</template>

<style scoped></style>