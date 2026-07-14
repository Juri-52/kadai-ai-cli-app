"""配送遅延予測課題用の汚れたCSVデータを生成するスクリプト。"""

import csv
import random


random.seed(20260715)

OUTPUT_FILE = "delivery_dirty.csv"
UNIQUE_ROWS = 29700
DUPLICATE_ROWS = 300

regions = [
    ("東京都", 0.05),
    ("大阪府", 0.10),
    ("北海道", 0.30),
    ("福岡県", 0.18),
    ("沖縄県", 0.42),
    ("宮城県", 0.20),
    ("広島県", 0.22),
    ("愛知県", 0.12),
]

region_names = {
    "東京都": ["東京都", "東京", "TOKYO", " 東京 "],
    "大阪府": ["大阪府", "大阪", "OSAKA", " 大阪 "],
    "北海道": ["北海道", "北海道 ", "HOKKAIDO"],
    "福岡県": ["福岡県", "福岡", "FUKUOKA"],
    "沖縄県": ["沖縄県", "沖縄", "OKINAWA"],
    "宮城県": ["宮城県", "仙台", "MIYAGI"],
    "広島県": ["広島県", "広島", "HIROSHIMA"],
    "愛知県": ["愛知県", "名古屋", "AICHI"],
}

companies = {
    "ヤマト運輸": ["ヤマト運輸", "ヤマト", "Yamato", " ヤマト運輸 "],
    "佐川急便": ["佐川急便", "佐川", "Sagawa", " 佐川急便 "],
    "日本郵便": ["日本郵便", "郵便", "Japan Post", " 日本郵便 "],
}

weather_names = {
    "晴れ": ["晴れ", " 晴れ ", "SUNNY"],
    "雨": ["雨", "雨天", "RAIN"],
    "雪": ["雪", "雪 ", "SNOW"],
}


def choose_region():
    names = [name for name, _ in regions]
    weights = [weight for _, weight in regions]
    return random.choices(names, weights=weights, k=1)[0]


def make_label(distance, weight, weather, traffic, preparation, past_delays, region_risk):
    """配送が遅れる可能性を元の正しい値から作る。"""
    weather_risk = {"晴れ": 0, "雨": 12, "雪": 28}[weather]
    score = (
        distance / 35
        + weight * 0.7
        + weather_risk
        + traffic * 0.45
        + preparation * 2.0
        + past_delays * 7
        + region_risk * 40
        + random.gauss(0, 9)
    )

    if score >= 95:
        return "遅延危険"
    if score >= 68:
        return "遅延注意"
    return "通常"


def dirty_number(value, unit, missing_rate=0.03, unknown_rate=0.01):
    roll = random.random()
    if roll < missing_rate:
        return ""
    if roll < missing_rate + unknown_rate:
        return "不明"
    if roll < 0.45:
        return f"{value}{unit}"
    if roll < 0.55:
        return f" {value}{unit} "
    return str(value)


def make_row(number):
    region, region_risk = random.choice(regions)
    company = random.choice(list(companies))
    weather = random.choices(["晴れ", "雨", "雪"], weights=[0.62, 0.28, 0.10], k=1)[0]

    distance = max(5, int(random.gauss(250 + region_risk * 550, 150)))
    weight = round(max(0.1, random.lognormvariate(1.1, 0.7)), 1)
    traffic = min(100, max(0, int(random.gauss(48, 25))))
    preparation = round(max(0.2, random.lognormvariate(1.0, 0.55)), 1)
    past_delays = min(12, max(0, int(random.expovariate(1 / 1.3))))
    order_amount = int(max(500, random.lognormvariate(8.4, 0.8)))
    daily_deliveries = min(250, max(10, int(random.gauss(105, 38))))
    driver_experience = min(30, max(0, round(random.expovariate(1 / 5), 1)))
    redelivery_count = min(10, max(0, int(random.expovariate(1 / 0.7))))
    season = random.choices(["通常期", "繁忙期"], weights=[0.72, 0.28], k=1)[0]
    address_type = random.choices(["住宅", "会社"], weights=[0.78, 0.22], k=1)[0]
    time_slot = random.choices(["午前", "午後", "夜間"], weights=[0.32, 0.48, 0.20], k=1)[0]
    status = make_label(
        distance, weight, weather, traffic, preparation, past_delays, region_risk
    )

    # 追加の現実的な要因。配送件数・再配達・繁忙期は遅延リスクを上げ、
    # ドライバー経験は少し下げる。元のラベルを再計算する。
    extra_score = (
        daily_deliveries * 0.13
        + redelivery_count * 9
        + (16 if season == "繁忙期" else 0)
        + (7 if time_slot == "夜間" else 0)
        - driver_experience * 1.1
        + random.gauss(0, 5)
    )
    base_score = {"通常": 45, "遅延注意": 78, "遅延危険": 108}[status]
    final_score = base_score + extra_score - 14
    if final_score >= 110:
        status = "遅延危険"
    elif final_score >= 74:
        status = "遅延注意"
    else:
        status = "通常"

    # 明らかに間違った値を少量だけ混ぜる。
    dirty_distance = dirty_number(distance, "km")
    dirty_weight = dirty_number(weight, "kg")
    dirty_traffic = dirty_number(traffic, "", missing_rate=0.02, unknown_rate=0.01)
    dirty_preparation = dirty_number(preparation, "h")
    dirty_past_delays = dirty_number(past_delays, "", missing_rate=0.02, unknown_rate=0.01)
    dirty_amount = dirty_number(f"{order_amount:,}", "円")
    dirty_daily_deliveries = dirty_number(daily_deliveries, "件", missing_rate=0.02, unknown_rate=0.01)
    dirty_experience = dirty_number(driver_experience, "年", missing_rate=0.03, unknown_rate=0.01)
    dirty_redelivery = dirty_number(redelivery_count, "回", missing_rate=0.02, unknown_rate=0.01)

    if random.random() < 0.004:
        dirty_distance = random.choice(["-50km", "99999km"])
    if random.random() < 0.004:
        dirty_weight = random.choice(["-3kg", "9999kg"])
    if random.random() < 0.004:
        dirty_traffic = random.choice(["-10", "150"])
    if random.random() < 0.004:
        dirty_preparation = random.choice(["-2h", "300h"])
    if random.random() < 0.004:
        dirty_past_delays = random.choice(["-1", "999"])
    if random.random() < 0.004:
        dirty_amount = random.choice(["-500円", "99999999円"])
    if random.random() < 0.004:
        dirty_daily_deliveries = random.choice(["-10件", "9999件"])
    if random.random() < 0.004:
        dirty_experience = random.choice(["-1年", "99年"])
    if random.random() < 0.004:
        dirty_redelivery = random.choice(["-1回", "99回"])

    if random.random() < 0.015:
        status = f"　{status}"
    elif random.random() < 0.015:
        status = f"{status} "

    return [
        f"ORD-{number:05d}",
        random.choice(region_names[region]),
        random.choice(companies[company]),
        dirty_distance,
        dirty_weight,
        random.choice(weather_names[weather]),
        dirty_traffic,
        dirty_preparation,
        dirty_past_delays,
        dirty_amount,
        dirty_daily_deliveries,
        dirty_experience,
        dirty_redelivery,
        random.choice([season, f" {season} ", "PEAK" if season == "繁忙期" else "NORMAL"]),
        random.choice([address_type, f" {address_type} ", "HOME" if address_type == "住宅" else "OFFICE"]),
        random.choice([time_slot, f" {time_slot} ", "MORNING" if time_slot == "午前" else ("AFTERNOON" if time_slot == "午後" else "NIGHT")]),
        status,
    ]


headers = [
    "注文ID",
    "地域",
    "配送会社",
    "距離",
    "荷物重量",
    "天気",
    "交通量",
    "発送準備時間",
    "過去遅延回数",
    "注文金額",
    "当日配送件数",
    "ドライバー経験年数",
    "再配達回数",
    "時期",
    "配送先種別",
    "配達希望時間帯",
    "配送状態",
]

rows = [make_row(number) for number in range(1, UNIQUE_ROWS + 1)]
rows.extend(random.choice(rows).copy() for _ in range(DUPLICATE_ROWS))
random.shuffle(rows)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"{OUTPUT_FILE} を作成しました: {len(rows)}行")
