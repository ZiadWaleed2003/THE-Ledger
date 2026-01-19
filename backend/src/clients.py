from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_cerebras import ChatCerebras
from langchain_core.rate_limiters import InMemoryRateLimiter
from functools import lru_cache
from langsmith import Client as LangSmithClient

from backend.src.core.config import CONFIG

# a Nvidia NIM model client to power the agent
@lru_cache(maxsize=None)
def get_nvidia_client()-> ChatNVIDIA:

    print("--- Initializing LLM Client LLama 3 ---")

    try:


        rate_limiter = InMemoryRateLimiter(
                requests_per_second= 40 / 60,  # since I'm using Nvidia NIM here so I'm getting 40 RPM max 
                check_every_n_seconds=0.1,  
                max_bucket_size=1
            )
        
        rate_limiter_cerebras = InMemoryRateLimiter(
                requests_per_second= 30 / 60,  # with Cerebras I'm getting 30 RPM max 
                check_every_n_seconds=0.1,  
                max_bucket_size=1
            )

        # model = ChatNVIDIA(
        #     model="meta/llama-3.3-70b-instruct",
        #     model_provider="langchain-nvidia-ai-endpoints",
        #     base_url = "https://integrate.api.nvidia.com/v1",
        #     temperature = 0,
        #     nvidia_api_key = CONFIG['NVIDIA_API_KEY'],
        #     rate_limiter = rate_limiter
        # ).with_fallbacks([
        #     ChatCerebras(
        #         model="llama-3.3-70b",
        #         temperature = 0,
        #         api_key = CONFIG['CEREBRAS_API_KEY'],
        #         rate_limiter= rate_limiter_cerebras
        #     ),
        # ])

        model = ChatCerebras(
                model="llama-3.3-70b",
                temperature = 0,
                api_key = CONFIG['CEREBRAS_API_KEY'],
                rate_limiter= rate_limiter_cerebras
            )

        return model

    except Exception as e:

        print(f"ERROR initializing LLM: {str(e)} : Nvidia from Langchain")
        raise

@lru_cache(maxsize=None)
def get_asset_manager_client()-> ChatCerebras:

    print("--- Initializing LLM Client LLama 3 ---")

    try:


        
        
        rate_limiter_cerebras = InMemoryRateLimiter(
                requests_per_second= 30 / 60,  # with Cerebras I'm getting 30 RPM max 
                check_every_n_seconds=0.1,  
                max_bucket_size=1
            )

        model = ChatCerebras(
                model="llama-3.3-70b",
                temperature = 0.7,
                api_key = CONFIG['CEREBRAS_API_KEY'],
                rate_limiter= rate_limiter_cerebras
            )


        return model

    except Exception as e:

        print(f"ERROR initializing LLM: {str(e)} : Nvidia from Langchain")
        raise


@lru_cache(maxsize=None)
def get_langsmith_client() -> LangSmithClient:
    """Initializes and returns a shared LangSmith Client instance."""
    print("--- Initializing LangSmith Client ---")
    return LangSmithClient()