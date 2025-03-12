from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url="https://gist.githubusercontent.com/rsnakul2021/18f0ac4abe776ad644a2aec860be03ab/raw/f54086c1e6e9467a91298671f947386617ad25de/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }
    return data

if __name__ == "__main__":
    load_dotenv()

    print("Hello LangChain")

    summary_template = """
    given the LinkedIn {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo") #temp is the level of creativity

    chain = summary_prompt_template | llm | StrOutputParser() #chain links multiple objects together 
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco/", mock = True)
    res = chain.invoke(input={"information": linkedin_data}) #have to create OPEN_API_KEY and set as env variable before running

    print(res)
