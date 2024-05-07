from truefoundry.langchain import TrueFoundryEmbeddings

from backend.modules.embedder.embedder import register_embedder
from backend.settings import settings

if settings.OPENAI_API_KEY:
    from langchain.embeddings.openai import OpenAIEmbeddings

    register_embedder("openai", OpenAIEmbeddings)

if settings.GIGACHAT_API_KEY:
    from langchain_community.embeddings.gigachat import GigaChatEmbeddings

    register_embedder("gigachat", GigaChatEmbeddings)

register_embedder("truefoundry", TrueFoundryEmbeddings)

if settings.LOCAL:
    from backend.modules.embedder.mixbread_embedder import MixBreadEmbeddings

    register_embedder("mixedbread", MixBreadEmbeddings)
