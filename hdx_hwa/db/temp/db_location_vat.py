from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import DateTime, Integer, String

from hdx_hwa.db.models.base import Base


class DBLocationVAT(Base):
    __tablename__ = 'location_vat'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    reference_period_start: Mapped[datetime] = mapped_column(DateTime, nullable=True, index=True)
    reference_period_end: Mapped[datetime] = mapped_column(DateTime, nullable=True, index=True)
