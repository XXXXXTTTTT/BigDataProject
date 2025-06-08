const express = require('express');
const router = express.Router();
const pool = require('../db');

// GET /api/hot-videos
router.get('/', async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT *
      FROM bilibili_hot_videos_server t1
      WHERE timestamp = (SELECT MAX(timestamp) FROM bilibili_hot_videos_server t2 WHERE t2.aid = t1.aid);
      `
    );
    res.json({ code: 0, data: rows });
  } catch (error) {
    console.error('数据库查询失败:', error);
    res.status(500).json({ code: 1, message: '服务器内部错误' });
  }
});

// GET /api/hot-videos/analyze/online-people
router.get('/analyze/online-people', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT 
        timestamp,
        COUNT(*) as video_count,
        SUM(
            CASE 
                WHEN real_time_all LIKE '%万+%' THEN 
                    CAST(REPLACE(REPLACE(real_time_all, '万+', ''), '+', '') AS DECIMAL(10,1)) * 10000
                WHEN real_time_all LIKE '%+%' THEN 
                    CAST(REPLACE(real_time_all, '+', '') AS DECIMAL(10,0))
                ELSE 
                    CAST(real_time_all AS DECIMAL(10,0))
            END
        ) as total_people,
        SUM(
            CASE 
                WHEN real_time_web LIKE '%万+%' THEN 
                    CAST(REPLACE(REPLACE(real_time_web, '万+', ''), '+', '') AS DECIMAL(10,1)) * 10000
                WHEN real_time_web LIKE '%+%' THEN 
                    CAST(REPLACE(real_time_web, '+', '') AS DECIMAL(10,0))
                ELSE 
                    CAST(real_time_web AS DECIMAL(10,0))
            END
        ) as total_people_web,
        AVG(
            CASE 
                WHEN real_time_all LIKE '%万+%' THEN 
                    CAST(REPLACE(REPLACE(real_time_all, '万+', ''), '+', '') AS DECIMAL(10,1)) * 10000
                WHEN real_time_all LIKE '%+%' THEN 
                    CAST(REPLACE(real_time_all, '+', '') AS DECIMAL(10,0))
                ELSE 
                    CAST(real_time_all AS DECIMAL(10,0))
            END
        ) as avg_people,
        AVG(
            CASE 
                WHEN real_time_web LIKE '%万+%' THEN 
                    CAST(REPLACE(REPLACE(real_time_web, '万+', ''), '+', '') AS DECIMAL(10,1)) * 10000
                WHEN real_time_web LIKE '%+%' THEN 
                    CAST(REPLACE(real_time_web, '+', '') AS DECIMAL(10,0))
                ELSE 
                    CAST(real_time_web AS DECIMAL(10,0))
            END
        ) as avg_people_web
      FROM bilibili_hot_videos_server 
      GROUP BY timestamp
      ORDER BY timestamp;
    `);
    res.json({ code: 0, data: rows });
  } catch (error) {
    console.error('数据库查询失败:', error);
    res.status(500).json({ code: 1, message: '服务器内部错误' });
  }
});


//GET /api/hot-videos/analyze/hot-tags
router.get('/analyze/hot-tags',async (req, res)=>{
  try {
    const [rows] = await pool.query(
      `SELECT aid, tags, title
      FROM bilibili_hot_videos_server t1
      WHERE timestamp = (
        SELECT MAX(timestamp) 
        FROM bilibili_hot_videos_server t2 
        WHERE t2.aid = t1.aid
      )
      ORDER BY aid;`
    )
    // 统计tag出现次数
    const tagCount = {};
    rows.forEach(row => {
      if (row.tags) {
        row.tags.split(',').forEach(tag => {
          tag = tag.trim();
          if (tag) {
            tagCount[tag] = (tagCount[tag] || 0) + 1;
          }
        });
      }
    });
    // 转为数组并排序，并过滤掉出现次数为1的tag
    const result = Object.entries(tagCount)
      .map(([tag, count]) => ({ tag, count }))
      .filter(item => item.count > 1)
      .sort((a, b) => b.count - a.count);
    res.json({ code:0, length:result.length, data: result });
  } catch (error) {
    console.error("hot-tags查询失败:",error);
    res.status(500).json({code:1,message:'服务器内部错误'});
  }
});

//GET /api/hot-videos/analyze/category
router.get('/analyze/category', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      WITH category_growth AS (
          SELECT 
              tname as category,
              aid,
              MAX(timestamp) as max_timestamp,
              MIN(timestamp) as min_timestamp,
              (MAX(timestamp) - MIN(timestamp)) / 3600.0 as time_diff_hours,
              MAX(stat_view) - MIN(stat_view) as view_growth,
              MAX(stat_like) - MIN(stat_like) as like_growth,
              MAX(stat_coin) - MIN(stat_coin) as coin_growth,
              MAX(stat_favorite) - MIN(stat_favorite) as favorite_growth,
              MAX(stat_share) - MIN(stat_share) as share_growth,
              MAX(stat_reply) - MIN(stat_reply) as reply_growth,
              MAX(stat_danmaku) - MIN(stat_danmaku) as danmaku_growth,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_view) - MIN(stat_view)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as view_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_like) - MIN(stat_like)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as like_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_coin) - MIN(stat_coin)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as coin_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_favorite) - MIN(stat_favorite)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as favorite_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_share) - MIN(stat_share)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as share_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_reply) - MIN(stat_reply)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as reply_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_danmaku) - MIN(stat_danmaku)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as danmaku_growth_per_hour,
              (SELECT stat_view FROM bilibili_hot_videos_server b 
               WHERE b.aid = bilibili_hot_videos_server.aid AND b.timestamp = MAX(bilibili_hot_videos_server.timestamp)) as latest_views
          FROM bilibili_hot_videos_server
          GROUP BY tname, aid
          HAVING COUNT(*) > 1
      )
      SELECT 
          category,
          COUNT(*) as unique_videos_with_growth,
          ROUND(AVG(time_diff_hours), 2) as avg_observation_hours,
          ROUND(AVG(view_growth_per_hour), 1) as avg_view_growth_per_hour,
          ROUND(AVG(like_growth_per_hour), 1) as avg_like_growth_per_hour,
          ROUND(AVG(coin_growth_per_hour), 1) as avg_coin_growth_per_hour,
          ROUND(AVG(favorite_growth_per_hour), 1) as avg_favorite_growth_per_hour,
          ROUND(AVG(share_growth_per_hour), 1) as avg_share_growth_per_hour,
          ROUND(AVG(reply_growth_per_hour), 1) as avg_reply_growth_per_hour,
          ROUND(AVG(danmaku_growth_per_hour), 1) as avg_danmaku_growth_per_hour
      FROM category_growth
      WHERE time_diff_hours > 0
      GROUP BY category
      ORDER BY avg_view_growth_per_hour DESC;
    `);
    res.json({ code: 0, data: rows });
  } catch (error) {
    console.error('category查询失败:', error);
    res.status(500).json({ code: 1, message: '服务器内部错误' });
  }
});

//GET /api/hot-videos/analyze/up-growth
router.get('/analyze/up-growth', async (req, res) => {
  try {
    // 第一步：up主增长数据
    const [dataRows] = await pool.query(`
      WITH up_growth AS (
          SELECT 
              owner_name,
              owner_mid,
              aid,
              COUNT(*) as appearances_per_video,
              (MAX(timestamp) - MIN(timestamp)) / 3600.0 as time_diff_hours,
              MAX(stat_view) - MIN(stat_view) as view_growth,
              MAX(stat_like) - MIN(stat_like) as like_growth,
              MAX(stat_coin) - MIN(stat_coin) as coin_growth,
              MAX(stat_favorite) - MIN(stat_favorite) as favorite_growth,
              MAX(stat_share) - MIN(stat_share) as share_growth,
              MAX(stat_reply) - MIN(stat_reply) as reply_growth
          FROM bilibili_hot_videos_server
          GROUP BY owner_name, owner_mid, aid
          HAVING COUNT(*) > 1
      )
      SELECT 
          owner_name,
          COUNT(*) as video_count,
          ROUND(AVG(time_diff_hours), 2) as avg_observation_hours,
          ROUND(AVG(view_growth / NULLIF(time_diff_hours, 0)), 1) as avg_view_growth_per_hour,
          ROUND(AVG(like_growth / NULLIF(time_diff_hours, 0)), 1) as avg_like_growth_per_hour,
          ROUND(AVG(coin_growth / NULLIF(time_diff_hours, 0)), 1) as avg_coin_growth_per_hour,
          ROUND(AVG(favorite_growth / NULLIF(time_diff_hours, 0)), 1) as avg_favorite_growth_per_hour,
          ROUND(AVG(share_growth / NULLIF(time_diff_hours, 0)), 1) as avg_share_growth_per_hour,
          ROUND(AVG(reply_growth / NULLIF(time_diff_hours, 0)), 1) as avg_reply_growth_per_hour
      FROM up_growth
      WHERE time_diff_hours > 0
      GROUP BY owner_name, owner_mid
      HAVING COUNT(*) >= 2
      ORDER BY video_count DESC
      LIMIT 100;
    `);
    // 第二步：获取最小和最大时间戳
    const [timeRows] = await pool.query(`
      SELECT 
        MIN(timestamp) AS min_timestamp,
        MAX(timestamp) AS max_timestamp
      FROM 
        bilibili_hot_videos_server;
    `);
    const { min_timestamp, max_timestamp } = timeRows[0] || {};
    res.json({ code: 0, min_timestamp, max_timestamp, data: dataRows });
  } catch (error) {
    console.error('up-growth查询失败:', error);
    res.status(500).json({ code: 1, message: '服务器内部错误' });
  }
});

//GET /api/hot-videos/analyze/video-types
router.get('/analyze/video-types', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      WITH video_growth AS (
          SELECT 
              aid,
              duration,
              MAX(timestamp) as max_timestamp,
              MIN(timestamp) as min_timestamp,
              (MAX(timestamp) - MIN(timestamp)) / 3600.0 as time_diff_hours,
              MAX(stat_view) - MIN(stat_view) as view_growth,
              MAX(stat_like) - MIN(stat_like) as like_growth,
              MAX(stat_coin) - MIN(stat_coin) as coin_growth,
              MAX(stat_favorite) - MIN(stat_favorite) as favorite_growth,
              MAX(stat_share) - MIN(stat_share) as share_growth,
              MAX(stat_reply) - MIN(stat_reply) as reply_growth,
              MAX(stat_danmaku) - MIN(stat_danmaku) as danmaku_growth,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_view) - MIN(stat_view)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as view_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_like) - MIN(stat_like)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as like_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_coin) - MIN(stat_coin)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as coin_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_favorite) - MIN(stat_favorite)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as favorite_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_share) - MIN(stat_share)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as share_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_reply) - MIN(stat_reply)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as reply_growth_per_hour,
              CASE 
                  WHEN (MAX(timestamp) - MIN(timestamp)) > 0 THEN
                      (MAX(stat_danmaku) - MIN(stat_danmaku)) / ((MAX(timestamp) - MIN(timestamp)) / 3600.0)
                  ELSE 0 
              END as danmaku_growth_per_hour
          FROM bilibili_hot_videos_server
          WHERE duration > 0
          GROUP BY aid, duration
          HAVING COUNT(*) > 1
      )
      SELECT 
          CASE 
              WHEN duration < 60 THEN '短视频(<1分钟)'
              WHEN duration < 300 THEN '短中视频(1-5分钟)'
              WHEN duration < 600 THEN '中等视频(5-10分钟)'
              WHEN duration < 1800 THEN '长视频(10-30分钟)'
              ELSE '超长视频(>30分钟)'
          END as duration_category,
          COUNT(*) as video_count,
          ROUND(AVG(time_diff_hours), 2) as avg_observation_hours,
          ROUND(AVG(view_growth_per_hour), 1) as view_hour,
          ROUND(AVG(like_growth_per_hour), 1) as like_hour,
          ROUND(AVG(coin_growth_per_hour), 1) as coin_hour,
          ROUND(AVG(favorite_growth_per_hour), 1) as favorite_hour,
          ROUND(AVG(share_growth_per_hour), 1) as share_hour,
          ROUND(AVG(reply_growth_per_hour), 1) as reply_hour,
          ROUND(AVG(danmaku_growth_per_hour), 1) as danmaku_hour
      FROM video_growth
      WHERE time_diff_hours > 0
      GROUP BY duration_category
      ORDER BY view_hour DESC;
    `);
    res.json({ code: 0, data: rows });
  } catch (error) {
    console.error('video-types查询失败:', error);
    res.status(500).json({ code: 1, message: '服务器内部错误' });
  }
});

//GET /api/hot-videos/analyze/video-info?aid=
router.get('/analyze/video-info', async (req, res) => {
  const aid = req.query.aid;
  if (!aid) {
    return res.status(400).json({ code: 1, message: '缺少参数aid' });
  }
  try {
    const [rows] = await pool.query(`
      SELECT
          timestamp,
          FROM_UNIXTIME(timestamp) as time_formatted,
          stat_view,
          stat_danmaku,
          stat_reply,
          stat_favorite,
          stat_coin,
          stat_share,
          stat_like,
          stat_view - LAG(stat_view) OVER (ORDER BY timestamp) as view_growth,
          stat_danmaku - LAG(stat_danmaku) OVER (ORDER BY timestamp) as danmaku_growth,
          stat_reply - LAG(stat_reply) OVER (ORDER BY timestamp) as reply_growth,
          stat_like - LAG(stat_like) OVER (ORDER BY timestamp) as like_growth
      FROM bilibili_hot_videos_server 
      WHERE aid = ?
      ORDER BY timestamp;
    `, [aid]);
    res.json({ code: 0, data: rows });
  } catch (error) {
    console.error('video-info查询失败:', error);
    res.status(500).json({ code: 1, message: '服务器内部错误' });
  }
});

module.exports = router; 