import os
from operator import itemgetter


from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.sql_database.query import create_sql_query_chain

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# os.environ['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#
# os.environ['http_proxy'] = '127.0.0.1:7890'
# os.environ['https_proxy'] = '127.0.0.1:7890'
#
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = "LangchainDemo"
# os.environ["LANGCHAIN_API_KEY"] = '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'
# # os.environ["TAVILY_API_KEY"] = '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'

# 聊天机器人案例
# 创建模型
# model = ChatOpenAI(
#     model='glm-4-0520',
#     temperature=0,
#     api_key='1e906fb3b115489b8e1284fe8f2b6c36.nvoWt12LAd0tIWvt',
#     base_url='https://open.bigmodel.cn/api/paas/v4/'
# )
#使用公司提供的open ai来代替
model = ChatOpenAI(
    model='gemini-2.0-flash',
    # model='qwen-max',
    temperature=0,
    api_key='sk-rCV1f1Z5sfNPISzoA1Fd7c2d35C748729eB7BdE071D1C035',
    base_url='https://llm-hub.parcelpanel.com/v1'
)

# sqlalchemy 初始化MySQL数据库的连接
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'returns_db'
USERNAME = 'root'
PASSWORD = 'root'
# mysqlclient驱动URL
MYSQL_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

db = SQLDatabase.from_uri(MYSQL_URI)

# 测试连接是否成功
# print(db.get_usable_table_names())
# print(db.run('select * from t_emp limit 10;'))

# 直接使用大模型和数据库整合, 只能根据你的问题生成SQL
# 初始化生成SQL的chain
create_sql = create_sql_query_chain(model, db)
create_sql = create_sql | (lambda x: x.replace('```sql', '').replace('```', ''))

#
# sql = resp.replace('```sql', '').replace('```', '')
# print(db.run(sql))
# #
answer_prompt = PromptTemplate.from_template(
    """给定以下用户问题, 分析涉及哪些表, 得到SQL语句和SQL执行后的结果，回答用户问题。
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    回答: """
)
# 创建一个执行sql语句的工具
execute_sql_tool = QuerySQLDatabaseTool(db=db)

# 1、生成SQL，2、执行SQL
# 2、模板
chain = (RunnablePassthrough.assign(query=create_sql).
         assign(result=itemgetter('query') | execute_sql_tool)
         | answer_prompt
         | model
         | StrOutputParser()
         )


rep = chain.invoke(input={'question': '已知 hs_code_list 为 hs code 列表，根据 hs_code_describe 描述关键词，对应描述中有互补的描述，获取 hs_code 对应的互补集合，互补是指产品直接的关系'})
print(rep)