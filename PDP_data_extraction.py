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
    # 'cookie': 'PJC_ANONYMOUS_COOKIE=cb08a6c0-0bb8-48a2-acff-22acd6125f4c; shared-user-info=1WZJl54aHCKtV4GwRhk9/o4pSwvg+Oz1hqLbpenbd10dLVhPSqDCfREFsPIFxA6Z; coveo_visitorId=95954d72-7f05-4719-a6f5-b7e81af75fce; NSC_JOrqtxzce4j5k4ycwiaupebxpegm3dT=5081a3dc9c1338280550cf40fba63d9b8e4b526da19b5761e34c9fb6716f6d8e3e02c359; OptanonAlertBoxClosed=2025-09-15T10:43:52.372Z; _gcl_au=1.1.964048228.1757933032; _ga=GA1.1.198001054.1757932395; _fbp=fb.1.1757933033261.802363891681333063; coveo_visitorId=95954d72-7f05-4719-a6f5-b7e81af75fce; CRITEO_RETAILER_VISITOR_COOKIE=2676ea53-dba5-4ad3-bbcb-8bdc8cf84b16; _hjSessionUser_741399=eyJpZCI6IjliNjJjNDJmLTc4MTUtNWEzNC1iYjYwLWViMzk0NmE3MjNkOCIsImNyZWF0ZWQiOjE3NTc5MzMwMzMwNDUsImV4aXN0aW5nIjp0cnVlfQ==; JSESSIONID=DDBD4EF26958A67C652D40F63C20A4AC; APP_D_USER_ID=rxNdOiKy-334657262; .ASPXANONYMOUS=V9BsBsQ93AEkAAAAMTRjYTMyODYtZmRlOC00MjdkLTkzMzItMmE0MmJjYWNkODAxt-ZFW2sGsGbK3c24aps-37avQLo1; ASP.NET_SessionId=4wbkriih52hkwnz3g3o0awgy; NSC_JOqdkmqodhdglkmc5kfb10boqnxogeT=4afda3dae0232bdb6451dc9362ca0815ba949dc9d52b8196723e566bae1fd322362033bc; hprl=fr; __cf_bm=fFdTIkxcN.OBZaCSMYCXuSnk8SEJO9YxdG3fuX3HNXI-1757935567-1.0.1.1-d3ixZzNNeuA38oYE8uCr.rOQZrPvtgNnOGVz5iqsvkV2vrsJUqWR8r_TEPAZmLgCU1m1aXImGyLUg8pHWxmlF7UMlaFu76fpdNomsBOoUJo; _cfuvid=jzHpciJaHtwEbs.Ni6w8KXGvCKsicpN1foymOtpGeYU-1757935567651-0.0.1.1-604800000; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+15+2025+16%3A56%3A08+GMT%2B0530+(India+Standard+Time)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=81d7ae33-ef5b-4b66-9f4c-28c0aa585c1d&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&AwaitingReconsent=false&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&intType=1&geolocation=IN%3BGJ; cf_clearance=nXvNtFYwkKp88DLAdGuDcnieMJW0_cCiTnRSLsu8lkw-1757935568-1.2.1.1-to9jPOJv4nxqd0bYwQ4wkSNeQkVXAzdq8eOBWzjGPoehs.uK53Yt0sg21W6sWXm0sGIgpZAXhTIQvCgOtF3mvTMOajUmXp9D44.0y7whHGurW1ytvYdmwGYdddZ7rOZwa2zFhGLk3Nv_l.becVUzAWr3xWejjTCd4AZWBWnJxSS3CIdLu7vzL7.mSgbqOkefUEPWOweiNa2rkpjwkUaHT8e9WeeBQo9.6D92J4rGLuA; cto_bundle=rNIuBV9uNXF6cWJ0Mk1CT2RQenN1UXlVcHhycDhLeXJxQkh2NGVyNk9jd01EcGVydVoxVXlGb0xiUjh1bnlFbm1STEc3bjZSJTJGSHdRVkNFMmc5ZXNyZm9DSkRlNlp3QjVZeHEwZyUyRkNyaG41TTdRQVNtTFJWZzczSk9abnhQdjA1Z0xwQzBDZ05VRTQyREpZVkglMkJTRm82WWFjbDVvNzJQbENTdFJmVEJNbVFxZnRiWk9oTVFrd25Od3BTeUpVZHJoNlFpZERwSktvbmE4WVhKYXJCczJkaUUlMkY3eDFpOWJCb0VvekIzNjdSOWtpZlNkMlRFJTJCUFdrVTRqYlVOcjV6SXBka0YzWmt5VThsMWE0MXNQbjhDcUN4bnIwMVElM0QlM0Q; _ga_S68WMGFS6Y=GS2.1.s1757932395$o1$g1$t1757935569$j27$l0$h0; _ga_TEC2Q17QRF=GS2.1.s1757933032$o1$g1$t1757935569$j27$l0$h0; _hjSession_741399=eyJpZCI6ImMyODZmY2RhLTY2ODYtNGIyMS1iN2UxLTcxYjVlMDE1Y2ZkMSIsImMiOjE3NTc5MzU1Njk0OTEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; forterToken=4939bf08bf29493691a2d8aff940a528_1757935568081__UDF43-m4_21ck_; forter-uid=4939bf08bf29493691a2d8aff940a528_1757935568081__UDF43-m4_21ck__tt',
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
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/puree-biologique-pour-enfants-bananes-fraises-peches/p/858860001039",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/puree-biologique-pour-enfants-pommes-kiwi-epinards-brocoli/p/858860001121",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/puree-biologique-mangue-peche-carotte-patate-douce/p/055000382229",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/lait-maternise/isomil-preparation-pour-nourrissons-a-base-de-soya-0-mois/p/055325988687",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/lait-maternise/pro-advance-preparation-pour-nourrissons-a-base-de-lait-enrechie-de-fer-0-mois/p/055325002819",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/baby-mum-mum-gaufrettes-de-dentition-douces-banane/p/686352809678",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/baby-mum-mum-gaufrettes-de-dentition-douces-fruits-tropicaux/p/686352602354",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/toddler-mum-mum-biscottes-de-dentition-fraise/p/686352808572",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/plus-3g-proteines-nourriture-biologique-pour-bebes-bananes-figues-avoine-et-yogourt-grec/p/628619200019",
        "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/baby-mum-mum-biscuits-de-dentition-pour-poupon-bleuet/p/686352605270",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/puree-biologique-banane-mangue-avocat-vanille/p/055000382205",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/gel-nettoyant-pour-bebe-avant-le-dodo/p/055989070322",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/cereales-bebe-pomme-et-cannelle/p/627987975994",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/lait-maternise/precision-lait-infantile-en-poudre-pour-les-6-12-mois/p/3572731403582",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/lait-maternise/riz-preparation-pour-nourrissons-0-12-mois/p/3572731403704",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/lait-maternise/enfamil/p/056796004784",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/cereale/gerber-ble-yogourt-pomme-poire-et-banane/p/065000684452",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/cereale/gerber-5-cereales-pommes-et-oranges/p/015000141547",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/purree-biologique-pour-bebe-a-saveur-de-smoothie-vert-tropical/p/628619800479",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/biscottes-biologiques-pour-bebe-a-saveur-de-pomme-et-patate-douce/p/628619800448",
        # "https://www.jeancoutu.com/magasiner/categories/confiserie-et-epicerie/bebe/aliments-et-jus/collation-pour-bebe-au-cheddar/p/628619881157",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/purree-biologique-pour-bebe-aux-carottes-et-cereales-anciennes/p/628619880945",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/cereale/cereales-pour-bebes-biologique-ble-et-avoine-complete-mangue-et-carotte/p/055000381772",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/lait-maternise/precision-lait-infantile-en-poudre-pour-les-0-6-mois/p/3572731403575",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/batonnets-biologique-pour-bebe-a-saveur-de-carotte/p/628619800332",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/purree-biologique-pour-bebe-a-la-noix-de-coco-et-baies/p/628619800486",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/cereales-bebe-bleuet-coco/p/627987976014",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/cereale/cereales-pour-bebes-biologique-ble-et-avoine-complete-banane/p/055000381765",
        # "https://www.jeancoutu.com/magasiner/categories/bebe/epicerie/aliments-et-jus/barres-de-fruits-legumes-et-avoine-biologiques-a-saveur-de-fraise-et-carotte/p/628619880921",
        # "https://www.jeancoutu.com/magasiner/categories/confiserie-et-epicerie/bebe/aliments-et-jus/crunchers-collation-pour-bebe-delice-aux-legumes/p/628619881140",
    ]

    # if not urls_list:
    #     print("No pending tasks found.")
    #     return

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
