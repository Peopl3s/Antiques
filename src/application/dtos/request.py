from typing import final
from uuid import UUID

from pydantic import BaseModel, field_validator


@final
class ArtifactInventoryIdRequestDTO(BaseModel):
    inventory_id: UUID

    @field_validator('inventory_id')
    def check_not_nil_uuid(cls, value: UUID) -> UUID:
        nil_uuid = UUID('00000000-0000-0000-0000-000000000000')
        if value == nil_uuid:
            raise ValueError('inventory_id cannot be nil UUID')
        return value
