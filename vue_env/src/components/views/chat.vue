<script setup lang="ts">
import { ref } from "vue";
import { onMounted } from 'vue';
import axios from "axios";
window.sessionStorage.setItem("user_id", "user001");// ユーザーIDをセッションストレージに保存
const user_id = window.sessionStorage.getItem("user_id"); // ユーザーIDを取得、なければデフォルト値を使用


// 初期化時にsessionStorageからmessagesを復元
const storedMessages = window.sessionStorage.getItem("messages");
const messages = ref<{ sender: string; text: string }[]>(storedMessages ? JSON.parse(storedMessages) : []);
const userInput = ref("");// ユーザーの入力を保持する

// TodaysChatsHistoryをセッションストレージから復元 or API取得
const storedHistory = window.sessionStorage.getItem("TodaysChatsHistory");
const TodaysChatsHistory = ref<{ sender: string; text: string }[]>(storedHistory ? JSON.parse(storedHistory) : []);

onMounted(async () => {
  if (!storedHistory) {
    const chats = await getTodaysChats(user_id as string);
    console.log('API返却値', chats); // ←ここでAPIの返却値を確認
    const chatArray = Array.isArray(chats?.chats) ? chats.chats : [];
    TodaysChatsHistory.value = chatArray.flatMap(c => [
      { sender: "user", text: c.user_prompt },
      { sender: "AI", text: c.AI_personalized_answer }
    ]);
    window.sessionStorage.setItem("TodaysChatsHistory", JSON.stringify(TodaysChatsHistory.value));
  }
});

// 今日の日付（YYYY-MM-DD形式）を取得
const today = new Date();
const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, '0');
const dd = String(today.getDate()).padStart(2, '0');
const start_date = `${yyyy}-${mm}-${dd}`;
// end_dateをstart_dateの1日後に設定
const nextDay = new Date(today);
nextDay.setDate(today.getDate() + 1);
const end_yyyy = nextDay.getFullYear();
const end_mm = String(nextDay.getMonth() + 1).padStart(2, '0');
const end_dd = String(nextDay.getDate()).padStart(2, '0');
const end_date = `${end_yyyy}-${end_mm}-${end_dd}`;
// APIから今日のチャット履歴を取得する関数
// ここでは、axiosを使用してGETリクエストを送信
async function getTodaysChats(user_id: string){
  try {
  const response = await axios.get(`http://127.0.0.1:8000/chats/${user_id}/2020-06-26_2025-06-27`);
    return response.data 
  }catch (error) {
    console.error(error)
  }
}

// 日時を "YYYY-MM-DDTHH:MM:SS" 形式で取得
// ここでは、現在の日時を取得してフォーマットする関数
const pad = (n: number) => n.toString().padStart(2, '0');

const sendMessage = async () => {
  if (userInput.value.trim() === "") return;
  messages.value.push({ sender: "user", text: userInput.value });
  window.sessionStorage.setItem("messages", JSON.stringify(messages.value));

  // 最新日時を生成
  const now = new Date();
  const date_time = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

  // 1. ユーザー発言をDB保存(API側でpost処理を実装)
  /*
  const postData = {
    user_id: user_id || "user001",
    date_time: date_time,
    user_prompt: userInput.value,
    AI_objective_answer: "samplesamplesamplesample",
    AI_personalized_answer: "samplesamplesamplesample"
  };
  try {
    await axios.post("http://127.0.0.1:8000/chats", postData);
  } catch (error) {
    messages.value.push({ sender: "AI", text: "会話内容がDBに保存されませんでした。" });
    window.sessionStorage.setItem("messages", JSON.stringify(messages.value));
    userInput.value = "";
    return;
  }
  */

  // 2. AI返答をAPIから取得
  const replyData = {
    user_id: user_id || "user001",
    date_time: date_time,
    user_prompt: userInput.value
  };
  try {
    const replyRes = await axios.post("http://127.0.0.1:8000/create_reply", replyData);
    const aiText = replyRes.data.AI_personalized_answer;
    messages.value.push({ sender: "AI", text: aiText });
    window.sessionStorage.setItem("messages", JSON.stringify(messages.value));
    // 3. AI返答もDB保存したい場合は下記を有効化(API側でpost処理を実装)
    /*
    const aiSaveData = {
      user_id: user_id || "user001",
      date_time: date_time,
      user_prompt: userInput.value,
      AI_objective_answer: "samplesamplesamplesample",
      AI_personalized_answer: aiText
    };
    await axios.post("http://127.0.0.1:8000/chats", aiSaveData);
    */
  } catch (error) {
    messages.value.push({ sender: "AI", text: "AI返答の取得に失敗しました。" });
    window.sessionStorage.setItem("messages", JSON.stringify(messages.value));
  }
  userInput.value = "";
};// a
</script>

<template>
  <div class="chat-container">
    <div class="todays-history">
      <h4>今日のチャット履歴</h4>
      <div class="messages">
        <div
          v-for="(msg, idx) in TodaysChatsHistory"
          :key="'history-' + idx"
          :class="['message', msg.sender]"
        >
          {{ msg.text }}
        </div>
      </div>
    </div>
    <div class="messages">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', msg.sender]"
      >
        {{ msg.text }}
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
.todays-history {
  margin-bottom: 16px;
  background: #f5f5f5;
  border-radius: 8px;
  padding: 8px 12px;
}
.todays-history h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  color: #388e3c;
}
.todays-history ul {
  margin: 0;
  padding-left: 18px;
}
.todays-history li {
  font-size: 0.95rem;
  color: #333;
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
