# 범주형(문자) 특성 갖는 학습 방법
# 1) 실습에 필요한 펭귄 계측 데이터
import seaborn as sns
df = sns.load_dataset('penguins')
df.info()

# 2) 전처리 : 결측치 제거
df = df.dropna().reset_index(drop=True) # 인덱스 초기화
df.info()

# 3) 다중분류 실습 위한 특성/타깃
x = df.drop(columns=['species'])
y = df['species'] # Adelie, Chinstrap, Gentoo

# 4) 분리
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)

# 5) 복합형 파이프라인 위한 수치형과 범주형 특성 분리
num_features = ['bill_length_mm', 'bill_depth_mm','flipper_length_mm','body_mass_g'] # 수치형
cat_features = ['island', 'sex'] # 범주형

# 6) 복합 특성
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
# ColumnTransformer( transformers=[ ('식별자', 전처리기, 컬럼명목록) ] )
# OneHotEncoder : 범주형 자료들을 0과 1표현
# drop='first' : 첫번째 범주에 대한 카테고리는 제외, (모두 0으로 채워진 행이면 첫번째 범주 사용)
# sparse_output=False : 반환된 자료들을 numpy 배열로 반환
pp = ColumnTransformer( transformers=[ 
    ('num', StandardScaler(), num_features), # 수치형 특성
    ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_features) # 범주형 특성
] )

# 파이프 라인
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
# Pipeline([ ('식별자', 변환기/추정기) ])
pipe = Pipeline([
    ('pp', pp), ('model', LogisticRegression())
])
pipe.fit(x_train,y_train)
y_pred = pipe.predict(x_test)
print( y_pred[:3])
print(pipe.classes_)
print( np.round(pipe.predict_proba(x_test[:3]),3))

# 리포트
from sklearn.metrics import f1_score, classification_report
print( f1_score(y_test, y_pred, average='macro') )
print( classification_report(y_test,y_pred))

