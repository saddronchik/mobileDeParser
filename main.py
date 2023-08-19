import requests
from bs4 import BeautifulSoup
import pymysql
import json
import time

headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2534 Yowser/2.5 Safari/537.36"
} 


def get_url():

    car_brands = ["audi","bmw","mercedes-benz","opel","skoda","volkswagen",
                  "abarth","alfa-romeo","alpina","aston-martin","bentley","bugatti",
                  "buick","cadillac","chevrolet","chrysler","corvette","citroën","cupra",
                  "dacia","daewoo","daihatsu","dfsk","dodge","ds-automobiles","ferrari","fiat",
                  "ford","hummer","hyundai","infiniti","iveco","jac","jaguar","jeep","kia","lada",
                  "lamborghini","lancia","land-rover","lexus","lotus","maserati","mazda","mclaren","mg",
                  "mini","mitsubishi","nissan","peugeot","porsche","renault","rolls-royce","saab","seat","smart",
                  "ssangyong","subaru","suzuki","tesla","toyota","volvo"]
    
    car_id = ["1900__","3500__","17200__","19000__","22900__",
              "25200__","140__","900__","1100__","1700__","3100__","4350__","4400__",
              "4700__","5600__","5700__","6325__","5900__","3__","6600__","6800__","7000__",
              "31864__","7700__","235__","8600__","8800__","9000__","11050__","11600__","11650__",
              "12100__","30708__","12400__","12600__","13200__","14400__","14600__","14700__","14800__",
              "15200__","15900__","16600__","16800__","137__","17300__","17500__","17700__","18700__","19300__",
              "20100__","20700__","21600__","21800__","22500__","23000__","23100__","23500__","23600__","135__",
              "24100__","25100__"]
    
  
    arrai_url = []
    for brand,id in zip(car_brands,car_id):
     
       for count in range(1, 41):
            
            url = f"https://www.mobile.de/ru/автомобиль/{brand}/vhc:car,pgn:{count}pgs:50,ms1:{id}"
            # arrai_url.append(url)
            if arrai_url == []:
                arrai_url.append(url)
            else:
                arrai_url.pop(++0)
                arrai_url.append(url)
           
            for url_page in arrai_url:
                print(arrai_url)
                response = requests.get(url_page, headers=headers)
               
                soup = BeautifulSoup(response.text, "lxml")
                data = soup.find_all("a", class_="track-event")
                   
                for i in data:
                    card_url = "https://www.mobile.de" + i.get("href")
                    yield card_url 


def array_items_teh_spec():
    result_list = []
    for card_url_item in get_url():
        try:
            response = requests.get(card_url_item,headers=headers)
            # time.sleep(1)
            soup = BeautifulSoup(response.text, "lxml")
            data_name = soup.find("div", class_="cBox")
            data = soup.find("div", class_="attributes-box")
            data_tec = soup.find("div", class_="further-tec-data")
            data_img = soup.find("div", class_="js-gallery-img-wrapper")
            data_img2 = soup.find("div", class_="js-slick-thumb")

            name_auto = data_name.find("h1", class_="h2")
            if name_auto == None:
                name_auto = "Марка не найдена"
            else:
                pass
                
            price_auto = data_name.find("p", class_="u-text-bold")
            if price_auto == None:
                price_auto = "цена не найдена"
            else:
                pass

            if price_auto == 'NoneType':
                price_auto = "цена не найдена"
            else:
                pass

            name_auto = name_auto.text
            try:
                connection = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    database='encar',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
                
                price_auto=price_auto.text.split("(Брутто)")[0]
                year_auto = data.find_all("span",class_="u-text-bold")[1].text.split("/")[1]
                mileage = data.find_all("span",class_="u-text-bold")[4].text
                kpp = data.find_all("span",class_="u-text-bold")[2].text
                engine_capacity = data_tec.find_all("span", class_="g-col-6")[1].text

                images_list_urls = []
                img = data_img.find("div",class_="js-load-on-demand").get("data-src")
                # image2 = images_list_urls.append(data_img2.find("img", class_="slick-img").get("src"))
                # print(str(images_list_urls))

                print(name_auto,price_auto,year_auto,mileage,kpp,engine_capacity,img)
            
                with connection.cursor() as cursor:
                    insert = "INSERT INTO `catalog_encar` (`name_auto`,`price_auto`,`year_auto`,`mileage`,`kpp`,`engine_capacity`,`img`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(insert,(name_auto,price_auto,year_auto,mileage,kpp,engine_capacity,img))
                    connection.commit()
                    
            except Exception as ex:
                print(ex)
                
            # result_list.append(
            #     {
            #         "name_auto":name_auto,
            #         "price_auto":price_auto,
            #         "year_auto":year_auto,
            #         "mileage":mileage,
            #         "kpp":kpp,
            #         "engine_capacity":engine_capacity,
            #         "img":img
            #     })

            # with open ("parce_avtos.json","w", encoding='utf-8') as file:
            #     json.dump(result_list, file, indent=4, ensure_ascii=False)

        except Exception as ex:
            print(ex)
        


def main():
    # get_url()
    array_items_teh_spec()


if __name__ == "__main__":
    main()

