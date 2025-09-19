from src.application.dtos.artifact import ArtifactDTO
from src.domain.entities.artifact import ArtifactEntity
from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material


class ArtifactMapper:
    @staticmethod
    def to_dto(entity: ArtifactEntity) -> ArtifactDTO:
        return ArtifactDTO.model_validate(entity)

    @staticmethod
    def to_entity(dto: ArtifactDTO) -> ArtifactEntity:
        return ArtifactEntity(
            inventory_id=dto.inventory_id,
            name=dto.name,
            acquisition_date=dto.acquisition_date,
            department=dto.department,
            era=Era(value=dto.era.value),
            material=Material(value=dto.material.value),
            description=dto.description,
        )