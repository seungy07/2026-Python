# Practice7 문제 [ 씨네21(Cine21) 영화 평점 및 핵심 정보 수집 ]  # 정적 페이지 사용 가능
# 출처 및 대상: 씨네21 영화 평점 페이지, https://cine21.com/movie/point


# [1. 목표]
# Playwright의 비동기 제어와 동적 페이지네이션(click)을 활용해 여러 페이지를 순회한다. # 
# 영화 아이템 카드에서 제목, 이미지 링크, 전문가 평점 3가지 핵심 데이터를 정확히 추출하여 구조화한다.

# [2. 데이터 수집 요구사항]
# 2-1 (페이지 순회): 1페이지부터 3페이지까지 반복문을 통해 동적으로 페이지를 이동한다.
# 2-2 (요소 추출): 각 영화 카드 내부에서 아래 3가지 요소를 각각 수집한다.
# 제목: .title 태그의 텍스트
# 이미지: img 태그의 src 속성값
# 전문가 평점: 평점 정보가 담긴 텍스트

# 2-3 (데이터 적재): 수집된 데이터를 딕셔너리로 묶어 리스트에 저장하고 최종 출력한다.
import asyncio
from playwright.async_api import async_playwright
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()
        await page.goto("https://cine21.com/movie/point")
        await page.wait_for_timeout(3000)

        movie_list = []
        for page_num in range(1,4):
            await page.locator(f'a[href="javascript:fetch_point_list({page_num})"]').click()
            await page.wait_for_timeout(3000)

            items = await page.query_selector_all(".list_with_upthumb_item a[href^='/movie/info/']")

            for item in items:
                title = await item.query_selector(".title")
                title = await title.inner_text() if title else "제목없음"
                img = await item.query_selector('img')
                img = await img.get_attribute('src') if img else "이미지 없음"
                rating = await item.query_selector('.star_on')
                rating =await rating.get_attribute('style') if rating else "평점없음"
                ## 평점 5점 만점은 변환은 나중에 ㅎㅎ

                movie_list.append({ '제목':title , '이미지': img , '전문가 평점':rating })

        await browser.close()
        return print(movie_list)

asyncio.run(run())

# 교수님 코드
# # p.title  , .img_wrap>img , .star_wrap > p.num
# # 4. 클릭이벤트 : dom.click() ,  .pagination .page a

# # 1] 라이브러리 호출 
# import asyncio # 비동기 라이브러리
# from playwright.async_api import async_playwright # 크롤링 라이브러리 
# # 2] 비동기 통신( 씨네21 비동기 페이지 이라서 ) 하기 위한 함수 선언 
# async def 실습7() : 
#     # 3] 비동기 통신 실행하고 종료 까지 브라우저(크로미움) 관리 
#     async with async_playwright() as 비동기통신 : 
#         # 4] 크롬과 비슷한 백그라운드 실행 가능한 브라우저 프로그램 
#         브라우저 = await 비동기통신.chromium.launch( headless= False ) # False = 뷰모드 # True = 백드라운드모드 
#         # 5] 브라우저에 새탭/페이지 열기 
#         페이지 = await 브라우저.new_page()
#         # 6] 열린페이지에 원하는 홈페이지 주소로 이동 
#         await 페이지.goto( "https://cine21.com/movie/point" )
#         await 페이지.wait_for_timeout( 5000 ) # 밀리초 만큼 일시정지 
#         # =============================================================  #
#         for i in range( 1, 4 ) :                # 1 부터 3까지 반복 
#             # 7] query_selector_all( 식별자 ) : 여러개 DOM 반환 , query_selector( 식별자 ) : 한개 DOM 반환 
#             페이지버튼리스트 = await 페이지.query_selector_all( '.pagination .page a')
#             # 8] 반복문 이용하여 버튼 하나씩 클릭 .click()
#             await 페이지버튼리스트[ i - 1 ].click()       # 0 인덱스 부터 a 마크업 클릭이벤트 
#             await 페이지.wait_for_timeout( 5000 )
#             # 9] 
#             items = await 페이지.query_selector_all('.list_with_upthumb_item')
#             for item in items : 
#                 # p.title  , .img_wrap>img , .star_wrap > p.num
#                 영화제목 = await item.query_selector( '.title')
#                 영화제목 = await 영화제목.inner_text() if 영화제목 else "제목없음" 
#                 이미지링크 = await item.query_selector( '.img_wrap>img')
#                 이미지링크 = await 이미지링크.get_attribute('src') if 이미지링크 else "이미지없음" 
#                 전문가평점 = await item.query_selector( '.star_wrap > p.num')
#                 전문가평점 = await 전문가평점.inner_text() if 전문가평점 else "전문가평점없음" 
#                 print( 영화제목 , 이미지링크 , 전문가평점 )
# asyncio.run( 실습7() )