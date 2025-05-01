from fastapi import APIRouter, Request
from loguru import logger

from src.database import ICP

router = APIRouter()

AllICP = ICP.select()


@router.get("/icp")
async def query_icp(request: Request):
    domain = str(request.base_url)

    icp = next(
        (icp for icp in AllICP if icp.domain in domain),
        None,
    )

    if icp is None:
        logger.error(f"domain not found: {domain}")
        return {
            "domain": domain,
            "icp_beian": "",
            "icp_url": "",
            "icp_entity": "",
        }

    return {
        "domain": domain,
        "icp_beian": icp.beian,
        "icp_url": icp.url,
        "icp_entity": icp.entity,
    }
