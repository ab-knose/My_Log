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

const USER_ID = 'user001' // ユーザーIDを定義（後でログイン中のユーザのものに変更すること）
const API_URL = 'http://127.0.0.1:8000'

//vueカレンダーで必要な情報を使えるようにする
export default defineComponent({
  components: { VueCal },
  setup() {
    const labeledData = ref<string[]>([]) // APIから取得した振り返りを行った日付のリスト
    const events = ref<CalendarEvent[]>([]) // vueカレンダーで表示するイベントのリスト
    const selectedDate = ref<Date>(new Date()) // カレンダー上で選択された日付
    
    //振り返りを行った日付を取得＆vueカレンダーで表示する形式に変換
    onMounted(async () => {
      labeledData.value = await getLabeledData(USER_ID)
      events.value = yearsToEventArray(labeledData.value)

      //quiz
      getLastQuizAnswerDate(USER_ID).then(lastAnswerDate => {
        // 最終クイズ回答日が今日でなければクイズ表示
        let today = new Date()
        let formattedTodayDate = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
        if (lastAnswerDate != formattedTodayDate) {
          alert(`最終クイズ回答日と一致`)
        } else {
          alert(`最終クイズ回答日と一致しません`)
        }

        //クイズ回答日を更新
        putLastQuizAnswereDate(USER_ID).then(() => {
          console.log('クイズ回答日を更新しました')
        })
      })
    })

    //日付クリック時の処理
    const onCellClick = (date: string) => {
      getSummary(USER_ID, date).then(summary => {
        console.log(summary.summaries[0]) //TODO: 二行下で使うために確認
        if (summary) {
          alert(`${USER_ID}: ${date} の振り返り内容は ${summary.summaries[0].summary}`)
        } else {
          alert(`${USER_ID}: ${date} の振り返り内容はありません`)
        }
      }) 
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
    const response = await axios.get(`${API_URL}/chats/labeled_dates/${user_id}`)
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

//要約を取得
async function getSummary(user_id: string, date: string) {
  try {
    //const response = await axios.get(`${API_URL}/summaries/${user_id}/${date}-${date}`)
    const response = await axios.get(`${API_URL}/summaries/${user_id}`)
    return response.data
  } catch (error) {
    console.error(error)
  }
}

//クイズ回答日を取得
async function getLastQuizAnswerDate(user_id: string) {
  try {
    const response = await axios.get(`${API_URL}/quiz/last_answeredate/${user_id}`)
    return response.data
  } catch (error) {
    console.error(error)
  }
}

async function putLastQuizAnswereDate(user_id: string) {
  const userData = {id: user_id}
  try {
    const response = await axios.put(`${API_URL}/quiz/last_answeredate/${user_id}`, userData)
    return response.data
  } catch (error) {
    console.error(error)
  }
}

//クイズを取得
async function getQuiz(){
  try{
    const response = await axios.get(`${API_URL}/quiz`)
    return response.data
  } catch (error) {
    console.error(error)
  }
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