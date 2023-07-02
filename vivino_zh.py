from playwright.sync_api import Playwright, sync_playwright, Locator, Page
import random


def run(pw: Playwright) -> None:
    browser = pw.chromium.launch(headless=False, channel='chrome')
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://vivino.cc/search/")
    # app > div > div.search-list > div.content > div.main-content > div.right-content > div:wine-card
    # page.wait_for_timeout(5000)
    with page.expect_request("data:image/png;*"):
        on_loaded(page)

    context.close()
    browser.close()


def on_loaded(page: Page):
    while True:
        while True:
            right_content = page.locator("div.search-list > div.content > div.main-content > div.right-content")
            loading_locator = right_content.locator("div.el-loading-mask")
            print(loading_locator.count())
            if loading_locator.count() <= 0:
                break
            elif loading_locator.is_hidden():
                break
            page.wait_for_timeout(random.randrange(100, 1000))

        one_page(right_content)
        next_button = right_content.locator("div.page > div > button.btn-next")
        if next_button.is_disabled():
            print("this is last page, return break")
            break
        next_button.click()
        page.wait_for_timeout(random.randrange(50, 3000))


def one_page(right_content: Locator):
    page_num = right_content.locator("div.page > div > ul > li.number.active").text_content()
    cards = right_content.locator(".wine-card")
    print(f"load completed,pageNum={page_num},pageCount={cards.count()}")
    for row in cards.all():
        loc = row.locator(".wine-bottle > img")
        img_src = loc.get_attribute("src") if loc.count() > 0 else ""

        loc = row.locator(".wine-title")
        title = loc.text_content() if loc.count() > 0 else ""

        loc = row.locator(".wine-origin-cn")
        origin_cn = loc.text_content() if loc.count() > 0 else ""

        loc = row.locator(".wine-oringin-en")
        origin_en = loc.text_content() if loc.count() > 0 else ""

        loc = row.locator(".tag-desc")
        tag_desc = loc.text_content() if loc.count() > 0 else ""

        loc = row.locator(".rate-counts")
        rate_counts = loc.text_content() if loc.count() > 0 else ""

        loc = row.locator(".rate-numbers")
        rate_numbers = loc.text_content() if loc.count() > 0 else ""

        loc = row.locator(".price.price1")
        price = loc.text_content() if loc.count() > 0 else ""
        print(f"{title};{origin_cn};{origin_en};{tag_desc};{rate_counts};{rate_numbers};{price};{img_src}")


with sync_playwright() as playwright:
    run(playwright)
