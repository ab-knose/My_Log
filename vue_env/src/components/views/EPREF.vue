<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user_id = window.sessionStorage.getItem("user_id");
console.log(user_id);

const router = useRouter();
const goToEdit = () => {
  router.push('/epr_edit');
};
const goToMake = () => {
  router.push('/epr_make');
};

const eprData = ref({
  pjName: '',
  startDate: '',
  goal1: '',
  goal2: '',
  goal3: '',
  goal4: '',
  goal5: ''
});

onMounted(async () => {
  const data = window.sessionStorage.getItem('EPR_DATA');
  if (data) {
    const parsed = JSON.parse(data);
    // 旧データ互換: pjNo→pjName, date→startDate
    if (parsed.pjNo && !parsed.pjName) parsed.pjName = parsed.pjNo;
    if (parsed.date && !parsed.startDate) parsed.startDate = parsed.date;
    Object.assign(eprData.value, parsed);
  } else if (user_id) {
    // sessionStorageがなければAPIから取得
    try {
      const res = await axios.get('http://127.0.0.1:8000/epr');
      // user_idが一致する最新EPRを取得
      const userEprs = Array.isArray(res.data) ? res.data.filter(epr => epr.user_id === user_id) : [];
      if (userEprs.length > 0) {
        // start_date降順で最新を取得（string→Date型で比較）
        userEprs.sort((a, b) => new Date(String(b.start_date)).getTime() - new Date(String(a.start_date)).getTime());
        const latest = userEprs[0];
        eprData.value = {
          pjName: latest.project_name,
          startDate: latest.start_date,
          goal1: latest.goal1 || '',
          goal2: latest.goal2 || '',
          goal3: latest.goal3 || '',
          goal4: latest.goal4 || '',
          goal5: latest.goal5 || ''
        };
      }
    } catch (err) {
      console.error('EPR取得失敗', err);
    }
  }
});
</script>

<template>
  <div class="epref-container">
    <div class="half upper">
      <div class="upper-header">
        <h2>EPR</h2>
        <div>
          <button class="edit-btn" @click="goToEdit">編集</button>
          <button class="new-btn" @click="goToMake">新規</button>
        </div>
      </div>
      <table>
        <tr><th>項目</th><th>値</th></tr>
        <tr><td>PJ Name</td><td>{{ eprData.pjName }}</td></tr>
        <tr><td>Start Date</td><td>{{ eprData.startDate }}</td></tr>
        <tr><td>Goal1</td><td>{{ eprData.goal1 }}</td></tr>
        <tr><td>Goal2</td><td>{{ eprData.goal2 }}</td></tr>
        <tr><td>Goal3</td><td>{{ eprData.goal3 }}</td></tr>
        <tr><td>Goal4</td><td>{{ eprData.goal4 }}</td></tr>
        <tr><td>Goal5</td><td>{{ eprData.goal5 }}</td></tr>
      </table>
    </div>
    <div class="half lower">
      <h2>EF</h2>
      <table>
        <tr><th>項目</th><th>値</th></tr>
        <tr><td>例A</td><td>データA</td></tr>
        <tr><td>例B</td><td>データB</td></tr>
      </table>
    </div>
  </div>
</template>

<style scoped>
.epref-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  background: #f4f7fa;
  overflow-y: auto;
  overflow-x: hidden; /* 横スクロール禁止 */
  padding-bottom: 32px; /* フッター分の余白 */
}
.half {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.upper, .lower {
  width: 600px;
  min-width: 340px;
  max-width: 90vw;
  margin: 32px auto 0 auto;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  background: #fff;
  padding: 32px 36px 24px 36px;
  box-sizing: border-box;
}
table {
  border-collapse: collapse;
  margin-top: 8px;
  width: 100%;
  table-layout: fixed;
}
th, td {
  border: 1px solid #888;
  padding: 6px 16px;
  text-align: left;
}
th, td:first-child {
  width: 120px;
  min-width: 80px;
  max-width: 160px;
  white-space: nowrap;
}
td:last-child {
  width: auto;
  word-break: break-all;
}
.upper {
  border-bottom: 1px solid #ccc;
  background: #f8f8ff;
  position: relative;
}
.upper-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  box-sizing: border-box;
}
.edit-btn {
  padding: 6px 16px;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  background: #4caf50;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
  margin-right: 8px;
}
.edit-btn:hover {
  background: #388e3c;
}
.new-btn {
  padding: 6px 16px;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  background: #2196f3;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}
.new-btn:hover {
  background: #1565c0;
}
.lower {
  background: #f0f8ff;
}
</style>
