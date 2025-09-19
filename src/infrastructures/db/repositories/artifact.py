from typing import Optional, override, final
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.application.interfaces.repositories import ArtifactRepositoryProtocol
from src.domain.entities.artifact import ArtifactEntity
from src.infrastructures.db.models.artifact import ArtifactModel


@final
class ArtifactRepositorySQLAlchemy(ArtifactRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def get_by_inventory_id(self, inventory_id: str | UUID) -> Optional[ArtifactEntity]:
        stmt = select(ArtifactModel).where(ArtifactModel.inventory_id == inventory_id)
        result = await self._session.execute(stmt)
        artifact_model = result.scalar_one_or_none()
        if artifact_model is None:
            return None
        return artifact_model.to_dataclass()

    @override
    async def save(self, artifact: ArtifactEntity) -> None:
        stmt = select(ArtifactModel).where(ArtifactModel.inventory_id == artifact.inventory_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            model.name = artifact.name
            model.era = artifact.era.value
            model.material = artifact.material.value
            model.description = artifact.description
            model.acquisition_date = artifact.acquisition_date
            model.department = artifact.department
        else:
            model = ArtifactModel.from_dataclass(artifact)
        self._session.add(model)
        await self._session.commit()