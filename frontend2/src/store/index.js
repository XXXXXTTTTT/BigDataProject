import { defineStore } from "pinia"

export const useAppStore = defineStore("app", {
  state: () => ({
    isDarkMode: false,
    isSidebarCollapsed: false,
    user: null,
    notifications: [
      { id: 1, title: "系统通知", message: "欢迎使用DataBili大数据平台", read: false, time: "2023-11-15 09:30" },
      { id: 2, title: "数据更新", message: "您的数据源已更新完成", read: false, time: "2023-11-14 14:45" },
      { id: 3, title: "报表生成", message: "每周数据报表已生成", read: false, time: "2023-11-13 18:20" },
    ],
  }),

  getters: {
    unreadNotificationsCount: (state) => {
      return state.notifications.filter((n) => !n.read).length
    },
  },

  actions: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
      localStorage.setItem("darkMode", this.isDarkMode)
    },

    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed
    },

    setUser(user) {
      this.user = user
    },

    logout() {
      this.user = null
    },

    markNotificationAsRead(id) {
      const notification = this.notifications.find((n) => n.id === id)
      if (notification) {
        notification.read = true
      }
    },
  },
})

export const useDataStore = defineStore("data", {
  state: () => ({
    lineChartData: {
      labels: ["1月", "2月", "3月", "4月", "5月", "6月", "7月"],
      datasets: [
        {
          label: "活跃用户",
          data: [65, 59, 80, 81, 56, 55, 72],
          borderColor: "#FB7299",
          backgroundColor: "rgba(251, 114, 153, 0.1)",
          tension: 0.4,
        },
        {
          label: "新注册用户",
          data: [28, 48, 40, 19, 36, 27, 40],
          borderColor: "#23ADE5",
          backgroundColor: "rgba(35, 173, 229, 0.1)",
          tension: 0.4,
        },
      ],
    },
    doughnutChartData: {
      labels: ["直接访问", "社交媒体", "搜索引擎", "外部链接", "邮件营销"],
      datasets: [
        {
          data: [30, 25, 20, 15, 10],
          backgroundColor: ["#FB7299", "#23ADE5", "#6D28D9", "#10B981", "#F59E0B"],
        },
      ],
    },
    barChartData: {
      labels: ["游戏", "科技", "动漫", "音乐", "生活"],
      datasets: [
        {
          label: "观看量（百万）",
          data: [4.3, 2.8, 3.5, 2.1, 1.9],
          backgroundColor: "#FB7299",
        },
      ],
    },
    tableData: [
      {
        id: "VID-7829",
        title: "使用Apache Spark进行大数据处理",
        thumbnail: "/placeholder.svg?height=40&width=60",
        category: "Technology",
        views: "1.2M",
        likes: "45.2K",
        comments: "3.8K",
        date: "2023-10-15",
      },
      {
        id: "VID-6547",
        title: "机器学习入门教程",
        thumbnail: "/placeholder.svg?height=40&width=60",
        category: "Education",
        views: "892K",
        likes: "32.1K",
        comments: "2.7K",
        date: "2023-10-12",
      },
      {
        id: "VID-5432",
        title: "数据可视化技术",
        thumbnail: "/placeholder.svg?height=40&width=60",
        category: "Design",
        views: "567K",
        likes: "18.9K",
        comments: "1.5K",
        date: "2023-10-08",
      },
      {
        id: "VID-4321",
        title: "SQL vs NoSQL：选择正确的数据库",
        thumbnail: "/placeholder.svg?height=40&width=60",
        category: "Technology",
        views: "723K",
        likes: "29.4K",
        comments: "2.1K",
        date: "2023-10-05",
      },
      {
        id: "VID-3210",
        title: "实时分析仪表板创建",
        thumbnail: "/placeholder.svg?height=40&width=60",
        category: "Design",
        views: "456K",
        likes: "15.7K",
        comments: "1.2K",
        date: "2023-10-01",
      },
    ],
    mediaData: [
      {
        id: 1,
        type: "video",
        title: "数据科学基础",
        thumbnail: "/placeholder.svg?height=160&width=280",
        duration: "12:34",
        views: "1.2M",
        likes: "45K",
        comments: "3.8K",
      },
      {
        id: 2,
        type: "video",
        title: "机器学习算法",
        thumbnail: "/placeholder.svg?height=160&width=280",
        duration: "18:22",
        views: "892K",
        likes: "32K",
        comments: "2.7K",
      },
      {
        id: 3,
        type: "image",
        title: "数据可视化信息图",
        thumbnail: "/placeholder.svg?height=160&width=280",
        views: "567K",
        likes: "19K",
        comments: "1.5K",
      },
      {
        id: 4,
        type: "video",
        title: "SQL数据库教程",
        thumbnail: "/placeholder.svg?height=160&width=280",
        duration: "22:15",
        views: "723K",
        likes: "29K",
        comments: "2.1K",
      },
      {
        id: 5,
        type: "image",
        title: "分析仪表板设计",
        thumbnail: "/placeholder.svg?height=160&width=280",
        views: "456K",
        likes: "16K",
        comments: "1.2K",
      },
      {
        id: 6,
        type: "video",
        title: "大数据处理技术",
        thumbnail: "/placeholder.svg?height=160&width=280",
        duration: "15:48",
        views: "678K",
        likes: "24K",
        comments: "1.9K",
      },
    ],
  }),

  actions: {
    async fetchData() {
      // 这里可以添加实际的API调用
      console.log("Fetching data from API...")
      // 模拟API延迟
      await new Promise((resolve) => setTimeout(resolve, 500))
      // 数据已经在state中预设
      return true
    },
  },
})
