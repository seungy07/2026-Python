import pandas as pd
from sklearn.metrics import f1_score
# 리뷰 데이터싯
url = "https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt"
df = pd.read_table(url, names=['rating', 'review'])
df = df[df['rating'] != 3] # 평점 3 제외
df['label'] = (df['rating'] >= 4).astype(int) # 평점 4이상은 긍정, 2이하는 부정
df_sample = df.sample(n=5000, random_state=42).reset_index(drop=True) # 전체 데이터셋에서 특정 n개 샘플링
df_sample.info()
print(df_sample.shape) # (5000, 3)
print(df_sample.head(3))

# '텍스트 마이닝'
# 1) 텍스트에서 전처리 = 정규표현식 자주 사용됨. vs 리액트/JS 입력 유효성검사
import re # 정규표현식 함수
cleaned_list = [] # 정규표현식을 통과한 목록

# 리뷰 텍스트에서 특수문자 제거
for text in df_sample['review']: # 리뷰만 반복
    text =  re.sub( r'[^가-힣a-zA-Z0-9\s]', ' ', str(text) ) # re.sub( r'[표현식]', '치환문자', str() ) 가-힣a-zA-Z0-9\s
    # .join(): 각 리스트 항목 사이에 특정 문자 연결  vs .split() : 하나의 문자열내 특정 문자로 분리하여 리스트로 반환
    cleaned_text =' '.join( text.split() ) # split 기본값 = 공백
    cleaned_list.append(cleaned_text)

df_sample['clean_review'] = cleaned_list
print(df_sample.head(3))

# 2) 한국어 형태소 분석기  , Kiwi
# pip install kiwipiepy
from kiwipiepy import Kiwi
kiwi = Kiwi() # 한국어 형태소 분석기 객체 생성

# 3. 사전 학습에 없는 단어 추가
for word in ['가성비', '내돈내산', '빠른배송']:
    kiwi.add_user_word(word, 'NNG') # kiwi.add_user_word('새로운단어', '품사키워드')

# 4. 불용어 : 핵심 의미가 없는 형태소를 1차적으로 걸러내기 위해
from kiwipiepy.utils import Stopwords
kiwi_stopwords = Stopwords()
custom_stopwords = {'모른다','그저', '그냥'}

# 5. kiwi 이용한 형태소 분석 함수
def tokenize_kiwi( text ):
    # kiwi.tokenize(분석할 문장, stopwords=불용어 객체)
    tokens = kiwi.tokenize(text, stopwords=kiwi_stopwords) 
    # 추출한 품사 키워드 # 5대 핵심 품사(일반명사 NNG, 고유명사 NNP, 동사 VV, 형용사 VA,일반부사 MAG)
    target_tags = {'NNG', 'NNP', 'VV', 'VA', 'MAG'}
    result = []

    for t in tokens: # 토큰나이즈가 된 리스트에서 원하는 것만 필터링/추출
        # t.tag : 품사, t.from : 형태소문자열 반환 
        if t.tag in target_tags and t.form not in custom_stopwords :
        # 내가 원하는 품사에 포함된 단어이면 , 불용어 아니면
            if len( t.form ) > 1 or t.form in {'안', '잘', '못'}: # 일부를 제외한 한단어 제외
                # 동사와 형용사 어간 뒤에 다 붙인다. 좋고, 좋아서, 좋네요 -> 좋다
                word = t.form +'다' if t.tag in {'VV', 'VA'} else t.form
                result.append(word)
    return result

print(df_sample['clean_review'].iloc[0]) # 마감이 안좋아요 실밥도 많고 바느질도 부족한 부분이 몇군데 있네요 교환받기 귀찮아서 그냥 씁니다
print( tokenize_kiwi(df_sample['clean_review'].iloc[0]) ) # ['마감', '안', '바느질', '부족', '부분', '교환', '귀찮다']

# [윗 부분은 전처리, 학습하기전 문장들 쪼개기]
#==========================================================================

# 6. 특성 타깃 분리
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split( 
    #  x= 리뷰, y = 평점라벨(0:부정, 1:긍정)
    df_sample['clean_review'], df_sample['label'],test_size=0.2 ,random_state=42, stratify=df_sample['label'] # 분류 모델에선 비율 맞추기 위해
)

# 7. 리뷰 --> 행렬(벡터) 변환
from sklearn.feature_extraction.text import TfidfVectorizer
# TfidfVectorizer( tokenizer= 토큰나이즈 함수)
tfidf = TfidfVectorizer(  # 자동 중복 제거
    tokenizer=tokenize_kiwi, # 생략시 공백/띄어쓰기 기준으로 분리 # 직접 만든 함수
    token_pattern=None # 실행중 발생하는 로그 비활성화 (활성화시 콘솔에나옴)
)
x_train_tfidf =tfidf.fit_transform(x_train)  # 학습 -> 변환
x_test_tfidf = tfidf.transform(x_test) 

print( x_train_tfidf.shape ) # (4000, 4107) # (문장, 총 단어수(토큰)) 2차원
print( x_test_tfidf.shape ) # (1000, 4107)
# 안녕 사과 바나나 하세요   
# 안녕 딸기 하세요
# (2, 5)
# 안녕 사과 바나나 하세요 딸기
#  1    1    1     1     0 
#   1    0    0     1    1
print( '추출한 피처 10개만 확인: ', tfidf.get_feature_names_out()[:10] ) # 
# 추출한 피처 10개만 확인:  ['가게' '가겨' '가격' '가격대' '가관' '가구' '가까이' '가끔' '가늘다' '가능']
# (문제점) 오타 등 유사한 단어들을 분별 불가능 해서 다른 단어로 취급 
# (해결) 유사도 거리 계산 (임베딩/BERT)


# =======================================================================

# 8. 긍정 / 부정 : 감성 분석
from sklearn.linear_model import LogisticRegression  #실습코드   # 실무적으로는 lightGBM
model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
model.fit( x_train_tfidf, y_train )  # 희소행렬로 학습
pred = model.predict( x_test_tfidf )

print(model.score( x_train_tfidf, y_train )) # 0.89125
print(model.score( x_test_tfidf, y_test )) # 0.834

print( f1_score( y_test, pred )) # 0.826722338204593
# 수치행렬로 확인 가능
print( x_train_tfidf.toarray()[0][:10] ) # [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

# 9. 예측하기
new_reviews = [
    "배송도 정말 빠르고 가성비 최고입니다! 재구매 의사 있어요.",
    "마감 상태가 엉망이고 실밥이 다 터져서 왔네요. 최악입니다.",
    "그냥 가격만큼 하는 것 같아요. 특별히 좋지도 나쁘지도 않음."
]

# 1) 정규표현식
cleaned_new = []
for text in new_reviews:
    text = re.sub( r'[^가-힣a-zA-Z0-9\s]', ' ', str(text) )
    cleaned_new.append( ' '.join(text.split()) )

# 정규표현식 이후 토큰나이즈
new_tfidf = tfidf.transform(cleaned_new)
# 토큰나이즈 이후 모델추론
probs = model.predict_proba(new_tfidf)
# 0.6 이상이면 긍정, 0.4 이하이면 부정 그외 중립
for i in range(len(new_reviews)): # 리뷰 수 만큼 반복
    pos= probs[i][1] # i번쨰 추론 결과 확률(0 인덱스 부정, 1인덱스 긍정 확률)
    if pos >= 0.6:
        contents ='긍정'
    elif pos <= 0.4:
        contents = '부정'
    else : 
        contents = '중립'
    print(f'리뷰: {new_reviews[i]}')
    print(f'감성분석: {contents} 긍정확률: {pos}, 부정확률: {probs[i][0]}')

# 리뷰: 배송도 정말 빠르고 가성비 최고입니다! 재구매 의사 있어요.
# 감성분석: 긍정 긍정확률: 0.9189972774697318, 부정확률: 0.08100272253026819
# 리뷰: 마감 상태가 엉망이고 실밥이 다 터져서 왔네요. 최악입니다.
# 감성분석: 부정 긍정확률: 0.048844698117842665, 부정확률: 0.9511553018821574
# 리뷰: 그냥 가격만큼 하는 것 같아요. 특별히 좋지도 나쁘지도 않음.
# 감성분석: 중립 긍정확률: 0.44430121495596286, 부정확률: 0.5556987850440371