from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Tuple, List
import models
import schemas


# ========== SHOP ==========
async def get_shop(db: AsyncSession, shop_id: int) -> models.Shop | None:
    result = await db.execute(select(models.Shop).where(models.Shop.id == shop_id))
    return result.scalar_one_or_none()


async def get_shops(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True
) -> List[models.Shop]:
    query = select(models.Shop)
    if active_only:
        query = query.where(models.Shop.is_active == True) # noqa: E712
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_shop(db: AsyncSession, shop: schemas.ShopCreate) -> models.Shop:
    db_shop = models.Shop(**shop.model_dump())
    db.add(db_shop)
    await db.commit()
    await db.refresh(db_shop)
    return db_shop


async def update_shop(
    db: AsyncSession,
    shop_id: int,
    shop_update: schemas.ShopUpdate
) -> models.Shop | None:
    db_shop = await get_shop(db, shop_id)
    if not db_shop:
        return None

    update_data = shop_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_shop, field, value)

    await db.commit()
    await db.refresh(db_shop)
    return db_shop


async def delete_shop(db: AsyncSession, shop_id: int) -> bool:
    db_shop = await get_shop(db, shop_id)
    if not db_shop:
        return False
    await db.delete(db_shop)
    await db.commit()
    return True


# ========== DUMPLING ==========
async def get_dumpling(db: AsyncSession, dumpling_id: int) -> models.Dumpling | None:
    result = await db.execute(select(models.Dumpling).where(models.Dumpling.id == dumpling_id))
    return result.scalar_one_or_none()


async def get_dumplings(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    is_available: Optional[bool] = None
) -> Tuple[List[models.Dumpling], int]:
    query = select(models.Dumpling)

    if search:
        query = query.where(models.Dumpling.name.ilike(f"%{search}%"))
    if is_available is not None:
        query = query.where(models.Dumpling.is_available == is_available)

    # Подсчёт общего количества
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all(), total


async def create_dumpling(db: AsyncSession, dumpling: schemas.DumplingCreate) -> models.Dumpling:
    db_dumpling = models.Dumpling(**dumpling.model_dump())
    db.add(db_dumpling)
    await db.commit()
    await db.refresh(db_dumpling)
    return db_dumpling


async def update_dumpling(
    db: AsyncSession,
    dumpling_id: int,
    dumpling_update: schemas.DumplingUpdate
) -> models.Dumpling | None:
    db_dumpling = await get_dumpling(db, dumpling_id)
    if not db_dumpling:
        return None

    update_data = dumpling_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_dumpling, field, value)

    await db.commit()
    await db.refresh(db_dumpling)
    return db_dumpling


async def delete_dumpling(db: AsyncSession, dumpling_id: int) -> bool:
    db_dumpling = await get_dumpling(db, dumpling_id)
    if not db_dumpling:
        return False
    await db.delete(db_dumpling)
    await db.commit()
    return True


# ========== PRICE ==========
async def get_price(db: AsyncSession, price_id: int) -> models.Price | None:
    result = await db.execute(select(models.Price).where(models.Price.id == price_id))
    return result.scalar_one_or_none()


async def get_prices_by_dumpling(
    db: AsyncSession,
    dumpling_id: int
) -> List[models.Price]:
    result = await db.execute(
        select(models.Price).where(models.Price.dumpling_id == dumpling_id)
    )
    return result.scalars().all()


async def get_prices_by_shop(
    db: AsyncSession,
    shop_id: int
) -> List[models.Price]:
    result = await db.execute(
        select(models.Price).where(models.Price.shop_id == shop_id)
    )
    return result.scalars().all()


async def create_price(db: AsyncSession, price: schemas.PriceCreate) -> models.Price:
    # Вычисляем price_per_kg, если не передан
    price_per_kg = price.price_per_kg
    if not price_per_kg:
        dumpling = await get_dumpling(db, price.dumpling_id)
        if dumpling and dumpling.weight_grams:
            price_per_kg = price.price / (dumpling.weight_grams / 1000)

    db_price = models.Price(
        shop_id=price.shop_id,
        dumpling_id=price.dumpling_id,
        price=price.price,
        price_per_kg=price_per_kg
    )
    db.add(db_price)
    await db.commit()
    await db.refresh(db_price)
    return db_price


async def update_price(
    db: AsyncSession,
    price_id: int,
    price_update: schemas.PriceUpdate
) -> models.Price | None:
    db_price = await get_price(db, price_id)
    if not db_price:
        return None

    update_data = price_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_price, field, value)

    # Если обновили цену — пересчитаем price_per_kg
    if "price" in update_data:
        dumpling = await get_dumpling(db, db_price.dumpling_id)
        if dumpling and dumpling.weight_grams:
            db_price.price_per_kg = db_price.price / (dumpling.weight_grams / 1000)

    await db.commit()
    await db.refresh(db_price)
    return db_price


async def delete_price(db: AsyncSession, price_id: int) -> bool:
    db_price = await get_price(db, price_id)
    if not db_price:
        return False
    await db.delete(db_price)
    await db.commit()
    return True