from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, final
from uuid import UUID

from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactEntity:
    inventory_id: UUID
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    acquisition_date: datetime
    name: str
    department: str
    era: Era
    material: Material
    description: Optional[str] = None
