const express = require('express');
const router = express.Router();
const pool = require('../db');

// GET /api/hot-videos
router.get('/', async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT * FROM bilibili_hot_videos_server WHERE \`timestamp\` = (SELECT MAX(\`timestamp\`) FROM bilibili_hot_videos_server);`
    );
    res.json({ code: 0, data: rows });
  } catch (error) {
    console.error('数据库查询失败:', error);
    res.status(500).json({ code: 1, message: '服务器内部错误' });
  }
});

module.exports = router; 