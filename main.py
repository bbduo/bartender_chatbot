import re
from nlu_train_model import interpreter
from search_drink import search_drink_inform
from search_material import search_materials
from search_cate import search_cate_drink
from search_drink_instruc import search_instruction


# 规则
INIT = 0
CHOOSED_INTRO = 1
CHOOSED_REC = 1
CHOOSED_CRAFT = 1
INFROMED1 = 2
INFROMED2 = 2
CRAFT = 2




# （旧状态，意图）= 规则中（新状态，回答）
policy = {
    (INIT, "none"): (INIT, "I'm sorry, I'm not sure I will help you, I'm just a bartending chatbot!"),
    (INIT, "greet"): (INIT, "Hello, nice to meet you!"),
    (INIT, "ask_explanation"): (INIT, "Hi, I'm a bartending chatbot! I can introduce you to all the cocktails in the world, recommend you a cocktail or teach you how to make it "),
    # 介绍酒
    (INIT, "introduce"): (INIT, "Ok,I will tell you something about it! If you wanna drink {0}, you should use {1}, It gives us the impression：{2}. Here is it {3}"),

    # 推荐酒
    # (1, "introduce"): (2, "Ok,I will tell you something about it! If you wanna drink {0}, you should use {1}, It gives us the impression：{2}. Here is it {3}"),# 介绍酒
    (INIT, "recommand"): (CHOOSED_REC, "Well, What kind of cocktail do you like?(ordinary drink/cocktail)"),
    (CHOOSED_REC, "like_ord_drink"): (INFROMED1, "I recommend  {0} to you, it would not fail to fascinating you! Here is it:{1}"),
    (CHOOSED_REC, "like_cocktail"): (INFROMED2, "I recommend  {0} to you, it would not fail to fascinating you! Here is it:{1}"),
    (INFROMED1,"introduce"):(INIT,"Ok,I will tell you something about it! If you wanna drink {0}, you should use {1}, It gives us the impression：{2}. Here is it {3}"),
    (INFROMED2,"introduce"):(INIT,"Ok,I will tell you something about it! If you wanna drink {0}, you should use {1}, It gives us the impression：{2}. Here is it {3}"),

    # 指导调酒
    (INIT, "instruct"): (CHOOSED_CRAFT, "Are you ready for the materials?:"),
    (CHOOSED_CRAFT,"denny"):(CHOOSED_CRAFT,"get ready for the marterials!"),
    (CHOOSED_CRAFT, "ready"): (INIT, "Ok, Let me teach you how to make {0}:{1}"),
}





#   发送消息
def send_message(policy, state, message):
    # print("USER : {}".format(message))
    new_state, response = respond(policy, state, message)
    print("BOT : {}".format(response))
    return new_state


#   得到回答
def respond(policy, state, message):

    # intent = interpret(message)
    intent = interpreter.parse(message)["intent"]["name"]

    # 判断需要往response里面加信息的意图：
    # 如果是这些意图，就需要往里面添加信息
    (new_state, response) = policy[(state, intent)] ## message 的意图在这找出来！！
    if intent in ["introduce","like_ord_drink","like_cocktail","ready"]: # 判断意图，返回需要填加的信息
        add_infor = judge_intent(intent)
        # （新的状态，回答）= 规则中（状态，意图）对应的value
        response = response.format(*add_infor)
    if intent in ["instruct"]:
        add_infor = judge_intent(intent)
        response = response + add_infor
    return new_state, response


#  找到message里的cocktail
def find_cocktails(message):
    cocktail = None

    # Create a pattern for finding capitalized words 条件2： 名字的形式
    cocktail_pattern = re.compile('[A-Z]{1}[a-z]*')##  cocktail里面 pattern的正则表达式模式

    # Get the matching words in the string 把cocktail摘出来
    cocktail_words = cocktail_pattern.findall(message)
    if len(cocktail_words) > 0:
        # Return the name if the keywords are present
        cocktail = ' '.join(cocktail_words)
    return cocktail


#    判断意图
def judge_intent(intent):
    # 如果意图是介绍一款酒的话
    if 'introduce' in intent:
        drink_information = search_drink_inform(cocktail)
        drink_information = tuple(drink_information)
        return drink_information

    # 如果意图是推荐酒的话，要看看意图里面有没有选择一种类型的酒
    if 'like_ord_drink' in intent:
        rec_drink = search_cate_drink("Ordinary Drink")
        return rec_drink

    if 'like_cocktail' in intent:
        rec_drink = search_cate_drink("Cocktail")
        return rec_drink

    # 如果意图是要找调酒的方法的话，要看看材料准备好没
    if 'instruct' in intent:
        #   materials :   Tequila,Triple sec,Lime juice,Salt,Blue Curacao,Lime Juice,Agave syrup,Ice,Cream of coconut,Strawberry schnapps,Lemon juice,Strawberries
        materials = search_materials(cocktail)
        return materials

    # 如果材料准备好了的话
    if 'ready' in intent:
        instruction = search_instruction()
        return instruction





# 主函数
if __name__ == '__main__':
    state = INIT

    # messages = ("can you tell me about Margarita?",)
    # message = "how can i mix Margarita"
    # cocktail = find_cocktails(message)
    #
    # state = send_message(policy, state, message)

    message = input('USER : ')
    while message is not():
        cocktail = find_cocktails(message)

        state = send_message(policy, state, message)
        message = input('USER : ')






