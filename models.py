from datetime import datetime
from sqlalchemy import ForeignKey, String, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from database import Base


class Shop(Base):

    """ Магазин"""

    __tablename__ = 'shops'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    prices: Mapped[list['Price']] = relationship(back_populates='shop')


class Dumpling(Base):

    """Таблица товаров (пельменей)"""

    __tablename__ = 'dumplings'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    img_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    prices: Mapped[list['Price']] = relationship(back_populates='dumpling')


class Price(Base):

    """"Таблица цен"""

    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"), nullable=False)
    dumpling_id: Mapped[int] = mapped_column(ForeignKey('dumplings.id'), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_kg: Mapped[float | None] = mapped_column(Float, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    shop: Mapped["Shop"] = relationship(back_populates="prices")
    dumpling: Mapped["Dumpling"] = relationship(back_populates="prices")