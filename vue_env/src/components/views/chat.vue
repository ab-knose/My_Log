<script setup lang="ts">
import HelloWorld from "./components/HelloWorld.vue";
import axios from "axios";
import { ref } from "vue";

const responseData = ref(null);

const fetchData = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/chats/single/user001"); // URLを適宜変更してください
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
