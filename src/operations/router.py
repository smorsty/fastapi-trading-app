import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['Operation'],
)


@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


@router.get('')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    # query for select
    # stmt (statement) for delete, upgrade etc...
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'success',
            'date': result.all(),
            'details': None
        }
    except Exception:
        # add exception to database or send it to the developers, for correction
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'date': None,
            'details': None
        })


@router.post('')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session), ):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}

