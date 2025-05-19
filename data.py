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

# 2. 데이터 수집
for chart, label in chart_names.items():
    url = f"https://api.blockchain.info/charts/{chart}?timespan={timespan}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        raw = response.json()
        df = pd.DataFrame(raw["values"])
        df["x"] = pd.to_datetime(df["x"], unit="s")
        df.columns = ["Date", label]
        chart_data[chart] = df
        print(f"✅ {label} 수집 완료")
    else:
        print(f"❌ {label} 수집 실패 (HTTP {response.status_code})")

# 3. 병합
merged_df = reduce(lambda left, right: pd.merge(left, right, on="Date", how="outer"), chart_data.values())
merged_df.sort_values("Date", inplace=True)

# 4. 저장
save_folder = "data"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "bitcoin_etf_indicators.csv")
merged_df.to_csv(save_path, index=False)
print(f"✅ 저장 완료: {save_path}")
