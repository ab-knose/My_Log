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
}

//vueカレンダーで必要な情報を使えるようにする
export default defineComponent({
  components: { VueCal },
  setup() {
    const labeledData = ref<string[]>([]) // APIから取得した振り返りを行った日付のリスト
    const events = ref<CalendarEvent[]>([]) // vueカレンダーで表示するイベントのリスト
    const selectedDate = ref<Date>(new Date()) // カレンダー上で選択された日付
    
    //振り返りを行った日付を取得＆vueカレンダーで表示する形式に変換
    onMounted(async () => {
      //TODO: ユーザーIDをログイン中のユーザのものに変更すること
      labeledData.value = await getLabeledData('user001')
      events.value = yearsToEventArray(labeledData.value)
    })

    //日付クリック時の処理
    const onCellClick = (date: string) => {
      alert(`${date} がクリックされました`)
    }

    return {
      selectedDate,
      events,
      onCellClick,
    }

  }
})

// APIから振り返りを行った日付を取得する関数
async function getLabeledData(user_id: string){
  try {
    const response = await axios.get(`http://127.0.0.1:8000/chats/labeled_dates/${user_id}`)
    return response.data 
  }catch (error) {
    console.error(error)
  }
  }

//APIから取得した日付をvueカレンダーで表示するための形式に変換
function yearsToEventArray(years: string[]): { start: string; end: string }[] {
  return years.map(year => ({
    start: year,
    end: year
  }));
}

</script>

<style>
/* マーク用のカスタムスタイル */
/* .marked-event {
  background: red !important;
  color: red !important;
  border-radius: 50%;
} */
</style>