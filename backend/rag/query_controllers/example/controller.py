import asyncio
import json

import async_timeout
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever, MultiQueryRetriever
from langchain.schema.vectorstore import VectorStoreRetriever
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.chat_models import GigaChat

from backend.logger import logger
from backend.rag.embedders.embedder import get_embedder
from backend.rag.metadata_store.client import METADATA_STORE_CLIENT
from backend.rag.query_controllers.example.schemas import GENERATION_TIMEOUT_SEC, ExampleQueryInput, AnswerResultDto
from backend.rag.reranker import MxBaiReranker
from backend.rag.vector_db.client import VECTOR_STORE_CLIENT
from backend.settings import settings


class ExampleQueryController:
    """
    Ответ на вопрос с примерами из коллекции документов
    """

    @classmethod
    async def answer(cls, request: ExampleQueryInput):
        """
        Метод для ответа на вопросы, используя контекст из коллекции
        """
        # Get the vector store
        vector_store = await cls._get_vector_store(request.collection_name)

        # Create the QA prompt templates
        QA_PROMPT = cls._get_prompt_template(
            input_variables=["context", "question"],
            template=request.prompt_template,
        )

        # Get the LLM
        llm = cls._get_llm(request.llm_configuration, request.stream)

        # get retriever
        retriever = await cls._get_retriever(
            vector_store=vector_store,
            retriever_name=request.retriever_name,
            retriever_config=request.retriever_config,
        )

        # Using LCEL
        rag_chain_from_docs = (
                RunnablePassthrough.assign(
                    context=(lambda x: cls._format_docs(x["context"]))
                )
                | QA_PROMPT
                | llm
                | StrOutputParser()
        )

        rag_chain_with_source = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        ).assign(answer=rag_chain_from_docs)

        if request.stream:
            return StreamingResponse(
                cls._stream_answer(rag_chain_with_source, request.query),
                media_type="text/event-stream",
            )

        else:
            outputs = await rag_chain_with_source.ainvoke(request.query)

            # Intermediate testing
            # Just the retriever
            # setup_and_retrieval = RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            # outputs = await setup_and_retrieval.ainvoke(request.query)
            # print(outputs)

            # Retriver and QA
            # outputs = await (setup_and_retrieval | QA_PROMPT).ainvoke(request.query)
            # print(outputs)

            # Retriver, QA and LLM
            # outputs = await (setup_and_retrieval | QA_PROMPT | llm).ainvoke(request.query)
            # print(outputs)
            if outputs["context"]:
                res = AnswerResultDto(answer=outputs["answer"], docs=[out.dict() for out in outputs["context"]])
            else:
                res = AnswerResultDto(answer=outputs["answer"], docs=[])
            return res

    @classmethod
    async def _stream_answer(cls, rag_chain, query):
        async with async_timeout.timeout(GENERATION_TIMEOUT_SEC):
            try:
                async for chunk in rag_chain.astream(query):
                    if "question " in chunk:
                        # print("Question: ", chunk['question'])
                        yield json.dumps({"question": chunk["question"]})
                        await asyncio.sleep(0.1)
                    elif "context" in chunk:
                        # print("Context: ", cls._format_docs_for_stream(chunk['context']))
                        yield json.dumps(
                            {"docs": cls._format_docs_for_stream(chunk["context"])}
                        )
                        await asyncio.sleep(0.1)
                    elif "answer" in chunk:
                        # print("Answer: ", chunk['answer'])
                        yield json.dumps({"answer": chunk["answer"]})
                        await asyncio.sleep(0.1)

                yield json.dumps({"end": "<END>"})
            except asyncio.TimeoutError:
                raise HTTPException(status_code=504, detail="Stream timed out")

    @staticmethod
    def _get_llm(llm_configuration, stream=False):
        """
        Возвращает объект LLM
        """
        system = "Ты — русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
        if llm_configuration.provider == "gigachat":
            logger.debug(f"Using GigaChat model {llm_configuration.name}")
            llm = GigaChat(
                credentials=settings.GIGACHAT_API_KEY,
                temperature=llm_configuration.parameters.get("temperature", 0.1),
                streaming=stream,
                verify_ssl_certs=False
            )
        else:  # llm_configuration.provider == "ollama":
            logger.debug(f"Using Ollama model {llm_configuration.name}")
            llm = ChatOllama(
                base_url=settings.OLLAMA_URL,
                model=llm_configuration.name,
                temperature=llm_configuration.parameters.get("temperature", 0.1),
                system=system,
            )
        return llm

    @staticmethod
    def _get_prompt_template(input_variables, template):
        """
        Возвращает prompt-шаблон
        """
        return PromptTemplate(input_variables=input_variables, template=template)

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    @staticmethod
    def _format_docs_for_stream(docs):
        return [
            {"page_content": doc.page_content, "metadata": doc.metadata} for doc in docs
        ]

    @staticmethod
    async def _get_vector_store(collection_name: str):
        """
        Возвращает vector store для коллекции
        """
        collection = METADATA_STORE_CLIENT.get_collection_by_name(collection_name)

        if collection is None:
            raise HTTPException(status_code=404, detail="Collection not found")

        return VECTOR_STORE_CLIENT.get_vector_store(
            collection_name=collection.name,
            embeddings=get_embedder(collection.embedder_config),
        )

    @staticmethod
    def _get_vector_store_retriever(vector_store, retriever_config):
        """
        Возвращает vector store retriever
        """
        return VectorStoreRetriever(
            vectorstore=vector_store,
            search_type=retriever_config.search_type,
            search_kwargs=retriever_config.search_kwargs,
        )

    @classmethod
    def _get_contextual_compression_retriever(cls, vector_store, retriever_config):
        """
        Возвращает contextual compression retriever
        """
        # Using mixbread-ai Reranker
        if retriever_config.compressor_model_provider == "mixbread-ai":
            retriever = cls._get_vector_store_retriever(vector_store, retriever_config)

            compressor = MxBaiReranker(
                model=retriever_config.compressor_model_name,
                top_k=retriever_config.top_k,
            )

            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=retriever
            )

            return compression_retriever
        # Can add other rerankers too!
        else:
            raise HTTPException(
                status_code=404, detail="Compressor model provider not found"
            )

    @classmethod
    def _get_multi_query_retriever(
            cls, vector_store, retriever_config, retriever_type="vectorstore"
    ):
        """
        Возвращает multi query retriever
        """
        if retriever_type == "vectorstore":
            base_retriever = cls._get_vector_store_retriever(
                vector_store, retriever_config
            )
        else:  # elif retriever_type == "contextual-compression":
            base_retriever = cls._get_contextual_compression_retriever(
                vector_store, retriever_config
            )

        return MultiQueryRetriever.from_llm(
            retriever=base_retriever,
            llm=cls._get_llm(retriever_config.retriever_llm_configuration),
        )

    @classmethod
    async def _get_retriever(cls, vector_store, retriever_name, retriever_config):
        """
        Возвращает retriever
        """
        if retriever_name == "vectorstore":
            logger.debug(
                f"Using VectorStoreRetriever with {retriever_config.search_type} search"
            )
            retriever = cls._get_vector_store_retriever(vector_store, retriever_config)

        elif retriever_name == "contextual-compression":
            logger.debug(
                f"Using ContextualCompressionRetriever with {retriever_config.search_type} search"
            )
            retriever = cls._get_contextual_compression_retriever(
                vector_store, retriever_config
            )

        elif retriever_name == "multi-query":
            logger.debug(
                f"Using MultiQueryRetriever with {retriever_config.search_type} search"
            )
            retriever = cls._get_multi_query_retriever(vector_store, retriever_config)

        elif retriever_name == "contextual-compression-multi-query":
            logger.debug(
                f"Using MultiQueryRetriever with {retriever_config.search_type} search and retriever type as contextual-compression"
            )
            retriever = cls._get_multi_query_retriever(
                vector_store, retriever_config, retriever_type="contextual-compression"
            )

        else:
            raise HTTPException(status_code=404, detail="Retriever not found")

        return retriever

#######
# Streaming Client
#
# import httpx
# from httpx import Timeout
# from backend.rag.query_controllers.example.schemas import ExampleQueryInput
#
# payload = {
#   "collection_name": "pstest",
#   "query": "What are the features of Diners club black metal edition?",
#   "llm_configuration": {
#     "name": "openai-devtest/gpt-3-5-turbo",
#     "parameters": {
#       "temperature": 0.1
#     },
#     "provider": "truefoundry"
#   },
#   "prompt_template": "Answer the question based only on the following context:\nContext: {context} \nQuestion: {question}",
#   "retriever_name": "vectorstore",
#   "retriever_config": {
#     "search_type": "similarity",
#     "search_kwargs": {
#       "k": 20
#     },
#     "filter": {}
#   },
#   "stream": True
# }
#
# data = ExampleQueryInput(**payload).dict()
# ENDPOINT_URL = 'http://localhost:8000/answer'
#
#
# with httpx.stream('POST', ENDPOINT_URL, json=data, timeout=Timeout(5.0*60)) as r:
#     for chunk in r.iter_text():
#         print(chunk)
#######
