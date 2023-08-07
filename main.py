import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2534 Yowser/2.5 Safari/537.36"
} 


def get_url():
    for count in range(1, 2):

        url = f"https://www.mobile.de/ru/категория/автомобиль/vhc:car,pgn:{count}pgs:50"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("a", class_="track-event")
        
        for i in data:
            card_url = "https://www.mobile.de" + i.get("href")
            # print (card_url)
            yield card_url 


def array_items_price_name():
    # result_list = []
    for card_url_item in get_url():
        response = requests.get(card_url_item,headers=headers)
        # time.sleep(1)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("div", class_="cBox")
       
        # name_auto = data.find("h1", class_="h2").text
        # price_auto = data.find("p", class_="u-text-bold").text.split("(Брутто)")[0]

    print(data)

    # result_list.append(
    #         {
    #             "name_auto":name_auto,
    #             "price_auto":price_auto,
                
    #         }
    # )

    # with open ("parce_result.json","w") as file:
    #     json.dump(result_list, file, indent=4, ensure_ascii=False)
        
    return "[INFO] Data collected successfully!"
        # print(data)

def array_items_teh_spec():
    result_list = []
    for card_url_item in get_url():
        try:
            response = requests.get(card_url_item,headers=headers)
            time.sleep(1)
            soup = BeautifulSoup(response.text, "lxml")
            data_name = soup.find("div", class_="cBox")
            data = soup.find("div", class_="attributes-box")
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
                # print(price_auto.text.split("(Брутто)")[0])

            if price_auto == 'NoneType':
                price_auto = "цена не найдена"
            else:
                pass
                # print(price_auto.text.split("(Брутто)")[0])
            name_auto = name_auto.text
            price_auto=price_auto.text.split("(Брутто)")[0]
            year_auto = data.find_all("span",class_="u-text-bold")[1].text
            mileage = data.find_all("span",class_="u-text-bold")[4].text
            kpp = data.find_all("span",class_="u-text-bold")[2].text

            print(name_auto,price_auto,year_auto,mileage,kpp)
            result_list.append(
                {
                    "name_auto":name_auto,
                    "price_auto":price_auto,
                    "year_auto":year_auto,
                    "mileage":mileage,
                    "kpp":kpp,
                })

            with open ("parce_result.json","w", encoding='utf-8') as file:
                json.dump(result_list, file, indent=4, ensure_ascii=False)
        except Exception as ex:
            print(ex)
        
        



        # data = soup.find("div", class_="further-tec-data")
       
        # if len(data) != 0:
        #     engine_capacity = data.find_all("span",class_="u-text-bold")[5].text
        #     print(engine_capacity)
        #     # 
        #     # print(engine_capacity)
        # else:
        #     pass
      

        # engine_capacity = data.select_one('.u-text-bold:nth-of-type(1)')


def main():
    array_items_teh_spec()


if __name__ == "__main__":
    main()

