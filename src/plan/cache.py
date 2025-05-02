from time import time
from src.database import Plan

CacheExpiration = 60  # 秒
_plan_cache = None

def get_plan_cache():
    now = time()
    
    global _plan_cache
    if not _plan_cache or (now - _plan_cache[1] > CacheExpiration):
        _plan_cache = (Plan.select().order_by(Plan.plan_index), now)

    return _plan_cache[0]