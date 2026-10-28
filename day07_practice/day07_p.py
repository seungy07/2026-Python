import numpy as np

data = np.genfromtxt(
    './day07_practice/한국도로교통공단.csv',
    delimiter=',',
    skip_header=1,
    encoding='cp949',
    dtype=str
)

# ["가해자차량용도","시간대","사고건수","사망자수","중상자수","경상자수","부상신고자수"]
print(f"데이터 형태: {data.shape}") 
cars = [] # 차량 종류 추출
for car in data[:,0]:
    if car not in cars:
        cars.append(car)
print(cars)

times = [] # 시간대 추출
for time in data[:,1]:
    if time not in times:
        times.append(time) 
print(times)

# step 1 : 기초 통계 차량 유형별, 시간대별, 사고건수(최댓값) , 차량별 사고건수(평균)

# step 3: 위기/효율 지수 산출
targets = [] # 차량명 + 시간대
accident_counts = [] # 사고건수
damage_counts = [] # 사망자수 + 중상자수
for car in cars:
    for time in times:
        # 차량명과 시간대가 모두 일치하는 행
        selected = data[ (data[:,0]==car) & (data[:,1] == time) ]

        if len(selected) == 0:
            continue

        targets.append([car, time])
        accident_counts.append( selected[:,2].astype(int).sum() ) # 사고건수

        damage = (selected[:, 3].astype(int).sum() + selected[:,4].astype(int).sum())
        damage_counts.append(damage)
targets = np.array(targets)
accident_counts = np.array(accident_counts)
damage_counts = np.array(damage_counts)
# 리스트는 같은 위치 요소끼리 연산이 안되기 때문에 배열로 변환
# ===========================================

# 사고 100건당 사망 중성자 수
# 사고가 1건 이상인 조합만 선택
valid = accident_counts > 0

valid_targets = targets[valid]
valid_accidents = accident_counts[valid]
valid_damage = damage_counts[valid]

# 사고 100건당 사망·중상자 수
risk_index = valid_damage / valid_accidents * 100

# 가장 높은 지수의 인덱스
max_index = np.argmax(risk_index)

print(f"차량용도: {valid_targets[max_index, 0]}")
print(f"시간대: {valid_targets[max_index, 1]}")
print(f"사고건수: {valid_accidents[max_index]}건")
print(f"사망·중상자 수: {valid_damage[max_index]}명")
print(f"사고 100건당 사망·중상자 수: {risk_index[max_index]:.2f}명")

# step 5: 차량별 사고 집중 시간대 찾기 
total_count = 0  

for car in cars:
    condition = targets[:, 0] == car # 차량명 + 시간대 조건

    car_targets = targets[condition] # 차량명 + 시간대 조건에 맞는 추출
    car_accidents = accident_counts[condition] # 차량별 시간대별 사고건수

    minimum = np.min(car_accidents)
    maximum = np.max(car_accidents)

    if maximum == minimum:
        print(f"{car}: 모든 시간대 사고건수가 같아 우선순위 구분 불가")
        continue

    normalized = ((car_accidents - minimum) / (maximum - minimum)) # 정규화 부분

    selected = normalized >= 0.9
    total_count += np.count_nonzero(selected)  # 

    print(f"\n[{car}] 우선 검토 시간대")

    for target, count, score in zip(
        car_targets[selected],
        car_accidents[selected],
        normalized[selected]
    ):
        print(
            f"{target[1]} | 사고 {count}건 "
            f"| 정규화 점수 {score:.3f}")

print(f"\n전체 우선 검토 대상: {total_count}개")  # 추가

# 시내버스, 시외버스, 고속버스, 마을버스, 전세버스, 특수여객(장의), 법인택시,
#  개인택시, 화물차, 렌터카, 위험물운송, 콘크리트믹서, 덤프트럭, 기타/건설기계, 승용차, 버스, 어린이통학버스,

# Step 1. 분석 결과
max_avg = 0
max_vehicle = ""

for vehicle in vehicle_types:
    avg = np.sum(accidents[vehicles == vehicle]) / 12

    if avg > max_avg:
        max_avg = avg
        max_vehicle = vehicle

max_count = 0
max_group = ""

for vehicle in vehicle_types:
    for time in time_types:
        count = np.sum(accidents[(vehicles == vehicle) & (times == time)])

        if count > max_count:
            max_count = count
            max_group = vehicle + " / " + time

print("평균 사고건수가 가장 높은 차량:", max_vehicle, round(max_avg, 2), "건")
print("차량유형+시간대별 최대 사고 그룹:", max_group, max_count, "건")

# Step 2. 특정 위험 그룹 필터링 (Boolean Indexing)

deaths = data[:, 3].astype(int)
serious = data[:, 4].astype(int)

results = []

for vehicle in vehicle_types:
    for time in time_types:
        condition = (vehicles == vehicle) & (times == time)

        total_deaths = np.sum(deaths[condition])
        total_serious = np.sum(serious[condition])

        results.append([vehicle, time, total_deaths, total_serious])

results = np.array(results, dtype=object)

# 사망자 50명 이상 또는 중상자 1,000명 이상
risk = (results[:, 2].astype(int) >= 50) | (results[:, 3].astype(int) >= 1000)
risk_groups = results[risk]

print("위험 그룹 수:", len(risk_groups), "개")
print("위험 그룹:", risk_groups)

# Step 4. 복합 위험군 분석

# 사망자 50명 이상 AND 중상자 1,000명 이상
complex_risk = (results[:, 2].astype(int) >= 50) & (results[:, 3].astype(int) >= 1000)

# Boolean Indexing
complex_groups = results[complex_risk]

# 전체 그룹 대비 비율
ratio = len(complex_groups) / len(results) * 100

print("복합 위험군 수:", len(complex_groups), "개")
print("복합 위험군 비율:", round(ratio, 2), "%")
print("복합 위험군:", complex_groups)

# Step 1. 분석 결과
max_avg = 0
max_vehicle = ""

for vehicle in vehicle_types:
    avg = np.sum(accidents[vehicles == vehicle]) / 12

    if avg > max_avg:
        max_avg = avg
        max_vehicle = vehicle

max_count = 0
max_group = ""

for vehicle in vehicle_types:
    for time in time_types:
        count = np.sum(accidents[(vehicles == vehicle) & (times == time)])

        if count > max_count:
            max_count = count
            max_group = vehicle + " / " + time

print("평균 사고건수가 가장 높은 차량:", max_vehicle, round(max_avg, 2), "건")
print("차량유형+시간대별 최대 사고 그룹:", max_group, max_count, "건")

# Step 2. 특정 위험 그룹 필터링 (Boolean Indexing)

deaths = data[:, 3].astype(int)
serious = data[:, 4].astype(int)

results = []

for vehicle in vehicle_types:
    for time in time_types:
        condition = (vehicles == vehicle) & (times == time)

        total_deaths = np.sum(deaths[condition])
        total_serious = np.sum(serious[condition])

        results.append([vehicle, time, total_deaths, total_serious])

results = np.array(results, dtype=object)

# 사망자 50명 이상 또는 중상자 1,000명 이상
risk = (results[:, 2].astype(int) >= 50) | (results[:, 3].astype(int) >= 1000)
risk_groups = results[risk]

print("위험 그룹 수:", len(risk_groups), "개")
print("위험 그룹:", risk_groups)

# Step 4. 복합 위험군 분석

# 사망자 50명 이상 AND 중상자 1,000명 이상
complex_risk = (results[:, 2].astype(int) >= 50) & (results[:, 3].astype(int) >= 1000)

# Boolean Indexing
complex_groups = results[complex_risk]

# 전체 그룹 대비 비율
ratio = len(complex_groups) / len(results) * 100

print("복합 위험군 수:", len(complex_groups), "개")
print("복합 위험군 비율:", round(ratio, 2), "%")
print("복합 위험군:", complex_groups)