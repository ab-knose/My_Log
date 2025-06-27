<template>
    <div class="term-eval-container">
        <div class="term-eval-card">
            <div>評価画面</div>
            <button>ボタン</button>
        </div>
    </div>
</template>

<script setup>
// ここにロジックを追加できます
</script>

<style scoped>
.term-eval-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f4f7fa;
}
.term-eval-card {
    width: 600px;
    min-width: 340px;
    max-width: 90vw;
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    padding: 48px 36px 36px 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
button {
    padding: 8px 16px;
    font-size: 16px;
    cursor: pointer;
}
</style>