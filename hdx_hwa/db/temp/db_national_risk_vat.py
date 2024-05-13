from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import DateTime, Integer, String, Float

from hdx_hwa.db.models.base import Base


class DBNationalRiskVAT(Base):
    __tablename__ = 'national_risk_vat'
    id = mapped_column(Integer, primary_key=True, autoincrement=False)
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    # location_ref: Mapped[int] = mapped_column(Integer)
    risk_class: Mapped[str] = mapped_column(String(9))
    global_rank: Mapped[int] = mapped_column(Integer)
    overall_risk: Mapped[float] = mapped_column(Float)
    hazard_exposure_risk: Mapped[float] = mapped_column(Float)
    vulnerability_risk: Mapped[float] = mapped_column(Float)
    coping_capacity_risk: Mapped[float] = mapped_column(Float)
    meta_missing_indicators_pct: Mapped[float] = mapped_column(Float)
    meta_avg_recentness_years: Mapped[float] = mapped_column(Float)
    reference_period_start: Mapped[datetime] = mapped_column(DateTime)
    reference_period_end: Mapped[datetime] = mapped_column(DateTime)
    location_code: Mapped[str] = mapped_column(String(128))
    location_name: Mapped[str] = mapped_column(String(512))
