from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from helper.fetchTemplates import fetch_template

from models import *
from templates import *
import config as args
    

class intentGPT():
    
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            openai_api_key= args.openai_api_key,
            temperature= 0.2,
            max_tokens=100,
            request_timeout= 30,
            max_retries=4
        )
        
        self.template = fetch_template('intent_identification_template')
        self.prompt = PromptTemplate(template=self.template, input_variables=["query"])
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def aiRespond(self,req: ForIntent):
            
        user_message = req.query
        response = self.chain.run(query=user_message)

        return response
    


