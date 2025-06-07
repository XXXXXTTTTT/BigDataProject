const express = require('express');
const axios = require('axios');
const router = express.Router();

// GET /proxy?url=xxx
router.get('/', async (req, res) => {
  const { url } = req.query;
  if (!url) {
    return res.status(400).send('Missing url');
  }
  try {
    const response = await axios.get(url, {
      responseType: 'stream',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });
    res.setHeader('Content-Type', response.headers['content-type'] || 'image/jpeg');
    response.data.pipe(res);
  } catch (err) {
    res.status(500).send('图片代理失败');
  }
});

module.exports = router; 