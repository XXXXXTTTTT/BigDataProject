# DataBili - Bilibili风格大数据可视化平台

一个基于Vue 3和Vite构建的现代化大数据可视化平台，采用Bilibili的设计风格。

# 安装依赖
`npm install`

# 启动开发服务器
`npm run dev`

# 构建生产版本
`npm run build`

# 预览生产版本
`npm run preview`

##  项目结构


src/
├── assets/          # 静态资源
├── components/      # 可复用组件
│   ├── Header.vue
│   ├── Sidebar.vue
│   ├── StatCard.vue
│   ├── ChartCard.vue
│   ├── DataTable.vue
│   └── MediaGallery.vue
├── router/          # 路由配置
├── store/           # Pinia状态管理
├── views/           # 页面组件
│   ├── Dashboard.vue
│   ├── UpSelect.vue
│   ├── UpAnalysis.vue
│   └── HotVideos.vue
├── App.vue          # 根组件
└── main.js          # 应用入口

## 主要页面

### 1. 首页(Dashboard)
- 项目总览概况

- 数据汇总统计

  

### 2. Up主查询 (UpSelect)
- 可按UID或模糊名称搜索和筛选已爬UP主

- 点击UP卡片可跳转至B站UP主页

- 分页展示UP主信息

  

### 3. Up主分析 (UpAnalysis)
- 分析Up主聚类结果将UP主分为大V， 潜力UP, 普通UP三类

- 根据三类进行数据统计分析图表展示

  

### 4. 热门视频总览(HotVideos)
- 展示爬取的热门视频(1h更新一次)
- 分页展示
- 可点击直接进入B站视频详细页

### 5.用户追踪(UserTrack)

- 输入b站点用户的uid,点击开始分析,向后端发送请求
- 后端接收uid,获取用户评论
- 分析用户互动活跃的时间
- 统计用户评论词云
- 使用Deepseek分析用户标签
- 使用Deepseek给出用户评论评分
- 使用Deepseek给出用户兴趣预测





