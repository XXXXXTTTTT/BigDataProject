import { createRouter, createWebHistory } from "vue-router"
import Dashboard from "../views/Dashboard.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "dashboard",
      component: Dashboard,
    },
    {
      path: "/analytics",
      name: "analytics",
      component: () => import("../views/Analytics.vue"),
    },
    {
      path: "/data-sources",
      name: "data-sources",
      component: () => import("../views/DataSources.vue"),
    },
    {
      path: "/tables",
      name: "tables",
      component: () => import("../views/Tables.vue"),
    },
    {
      path: "/reports",
      name: "reports",
      component: () => import("../views/Reports.vue"),
    },
    {
      path: "/media",
      name: "media",
      component: () => import("../views/Media.vue"),
    },
    {
      path: "/users",
      name: "users",
      component: () => import("../views/Users.vue"),
    },
    {
      path: "/settings",
      name: "settings",
      component: () => import("../views/Settings.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/Login.vue"),
    },
    {
      path: "/hot-videos",
      name: "hot-videos",
      component: () => import("../views/HotVideos.vue"),
    },
    {
      path: "/user-tracking",
      name: "user-tracking",
      component: () => import("../views/UserTracking.vue"),
    },
    {
      path: "/up-select",
      name: "up-select",
      component: () => import("../views/UpSelect.vue"),
    },
    {
      path: '/up-analysis',
      name: 'UpAnalysis',
      component: () => import('@/views/UpAnalysis.vue')
    },
  ],
})

export default router
