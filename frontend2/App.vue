<template>
  <div class="app-container" :class="{ 'dark-mode': isDarkMode }">
    <!-- Header -->
    <header class="header">
      <div class="logo-container">
        <img src="/placeholder.svg?height=40&width=40" alt="Logo" class="logo" />
        <h1 class="site-title">DataBili</h1>
      </div>
      <div class="search-container">
        <div class="search-box">
          <input type="text" placeholder="Search data, charts, reports..." />
          <button class="search-button">
            <i class="icon"><SearchIcon /></i>
          </button>
        </div>
      </div>
      <div class="header-actions">
        <button class="theme-toggle" @click="toggleDarkMode">
          <SunIcon v-if="isDarkMode" />
          <MoonIcon v-else />
        </button>
        <div class="notification-icon">
          <BellIcon />
          <span class="notification-badge">3</span>
        </div>
        <div class="user-profile" @click="toggleUserMenu">
          <img src="/placeholder.svg?height=40&width=40" alt="User Avatar" class="avatar" />
          <div class="user-menu" v-if="isUserMenuOpen">
            <ul>
              <li><UserIcon /> Profile</li>
              <li><SettingsIcon /> Settings</li>
              <li><LogOutIcon /> Logout</li>
            </ul>
          </div>
        </div>
      </div>
    </header>

    <div class="main-container">
      <!-- Sidebar -->
      <aside class="sidebar" :class="{ 'collapsed': isSidebarCollapsed }">
        <button class="collapse-button" @click="toggleSidebar">
          <ChevronLeftIcon v-if="!isSidebarCollapsed" />
          <ChevronRightIcon v-else />
        </button>
        <nav class="sidebar-nav">
          <ul>
            <li class="active">
              <HomeIcon />
              <span v-if="!isSidebarCollapsed">Dashboard</span>
            </li>
            <li>
              <BarChartIcon />
              <span v-if="!isSidebarCollapsed">Analytics</span>
            </li>
            <li>
              <DatabaseIcon />
              <span v-if="!isSidebarCollapsed">Data Sources</span>
            </li>
            <li>
              <TableIcon />
              <span v-if="!isSidebarCollapsed">Tables</span>
            </li>
            <li>
              <FileTextIcon />
              <span v-if="!isSidebarCollapsed">Reports</span>
            </li>
            <li>
              <VideoIcon />
              <span v-if="!isSidebarCollapsed">Media</span>
            </li>
            <li>
              <UsersIcon />
              <span v-if="!isSidebarCollapsed">Users</span>
            </li>
            <li>
              <SettingsIcon />
              <span v-if="!isSidebarCollapsed">Settings</span>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="content">
        <div class="page-header">
          <h2>Dashboard Overview</h2>
          <div class="date-filter">
            <button class="date-button">
              <CalendarIcon />
              Last 7 Days
              <ChevronDownIcon />
            </button>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="stats-container">
          <div class="stat-card">
            <div class="stat-icon users">
              <UsersIcon />
            </div>
            <div class="stat-info">
              <h3>Total Users</h3>
              <p class="stat-value">2.4M</p>
              <p class="stat-change positive">+12.5% <ArrowUpIcon /></p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon views">
              <EyeIcon />
            </div>
            <div class="stat-info">
              <h3>Page Views</h3>
              <p class="stat-value">18.6M</p>
              <p class="stat-change positive">+8.2% <ArrowUpIcon /></p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon revenue">
              <DollarSignIcon />
            </div>
            <div class="stat-info">
              <h3>Revenue</h3>
              <p class="stat-value">$842K</p>
              <p class="stat-change positive">+5.3% <ArrowUpIcon /></p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon engagement">
              <ActivityIcon />
            </div>
            <div class="stat-info">
              <h3>Engagement</h3>
              <p class="stat-value">64.7%</p>
              <p class="stat-change negative">-2.1% <ArrowDownIcon /></p>
            </div>
          </div>
        </div>

        <!-- Charts Section -->
        <div class="charts-container">
          <div class="chart-card large">
            <div class="card-header">
              <h3>User Activity Trends</h3>
              <div class="card-actions">
                <button><RefreshCwIcon /></button>
                <button><MoreVerticalIcon /></button>
              </div>
            </div>
            <div class="chart-area">
              <LineChart :chartData="lineChartData" />
            </div>
          </div>
          <div class="chart-card">
            <div class="card-header">
              <h3>Traffic Sources</h3>
              <div class="card-actions">
                <button><RefreshCwIcon /></button>
                <button><MoreVerticalIcon /></button>
              </div>
            </div>
            <div class="chart-area">
              <DoughnutChart :chartData="doughnutChartData" />
            </div>
          </div>
          <div class="chart-card">
            <div class="card-header">
              <h3>Content Categories</h3>
              <div class="card-actions">
                <button><RefreshCwIcon /></button>
                <button><MoreVerticalIcon /></button>
              </div>
            </div>
            <div class="chart-area">
              <BarChart :chartData="barChartData" />
            </div>
          </div>
        </div>

        <!-- Data Table Section -->
        <div class="table-section">
          <div class="card-header">
            <h3>Recent Data Entries</h3>
            <div class="table-actions">
              <div class="search-filter">
                <input type="text" placeholder="Search entries..." />
                <SearchIcon />
              </div>
              <button class="filter-button">
                <FilterIcon />
                Filter
              </button>
              <button class="export-button">
                <DownloadIcon />
                Export
              </button>
            </div>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Title</th>
                  <th>Category</th>
                  <th>Views</th>
                  <th>Likes</th>
                  <th>Comments</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in tableData" :key="item.id">
                  <td>{{ item.id }}</td>
                  <td class="title-cell">
                    <img :src="item.thumbnail" :alt="item.title" class="thumbnail" />
                    <span>{{ item.title }}</span>
                  </td>
                  <td>
                    <span class="category-tag" :class="item.category.toLowerCase()">
                      {{ item.category }}
                    </span>
                  </td>
                  <td>{{ item.views }}</td>
                  <td>{{ item.likes }}</td>
                  <td>{{ item.comments }}</td>
                  <td>{{ item.date }}</td>
                  <td>
                    <div class="action-buttons">
                      <button><EditIcon /></button>
                      <button><TrashIcon /></button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div class="pagination">
              <button class="pagination-button"><ChevronLeftIcon /></button>
              <button class="pagination-number active">1</button>
              <button class="pagination-number">2</button>
              <button class="pagination-number">3</button>
              <span>...</span>
              <button class="pagination-number">10</button>
              <button class="pagination-button"><ChevronRightIcon /></button>
            </div>
          </div>
        </div>

        <!-- Media Gallery Section -->
        <div class="media-section">
          <div class="card-header">
            <h3>Media Gallery</h3>
            <div class="view-options">
              <button class="active"><GridIcon /></button>
              <button><ListIcon /></button>
            </div>
          </div>
          <div class="media-gallery">
            <div class="media-card" v-for="media in mediaData" :key="media.id">
              <div class="media-thumbnail">
                <img :src="media.thumbnail" :alt="media.title" />
                <div class="media-overlay">
                  <button class="play-button" v-if="media.type === 'video'">
                    <PlayIcon />
                  </button>
                  <button class="expand-button" v-else>
                    <MaximizeIcon />
                  </button>
                </div>
                <span class="media-duration" v-if="media.duration">{{ media.duration }}</span>
              </div>
              <div class="media-info">
                <h4>{{ media.title }}</h4>
                <div class="media-meta">
                  <span><EyeIcon /> {{ media.views }}</span>
                  <span><ThumbsUpIcon /> {{ media.likes }}</span>
                  <span><MessageSquareIcon /> {{ media.comments }}</span>
                </div>
              </div>
            </div>
          </div>
          <button class="load-more">Load More</button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { 
  Search as SearchIcon, 
  Bell as BellIcon, 
  User as UserIcon, 
  Settings as SettingsIcon, 
  LogOut as LogOutIcon,
  Home as HomeIcon,
  BarChart as BarChartIcon,
  Database as DatabaseIcon,
  Table as TableIcon,
  FileText as FileTextIcon,
  Video as VideoIcon,
  Users as UsersIcon,
  Calendar as CalendarIcon,
  ChevronDown as ChevronDownIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Eye as EyeIcon,
  DollarSign as DollarSignIcon,
  Activity as ActivityIcon,
  ArrowUp as ArrowUpIcon,
  ArrowDown as ArrowDownIcon,
  RefreshCw as RefreshCwIcon,
  MoreVertical as MoreVerticalIcon,
  Filter as FilterIcon,
  Download as DownloadIcon,
  Edit as EditIcon,
  Trash as TrashIcon,
  Grid as GridIcon,
  List as ListIcon,
  Play as PlayIcon,
  Maximize as MaximizeIcon,
  ThumbsUp as ThumbsUpIcon,
  MessageSquare as MessageSquareIcon,
  Sun as SunIcon,
  Moon as MoonIcon
} from 'lucide-vue-next';

// State
const isDarkMode = ref(false);
const isSidebarCollapsed = ref(false);
const isUserMenuOpen = ref(false);

// Toggle functions
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
};

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value;
};

// Chart data
const lineChartData = reactive({
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
  datasets: [
    {
      label: 'Active Users',
      data: [65, 59, 80, 81, 56, 55, 72],
      borderColor: '#FB7299',
      backgroundColor: 'rgba(251, 114, 153, 0.1)',
      tension: 0.4,
    },
    {
      label: 'New Registrations',
      data: [28, 48, 40, 19, 36, 27, 40],
      borderColor: '#23ADE5',
      backgroundColor: 'rgba(35, 173, 229, 0.1)',
      tension: 0.4,
    }
  ]
});

const doughnutChartData = reactive({
  labels: ['Direct', 'Social Media', 'Search', 'Referral', 'Email'],
  datasets: [
    {
      data: [30, 25, 20, 15, 10],
      backgroundColor: ['#FB7299', '#23ADE5', '#6D28D9', '#10B981', '#F59E0B'],
    }
  ]
});

const barChartData = reactive({
  labels: ['Gaming', 'Tech', 'Anime', 'Music', 'Lifestyle'],
  datasets: [
    {
      label: 'Views (millions)',
      data: [4.3, 2.8, 3.5, 2.1, 1.9],
      backgroundColor: '#FB7299',
    }
  ]
});

// Table data
const tableData = [
  { 
    id: 'VID-7829', 
    title: 'Big Data Processing with Apache Spark', 
    thumbnail: '/placeholder.svg?height=40&width=60', 
    category: 'Technology', 
    views: '1.2M', 
    likes: '45.2K', 
    comments: '3.8K', 
    date: '2023-10-15' 
  },
  { 
    id: 'VID-6547', 
    title: 'Machine Learning for Beginners', 
    thumbnail: '/placeholder.svg?height=40&width=60', 
    category: 'Education', 
    views: '892K', 
    likes: '32.1K', 
    comments: '2.7K', 
    date: '2023-10-12' 
  },
  { 
    id: 'VID-5432', 
    title: 'Data Visualization Techniques', 
    thumbnail: '/placeholder.svg?height=40&width=60', 
    category: 'Design', 
    views: '567K', 
    likes: '18.9K', 
    comments: '1.5K', 
    date: '2023-10-08' 
  },
  { 
    id: 'VID-4321', 
    title: 'SQL vs NoSQL: Choosing the Right Database', 
    thumbnail: '/placeholder.svg?height=40&width=60', 
    category: 'Technology', 
    views: '723K', 
    likes: '29.4K', 
    comments: '2.1K', 
    date: '2023-10-05' 
  },
  { 
    id: 'VID-3210', 
    title: 'Real-time Analytics Dashboard Creation', 
    thumbnail: '/placeholder.svg?height=40&width=60', 
    category: 'Design', 
    views: '456K', 
    likes: '15.7K', 
    comments: '1.2K', 
    date: '2023-10-01' 
  }
];

// Media gallery data
const mediaData = [
  {
    id: 1,
    type: 'video',
    title: 'Data Science Fundamentals',
    thumbnail: '/placeholder.svg?height=160&width=280',
    duration: '12:34',
    views: '1.2M',
    likes: '45K',
    comments: '3.8K'
  },
  {
    id: 2,
    type: 'video',
    title: 'Machine Learning Algorithms',
    thumbnail: '/placeholder.svg?height=160&width=280',
    duration: '18:22',
    views: '892K',
    likes: '32K',
    comments: '2.7K'
  },
  {
    id: 3,
    type: 'image',
    title: 'Data Visualization Infographic',
    thumbnail: '/placeholder.svg?height=160&width=280',
    views: '567K',
    likes: '19K',
    comments: '1.5K'
  },
  {
    id: 4,
    type: 'video',
    title: 'SQL Database Tutorial',
    thumbnail: '/placeholder.svg?height=160&width=280',
    duration: '22:15',
    views: '723K',
    likes: '29K',
    comments: '2.1K'
  },
  {
    id: 5,
    type: 'image',
    title: 'Analytics Dashboard Design',
    thumbnail: '/placeholder.svg?height=160&width=280',
    views: '456K',
    likes: '16K',
    comments: '1.2K'
  },
  {
    id: 6,
    type: 'video',
    title: 'Big Data Processing Techniques',
    thumbnail: '/placeholder.svg?height=160&width=280',
    duration: '15:48',
    views: '678K',
    likes: '24K',
    comments: '1.9K'
  }
];

// Chart components (simplified for this example)
const LineChart = {
  props: ['chartData'],
  template: `
    <div class="chart-container">
      <!-- This would be a real chart in production -->
      <div class="chart-placeholder line-chart">
        <div class="chart-lines">
          <div class="chart-line" v-for="(_, i) in 5" :key="i" :style="{ height: (20 + i * 20) + '%' }"></div>
        </div>
      </div>
    </div>
  `
};

const DoughnutChart = {
  props: ['chartData'],
  template: `
    <div class="chart-container">
      <!-- This would be a real chart in production -->
      <div class="chart-placeholder doughnut-chart">
        <div class="doughnut-segments">
          <div class="doughnut-segment" 
               v-for="(data, i) in chartData.datasets[0].data" 
               :key="i"
               :style="{ 
                 backgroundColor: chartData.datasets[0].backgroundColor[i],
                 transform: \`rotate(\${i * 72}deg)\`,
                 clipPath: 'polygon(50% 50%, 100% 0, 100% 100%, 50% 100%)'
               }">
          </div>
        </div>
      </div>
    </div>
  `
};

const BarChart = {
  props: ['chartData'],
  template: `
    <div class="chart-container">
      <!-- This would be a real chart in production -->
      <div class="chart-placeholder bar-chart">
        <div class="bar-container">
          <div class="chart-bar" 
               v-for="(data, i) in chartData.datasets[0].data" 
               :key="i"
               :style="{ 
                 height: (data / 5 * 100) + '%',
                 backgroundColor: chartData.datasets[0].backgroundColor
               }">
          </div>
        </div>
      </div>
    </div>
  `
};
</script>

<style>
/* Base Styles */
:root {
  --primary: #FB7299;
  --primary-light: rgba(251, 114, 153, 0.1);
  --secondary: #23ADE5;
  --secondary-light: rgba(35, 173, 229, 0.1);
  --background: #ffffff;
  --foreground: #111827;
  --muted: #f3f4f6;
  --muted-foreground: #6b7280;
  --card: #ffffff;
  --card-foreground: #111827;
  --border: #e5e7eb;
  --input: #e5e7eb;
  --ring: #FB7299;
  --radius: 0.5rem;
  --header-height: 64px;
  --sidebar-width: 240px;
  --sidebar-collapsed-width: 64px;
}

.dark-mode {
  --primary: #FB7299;
  --primary-light: rgba(251, 114, 153, 0.2);
  --secondary: #23ADE5;
  --secondary-light: rgba(35, 173, 229, 0.2);
  --background: #1f2937;
  --foreground: #f9fafb;
  --muted: #374151;
  --muted-foreground: #9ca3af;
  --card: #111827;
  --card-foreground: #f9fafb;
  --border: #374151;
  --input: #374151;
  --ring: #FB7299;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--background);
  color: var(--foreground);
  line-height: 1.5;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--background);
  color: var(--foreground);
}

/* Header Styles */
.header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  background-color: var(--card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo {
  height: 2rem;
  width: 2rem;
}

.site-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
}

.search-container {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 600px;
  margin: 0 2rem;
}

.search-box {
  position: relative;
  width: 100%;
}

.search-box input {
  width: 100%;
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border-radius: var(--radius);
  border: 1px solid var(--input);
  background-color: var(--muted);
  color: var(--foreground);
}

.search-button {
  position: absolute;
  left: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--muted-foreground);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-left: auto;
}

.theme-toggle {
  background: none;
  border: none;
  color: var(--foreground);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.theme-toggle:hover {
  background-color: var(--muted);
}

.notification-icon {
  position: relative;
  cursor: pointer;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: var(--primary);
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-profile {
  position: relative;
  cursor: pointer;
}

.avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--primary);
}

.user-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 200px;
  z-index: 10;
}

.user-menu ul {
  list-style: none;
  padding: 0.5rem 0;
}

.user-menu li {
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-menu li:hover {
  background-color: var(--muted);
}

/* Main Container Styles */
.main-container {
  display: flex;
  flex: 1;
  height: calc(100vh - var(--header-height));
}

/* Sidebar Styles */
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--card);
  border-right: 1px solid var(--border);
  transition: width 0.3s ease;
  position: relative;
  overflow-y: auto;
  height: 100%;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.collapse-button {
  position: absolute;
  top: 1rem;
  right: -12px;
  width: 24px;
  height: 24px;
  background-color: var(--primary);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  z-index: 10;
}

.sidebar-nav {
  padding: 1.5rem 0;
}

.sidebar-nav ul {
  list-style: none;
}

.sidebar-nav li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
  color: var(--muted-foreground);
}

.sidebar-nav li.active {
  background-color: var(--primary-light);
  color: var(--primary);
  font-weight: 500;
  position: relative;
}

.sidebar-nav li.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background-color: var(--primary);
}

.sidebar-nav li:hover:not(.active) {
  background-color: var(--muted);
}

/* Content Styles */
.content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
}

.date-filter {
  display: flex;
  align-items: center;
}

.date-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--foreground);
}

/* Stats Cards */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background-color: var(--card);
  border-radius: var(--radius);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon.users {
  background-color: var(--primary);
}

.stat-icon.views {
  background-color: var(--secondary);
}

.stat-icon.revenue {
  background-color: #10B981;
}

.stat-icon.engagement {
  background-color: #F59E0B;
}

.stat-info h3 {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-change {
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-change.positive {
  color: #10B981;
}

.stat-change.negative {
  color: #EF4444;
}

/* Charts Container */
.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.chart-card {
  background-color: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chart-card.large {
  grid-column: span 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
}

.card-header h3 {
  font-size: 1rem;
  font-weight: 600;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.card-actions button {
  background: none;
  border: none;
  color: var(--muted-foreground);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.card-actions button:hover {
  background-color: var(--muted);
  color: var(--foreground);
}

.chart-area {
  padding: 1.5rem;
  height: 300px;
}

/* Chart placeholders for demo */
.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  position: relative;
}

.chart-lines {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.chart-line {
  width: 100%;
  height: 1px;
  background-color: var(--border);
}

.line-chart::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60%;
  background: linear-gradient(to top, var(--primary-light), transparent);
  z-index: 1;
}

.line-chart::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--primary);
  z-index: 2;
  clip-path: polygon(
    0% 0%, 
    15% 50%, 
    30% 20%, 
    45% 60%, 
    60% 40%, 
    75% 60%, 
    90% 10%, 
    100% 30%, 
    100% 100%, 
    0% 100%
  );
}

.doughnut-chart {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
}

.doughnut-segments {
  width: 100%;
  height: 100%;
  position: relative;
}

.doughnut-segment {
  position: absolute;
  width: 100%;
  height: 100%;
  transform-origin: center;
}

.doughnut-chart::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60%;
  height: 60%;
  background-color: var(--card);
  border-radius: 50%;
}

.bar-chart {
  align-items: flex-end;
}

.bar-container {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  width: 100%;
  height: 100%;
  padding-top: 20px;
}

.chart-bar {
  width: 40px;
  background-color: var(--primary);
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

/* Table Section */
.table-section {
  background-color: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.table-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-filter {
  position: relative;
}

.search-filter input {
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border-radius: var(--radius);
  border: 1px solid var(--input);
  background-color: var(--muted);
  color: var(--foreground);
}

.search-filter svg {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--muted-foreground);
}

.filter-button, .export-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: var(--muted);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--foreground);
}

.export-button {
  background-color: var(--primary);
  color: white;
  border: none;
}

.data-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: var(--muted);
}

th, td {
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

th {
  font-weight: 600;
  color: var(--muted-foreground);
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.thumbnail {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
}

.category-tag {
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.category-tag.technology {
  background-color: var(--primary-light);
  color: var(--primary);
}

.category-tag.education {
  background-color: var(--secondary-light);
  color: var(--secondary);
}

.category-tag.design {
  background-color: rgba(124, 58, 237, 0.1);
  color: #7C3AED;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-buttons button {
  background: none;
  border: none;
  color: var(--muted-foreground);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.action-buttons button:hover {
  background-color: var(--muted);
  color: var(--foreground);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid var(--border);
}

.pagination-button, .pagination-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background-color: var(--card);
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-number.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
}

.pagination-button:hover, .pagination-number:hover:not(.active) {
  background-color: var(--muted);
}

/* Media Gallery */
.media-section {
  background-color: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.view-options {
  display: flex;
  gap: 0.5rem;
}

.view-options button {
  background: none;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.25rem;
  cursor: pointer;
  color: var(--muted-foreground);
}

.view-options button.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
}

.media-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.media-card {
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
}

.media-card:hover {
  transform: translateY(-5px);
}

.media-thumbnail {
  position: relative;
  height: 160px;
}

.media-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.media-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.media-thumbnail:hover .media-overlay {
  opacity: 1;
}

.play-button, .expand-button {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  border: 2px solid white;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.play-button:hover, .expand-button:hover {
  background-color: var(--primary);
  border-color: var(--primary);
  transform: scale(1.1);
}

.media-duration {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.media-info {
  padding: 1rem;
  background-color: var(--card);
}

.media-info h4 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.media-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

.media-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.load-more {
  display: block;
  margin: 0 auto 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: var(--muted);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--foreground);
  font-weight: 500;
  transition: all 0.2s;
}

.load-more:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart-card.large {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 50;
    height: 100vh;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.active {
    transform: translateX(0);
  }
  
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .media-gallery {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
}

@media (max-width: 640px) {
  .search-container {
    display: none;
  }
  
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .table-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .search-filter {
    width: 100%;
  }
  
  .search-filter input {
    width: 100%;
  }
}
</style>
