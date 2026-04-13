from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/dumplings", tags=["Пельмени"])


@router.get("/", response_model=list[schemas.DumplingResponse])
async def get_dumplings(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    is_available: bool | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Получить список пельменей"""
    dumplings, _ = await crud.get_dumplings(
        db, skip=skip, limit=limit, search=search, is_available=is_available
    )
    return dumplings


@router.get("/{dumpling_id}", response_model=schemas.DumplingResponse)
async def get_dumpling(dumpling_id: int, db: AsyncSession = Depends(get_db)):
    """Получить пельмени по ID"""
    dumpling = await crud.get_dumpling(db, dumpling_id)
    if not dumpling:
        raise HTTPException(status_code=404, detail="Пельмени не найдены")
    return dumpling


@router.post("/", response_model=schemas.DumplingResponse, status_code=201)
async def create_dumpling(dumpling: schemas.DumplingCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый вид пельменей"""
    return await crud.create_dumpling(db, dumpling)


@router.put("/{dumpling_id}", response_model=schemas.DumplingResponse)
async def update_dumpling(
    dumpling_id: int,
    dumpling_update: schemas.DumplingUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить пельмени"""
    dumpling = await crud.update_dumpling(db, dumpling_id, dumpling_update)
    if not dumpling:
        raise HTTPException(status_code=404, detail="Пельмени не найдены")
    return dumpling


@router.delete("/{dumpling_id}", status_code=204)
async def delete_dumpling(dumpling_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить пельмени"""
    deleted = await crud.delete_dumpling(db, dumpling_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Пельмени не найдены")
    return None