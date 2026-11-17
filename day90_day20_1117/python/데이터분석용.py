import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 불러오기
df = pd.read_csv("./python/train.csv")
print("원본 데이터 형태:", df.shape)

# 2. 문자열 공백과 결측값 정리
for col in df.select_dtypes(include=['object', 'string']).columns:
    df[col] = df[col].str.strip()

df = df.replace(['NaN', 'conditions NaN', ''], pd.NA)

# 3. 배달 시간: "(min) 24" → 숫자 24
df['Time_taken(min)'] = pd.to_numeric(
    df['Time_taken(min)']
    .astype('string')
    .str.replace('(min)', '', regex=False)
    .str.strip(),
    errors='coerce'
)

# 4. 수치형 컬럼 변환
number_cols = [
    'Delivery_person_Age',
    'Delivery_person_Ratings',
    'multiple_deliveries',
    'Restaurant_latitude',
    'Restaurant_longitude',
    'Delivery_location_latitude',
    'Delivery_location_longitude'
]

for col in number_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 5. 좌표 유효성 확인
coordinate_cols = [
    'Restaurant_latitude',
    'Restaurant_longitude',
    'Delivery_location_latitude',
    'Delivery_location_longitude'
]

# 이번 분석에서는 0으로 기록된 좌표도 결측으로 취급
# 일반적으로 위도·경도 0 자체가 잘못된 값인 것은 아님
valid_coordinates = (
    df['Restaurant_latitude'].between(-90, 90)
    & df['Delivery_location_latitude'].between(-90, 90)
    & df['Restaurant_longitude'].between(-180, 180)
    & df['Delivery_location_longitude'].between(-180, 180)
    & df[coordinate_cols].notna().all(axis=1)
    & df[coordinate_cols].ne(0).all(axis=1)
)

# 6. 식당과 배달지 사이 거리 계산
# 도 단위 → 라디안 단위
lat1 = np.radians(df['Restaurant_latitude'])
lon1 = np.radians(df['Restaurant_longitude'])
lat2 = np.radians(df['Delivery_location_latitude'])
lon2 = np.radians(df['Delivery_location_longitude'])

# 하버사인 공식: 실제 도로 거리가 아닌 지표면상 최단 거리
a = (
    np.sin((lat2 - lat1) / 2) ** 2
    + np.cos(lat1) * np.cos(lat2)
    * np.sin((lon2 - lon1) / 2) ** 2
)

df['distance_km'] = 6371 * 2 * np.arcsin(np.sqrt(a.clip(0, 1)))
# 유효하지 않은 좌표의 거리는 결측 처리
df.loc[~valid_coordinates, 'distance_km'] = np.nan

# 7. 거리 100km 초과 행 제거
print("\n[제거 전 거리와 배달 시간의 상관계수]")
print(df['distance_km'].corr(df['Time_taken(min)']))
over_100 = df['distance_km'] > 100

print("\n100km 초과 행 수:", over_100.sum())
print("\n[100km 초과 데이터 중 거리가 큰 10개]")
print(
    df.loc[
        over_100,['ID', 'distance_km', 'Time_taken(min)']].sort_values('distance_km', ascending=False).head(10)
)

# 100km 초과 행과 거리 결측값을 모두 제거
df = df.loc[df['distance_km'].between(0, 100)].copy()
df = df.reset_index(drop=True)

print("\n제거 후 데이터 형태:", df.shape)
print("거리 결측값 수:", df['distance_km'].isna().sum())

print("\n[제거 후 거리 분포]")
print(df['distance_km'].describe(percentiles=[0.95, 0.99]))

print("\n[제거 후 거리와 배달 시간의 상관계수]")
print(df['distance_km'].corr(df['Time_taken(min)']))

# 평점이 있는 데이터 중 1~5점 범위 밖의 행 제거
invalid_rating = (
    df['Delivery_person_Ratings'].notna()
    & ~df['Delivery_person_Ratings'].between(1, 5)
)

print("제거할 평점 이상치:", invalid_rating.sum())

df = df.loc[~invalid_rating].copy()
df = df.reset_index(drop=True)

# 차량 상태 컬럼 제외
df = df.drop(columns=['Vehicle_condition'])


# 8. 수치형 특성과 배달 시간의 상관계수
cols = [
    'Delivery_person_Age',
    'Delivery_person_Ratings',
    'multiple_deliveries',
    'distance_km',
    'Time_taken(min)'
]

numeric_data = df[cols]

# 배달 시간과의 상관계수만 추출
corr = numeric_data.corr()['Time_taken(min)']
corr = corr.drop('Time_taken(min)')

# 절댓값 기준으로 관계가 강한 순서로 정렬
corr = corr.sort_values(
    key=lambda values: values.abs(),
    ascending=False
)

print("\n[배달 시간과의 상관계수]")
print(corr)

print("\n[수치형 컬럼 결측값 수]")
print(numeric_data.isna().sum())

# 상관계수 히트맵
plt.figure(figsize=(7, 5))

sns.heatmap(
    corr.to_frame(name='배달 소요 시간'),
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    vmin=-1,
    vmax=1
)

plt.title('수치형 특성과 배달 시간의 상관계수\n(100km 초과 행 제외)')
plt.tight_layout()
plt.show()

# 9. 주문 시간대와 요일 추출
df['order_hour'] = pd.to_numeric(
    df['Time_Orderd']
    .astype('string')
    .str.split(':')
    .str[0],
    errors='coerce'
)

# 0~23 범위 밖의 시간대는 결측 처리
df.loc[
    ~df['order_hour'].between(0, 23),
    'order_hour'
] = np.nan

# 월요일 0 ~ 일요일 6
df['order_weekday'] = pd.to_datetime(
    df['Order_Date'],
    format='%d-%m-%Y',
    errors='coerce'
).dt.dayofweek

# 10. 범주별 배달 시간 비교
category_cols = [
    'Weatherconditions',
    'Road_traffic_density',
    'Type_of_order',
    'Type_of_vehicle',
    'Festival',
    'City',
    'order_hour',
    'order_weekday'
]

for col in category_cols:
    # 각 그룹의 유효한 배달 시간 개수, 평균, 중앙값
    summary = (
        df.groupby(col)['Time_taken(min)']
        .agg(['count', 'mean', 'median'])
        .sort_values('mean', ascending=False)
    )

    print(f"\n[{col}별 배달 시간]")
    print(summary.round(2))

    # 해당 컬럼이나 배달 시간이 결측인 행은 그래프에서 제외
    plot_data = df.dropna(
        subset=[col, 'Time_taken(min)']
    )

    if plot_data.empty:
        continue

    plt.figure(figsize=(11, 5))

    sns.boxplot(
        data=plot_data,
        x=col,
        y='Time_taken(min)'
    )

    plt.title(f'{col}별 배달 시간 분포\n(100km 초과 행 제외)')
    plt.xlabel(col)
    plt.ylabel('배달 소요 시간(분)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()