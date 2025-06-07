import pandas as pd
from sqlalchemy import create_engine
import os

def extract_and_preprocess():
    # 替换成你自己的数据库连接配置
    engine = create_engine("mysql+pymysql://remote:123456@114.116.251.42:3306/bilibili")


    print("✅ 正在连接数据库...")
    df = pd.read_sql("SELECT * FROM hot_videos", con=engine)

    print("✅ 数据读取成功，开始预处理...")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.weekday
    df["点赞率"] = df["stat_like"] / (df["stat_view"] + 1)
    df["弹幕率"] = df["stat_danmaku"] / (df["stat_view"] + 1)
    df["评论率"] = df["stat_reply"] / (df["stat_view"] + 1)
    df["投币率"] = df["stat_coin"] / (df["stat_view"] + 1)

    threshold = df["stat_view"].quantile(0.8)
    df["是否热门"] = (df["stat_view"] >= threshold).astype(int)

    features = ["点赞率", "弹幕率", "评论率", "投币率", "hour", "weekday", "duration"]
    X = df[features]
    y = df["是否热门"]

    return X, y

if __name__ == "__main__":
    try:
        print("🚀 启动预处理流程...")
        X, y = extract_and_preprocess()
        print("💾 正在保存为 CSV 文件...")
        X.to_csv("X.csv", index=False)
        y.to_csv("y.csv", index=False)
        print("✅ 成功写入 X.csv 和 y.csv！")
    except Exception as e:
        print("❌ 发生错误：", e)
