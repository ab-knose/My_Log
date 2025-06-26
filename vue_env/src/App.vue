<template>
    <header>
      ヘッダー
    </header>
    <main style="min-height: 70vh; padding-bottom: 60px;">
      <RouterView />
    </main>
    <footer>
      <nav class="bottom-nav">
        <button @click="$router.push('/')">カレンダー</button>
        <button @click="$router.push('/chat')">チャット</button>
        <button @click="$router.push('/epref')">EPREF</button>
        <button @click="$router.push('/term_evaluation')">評価</button>
      </nav>
    </footer>
</template>

<script setup lang="ts">
// ...existing code...
</script>

<style scoped>
.bottom-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 0;
  background: #f0f0f0;
  border-top: 1px solid #ccc;
}
.bottom-nav button {
  flex: 1;
  margin: 0 4px;
  padding: 12px 0;
  border: none;
  background: #4caf50;
  color: #fff;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.bottom-nav button:hover {
  background: #388e3c;
}
main {
  min-height: 70vh;
  padding-bottom: 60px;
}
</style>