from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from helper.fetchTemplates import fetch_template
from models import *
# from templates import *
import config as args

class ResponseGPT():
    
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            openai_api_key= args.openai_api_key,
            temperature= 0.2,
            max_tokens=150,
            request_timeout= 30,
            max_retries=4
        )
        
        self.template = fetch_template('response_template')
        self.prompt = PromptTemplate(template=self.template, input_variables=["query", "condition"])
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, verbose=True) #, memory=self.memory)


    def aiRespond(self,req: HumanMessage):
            
        user_message = req.query
        user_condition = req.condition

        response = self.chain.run(query=user_message, condition=user_condition)

        return response

    


