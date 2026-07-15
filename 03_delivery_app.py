"""課題3：配送遅延を予測するCLIアプリを作成する。"""

# TODO: joblibとpandasをimportする
import pandas as pd
import joblib

# TODO: delivery_model.pklを読み込む
bundle = joblib.load("delivery_model.pkl")
model = bundle["model"]
features = bundle["features"]

# TODO: メニューを表示する
def main():
    while True:
        print("\n===配達遅延予測アプリ===")
        print("1: 予測する")
        print("2: 終了")
        choice = input("--選択してください--:")
        if choice == "1":
            print("--入力してください--")
            user_input()
        elif choice == "2":
            print("--アプリを終了します--")
            break
        else:
            print("1 または 2 を入力してください")

# TODO: FEATURESに含めた配送情報をユーザーから入力してもらう
inputs = {
    "距離" : "距離（km）",
    "荷物重量" : "荷物重量（kg）",
    "天気F" : "天気（ 晴れ / 雨 / 雪 ）",
    "交通量" : "交通量（%）",
    "発送準備時間" : "発送準備時間（h）",
    "過去遅延回数" : "過去遅延回数（回）",
    "当日配送件数" : "当日配送件数（件）",
    "再配達回数" : "再配達回数（回）",
    "時期F" : "時期（ 通常期 / 繁忙期 ）",
    "配達希望時間帯F" : "配達希望時間帯（ 午前 / 午後 / 夜間 ）"
}

message = {
    "通常" : "通常通り配送できる見込みです。",
    "遅延注意" : "遅延の可能性が見込まれます。ご了承ください。",
    "遅延危険" : "大きな遅延が見込まれます。配送方法を確認してください。"
}

def input_check(category,text):
    if category == 0:
        while True:
            try:
                return int(input(text))
            except ValueError:
                print("数値を入力してください")
    elif category == 1:
        while True:
            weather = input(text)
            if weather == "晴れ":
                return 0
            elif weather == "雨":
                return 1
            elif weather == "雪":
                return 2
            else:
                print("晴れ/雨/雪 のいずれかを入力してください")
                continue
    elif category == 2:
        while True:
            season = input(text)
            if season == "通常期":
                return 0
            elif season =="繁忙期":
                return 1
            else:
                print("通常期/繁忙期 のいずれかを入力してください")
                continue
    elif category == 3:
        while True:
            time = input(text)
            if time == "午前":
                return 0
            elif time == "午後":
                return 1
            elif time == "夜間":
                return 2
            else:
                print("午前/午後/夜間 のいずれかを入力してください")
    return None


def user_input():
    values = []
    for col in features:
        if col == "天気F":
            values.append(input_check(1,inputs[col]))
        elif col == "時期F":
            values.append(input_check(2,inputs[col]))
        elif col == "配達希望時間帯F":
            values.append(input_check(3,inputs[col]))
        else:
            values.append(input_check(0,inputs[col]))

# TODO: モデルで予測し、結果を表示する
    data = pd.DataFrame([values],columns=features)
    pred = model.predict(data)[0]

    print("予測結果:",pred)
    print(message[pred])

if __name__ == "__main__":
    main()