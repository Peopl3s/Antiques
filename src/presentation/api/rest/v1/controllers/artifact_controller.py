from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.application.dtos.artifact import ArtifactDTO
from src.application.use_cases.register_artifact import RegisterArtifactUseCase
from src.presentation.api.rest.v1.exceptions import ArtifactNotFoundException

router = APIRouter(prefix="/v1/artifacts", tags=["Artifacts"])


@router.get("/{inventory_id}", response_model=ArtifactDTO)
@inject
async def get_artifact(
    inventory_id: str | UUID,
    use_case: FromDishka[RegisterArtifactUseCase] = None,
):
    try:
        artifact = await use_case.execute(inventory_id)
        return artifact
    except ArtifactNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")
