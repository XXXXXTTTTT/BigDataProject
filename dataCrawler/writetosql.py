import pymysql

def insert_bilibili_data(data, host='localhost', port=3306, user='root', password='123456', database='bilibili'):
    """
    插入B站视频数据到数据库
    
    Args:
        data: 包含timestamp、formatted_time和data字段的字典
        host, port, user, password, database: 数据库连接参数
        
    Returns:
        bool: 插入是否成功
    """
    connection = None
    try:
        # 连接数据库
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # 检查表是否存在，不存在则创建
            cursor.execute("SHOW TABLES LIKE 'bilibili_videos'")
            if not cursor.fetchone():
                create_table_sql = """
                CREATE TABLE bilibili_videos (
                    timestamp BIGINT NOT NULL,
                    aid BIGINT NOT NULL,
                    videos INT,
                    tid INT,
                    tname VARCHAR(50),
                    copyright TINYINT,
                    pic VARCHAR(500),
                    title TEXT,
                    pubdate BIGINT,
                    ctime BIGINT,
                    `desc` TEXT,
                    state INT,
                    duration INT,
                    tnamev2 VARCHAR(50),
                    pid_name_v2 VARCHAR(50),
                    short_link_v2 VARCHAR(200),
                    dynamic TEXT,
                    stat_view INT,
                    stat_danmaku INT,
                    stat_reply INT,
                    stat_favorite INT,
                    stat_coin INT,
                    stat_share INT,
                    stat_now_rank INT,
                    stat_his_rank INT,
                    stat_like INT,
                    stat_dislike INT,
                    stat_vt INT,
                    stat_vv INT,
                    stat_fav_g INT,
                    stat_like_g INT,
                    owner_mid BIGINT,
                    owner_name VARCHAR(100),
                    owner_face VARCHAR(500),
                    tags TEXT,
                    formatted_time VARCHAR(30),
                    PRIMARY KEY (timestamp, aid),
                    INDEX idx_aid (aid),
                    INDEX idx_pubdate (pubdate),
                    INDEX idx_owner_mid (owner_mid),
                    INDEX idx_stat_view (stat_view)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                """
                cursor.execute(create_table_sql)
                print("表 bilibili_videos 创建成功")
            
            # 获取全局timestamp和formatted_time
            global_timestamp = data.get('timestamp')
            global_formatted_time = data.get('formatted_time')
            video_list = data.get('data', [])
            
            if not video_list:
                print("没有视频数据需要插入")
                return False
            
            # 插入数据 - 修正：包含所有字段，包括tags
            insert_sql = """
            INSERT INTO bilibili_videos (
                timestamp, aid, videos, tid, tname, copyright, pic, title, pubdate, ctime,
                `desc`, state, duration, tnamev2, pid_name_v2, short_link_v2, dynamic,
                stat_view, stat_danmaku, stat_reply, stat_favorite, stat_coin, stat_share,
                stat_now_rank, stat_his_rank, stat_like, stat_dislike, stat_vt, stat_vv,
                stat_fav_g, stat_like_g, owner_mid, owner_name, owner_face, tags, formatted_time
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            """
            
            success_count = 0
            for video in video_list:
                try:
                    # 使用视频自身的timestamp，如果没有则使用全局timestamp
                    video_timestamp = video.get('timestamp', global_timestamp)
                    video_formatted_time = video.get('formatted_time', global_formatted_time)
                    
                    # 处理tags字段 - 如果是列表则转换为JSON字符串
                    tags_value = video.get('tags')
                    if isinstance(tags_value, list):
                        import json
                        tags_value = json.dumps(tags_value, ensure_ascii=False)
                    
                    values = (
                        video_timestamp,
                        video.get('aid'),
                        video.get('videos'),
                        video.get('tid'),
                        video.get('tname'),
                        video.get('copyright'),
                        video.get('pic'),
                        video.get('title'),
                        video.get('pubdate'),
                        video.get('ctime'),
                        video.get('desc'),
                        video.get('state'),
                        video.get('duration'),
                        video.get('tnamev2'),
                        video.get('pid_name_v2'),
                        video.get('short_link_v2'),
                        video.get('dynamic'),
                        video.get('stat_view'),
                        video.get('stat_danmaku'),
                        video.get('stat_reply'),
                        video.get('stat_favorite'),
                        video.get('stat_coin'),
                        video.get('stat_share'),
                        video.get('stat_now_rank'),
                        video.get('stat_his_rank'),
                        video.get('stat_like'),
                        video.get('stat_dislike'),
                        video.get('stat_vt'),
                        video.get('stat_vv'),
                        video.get('stat_fav_g'),
                        video.get('stat_like_g'),
                        video.get('owner_mid'),
                        video.get('owner_name'),
                        video.get('owner_face'),
                        tags_value,  # 添加了tags字段
                        video_formatted_time
                    )
                    
                    cursor.execute(insert_sql, values)
                    success_count += 1
                    
                except Exception as e:
                    print(f"插入视频 aid={video.get('aid')} 失败: {e}")
            
            connection.commit()
            print(f"成功插入 {success_count} 条视频记录")
            return success_count > 0
            
    except Exception as e:
        print(f"数据库操作失败: {e}")
        if connection:
            connection.rollback()
        return False
        
    finally:
        if connection:
            connection.close()