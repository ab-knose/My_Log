import { createRouter, createWebHistory } from "vue-router";
import chat from "../components/views/chat.vue";
import calendar from "../components/views/calendar.vue";


const routes = [
    { path: "/", component: chat },
    { path: "/calendar", component: calendar },

];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;