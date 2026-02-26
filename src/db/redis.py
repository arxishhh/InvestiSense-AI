import aioredis
from src.config import Config

JTI_EXPIRY = 3600
CACHE_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0)

retrieval_cache = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=1
)

async def add_jti_to_blocklist(jti : str)-> None:
    await token_blocklist.set(
        name=jti,
        value="blocked",
        ex=JTI_EXPIRY)

async def token_in_blocklist(jti : str) -> bool:
    jti = await token_blocklist.get(jti)
    return jti is not None

async def cache_retrieval(key : str):
    context = await retrieval_cache.get(key)
    return context 

async def get_cached_retrieval(key : str,value : str):
    await retrieval_cache.set(
        name=key,
        value=value,
        ex=CACHE_EXPIRY
    )


