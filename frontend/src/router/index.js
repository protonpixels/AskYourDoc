import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: () => import("@/pages/HomePage.vue"),
    },
    {
      path: "/info",
      name: "InfoPage",
      component: () => import("@/pages/InfoPage.vue"),
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0, behavior: "smooth" };
  },
});

export default router;
