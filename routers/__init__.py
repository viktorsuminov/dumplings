from .shops import router as shops_router
from .dumplings import router as dumplings_router
from .prices import router as prices_router

__all__ = ["shops_router", "dumplings_router", "prices_router"]