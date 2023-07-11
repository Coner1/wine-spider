import json
import os
import random
from urllib import parse

from playwright.sync_api import Playwright, sync_playwright, Locator, Page, Response

from config import condition_config

data_total_num = 0
data_total_pages = 0
current_page = 0

# Define the directory path
# 输出数据根目录
# 结构如下
# --root
#    --data.txt
#    --images
OUTPUT_DIRECTORY_PATH = condition_config["OUTPUT_DIRECTORY_PATH"]
OUTPUT_FILE_NAME = 'data.txt'


def condition_logic(page: Page):
    global OUTPUT_DIRECTORY_PATH
    base_path = OUTPUT_DIRECTORY_PATH
    if condition_config["searchEnable"]:
        OUTPUT_DIRECTORY_PATH = base_path + "_search_input"
        search_input = page.locator(
            "div > div.header > div > div > div.container-top > div.logo-search > div.search > div > div > input")
        search_input.type(condition_config["searchWords"], delay=100)
    if condition_config["wineTypeEnable"]:
        OUTPUT_DIRECTORY_PATH = base_path + "_type_list"
        # 葡萄酒类别 选项列表
        type_list = page.locator(
            "div.search-list > div.content > div.main-content > div.left-content > div.grape-type > div.type-item") \
            .all()
        wine_type_index = condition_config["wineTypeIndex"]
        for i1, cond1 in enumerate(type_list):
            if i1 < wine_type_index:
                continue
            print(f"type_list, index={i1},value={cond1.text_content()}")
            cond1.click()
            page.wait_for_timeout(random.randrange(3000, 6000))
            load_next_page(page)
            cond1.click()

    if condition_config["scoreEnable"]:
        OUTPUT_DIRECTORY_PATH = base_path + "_rate_list"
        # 平均评分选项列表
        score_list = page.locator(
            "div.search-list > div.content > div.main-content > div.left-content > div.rate-class  div.check-box").all()
        score_index = condition_config["scoreIndex"]
        for i2, cond2 in enumerate(score_list):
            if i2 < score_index:
                continue
            print(f"rate_list, index={i2},value={cond2.text_content()}")
            cond2.click()
            page.wait_for_timeout(random.randrange(1000, 3000))
            load_next_page(page)

    search_items = page.locator(
        "div.search-list > div.content > div.main-content > div.left-content > div.search-items")
    if condition_config["breedEnable"]:
        OUTPUT_DIRECTORY_PATH = base_path + "_breed"
        # 葡萄品种 选项列表
        breed = search_items.all()[0].locator("div.select-content > div.type-item").all()
        breed_index = condition_config["breedIndex"]
        for i3, cond3 in enumerate(breed):
            if i3 < breed_index:
                continue
            print(f"breed_list, index={i3},value={cond3.text_content()}")
            cond3.click()
            page.wait_for_timeout(random.randrange(1000, 3000))
            load_next_page(page)
            breed[0].click()
    if condition_config["areaEnable"]:
        OUTPUT_DIRECTORY_PATH = base_path + "_area"
        # 产区 选项列表
        area = search_items.all()[1].locator("div.select-content > div.type-item").all()
        area_index = condition_config["areaIndex"]
        for i4, cond4 in enumerate(area):
            if i4 < area_index:
                continue
            print(f"area_list, index={i4},value={cond4.text_content()}")
            cond4.click()
            page.wait_for_timeout(random.randrange(1000, 6000))
            load_next_page(page)
            area[0].click()

    if condition_config["nationEnable"]:
        OUTPUT_DIRECTORY_PATH = base_path + "_nation"
        # 国家 选项列表
        nation = search_items.all()[2].locator("div.select-content > div.type-item").all()
        nation_index = condition_config["nationIndex"]
        for i5, cond5 in enumerate(nation):
            if i5 < nation_index:
                continue
            print(f"nation, index={i5},value={cond5.text_content()}")
            cond5.click()
            page.wait_for_timeout(random.randrange(1000, 6000))
            load_next_page(page)
            nation[0].click()

    if condition_config["styleEnable"]:
        OUTPUT_DIRECTORY_PATH = base_path + "_style"
        # 葡萄酒风格 选项列表
        style = search_items.all()[3].locator("div.select-content > div.type-item").all()
        style_index = condition_config["styleIndex"]
        for i6, cond6 in enumerate(style):
            if i6 < style_index:
                continue
            print(f"style, index={i6},value={cond6.text_content()}")
            cond6.click()
            page.wait_for_timeout(random.randrange(1000, 6000))
            load_next_page(page)
            style[0].click()
    if condition_config["assortedEnable"]:
        OUTPUT_DIRECTORY_PATH = base_path + "_assorted"
        # 配餐 选项列表
        assorted = search_items.all()[4].locator("div.select-content > div.type-item").all()
        assorted_index = condition_config["assortedIndex"]
        for i7, cond7 in enumerate(assorted):
            if i7 < assorted_index:
                continue
            print(f"assorted, index={i7},value={cond7.text_content()}")
            cond7.click()
            page.wait_for_timeout(random.randrange(1000, 6000))
            load_next_page(page)
            assorted[0].click()


def print_list(array):
    print_list_array = []
    for i1, v1 in enumerate(array):
        print_list_array.append({i1, v1.text_content()})
    print(print_list_array)


def run(pw: Playwright) -> None:
    browser = pw.chromium.launch(headless=condition_config["headless"], channel='chrome')
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://vivino.cc/search/")
    with page.expect_request("data:image/png;*"):
        page.on("response", on_response)
        condition_logic(page)

    # page.pause()
    context.close()
    browser.close()


def handle_request(route, request):
    print(request.url)
    new_url = request.url.replace("page=1", "page=" + str(current_page + 1))
    print(new_url)
    route.continue_(url=new_url)


def on_response(resp: Response):
    if "nodeFind" in resp.request.url:
        # print(resp.body().decode('utf-8'))
        # print(resp.json())
        json_obj = resp.json()
        data_records = json_obj["data"]["records"]
        # data_total = json_obj["data"]["total"]
        # data_pages = json_obj["data"]["pages"]
        append_to_file(data_records)
        print(f"page data has appended to file")
    if "find-by-uuid" in resp.request.url:
        # print(resp.request.url)
        parsed = parse.urlparse(resp.request.url)
        parsed_q = parse.parse_qs(parsed.query)
        save_image(str(parsed_q["uuid"][0]) + ".png", resp.body())


def load_next_page(page: Page):
    for i in range(20):
        right_content = page.locator("div.search-list > div.content > div.main-content > div.right-content")
        if "没有找到合适的葡萄酒" in right_content.text_content():
            break
        while True:
            right_content = page.locator("div.search-list > div.content > div.main-content > div.right-content")
            loading_locator = right_content.locator("div.el-loading-mask")
            print("waiting for loading, 1s")
            if loading_locator.count() <= 0:
                break
            elif loading_locator.is_hidden():
                break
            page.wait_for_timeout(1000)

        next_button = right_content.locator("div.page > div > button.btn-next")
        if next_button.is_disabled():
            print("this is last page, return break")
            break
        next_button.click()
        page.wait_for_timeout(random.randrange(3000, 6000))
        page.mouse.move(random.randrange(0, 500), random.randrange(0, 500))


def one_page(right_content: Locator):
    page_num = right_content.locator("div.page > div > ul > li.number.active").text_content()
    cards = right_content.locator(".wine-card")
    print(f"load completed,pageNum={page_num},pageCount={cards.count()}")
    rows = []
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
        rows.append({
            "title": title,
            "origin-cn": origin_cn,
            "origin-en": origin_en,
            "tag-desc": tag_desc,
            "rate-counts": rate_counts,
            "rate-numbers": rate_numbers,
            "price": price,
            "img": img_src
        })
        # print(f"{title};{origin_cn};{origin_en};{tag_desc};{rate_counts};{rate_numbers};{price};{img_src}")
    # print(rows)
    append_to_file(rows)


def append_to_file(array: []):
    check_path()

    with open(os.path.join(OUTPUT_DIRECTORY_PATH, OUTPUT_FILE_NAME), mode="at", encoding="utf-8") as f:
        for item in array:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")


def save_image(name, b):
    # Check if the file exists
    image_full_path = os.path.join(os.path.join(OUTPUT_DIRECTORY_PATH, "images"), name)
    if not os.path.exists(image_full_path):
        with open(image_full_path, "wb") as f:
            f.write(b)
            print(
                f"image saved,path={image_full_path}")
    else:
        print(
            f"image exists, path={image_full_path}")


# Create the directory if it doesn't exist
def check_path():
    if not os.path.exists(OUTPUT_DIRECTORY_PATH):
        os.makedirs(OUTPUT_DIRECTORY_PATH)
        print(f"Directory '{OUTPUT_DIRECTORY_PATH}' created successfully.")
    else:
        print(f"Directory '{OUTPUT_DIRECTORY_PATH}' already exists.")

    # Configure logging to write to a file
    # logging.basicConfig(filename=OUTPUT_LOG_PATH, level=print)

    # if not os.path.exists(OUTPUT_IMAGE_PATH):
    #     os.makedirs(OUTPUT_IMAGE_PATH)
    #     print(f"Directory '{OUTPUT_IMAGE_PATH}' created successfully.")
    # else:
    #     print(f"Directory '{OUTPUT_IMAGE_PATH}' already exists.")

    # Check if the file exists
    if not os.path.exists(os.path.join(OUTPUT_DIRECTORY_PATH, OUTPUT_FILE_NAME)):
        # Create the file
        with open(os.path.join(OUTPUT_DIRECTORY_PATH, OUTPUT_FILE_NAME), mode='w', encoding="utf-8") as file_data:
            # Write some initial content to the file if desired
            file_data.write('')

        print(f"File '{os.path.join(OUTPUT_DIRECTORY_PATH, OUTPUT_FILE_NAME)}' created successfully.")
    else:
        print(f"File '{os.path.join(OUTPUT_DIRECTORY_PATH, OUTPUT_FILE_NAME)}' already exists.")

    image_path = os.path.join(OUTPUT_DIRECTORY_PATH, "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)
        print(f"Directory '{image_path}' created successfully.")
    else:
        print(f"Directory '{image_path}' already exists.")


def main():
    # start monitor
    # start_monitor()

    with sync_playwright() as playwright:
        run(playwright)


main()
