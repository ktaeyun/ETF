import requests
import pandas as pd
import os
from functools import reduce

# 1. 차트 설정
chart_names = {
    "n-unique-addresses": "Unique Addresses",
    "market-price": "Market Price (USD)",
    "n-transactions": "Number of Transactions",
    "output-volume": "Output Volume (BTC)",
    "hash-rate": "Hash Rate (TH/s)",
    "total-bitcoins": "Total Bitcoins in Circulation"
}
timespan = "1095days"
chart_data = {}

for chart, label in chart_names.items():
    url = f"https://api.blockchain.info/charts/{chart}?timespan={timespan}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        raw = response.json()
        values = raw.get("values", [])
        if values:
            df = pd.DataFrame(values)
            df["x"] = pd.to_datetime(df["x"], unit="s")
            df.columns = ["DateTime", label]

            if chart != "total-bitcoins":
                # 다른 지표들은 날짜 기준으로 정리
                df["Date"] = df["DateTime"].dt.floor("D")
                df = df[["Date", label]]
            else:
                # total-bitcoins: 각 날짜 중 가장 늦은 시간 값만 남김
                df["Date"] = df["DateTime"].dt.date
                df = df.sort_values(["Date", "DateTime"])
                df = df.groupby("Date").tail(1)  # 하루 중 마지막 값만 선택
                df["Date"] = pd.to_datetime(df["Date"])  # 다시 datetime으로 변환
                df = df[["Date", label]]

            chart_data[chart] = df
            print(f"✅ {label} 수집 및 전처리 완료")
        else:
            print(f"⚠️ {label}: values 없음")
    else:
        print(f"❌ {label} 수집 실패 (HTTP {response.status_code})")

# 병합
merged_df = reduce(lambda left, right: pd.merge(left, right, on="Date", how="outer"), chart_data.values())
merged_df.sort_values("Date", inplace=True)

# 저장
save_folder = "data"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "bitcoin_etf_indicators.csv")
merged_df.to_csv(save_path, index=False)

print(f"\n📁 저장 완료: {save_path}")

