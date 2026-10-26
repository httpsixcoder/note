<script setup>
import { ref } from "vue";
let userarr = ref([
  { id: 1, name: "张三", age: 18 },
  { id: 2, name: "李四", age: 20 },
  { id: 3, name: "王五", age: 22 },
  { id: 4, name: "赵六", age: 24 }
])

</script>

<template>
  <div>

    <table border="1">
      <tr>
        <th>id</th>
        <th>姓名</th>
        <th>年龄</th>
      </tr>
      <tr v-for="user in userarr" :key="user.id">
        <td>{{ user.id }}</td>
        <td>{{ user.name }}</td>
        <td>{{ user.age }}</td>
      </tr>
    </table>

  </div>
</template>

<style scoped>
th,
td {
  width: 100px;
  padding: 10px;
}
</style>