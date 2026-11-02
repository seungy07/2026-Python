import asyncio
from playwright.async_api import async_playwright

# 예제4] 동적 크롤링
# 1) 크롤링할 페이지 (중고나라)  url = "https://web.joongna.com/search/"
async def run():
    # 콘솔에 입력 받기
    keyword = input("중고제품명: ")
    min_price = input("최소 가격: ")
    max_price = input("최대 가격: ")

    # 2) async_playwright() 실행하고 끝날 때 까지 대기상태
    async with async_playwright() as p:
        # 3) 크로미움 실행
        browser = await p.chromium.launch( headless=False ) # 뷰모드
        # 기존 브라우저 선언 아래에 추가
        browser = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
        )

        # 4) 빈 페이지 열기
        page =  await browser.new_page()
        await page.goto( f"https://web.joongna.com/search/{keyword}" )
        await page.wait_for_timeout(3000)

        # 7) 입력받은 값을 웹 페이지에 채우기
        # page.get_by_placeholder('속성값')
        # DOM.fill(값) # 속성갑 대입
        await page.get_by_placeholder('최소 가격').fill(min_price) # html placeholder 이용하여 특정 마크업 식별
        await page.wait_for_timeout(1000)
        await page.get_by_placeholder('최대 가격').fill(max_price)
        await page.wait_for_timeout(1000)

        # 8) 특정한 마크업 클릭 이벤트 실행 , DOM.click()
        await page.get_by_text("적용").click() # 텍스트 '적용' 갖고 있는 마크업 선택
        await page.wait_for_timeout(3000)

        # 9) 제품사진, 제품명, 제품가격 추출, href^ : '/시작주소/' : 시작주소로 식별하는 모든 주소 식벼
        items = await page.query_selector_all("div.group > div > a[href^='/product/']")
        # print( items )

        for item in items: 
            title = await item.query_selector(".typo-body-sm-medium-14")
            title = await title.inner_text() if title else "제품명 없음"
            price = await item.query_selector(".typo-title-lg-semibold-18")
            price = await price.inner_text() if price else "가격 없음"
            img  = await item.query_selector( 'img')
            img = await img.get_attribute('src') if img else "이미지 없음"
            print(title,price,img)

        # 10) 안전하게 브라우저 종료
        await browser.close()
            
asyncio.run(run())