<script setup lang="ts">
import HelloWorld from "./components/HelloWorld.vue";
import axios from "axios";
import { ref } from "vue";

const responseData = ref(null);

const fetchData = async () => {
  try {
    const response = await axios.get("http://localhost:51731/"); // URLを適宜変更してください
    responseData.value = response.data;
  } catch (error) {
    console.error(error);
    responseData.value = "エラーが発生しました";
  }
};
</script>

<template>
  <button @click="fetchData">GETリクエスト送信</button>
  <div v-if="responseData">
    {{ responseData }}
  </div>
</template>
