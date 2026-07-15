"""課題1：delivery_dirty.csvを清掃してdelivery_clean.csvを作成する。"""

# TODO: import pandas as pd
import pandas as pd

# TODO: CSVを読み込む
df = pd.read_csv("delivery_dirty.csv")

# TODO: READMEの「課題1」に従ってデータを清掃する
print(df.dtypes)
df.columns = df.columns.str.strip()

df["注文ID"] = df["注文ID"].str.strip().str.upper()
df.drop_duplicates(subset="注文ID",keep="last")

df["地域"] = df["地域"].str.strip().str.upper()
df["地域"] = df["地域"].str.replace({
    "県" : "",
    "都" : "",
    "府" : "",
    "FUKUOKA" : "福岡",
    "OSAKA" : "大阪",
    "TOKYO" : "東京",
    "HOKKAIDO" : "北海道",
    "OKINAWA" : "沖縄",
    "HIROSHIMA" : "広島",
    "AICHI" : "愛知",
    "MIYAGI" : "宮城"
})

df["配送会社"] = df["配送会社"].str.strip().str.upper()
df["配送会社"] = df["配送会社"].str.replace({
    "ヤマト運輸" : "ヤマト",
    "YAMATO" : "ヤマト",
    "ヤマト" : "ヤマト運輸",
    "佐川急便" : "佐川",
    "SAGAWA" : "佐川",
    "佐川" : "佐川急便",
    "日本郵便" : "郵便",
    "JAPAN POST" : "郵便",
    "郵便" : "日本郵便"
})

df["距離"] = df["距離"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["距離"] = pd.to_numeric(df["距離"],errors="coerce")
df.loc[
    (df["距離"] < 0), "距離"
] = pd.NA

df["荷物重量"] = df["荷物重量"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["荷物重量"] = pd.to_numeric(df["荷物重量"],errors="coerce")
df.loc[
    (df["荷物重量"] < 0), "荷物重量"
] = pd.NA

df["天気"] = df["天気"].str.strip().str.upper()
df["天気"] = df["天気"].str.replace({
    "RAIN" : "雨",
    "SUNNY" : "晴れ",
    "SNOW" : "雪",
    "雨天" : "雨"
})

df["交通量"] = df["交通量"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["交通量"] = pd.to_numeric(df["交通量"],errors="coerce")
df.loc[
    (df["交通量"] < 0) | (df["交通量"] > 100), "交通量"
] = pd.NA

df["発送準備時間"] = df["発送準備時間"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["発送準備時間"] = pd.to_numeric(df["発送準備時間"],errors="coerce")
df.loc[
    (df["発送準備時間"] < 0), "発送準備時間"
] = pd.NA

df["過去遅延回数"] = df["過去遅延回数"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["過去遅延回数"] = pd.to_numeric(df["過去遅延回数"],errors="coerce")
df.loc[
    (df["過去遅延回数"] < 0), "過去遅延回数"
] = pd.NA

df["注文金額"] = df["注文金額"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["注文金額"] = pd.to_numeric(df["注文金額"],errors="coerce")
df.loc[
    (df["注文金額"] < 0), "注文金額"
] = pd.NA

df["当日配送件数"] = df["当日配送件数"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["当日配送件数"] = pd.to_numeric(df["当日配送件数"],errors="coerce")
df.loc[
    (df["当日配送件数"] < 0), "当日配送件数"
] = pd.NA

df["ドライバー経験年数"] = df["ドライバー経験年数"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["ドライバー経験年数"] = pd.to_numeric(df["ドライバー経験年数"],errors="coerce")
df.loc[
    (df["ドライバー経験年数"] < 0), "ドライバー経験年数"
] = pd.NA

df["再配達回数"] = df["再配達回数"].str.strip().str.replace(r"[^0-9\.-]","",regex=True)
df["再配達回数"] = pd.to_numeric(df["再配達回数"],errors="coerce")
df.loc[
    (df["再配達回数"] < 0), "再配達回数"
] = pd.NA

df["時期"] = df["時期"].str.strip().str.upper()
df["時期"] = df["時期"].str.replace({
    "NORMAL" : "通常期",
    "PEAK" : "繁忙期"
})
df["配送先種別"] = df["配送先種別"].str.strip().str.upper()
df["配送先種別"] = df["配送先種別"].str.replace({
    "HOME" : "住宅",
    "OFFICE" : "会社"
})
df["配達希望時間帯"] = df["配達希望時間帯"].str.strip().str.upper()
df["配達希望時間帯"] = df["配達希望時間帯"].str.replace({
    "MORNING" : "午前",
    "AFTERNOON" : "午後",
    "NIGHT" : "夜間"
})

df["配送状態"] = df["配送状態"].str.strip()

# TODO: delivery_clean.csvとして保存する
print(df)
df.to_csv("delivery_clean.csv",index=False,encoding="UTF-8")