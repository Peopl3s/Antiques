from uuid import UUID

from fastapi import APIRouter, Path, HTTPException, status, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.application.dtos.artifact import ArtifactDTO
from src.application.dtos.request import ArtifactInventoryIdRequestDTO
from src.application.use_cases.register_artifact import RegisterArtifactUseCase
from src.presentation.api.rest.v1.exceptions import ArtifactNotFoundException

router = APIRouter(prefix="/v1/artifacts", tags=["Artifacts"])


def artifact_dto_from_path(
    inventory_id: UUID = Path(..., description="Artifact inventory id"),
) -> ArtifactInventoryIdRequestDTO:
    return ArtifactInventoryIdRequestDTO(id=inventory_id)


@router.get("/{inventory_id}", response_model=ArtifactDTO)
@inject
async def get_artifact(
    inventory: ArtifactInventoryIdRequestDTO = Depends(artifact_dto_from_path),
    use_case: FromDishka[RegisterArtifactUseCase] = None,
):
    try:
        artifact = await use_case.execute(inventory.id)
        return artifact
    except ArtifactNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")