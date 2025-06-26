import { createRouter, createWebHistory } from 'vue-router';
import Chat from '../components/views/chat.vue';
import Calendar from '../components/views/calendar.vue';
import EPREF from '../components/views/EPREF.vue';
import TermEvaluation from '../components/views/term_evaluation.vue';

const routes = [
    { path: '/calendar', name: 'Calendar', component: Calendar },
    { path: '/chat', name: 'Chat', component: Chat },
    { path: '/epref', name: 'EPREF', component: EPREF },
    { path: '/term_evaluation', name: 'TermEvaluation', component: TermEvaluation },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
