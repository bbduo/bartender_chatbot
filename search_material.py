import requests
import json

def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def search_materials(drinks):
    url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?"

    querystring = {"s": drinks}

    headers = {
        'x-rapidapi-host': "the-meal-db.p.rapidapi.com",
        'x-rapidapi-key': "bb2e26ff87msh8699471279b3633p1c1767jsna007fb73afc9"
    }
    # response是个json数据,必须要转化一下
    response = requests.request("GET", url, headers=headers, params=querystring)

    # response 是字典类型  {"drinks":[{"idDrink":"11009","strDrink":"Moscow Mule","strDrinkAlternate":null,"strDrinkES":null,"strDrinkDE":null,"strDrinkFR":null,"strDrinkZH-HANS":null,"strDrinkZH-HANT":null,"strTags":"IBA,ContemporaryClassic","strVideo":null,"strCategory":"Punch \/ Party Drink","strIBA":"Contemporary Classics","strAlcoholic":"Alcoholic","strGlass":"Copper Mug","strInstructions":"Combine vodka and ginger beer in a highball glass filled with ice. Add lime juice. Stir gently. Garnish.","strInstructionsES":null,"strInstructionsDE":"Mischen Sie Wodka und Ingwerbier in einem mit Eis gef\u00fcllten Highball-Glas. Limettensaft hinzuf\u00fcgen. Vorsichtig umr\u00fchren. Garnieren.","strInstructionsFR":null,"strInstructionsZH-HANS":null,"strInstructionsZH-HANT":null,"strDrinkThumb":"https:\/\/www.thecocktaildb.com\/images\/media\/drink\/3pylqc1504370988.jpg","strIngredient1":"Vodka","strIngredient2":"Lime juice","strIngredient3":"Ginger ale","strIngredient4":null,"strIngredient5":null,"strIngredient6":null,"strIngredient7":null,"strIngredient8":null,"strIngredient9":null,"strIngredient10":null,"strIngredient11":null,"strIngredient12":null,"strIngredient13":null,"strIngredient14":null,"strIngredient15":null,"strMeasure1":"2 oz ","strMeasure2":"2 oz ","strMeasure3":"8 oz ","strMeasure4":null,"strMeasure5":null,"strMeasure6":null,"strMeasure7":null,"strMeasure8":null,"strMeasure9":null,"strMeasure10":null,"strMeasure11":null,"strMeasure12":null,"strMeasure13":null,"strMeasure14":null,"strMeasure15":null,"strCreativeCommonsConfirmed":"No","dateModified":"2017-09-02 17:49:48"}]}
    response = json.loads(response.text)

    # print(response)

    list = []
    # # # ent就是 {"idDrink":"11009","strDrink":"Moscow Mule","strDrinkAlternate":null,"strDrinkES":n。。。。
    for ent in response["drinks"]:
        # print(ent)
        # for sec_ent in range(ent["strIngredient1"],ent["strIngredient2"]):
        ingre_list = ["strIngredient1", "strIngredient2", "strIngredient3", "strIngredient4", "strIngredient5",
                      "strIngredient6", "strIngredient7", "strIngredient8", "strIngredient9", "strIngredient10",
                      "strIngredient11", "strIngredient12", "strIngredient13", "strIngredient14", "strIngredient15"]
        for k in ingre_list:
            # print(k)
            if ent[k] is not None:
                list.append(ent[k])
                list = getUniqueItems(list)
    list2 = ",".join(list)
    return list2