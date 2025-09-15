import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from curl_cffi import requests
from parsel import Selector
import pandas as pd

folder_path = r"D:\Danesh\jeancoutu\image_download"
os.makedirs(folder_path, exist_ok=True)


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

results_list = []

def process_task(fetch_Product_URL):

    response = requests.get(url=fetch_Product_URL,  headers=headers, impersonate="chrome120")
    if "pi--name" in response.text and response.status_code == 200:
        # TODO::Contain json
        try:
            my_common_selector = Selector(response.text)
        except Exception as e:
            print(e)

        item = {}

        #TODO:: Link
        try:
            item['Link'] = fetch_Product_URL
        except:...

        # TODO:: prouct_id
        try:
            product_id = fetch_Product_URL.split("/p/")[-1]
            item['prouct_id'] = product_id
        except:...

        # TODO:: product_brand
        try:
            product_brand = my_common_selector.xpath('//div[@class="pi--brand"]/text()').get()
            item['product_brand'] = product_brand.strip() if product_brand else ""
        except:
            ...

        # TODO:: product_name
        try:
            product_name = my_common_selector.xpath('//div[@class="pi--name"]/h1/text()').get()
            item['product_name'] = product_name.strip() if product_name else ""
        except:
            ...

        # TODO:: breadcrumb
        try:
            breadcrumb = my_common_selector.xpath('//div[@class="breadcrumb breadcrumb--desktop"]/ul/li/a/span/text()').getall()
            item['breadcrumb'] = ",".join(breadcrumb) if breadcrumb else ""
        except:
            ...

        # TODO:: unit
        try:
            unit = my_common_selector.xpath('//div[@class="pi--weight"]/text()').get()
            item['unit'] = unit.strip() if unit else ""
        except:...

        # TODO:: image
        try:
            image = my_common_selector.xpath('//picture[@class="pi--main-img defaultable-picture"]//img/@src').getall()
            if not image:
                image = my_common_selector.xpath('//picture[@class="pi--main-img defaultable-picture"]/img/@src').getall()
            if not image:
                image = my_common_selector.xpath('//div[@class="pi--product--img pt__carousel"]//div[@class="slick-list"]//picture/img/@src').getall()
            item['image'] = ",".join(image)
        except:...

        #TODO::img Download
        try:
            # URL of the image
            image_url = item['image']
            file_path = os.path.join(folder_path, f"{product_id}.jpg")
            response = requests.get(image_url.split(",")[0])

            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
            else:
                print(image_url)
                print(f"Failed to download image. Status code: {response.status_code}")
        except:...

        # TODO:: price // mrp
        try:
            price = my_common_selector.xpath('//div[@class="pdpDetailsContainer relative"]//span[@class="price-update pi-price-promo"]/text()').get()
            if not price:
                price = my_common_selector.xpath('//div[@class="pdpDetailsContainer relative"]//span[@class="price-update"]/text()').get()
            mrp = my_common_selector.xpath('//div[@class="pdpDetailsContainer relative"]//div[@class="pricing__before-price"]/span[contains(text(),"$")]/text()').get()

            if price and mrp:
                item['price'] = price.replace("$","").replace(",",".").strip()
                item['mrp'] = mrp.replace("$","").replace(",",".").strip()
            elif price and not mrp:
                item['price'] = price.replace("$", "").replace(",", ".").strip()
                item['mrp'] = price.replace("$", "").replace(",", ".").strip()
            else:
                item['price'] = "N/A"
                item['mrp'] = "N/A"
        except:
            ...

        #TODO:: Inventory
        try:
            Inventory_check = my_common_selector.xpath('//div[@class="pi--stock-level in-stock"]//p[contains(text(),"disponibles")]//text()').get()
            invertory = (Inventory_check.split("disponibles")[0]).strip() if 'disponibles' in Inventory_check else ""
            item['invertory'] = (invertory.strip()).replace("\u202f",'') if invertory else ""
        except:...

        #TODO:: description
        try:
            description_checks = my_common_selector.xpath('//div[@class="accordion--standalone pi--additional-info accordion-default-is_initialized active"]//div[@class="accordion--text"]/p/text()').get()
            description = description_checks
            if not description_checks:
                description_checks = my_common_selector.xpath('//meta[@name="description"][contains(@content,":")]/@content').get()
                description = description_checks.split(":")[-1] if ":" in description_checks else ""
                if not description_checks:
                    description_checks = my_common_selector.xpath('//div[@class="accordion--standalone pi--additional-info accordion-default-is_initialized active"]//div[@class="accordion--text"]/p/text()').get()
                    description = description_checks
            item["description"] = description.strip() if description else ""
        except:...

        #TODO:: ingredient
        try:
            ingredient_checks = my_common_selector.xpath('//div[@class="accordion--standalone pi--additional-info accordion-default-is_initialized active"]//div[@class="accordion--text"]/p/text()').get()
            if not ingredient_checks:
                ingredient_checks = my_common_selector.xpath('//button[contains(text(),"Ingrédients")]/following-sibling::div/p/text()').get()
            item["ingredient"] = ingredient_checks.strip() if ingredient_checks else ""
        except:...

        #TODO:: other_data
        try:
            other_data_list = my_common_selector.xpath('//div[@class="pc--icons"]/div/p/text()').getall()
            item["other_data"] = other_data_list if other_data_list else ""
        except:...

        results_list.append(item)
        print("Done")

def main():
    MAX_THREADS = 30

    urls_list = [
        "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/puree-biologique-pour-enfants-bananes-fraises-peches/p/858860001039",
    ]

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for url in urls_list:
            future = executor.submit(process_task, url)
            futures.append(future)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing task: {e}")

    print("All tasks completed.")

if __name__ == '__main__':
    main()

# print(results_list)
df = pd.DataFrame(results_list)

# Export to Excel
output_path = "jeancoutu_sampledata.xlsx"
df.to_excel(output_path, index=False)
print(f"Excel file saved to {output_path}")
