<template>
  <header v-if="showHeader">EPR編集</header>
  <main>
    <form @submit.prevent="saveEdit">
      <div class="form-row">
        <label>PJ Name</label>
        <input v-model="form.pjName" type="text" disabled />
      </div>
      <div class="form-row">
        <label>Start Date</label>
        <input v-model="form.startDate" type="date" disabled />
      </div>
      <div class="form-row">
        <label>Goal1</label>
        <input v-model="form.goal1" type="text" />
      </div>
      <div class="form-row">
        <label>Goal2</label>
        <input v-model="form.goal2" type="text" />
      </div>
      <div class="form-row">
        <label>Goal3</label>
        <input v-model="form.goal3" type="text" />
      </div>
      <div class="form-row">
        <label>Goal4</label>
        <input v-model="form.goal4" type="text" />
      </div>
      <div class="form-row">
        <label>Goal5</label>
        <input v-model="form.goal5" type="text" />
      </div>
      <div class="button-row">
        <button type="button" @click="cancelEdit">キャンセル</button>
        <button type="button" @click="resetEdit">リセット</button>
        <button type="submit">編集完了</button>
      </div>
    </form>
  </main>
</template>

<script setup lang="ts">
const user_id = window.sessionStorage.getItem("user_id"); 
import { useRouter } from 'vue-router';
import { reactive } from 'vue';
const router = useRouter();
const showHeader = true;

// 編集フォームの状態
const form = reactive({
  pjName: '',
  startDate: '',
  goal1: '',
  goal2: '',
  goal3: '',
  goal4: '',
  goal5: ''
});

// 初期値をsessionStorageから取得（なければ空）
const loadFromStorage = () => {
  const data = window.sessionStorage.getItem('EPR_DATA');
  if (data) {
    const parsed = JSON.parse(data);
    // 旧データ互換: date→startDate
    if (parsed.date && !parsed.startDate) parsed.startDate = parsed.date;
    Object.assign(form, parsed);
  }
};
loadFromStorage();

const saveEdit = () => {
  window.sessionStorage.setItem('EPR_DATA', JSON.stringify(form));
  router.push('/epref');
};
const cancelEdit = () => {
  router.push('/epref');
};
const resetEdit = () => {
  form.pjName = '';
  form.startDate = '';
  form.goal1 = '';
  form.goal2 = '';
  form.goal3 = '';
  form.goal4 = '';
  form.goal5 = '';
};
</script>

<style scoped>
main {
  min-height: 70vh;
}
.form-row {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.form-row label {
  width: 80px;
  font-weight: bold;
}
input[type="text"], input[type="date"] {
  flex: 1;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.button-row {
  display: flex;
  gap: 16px;
  margin-top: 20px;
}
button {
  padding: 8px 20px;
  border-radius: 8px;
  border: none;
  background: #4caf50;
  color: #fff;
  cursor: pointer;
  font-size: 1rem;
}
button:hover {
  background: #388e3c;
}
</style>
