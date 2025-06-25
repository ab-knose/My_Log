<script setup lang="ts">
import { ref } from "vue";

const userInput = ref("");// ユーザーの入力を保持する
const messages = ref<{ sender: string; text: string }[]>([]);// チャットメッセージのリストを保持する

const sendMessage = () => {
  if (userInput.value.trim() === "") return;
  messages.value.push({ sender: "user", text: userInput.value });
  setTimeout(() => {
    messages.value.push({ sender: "AI", text: "こんにちは！ご質問ありがとうございます。" });
  }, 500);
  userInput.value = "";
};
</script>

<template>
  <div class="chat-container">
    <div class="messages">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', msg.sender]"
      >
        {{ msg.text }}<!-- メッセージのテキスト -->
      </div>
    </div>
    <div class="input-area">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="メッセージを入力"
      />
      <button @click="sendMessage">送信</button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  max-width: 400px;
  margin: 40px auto;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  background: #fafafa;
}
.messages {
  min-height: 200px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.message {
  padding: 8px 12px;
  border-radius: 16px;
  max-width: 70%;
  word-break: break-all;
}
.message.user {
  align-self: flex-end;
  background: #d0f5c8;
}
.message.AI {
  align-self: flex-start;
  background: #e6e6e6;
}
.input-area {
  display: flex;
  gap: 8px;
}
input[type="text"], input {
  flex: 1;
  padding: 8px;
  border-radius: 16px;
  border: 1px solid #ccc;
}
button {
  padding: 8px 16px;
  border-radius: 16px;
  border: none;
  background: #4caf50;
  color: #fff;
  cursor: pointer;
}
button:hover {
  background: #388e3c;
}
</style>
