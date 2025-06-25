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
import { defineComponent, ref, onMounted } from 'vue'
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
import axios from 'axios'

interface CalendarEvent {
  start: string
  end: string
  //title: string
  //class: string
}

export default defineComponent({
  components: { VueCal },
  setup() {
    const labeledData = ref<string[]>([])

    const getLabeledData = async (user_id: string) => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/chats/labeled_dates/${user_id}`)
        labeledData.value = response.data
        console.log('Labeled data:', labeledData.value) 
      } catch (error) {
        console.error(error)
      }
    }

    function yearsToEventArray(years: string[]): { start: string; end: string }[] {
      return years.map(year => ({
        start: year,
        end: year
      }));
    }

    const events = ref<CalendarEvent[]>([])

    onMounted(async () => {
      await getLabeledData('user001')
      events.value = yearsToEventArray(labeledData.value)
    })

    const selectedDate = ref<Date>(new Date())

    const onCellClick = ({ date }: { date: string }) => {
      alert(`${date} がクリックされました`)
    }
    console.log(events.value)
    return {
      selectedDate,
      events,
      onCellClick,
    }
  }
})
</script>

<style>
/* マーク用のカスタムスタイル */
.marked-event {
  background: red !important;
  color: red !important;
  border-radius: 50%;
}
</style>