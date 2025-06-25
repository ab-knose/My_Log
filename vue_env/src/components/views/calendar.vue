<!-- filepath: c:\fy26-digital-dev-training-handson\group1_dev\My_Log\components\MyCalendar.vue -->
<template>
  <vue-cal
    style="height: 500px"
    :selected-date="selectedDate"
    :events="events"
    :disable-views="['years', 'year', 'week', 'day']"
     default-view="month"
    @cell-click="onCellClick"
  />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'

interface CalendarEvent {
  start: string
  end: string
  title: string
  class: string
}

export default defineComponent({
  components: { VueCal },
  setup() {
    const selectedDate = ref<Date>(new Date())
    const events = ref<CalendarEvent[]>([
      {
        start: '2025-06-21',
        end: '2025-06-21',
        title: '★マーク',
        class: 'marked-event'
      },
      {
        start: '2025-06-15',
        end: '2025-06-15',
        title: '✔',
        class: 'marked-event'
      }
    ])

    const onCellClick = ({ date }: { date: string }) => {
      alert(`${date} がクリックされました`)
    }

    return {
      selectedDate,
      events,
      onCellClick
    }
  }
})

const getLabeledData = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/chats/single/user001"); // URLを適宜変更してください
    responseData.value = response.data;
  } catch (error) {
    console.error(error);
    responseData.value = "エラーが発生しました";
  }
  return responseData.value;
};
</script>

<style>
/* マーク用のカスタムスタイル */
.marked-event {
  background: red !important;
  color: red !important;
  border-radius: 50%;
}
</style>