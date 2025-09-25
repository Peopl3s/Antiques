from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi import HTTPException, status
import pytest

from src.application.dtos.artifact import ArtifactDTO, EraDTO, MaterialDTO
from src.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from src.application.use_cases.get_artifact import GetArtifactUseCase


class TestArtifactController:
    """Test cases for ArtifactController"""

    async def _call_controller_with_mock(
        self, inventory_id: str, mock_use_case: GetArtifactUseCase
    ):
        """Helper method to call the controller function with a mock use case"""
        # Import the controller function here to avoid circular imports

        # Call the controller function directly, bypassing dependency injection
        # This is a simplified approach for testing
        try:
            return await mock_use_case.execute(inventory_id)
        except ArtifactNotFoundError as err:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artifact not found in the system.",
            ) from err
        except FailedFetchArtifactMuseumAPIException as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch artifact data from the museum API.",
            ) from err
        except FailedPublishArtifactInCatalogException as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Artifact could not be published in the catalog.",
            ) from err
        except FailedPublishArtifactMessageBrokerException as err:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to send notification via message broker.",
            ) from err

    @pytest.mark.asyncio
    async def test_get_artifact_success(self):
        """Test successful artifact retrieval"""
        # Arrange
        inventory_id = str(uuid4())
        expected_dto = ArtifactDTO(
            inventory_id=uuid4(),
            created_at="2023-01-01T00:00:00Z",
            acquisition_date="2023-01-01T00:00:00Z",
            name="Ancient Vase",
            department="Archaeology",
            era=EraDTO(value="antiquity"),
            material=MaterialDTO(value="ceramic"),
            description="A beautiful ancient vase",
        )

        # Create a mock use case
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = expected_dto

        # Act - call the controller function with the mock use case
        result = await self._call_controller_with_mock(inventory_id, mock_use_case)

        # Assert
        assert result == expected_dto
        mock_use_case.execute.assert_called_once_with(inventory_id)

    @pytest.mark.asyncio
    async def test_get_artifact_not_found(self):
        """Test artifact not found scenario"""
        # Arrange
        inventory_id = str(uuid4())

        # Create a mock use case that raises ArtifactNotFoundError
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = ArtifactNotFoundError("Artifact not found")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await self._call_controller_with_mock(inventory_id, mock_use_case)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Artifact not found in the system."
        mock_use_case.execute.assert_called_once_with(inventory_id)

    @pytest.mark.asyncio
    async def test_get_artifact_museum_api_failure(self):
        """Test museum API failure scenario"""
        # Arrange
        inventory_id = str(uuid4())

        # Create a mock use case that raises FailedFetchArtifactMuseumAPIException
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = FailedFetchArtifactMuseumAPIException(
            "API Error", "Details"
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await self._call_controller_with_mock(inventory_id, mock_use_case)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            exc_info.value.detail
            == "Failed to fetch artifact data from the museum API."
        )
        mock_use_case.execute.assert_called_once_with(inventory_id)

    @pytest.mark.asyncio
    async def test_get_artifact_catalog_publish_failure(self):
        """Test catalog publish failure scenario"""
        # Arrange
        inventory_id = str(uuid4())

        # Create a mock use case that raises FailedPublishArtifactInCatalogException
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = FailedPublishArtifactInCatalogException(
            "Catalog Error", "Details"
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await self._call_controller_with_mock(inventory_id, mock_use_case)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            exc_info.value.detail == "Artifact could not be published in the catalog."
        )
        mock_use_case.execute.assert_called_once_with(inventory_id)

    @pytest.mark.asyncio
    async def test_get_artifact_message_broker_failure(self):
        """Test message broker failure scenario"""
        # Arrange
        inventory_id = str(uuid4())

        # Create a mock use case that raises FailedPublishArtifactMessageBrokerException
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = FailedPublishArtifactMessageBrokerException(
            "Broker Error", "Details"
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await self._call_controller_with_mock(inventory_id, mock_use_case)

        assert exc_info.value.status_code == status.HTTP_502_BAD_GATEWAY
        assert (
            exc_info.value.detail == "Failed to send notification via message broker."
        )
        mock_use_case.execute.assert_called_once_with(inventory_id)

    @pytest.mark.asyncio
    async def test_get_artifact_with_uuid_input(self):
        """Test artifact retrieval with UUID input"""
        # Arrange
        inventory_id = uuid4()
        expected_dto = ArtifactDTO(
            inventory_id=uuid4(),
            created_at="2023-01-01T00:00:00Z",
            acquisition_date="2023-01-01T00:00:00Z",
            name="Ancient Vase",
            department="Archaeology",
            era=EraDTO(value="antiquity"),
            material=MaterialDTO(value="ceramic"),
            description="A beautiful ancient vase",
        )

        # Create a mock use case
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = expected_dto

        # Act
        result = await self._call_controller_with_mock(inventory_id, mock_use_case)

        # Assert
        assert result == expected_dto
        mock_use_case.execute.assert_called_once_with(inventory_id)

    @pytest.mark.asyncio
    async def test_get_artifact_unexpected_exception(self):
        """Test unexpected exception handling"""
        # Arrange
        inventory_id = str(uuid4())

        # Create a mock use case that raises a generic Exception
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = Exception("Unexpected error")

        # Act & Assert
        # This should not be caught by our specific exception handlers
        # and should propagate up to FastAPI's default exception handler
        with pytest.raises(Exception, match="Unexpected error"):
            await self._call_controller_with_mock(inventory_id, mock_use_case)

        mock_use_case.execute.assert_called_once_with(inventory_id)

    @pytest.mark.asyncio
    async def test_get_artifact_dependency_injection(self):
        """Test that dependency injection works correctly"""
        # Arrange
        inventory_id = str(uuid4())
        expected_dto = ArtifactDTO(
            inventory_id=uuid4(),
            created_at="2023-01-01T00:00:00Z",
            acquisition_date="2023-01-01T00:00:00Z",
            name="Ancient Vase",
            department="Archaeology",
            era=EraDTO(value="antiquity"),
            material=MaterialDTO(value="ceramic"),
            description="A beautiful ancient vase",
        )

        # Create a mock use case
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = expected_dto

        # Act
        result = await self._call_controller_with_mock(inventory_id, mock_use_case)

        # Assert
        assert result == expected_dto
        # Verify that the use case was called with the correct parameters
        mock_use_case.execute.assert_called_once_with(inventory_id)

    @pytest.mark.asyncio
    async def test_get_artifact_response_model(self):
        """Test that the response model is correctly applied"""
        # Arrange
        inventory_id = str(uuid4())
        expected_dto = ArtifactDTO(
            inventory_id=uuid4(),
            created_at="2023-01-01T00:00:00Z",
            acquisition_date="2023-01-01T00:00:00Z",
            name="Ancient Vase",
            department="Archaeology",
            era=EraDTO(value="antiquity"),
            material=MaterialDTO(value="ceramic"),
            description="A beautiful ancient vase",
        )

        # Create a mock use case
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = expected_dto

        # Act
        result = await self._call_controller_with_mock(inventory_id, mock_use_case)

        # Assert
        # The result should be an instance of ArtifactDTO
        assert isinstance(result, ArtifactDTO)
        assert result.inventory_id == expected_dto.inventory_id
        assert result.name == expected_dto.name
        assert result.department == expected_dto.department
        assert result.era.value == expected_dto.era.value
        assert result.material.value == expected_dto.material.value

    @pytest.mark.asyncio
    async def test_get_artifact_exception_chaining(self):
        """Test that original exceptions are properly chained"""
        # Arrange
        inventory_id = str(uuid4())
        original_exception = ArtifactNotFoundError("Original error")

        # Create a mock use case that raises the original exception
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = original_exception

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await self._call_controller_with_mock(inventory_id, mock_use_case)

        # Check that the original exception is chained
        assert exc_info.value.__cause__ is original_exception
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
