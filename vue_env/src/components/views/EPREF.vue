<script setup lang="ts">
const user_id = window.sessionStorage.getItem("user_id");
console.log(user_id);
</script>

<template>
  <div class="epref-container">
    <div class="half upper">
      <div class="upper-header">
        <h2>EPR</h2>
        <button class="edit-btn">編集</button>
      </div>
      <table>
        <tr><th>項目</th><th>値</th></tr>
        <tr><td>PJ No.</td><td>XXX</td></tr>
        <tr><td>Date</td><td>XXX</td></tr>
        <tr><td>Goal1</td><td>XXX</td></tr>
        <tr><td>Goal2</td><td>XXX</td></tr>
        <tr><td>Goal3</td><td>XXX</td></tr>
        <tr><td>Goal4</td><td>XXX</td></tr>
        <tr><td>Goal5</td><td>XXX</td></tr>
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
  height: 100vh;
}
.half {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
}
.edit-btn:hover {
  background: #388e3c;
}
.lower {
  background: #f0f8ff;
}
table {
  border-collapse: collapse;
  margin-top: 8px;
}
th, td {
  border: 1px solid #888;
  padding: 6px 16px;
}
</style>
