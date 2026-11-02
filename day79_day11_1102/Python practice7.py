# Practice7 문제 [ 씨네21(Cine21) 영화 평점 및 핵심 정보 수집 ]
# 출처 및 대상: 씨네21 영화 평점 페이지, https://cine21.com/movie/point
import asyncio
from playwright.async_api import async_playwright

# [1. 목표]
# Playwright의 비동기 제어와 동적 페이지네이션(click)을 활용해 여러 페이지를 순회한다.
# 영화 아이템 카드에서 제목, 이미지 링크, 전문가 평점 3가지 핵심 데이터를 정확히 추출하여 구조화한다.

# [2. 데이터 수집 요구사항]
# 2-1 (페이지 순회): 1페이지부터 3페이지까지 반복문을 통해 동적으로 페이지를 이동한다.
# 2-2 (요소 추출): 각 영화 카드 내부에서 아래 3가지 요소를 각각 수집한다.
# 제목: .title 태그의 텍스트
# 이미지: img 태그의 src 속성값
# 전문가 평점: 평점 정보가 담긴 텍스트

# 2-3 (데이터 적재): 수집된 데이터를 딕셔너리로 묶어 리스트에 저장하고 최종 출력한다.

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
