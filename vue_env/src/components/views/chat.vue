<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
//window.sessionStorage.setItem("user_id", "user001");// ユーザーIDをセッションストレージに保存

const userInput = ref("");// ユーザーの入力を保持する
const messages = ref<{ sender: string; text: string }[]>([]);// チャットメッセージのリストを保持する

// 日時を "YYYY-MM-DDTHH:MM:SS" 形式で取得
// ここでは、現在の日時を取得してフォーマットする関数を定
const pad = (n: number) => n.toString().padStart(2, '0');

const sendMessage = async () => {
  if (userInput.value.trim() === "") return;
  messages.value.push({ sender: "user", text: userInput.value });

  // ボタンを押すたびに最新日時を生成
  const now = new Date();
  const date_time = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

  // POSTするデータ
  const postData = {
    user_id: "user001",
    date_time: date_time, // 最新の日時
    user_prompt: userInput.value,
    AI_objective_answer: "samplesamplesamplesample",
    AI_personalized_answer: "samplesamplesamplesample"
  };

  try {
    await axios.post("http://127.0.0.1:8000/chats", postData);
    setTimeout(() => {
      messages.value.push({ sender: "AI", text: "DBに保存しました。" });
    }, 500);
  } catch (error) {
    messages.value.push({ sender: "AI", text: "会話内容がDBに保存されませんでした。" });
  }
  userInput.value = "";
};// a
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
