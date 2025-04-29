from fastapi import HTTPException
from langchain_aws import ChatBedrock
from langchain_community.utilities import SQLDatabase
from langchain.prompts import ChatPromptTemplate
from sqlalchemy.exc import SQLAlchemyError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from urllib.parse import quote_plus
from src.config import settings

from src.agent.prompt_template import (
    get_full_sql_agent_prompt,
    get_sql_chain_prompt,
)

# DB Connection
ENCODED_PASSWORD = quote_plus(settings.db_password)
database_url = f"postgresql+psycopg2://{settings.db_user}:{ENCODED_PASSWORD}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
db = SQLDatabase.from_uri(database_url)

llm = ChatBedrock(
    model_id=settings.foundational_model,
    region_name=settings.aws_region,
    temperature=0,
    streaming=False,
)

sql_prompt = ChatPromptTemplate.from_template(get_sql_chain_prompt())


def get_schema(_):
    schema = db.get_table_info()
    return schema


def run_query(query):
    try:
        result = db.run(query)
        return result
    except SQLAlchemyError as e:
        return f"SQL ERROR: {str(e)}"


sql_chain = (
    RunnablePassthrough.assign(schema=get_schema) | sql_prompt | llm | StrOutputParser()
)


full_prompt = ChatPromptTemplate.from_template(get_full_sql_agent_prompt())

response_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=get_schema,
        response=lambda items: run_query(items["query"]),
    )
    | full_prompt
    | llm
)
