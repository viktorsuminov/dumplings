from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ShopBase(BaseModel):

    """Базовая схема магазина"""

    name: str = Field(..., min_length=1, max_length=100, description='Название магазина')
    location: str| None = Field(None, max_length=255, description='Адрес')
    lat: float | None = Field(None, ge=-90, le=90, description='Широта')
    lon: float | None = Field(None, ge=-180, le=180, description='Долгота')
    is_active: bool = Field(True, description='Активен ли магазин')


class ShopCreate(ShopBase):
    """Создание маназина"""
    pass


class ShopUpdate(BaseModel):

    """Обновление данных о магазине"""

    name: str | None = Field(None, min_length=1, max_length=100)
    location: str| None = Field(None, max_length=255)
    lat: float | None = Field(None, ge=-90, le=90)
    lon: float | None = Field(None, ge=-180, le=180)
    is_active: bool | None = None


class ShopResponse(ShopBase):
    
    """Ответ с данными маганизина"""

    id: int
    created_at: datetime
    updated_at: datetime


class DumplingBase(BaseModel):

    """Базовая схема пельменей"""

    name: str = Field(..., min_length=1, max_length=200, description='Название пельменей')
    img_url: str | None = Field(None, max_length=255, description='Ссылка на изображение')
    is_available: bool = Field(True, description='Доступен ли товар')


class DumplingCreate(DumplingBase):

    """Создание пельмений"""

    pass


class DumplingUpdate(BaseModel):

    """Обновление данных о товаре"""

    name: str | None = Field(None, min_length=1, max_length=200)
    img_url: str | None = Field(None, max_length=255)
    is_available: bool | None = None


class DumplingResponse(DumplingBase):

    """Ответ с данными о пельменях"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PriceBase(BaseModel):

    """Базовая схема цены"""

    shop_id: int = Field(..., gt=0, description="ID магазина")
    dumpling_id: int = Field(..., gt=0, description="ID пельменей")
    price: float = Field(..., gt=0, description="Цена в рублях")
    price_per_kg: float | None = Field(None, gt=0, description="Цена за кг")


class PriceCreate(PriceBase):

    """Создание цены"""

    pass


class PriceUpdate(BaseModel):

    """Обновление цены"""

    price: float | None = Field(None, gt=0)
    price_per_kg: float | None = Field(None, gt=0)


class PriceResponse(PriceBase):

    """Ответ с данными цены"""

    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)