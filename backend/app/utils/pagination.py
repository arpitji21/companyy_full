import math

from fastapi import Query

from app.core.config import settings
from app.schemas.common import Page


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    ):
        self.page = page
        self.page_size = page_size


def build_page(items: list, total: int, page: int, page_size: int) -> Page:
    total_pages = math.ceil(total / page_size) if page_size else 0
    return Page(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)
