import re
from nlu_train_model import interpreter
from search_drink import search_drink_inform
from search_material import search_materials
from search_cate import search_cate_drink
from search_drink_instruc import search_instruction
from wxpy import *

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
state = INIT

def get_response(msg):
    cocktail = None

    # Create a pattern for finding capitalized words 条件2： 名字的形式
    cocktail_pattern = re.compile('[A-Z]{1}[a-z]*')  ##  cocktail里面 pattern的正则表达式模式

    # Get the matching words in the string 把cocktail摘出来
    cocktail_words = cocktail_pattern.findall(msg)
    if len(cocktail_words) > 0:
        # Return the name if the keywords are present
        cocktail = ' '.join(cocktail_words)


    intent = interpreter.parse(msg)["intent"]["name"]

    # 判断需要往response里面加信息的意图：
    # 如果是这些意图，就需要往里面添加信息
    (new_state, response) = policy[(state, intent)]  ## message 的意图在这找出来！！
    if intent in ["introduce", "like_ord_drink", "like_cocktail", "ready"]:  # 判断意图，返回需要填加的信息
        add_infor = 0
        if 'introduce' in intent:
            drink_information = search_drink_inform(cocktail)
            add_infor = tuple(drink_information)
            # 如果意图是推荐酒的话，要看看意图里面有没有选择一种类型的酒
        if 'like_ord_drink' in intent:
            add_infor = search_cate_drink("Ordinary Drink")
        if 'like_cocktail' in intent:
            add_infor = search_cate_drink("Cocktail")
            # 如果材料准备好了的话
        if 'ready' in intent:
            add_infor = search_instruction()
        # （新的状态，回答）= 规则中（状态，意图）对应的value
        response = response.format(*add_infor)
    if intent in ["instruct"]:
        add_infor = search_materials(cocktail)
        response = response + add_infor
    return new_state, response

# 主函数
# new_state, ret = get_response(str("can you tell me about Margarita?"))
# state = new_state
# print(state)
# print(ret)
bot = Bot(cache_path=True)
friend = bot.friends().search('许多')[0]  # 按关键字搜索好友
friend.send("---------------------------------Bartender robot is running!!!!---------------------------------")


@bot.register(friend)
def reply_my_friend(msg):

    print(str(msg.text))
    new_state, ret = get_response(str(msg.text))
    global state
    state = new_state
    print(str(ret))
    return ret

embed()










