const express = require('express');
const cors = require('cors');
const hotVideosRouter = require('./routes/hotVideos');
const proxyRouter = require('./routes/proxy');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// 路由
app.use('/api/hot-videos', hotVideosRouter);
app.use('/proxy', proxyRouter);

// 404处理
app.use((req, res) => {
  res.status(404).json({ message: '接口不存在' });
});

app.listen(PORT, () => {
  console.log(`服务器已启动，端口：${PORT}`);
}); 