const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: '114.116.251.42',
  port: 3306,
  user: 'remote',
  password: '123456',
  database: 'bilibili',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

module.exports = pool; 