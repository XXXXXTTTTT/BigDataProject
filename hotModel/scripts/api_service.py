
from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
import joblib
from pydantic import BaseModel
from typing import Optional
import os, json

app = FastAPI()

# 数据库与模型
engine = create_engine("mysql+pymysql://remote:123456@114.116.251.42:3306/bilibili")
model = joblib.load(os.path.join(os.path.dirname(__file__), "..", "hot_video_model.pkl"))

class VideoFeatures(BaseModel):
    点赞率: float
    弹幕率: float
    评论率: float
    投币率: float
    hour: int
    weekday: int
    duration: int

@app.post("/predict")
def predict(features: VideoFeatures):
    data = pd.DataFrame([features.dict()])
    prediction = model.predict(data)[0]
    prob = model.predict_proba(data)[0][1]
    level = "高热" if prob > 0.8 else "中热" if prob > 0.5 else "低热"
    play_range = "10w+" if prob > 0.8 else "1w~10w" if prob > 0.5 else "0~1w"
    return {
        "prediction": int(prediction),
        "confidence": round(prob, 4),
        "level": level,
        "play_range": play_range
    }

@app.get("/video/wordcloud")
def video_wordcloud():
    df = pd.read_sql("SELECT tags FROM hot_videos WHERE tags IS NOT NULL", con=engine)
    from collections import Counter
    tags = df["tags"].str.cat(sep=",").split(",")
    counter = Counter([t.strip() for t in tags if t.strip()])
    result = [{"name": k, "value": v} for k, v in counter.most_common(100)]
    return {"keywords": result}

@app.get("/video/rank")
def video_rank():
    df = pd.read_sql("SELECT tname, stat_view FROM hot_videos", con=engine)
    rank = df.groupby("tname").agg(
        热门视频数=pd.NamedAgg(column="stat_view", aggfunc="count"),
        平均播放量=pd.NamedAgg(column="stat_view", aggfunc="mean")
    ).reset_index()
    return rank.to_dict(orient="records")

@app.get("/up/{mid}")
def up_detail(mid: int):
    df = pd.read_sql(f"SELECT * FROM hot_videos WHERE owner_mid = {mid}", con=engine)
    if df.empty:
        return {"error": "UP主不存在"}

    up_info = {
        "mid": mid,
        "name": df["owner_name"].iloc[0],
        "fans": int(df["stat_favorite"].mean()),
        "等级": "Lv3",
        "视频数": df.shape[0],
        "平均播放": int(df["stat_view"].mean()),
        "播放_粉丝比": round(df["stat_view"].mean() / (df["stat_favorite"].mean() + 1), 2),
        "互动率": round((df["stat_like"] + df["stat_reply"] + df["stat_coin"]).sum() / (df["stat_view"].sum() + 1), 4)
    }
    latest = df.sort_values(by="ctime", ascending=False)[["title", "ctime", "stat_view", "stat_like", "stat_reply", "stat_danmaku"]].head(5)
    latest["ctime"] = pd.to_datetime(latest["ctime"], unit="s").dt.strftime("%Y-%m-%d %H:%M")
    return {
        "info": up_info,
        "latest_videos": latest.to_dict(orient="records")
    }

@app.get("/up/{mid}/history")
def up_history(mid: int):
    df = pd.read_sql(f"SELECT timestamp, stat_view, stat_like, stat_reply, stat_coin, stat_favorite FROM hot_videos WHERE owner_mid = {mid}", con=engine)
    if df.empty:
        return {"error": "无数据"}
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["互动数"] = df["stat_like"] + df["stat_reply"] + df["stat_coin"]
    df["互动率"] = df["互动数"] / (df["stat_view"] + 1)
    grouped = df.resample("W", on="timestamp").agg({
        "stat_favorite": "mean",
        "stat_view": "mean",
        "互动率": "mean"
    }).dropna()
    grouped.reset_index(inplace=True)
    return {
        "timeline": grouped["timestamp"].dt.strftime("%Y-%m-%d").tolist(),
        "粉丝": grouped["stat_favorite"].round(1).tolist(),
        "播放": grouped["stat_view"].round(1).tolist(),
        "互动率": (grouped["互动率"] * 100).round(2).tolist()
    }
