from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import Boolean, DateTime, Integer, String

from hdx_hwa.db.models.base import Base


class DBOperationalPresenceVAT(Base):
    __tablename__ = 'operational_presence_vat'
    id = mapped_column(Integer, primary_key=True, autoincrement=False)
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer, index=True, nullable=True)
    org_acronym: Mapped[str] = mapped_column(String)
    org_name: Mapped[str] = mapped_column(String)
    sector_code: Mapped[str] = mapped_column(String(32))
    reference_period_start: Mapped[datetime] = mapped_column(DateTime)
    reference_period_end: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=True)
    org_type_code: Mapped[str] = mapped_column(String(32))
    sector_name: Mapped[str] = mapped_column(String(512))
    location_code: Mapped[str] = mapped_column(String(128))
    location_name: Mapped[str] = mapped_column(String(512), index=True)
    admin1_code: Mapped[str] = mapped_column(String(128))
    admin1_name: Mapped[str] = mapped_column(String(512))
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    location_ref: Mapped[int] = mapped_column(Integer, nullable=True)
    admin2_code: Mapped[str] = mapped_column(String(128), index=True)
    admin2_name: Mapped[str] = mapped_column(String(512), index=True)
    admin2_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin1_ref: Mapped[int] = mapped_column(Integer, nullable=True)
