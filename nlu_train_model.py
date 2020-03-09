from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer,Interpreter
from rasa_nlu import config



# # def interpret(message):

# 重新训练模型的方法
# trainer = Trainer(config.load("config_spacy.yml"))
# #
# # Load the training data
# training_data = load_data('demo-rasa-onlyintent.json')
# interpreter = trainer.train(training_data)

# 保存模型
# model_directory = trainer.persist('./models/nlu/model_20200307-135959')  # Returns the directory the model is stored in
# 读模型
interpreter = Interpreter.load('./models/nlu/nlu/model_20200308-120117')



# intent = interpreter.parse(message)["intent"]["name"]
# print(intent)
#
# return intent