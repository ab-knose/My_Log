import { createRouter, createWebHistory } from 'vue-router';
import Chat from '../views/chat.vue';
import Calendar from '../views/calendar.vue';
import EPREF from '../views/EPREF.vue';
import TermEvaluation from '../views/term_evaluation.vue';

const routes = [
    { path: '/', name: 'Calendar', component: Calendar },
  { path: '/chat', name: 'Chat', component: Chat },
  { path: '/epref', name: 'EPREF', component: EPREF },
  { path: '/term_evaluation', name: 'TermEvaluation', component: TermEvaluation },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
