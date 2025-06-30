<template>
    <div class="term-eval-container">
        <div class="term-eval-card">
            <div class="date-range-row">
                <label>開始日</label>
                <input type="date" v-model="startDate" />
                <label>終了日</label>
                <input type="date" v-model="endDate" />
            </div>
            <button @click="showSummary">要約作成開始</button>
            <div v-if="summary" class="summary-box">{{ summary }}</div>
        </div>
    </div>
</template>

<script setup>
const user_id = window.sessionStorage.getItem("user_id"); 
import { ref } from 'vue';
const summary = ref("");
const startDate = ref("");
const endDate = ref("");
const showSummary = () => {
    summary.value = `これは仮の要約テキストです。期間: ${startDate.value || '未指定'} ～ ${endDate.value || '未指定'}`;
};
</script>

<style scoped>
.term-eval-container {
    height: 500px;
    min-height: 500px;
    max-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f4f7fa;
    border-radius: 8px;
}
.term-eval-card {
    width: 600px;
    min-width: 340px;
    max-width: 90vw;
    height: 500px;
    min-height: 500px;
    max-height: 500px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    padding: 48px 36px 36px 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.date-range-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}
.summary-box {
    margin-top: 24px;
    padding: 16px 20px;
    background: #f0f8ff;
    border-radius: 10px;
    color: #333;
    font-size: 1.1rem;
    width: 100%;
    text-align: left;
    box-sizing: border-box;
}
button {
    padding: 8px 16px;
    font-size: 16px;
    cursor: pointer;
}
</style>