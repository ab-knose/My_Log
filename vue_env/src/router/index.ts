import { createRouter, createWebHistory } from "vue-router";
import chat from "../components/views/chat.vue";

const routes = [
    { path: "/", component: chat },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;