import pandas as pd
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
    kiwi.add_user_word('word', 'NNG') # kiwi.add_user_word('새로운단어', '품사키워드')

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

