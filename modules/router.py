import config as args
from models import ForRouter

from helper.routerTemplates import RouterTemplate
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.memory import ConversationSummaryBufferMemory

from langchain.chat_models import ChatOpenAI

from langchain.chains.llm import LLMChain
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate


class RouterGPT:
    q: str = None
    condition: str

    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            openai_api_key= args.openai_api_key,
            temperature= 0.2,
            max_tokens=100,
            request_timeout= 30,
            max_retries=4
        )

    def generate_destination_chains(self, condition):
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm, 
            max_token_limit=100, 
            return_messages=True,
            memory_key="chat_history")
        
        prompt_factory = RouterTemplate(condition)
        destination_chains = {}
        for p_info in prompt_factory.prompt_infos:
            name = p_info['name']
            prompt_template = p_info['prompt_template']
            prompt = PromptTemplate(
            input_variables=["chat_history", "input"], 
            partial_variables= {
                "condition": self.condition
            },
            template= prompt_template
            )
            chain = LLMChain(
                llm=self.llm, 
                prompt=prompt,
                memory= self.memory,
            )
            destination_chains[name] = chain
        default_chain = ConversationChain(llm= self.llm, output_key="text")
        return prompt_factory.prompt_infos, destination_chains, default_chain


    def generate_router_chain(self, prompt_infos, destination_chains, default_chain):
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = '\n'.join(destinations)
        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=['input'],
            output_parser=RouterOutputParser()
        )
        router_chain = LLMRouterChain.from_llm(self.llm, router_prompt)

        return MultiPromptChain(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=default_chain,
            verbose=True
        )


    def route_the_query(self, req: ForRouter):
        self.q = req.query
        self.condition = req.condition

        prompt_infos, destination_chains, default_chain = self.generate_destination_chains(self.condition)
        self.agent_chain = self.generate_router_chain(prompt_infos, destination_chains, default_chain)
        a = self.agent_chain.run(input=self.q)
        return (a)

