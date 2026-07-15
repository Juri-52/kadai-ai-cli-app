"""課題2：配送遅延予測モデルを学習してdelivery_model.pklを作成する。"""

# TODO: pandas、joblib、DecisionTreeClassifierなどをimportする
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier

# TODO: delivery_clean.csvを読み込む
df = pd.read_csv("delivery_clean.csv")

# TODO: 使用したいカテゴリ列を数値へ変換する
weather = {
    "晴れ" : 0,
    "雨" : 1,
    "雪" : 2
}
df["天気F"] = df["天気"].map(weather)

season = {
    "通常期" : 0,
    "繁忙期" : 1
}
df["時期F"] = df["時期"].map(season)

time = {
    "午前" : 0,
    "午後" : 1,
    "夜間" : 2
}
df["配達希望時間帯F"] = df["配達希望時間帯"].map(time)

# TODO: 特徴量を自分で選び、FEATURESリストを作る
features = ["距離",
            "荷物重量",
            "天気F",
            "交通量",
            "発送準備時間",
            "過去遅延回数",
            "当日配送件数",
            "再配達回数",
            "時期F",
            "配達希望時間帯F"
            ]

# TODO: DecisionTreeClassifierを学習する
x = df[features]
y = df["配送状態"]

model = DecisionTreeClassifier()
model.fit(x, y)

# TODO: delivery_model.pklへ保存する
bundle = {"model":model,"features":features}
joblib.dump(bundle,"delivery_model.pkl")