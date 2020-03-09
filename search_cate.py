import requests
import json



# 查查看某个种类（ordinary_drink或者cocktail）有什么酒
def search_cate_drink(cate):
    url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?"

    querystring = {"c":cate}

    headers = {
        'x-rapidapi-host': "the-meal-db.p.rapidapi.com",
        'x-rapidapi-key': "bb2e26ff87msh8699471279b3633p1c1767jsna007fb73afc9"
        }
    # response是个json数据,必须要转化一下
    response = requests.request("GET", url, headers=headers, params=querystring)

    response = json.loads(response.text)

    list = []
    # # ent就是 {"idDrink":"11009","strDrink":"Moscow Mule","strDrinkAlternate":null,"strDrinkES":n。。。。
    for ent in response["drinks"]:
        if len(list) < 2:
            list.append(ent["strDrink"])
            list.append(ent["strDrinkThumb"])
    tup = tuple(list)
    return tup
