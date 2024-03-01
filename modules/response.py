from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.cache import InMemoryCache
from models import *
from templates import *
import config as args

class ResponseGPT():
    
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            openai_api_key= args.openai_api_key,
            temperature= 0,
            max_tokens=150,
            request_timeout= 30,
            max_retries=4
        )

        self.prompt = PromptTemplate(template=dc_template, input_variables=["query", "condition"])
        self.memory = ConversationBufferWindowMemory(k=3)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, verbose=True) #, memory=self.memory)


    def aiRespond(self,req: HumanMessage):
            
        user_message = req.query
        user_condition = req.condition

        response = self.chain.run(query=user_message, condition=user_condition)

        return response

    


