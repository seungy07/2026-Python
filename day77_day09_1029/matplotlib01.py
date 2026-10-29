# matplotlib : 파이썬에서 시작적으로 표현하는 라이브러리
# 설치 : pip install matplotlib , py -m pip install matplotlib
# 확인
import matplotlib.pyplot as plt
import matplotlib
print(matplotlib.__version__)

# 윈도우 기준 한글 폰트 설정 및 마이너스(-) 기호 깨짐 방지
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False


# 1] 선 차트  plt.plot
epochs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
train_loss = [0.9, 0.7, 0.55, 0.45, 0.38, 0.32, 0.28, 0.25, 0.23, 0.20]
val_loss = [0.95, 0.75, 0.60, 0.52, 0.48, 0.45, 0.44, 0.43, 0.44, 0.45]

# 차트를 어떻게 실행할건지 
plt.figure( figsize=(7,4) ) # 1) 차트의 전체 크기 설정, figsize=( 가로inch, 세로inch )
# 2) 선차트: plt.plot( x축값, y축값 , label = "계열명" , color = "색상명", linestyle="선종류", marker="점모양") 
plt.plot( epochs, train_loss, label="Train Loss", color="blue", linestyle="--", marker="o" )
plt.plot( epochs, val_loss, label="Validation Loss", color="red", linestyle="-", marker="s" )

# 3) 차트 제목
plt.title( 'Epoch별 모델 손실값(Loss) 추세' ) # 차트 큰제목
plt.xlabel( 'Epochs' ) # x축 제목
plt.ylabel( 'Loss' ) # y축 제목

# 4) 차트 배경
plt.grid( True, linestyle=":", alpha=0.6 ) # 눈금선(구분선) alpha: 투명도
plt.legend() # 범례 

plt.show() # 차트 실행

# 2] 바 차트 
classes = ['Cat', 'Dog', 'Bird', 'Fish']
counts = [120, 150, 80, 45]
plt.figure( figsize=(6,4) )

# 2) 바차트: plt.bar( x, y , color=[], width=막대크기 )
bars = plt.bar( classes, counts, color=['#4C72B0', '#55A868', '#C44E52', '#8172B2'], width=0.5 )  # width 막대크기   0.8 기본
# 2-2) 막대 값 레이블 # plt.bar_label( 막대차트변수, padding=막대와레이블간격, fontsize=폰트크기 )
plt.bar_label( bars, padding=3, fontsize=8 ) # (데이터) 계열 값 표시 

plt.title('데이터세 클래스별 샘플 수 바 차트')
plt.xlabel('클래스 레이블')
plt.ylabel('샘플 개수')
plt.grid( axis='y', linestyle='--' , alpha=0.5 ) # 구분선 축 설정, 선 스타일, 투명도
plt.show()

import numpy as np
# 3] 산점도 (상관관계)
x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])
y = np.array([2.3, 3.8, 5.1, 7.0, 7.8, 9.2, 10.5])
plt.figure(figsize=(6,4))

# 3) 산점도 plt.scatter( x, y, color=색상, s=점크기, alpha=투명도 , edgecolors=점테두리색상 )
plt.scatter( x, y, color='purple', s=80, alpha=0.5 )
plt.title('선형 상관관계 산점도')
plt.xlabel('공부 시간')
plt.ylabel('시험 점수')
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()

# 4] 히스토그램 (연속형 수치/값 분포)  
heights = np.random.normal(loc=170, scale=5, size=1000) # loc=평균, scale=표준편차, size=샘플개수 , 종모양 분포( 가우시안 분포 )
plt.figure( figsize=(6,4) )

# 4) 히스토그램 plt.hist( 연속된수치데이터, bins=구간개수, color=, edgecolor=테두리색, alpha= )
plt.hist( heights, bins=30, color='gray', edgecolor='black', alpha=0.7 )
plt.title('종모양 히스토 그램')
plt.xlabel('키 cm')
plt.ylabel('빈도수')
plt.grid(axis='y', linestyle=":")
plt.show()

# 5] 박스플롯 ( 분포 범위내 이상치 확인 )
data_with_outliers = np.append(heights, [210, 215, 120]) # 정상 데이터 사이에 극단값(이상치: 250, 110) 삽입
plt.figure( figsize=(6,4) )

# 5) 박스플롯 plt.boxplot( 수치데이터, vert=세로True/가로방향False 출력 , patch_artist=상자내부 색상 채움True/False  )
plt.boxplot( data_with_outliers, vert=True , patch_artist=True )
plt.title('이상치 탐지 박스플롯')
plt.ylabel('값')
plt.grid(axis='y', linestyle=":", alpha=0.7)
plt.show()

# 6] 다중 그래프, 한번에 출력
#   fig, axs = plt.subplots( 행개수, 열개수, figzise=(가로,세로) )
fig, axs = plt.subplots( 1, 2 , figsize=(10,4) )  # fig 전체 axs는 개별 (공간 , 축)

# 1번 서브 차트  개별로 넣을떄는  set_XXX
axs[0].plot( [1,2,3],[10,20,30], color='green' )
axs[0].set_title('섭 차트 1')
axs[0].set_xlabel('x축')
axs[0].set_ylabel('y축')
axs[0].grid(True)

# 2 번차트
axs[1].bar( ['A', 'B', 'C'], [30,15,40], color='red' )

fig.suptitle('메목') # 전체 제목 # fig.suptitle("두 그래프의 전체 제목") 
# plt 활성화 된 기준
# fig 변수가 가리키는 그림 기준 
plt.title('다중 그래프') # 활성화된 차트 기준 제목

# plt.tight_layout()  # 여백 자동 조정( 레이블 겹칩 방지 필수 옵션)
# plt.savefig('eda_summart.png', dpi=200) #  주의: plt.show() 호출 전에 savefig를 실행해야 백지 저장 방지

plt.show()
 
