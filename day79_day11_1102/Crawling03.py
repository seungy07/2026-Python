# 예제3] 동적 페이지 크롤링, 대시/이벤트 존재하는 상태
# pip install playwright # 셀레니움과 비슷한 동적 페이지 조작 라이브러리
# playwright install # 크롬(구글회사브라우저)과 비슷한 백그라운드 브라우저 (크로미움)

import asyncio  # 비동기 라이브러리
from playwright.async_api import async_playwright # 비동기 동적 페이지 라이브러리

# 1) 크롤링할 페이지 주소 가져온다. 파라미터 분석
url = "https://search.naver.com/search.naver?ssc=tab.image.all&query=짱구"

# 2) 비동기 페이지들을 동기화로 제어하는 함수 만들기
# async def 함수명(): # 함수 선언 동기화
async def run():
    # 2-1)  async_playwright() 실행 하고 종료되기 전까지 동기화 처리
    async with async_playwright() as p:
        # 2-2) 크로미움)구글회사에서 제공하는 백그라운드용 오픈소스 브라우저) 
        # await p.chromium.lanuch( headless = True(백그라운드)/False(뷰모드))
        brower = await p.chromium.launch( headless = False)
        # 2-3) 현재 실행된 크로미움의 새로운 페이지(빈 페이지) 열기
        page = await brower.new_page()
        # 2-4) 빈 페이지에 특정한 URL 주소 대입/이동
        await page.goto( url )
        # 3) 스크롤 내리기
        for i in range(2):
            await page.wait_for_timeout( 2000 ) # 스크롤 대기상태 (밀리초)
            # await page.evaluate("JS 코드 삽입")
            # window.scrollTo() : 스크롤 이동 함수
            # document.body.scrollHeight : 현재 페이지의 스크롤 세로높이
            await page.evaluate( "window.scrollTo(0,document.body.scrollHeight)" ) # 현재 스크롤을 페이지의 가장 하단으로 이동

            # 4) 특정 마크업 가져오기  ,query_selector_all 여러개 추출  //  query_selector 한개 추출
            items = await page.query_selector_all('.tile_item') # 이미지와 사진이름 포함하는 마크업 여러개
            print(items)

            # 5) 반복문 이용한 사진/제목
            for item in items:
                title = await item.query_selector('.info_title')
                title = await title.inner_text() if title else '제목없음' # 특정한 마크업의 사이 텍스트 추출( .inner_text )
                img = await item.query_selector('img._fe_image_tab_content_thumbnail_image')
                img = await img.get_attribute('src') if img else '이미지없음' # 특정마크업의 속성값 추출
                print(title, img)

# ** asyncio.run( 동기화함수() ) 
asyncio.run( run() )
