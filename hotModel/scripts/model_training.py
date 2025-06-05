import xgboost as xgb
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

print("正在加载特征数据...")
X_path = os.path.abspath("X.csv")
y_path = os.path.abspath("y.csv")

if not os.path.exists(X_path) or not os.path.exists(y_path):
    print("❌ 没有找到 X.csv 或 y.csv，请先运行 data_preprocessing.py")
    exit()

X = pd.read_csv(X_path)
y = pd.read_csv(y_path).squeeze()

print("训练集中样本数：", len(X))

print("开始划分数据...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("正在训练模型...")
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train)

print("正在预测...")
y_pred = model.predict(X_test)
print("分类报告:")
print(classification_report(y_test, y_pred))

# 保存模型
model_path = os.path.abspath("hot_video_model.pkl")
joblib.dump(model, model_path)
print(f"✅ 模型已保存为 {model_path}")
