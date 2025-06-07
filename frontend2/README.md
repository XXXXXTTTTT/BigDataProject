# DataBili - Bilibili风格大数据可视化平台

一个基于Vue 3和Vite构建的现代化大数据可视化平台，采用Bilibili的设计风格。

## 🚀 特性

- **现代化技术栈**: Vue 3 + Vite + Pinia + Vue Router
- **响应式设计**: 适配桌面端、平板和移动设备
- **Bilibili风格**: 采用Bilibili的粉色/蓝色配色方案
- **数据可视化**: 支持多种图表类型（折线图、饼图、柱状图）
- **交互式表格**: 支持搜索、排序、分页和导出功能
- **媒体库**: 支持图片和视频的展示和管理
- **暗黑模式**: 支持明暗主题切换
- **用户认证**: 包含登录和用户管理功能
- **模块化组件**: 易于扩展和自定义

## 📦 安装

\`\`\`bash
# 克隆项目
git clone <repository-url>
cd bilibili-data-platform

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
\`\`\`

## 🏗️ 项目结构

\`\`\`
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
│   ├── Analytics.vue
│   ├── Login.vue
│   └── ...
├── App.vue          # 根组件
└── main.js          # 应用入口
\`\`\`

## 🎨 主要组件

### 1. 仪表盘 (Dashboard)
- 统计卡片显示关键指标
- 多种图表展示数据趋势
- 数据表格管理
- 媒体库展示

### 2. 数据表格 (DataTable)
- 搜索和筛选功能
- 排序和分页
- 数据导出
- 自定义列模板

### 3. 图表组件 (ChartCard)
- 支持多种图表类型
- 响应式设计
- 数据刷新功能
- 可配置的图表选项

### 4. 媒体库 (MediaGallery)
- 网格和列表视图切换
- 图片和视频支持
- 悬停效果和交互
- 懒加载支持

## 🔧 自定义配置

### 主题配置
在 `src/assets/main.css` 中修改CSS变量来自定义主题：

\`\`\`css
:root {
  --primary: #FB7299;        /* 主色调 */
  --secondary: #23ADE5;      /* 次要色调 */
  --background: #ffffff;     /* 背景色 */
  --foreground: #111827;     /* 前景色 */
  /* ... 更多变量 */
}
\`\`\`

### 添加新页面
1. 在 `src/views/` 中创建新的Vue组件
2. 在 `src/router/index.js` 中添加路由配置
3. 在 `src/components/Sidebar.vue` 中添加导航菜单项

### 集成真实图表库
替换示例图表组件为真实的图表库（如ECharts或Chart.js）：

\`\`\`bash
# 安装ECharts
npm install echarts vue-echarts

# 或安装Chart.js
npm install chart.js vue-chartjs
\`\`\`

## 📊 数据管理

项目使用Pinia进行状态管理，包含两个主要store：

- `useAppStore`: 应用全局状态（主题、用户信息、通知等）
- `useDataStore`: 数据相关状态（图表数据、表格数据、媒体数据等）

## 🌐 API集成

在生产环境中，您需要：

1. 替换模拟数据为真实API调用
2. 添加错误处理和加载状态
3. 实现用户认证和授权
4. 添加数据缓存机制

## 📱 响应式设计

项目采用移动优先的响应式设计：

- **桌面端**: 完整的侧边栏和多列布局
- **平板**: 自适应的网格布局
- **移动端**: 折叠式侧边栏和单列布局

## 🔒 安全考虑

- 实现适当的用户认证和授权
- 验证所有用户输入
- 使用HTTPS进行数据传输
- 实施CSRF保护

## 🚀 部署

### Vercel部署
\`\`\`bash
npm run build
# 将dist文件夹部署到Vercel
\`\`\`

### Nginx部署
\`\`\`bash
npm run build
# 将dist文件夹内容复制到Nginx服务器
\`\`\`

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 支持

如果您有任何问题或建议，请创建一个Issue或联系开发团队。
