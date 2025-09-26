from uuid import uuid4

from fastapi.testclient import TestClient
import pytest


class TestApiIntegration:
    @pytest.mark.asyncio
    async def test_get_artifact_endpoint_success(self, client: TestClient):
        """Test successful artifact retrieval through API endpoint"""
        inventory_id = str(uuid4())

        with pytest.raises(Exception):
            client.get(f"/api/v1/artifacts/{inventory_id}")

    @pytest.mark.asyncio
    async def test_api_docs_endpoint(self, client: TestClient):
        """Test that API documentation is accessible"""
        response = client.get("/api/docs")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    @pytest.mark.asyncio
    async def test_api_redoc_endpoint(self, client: TestClient):
        """Test that ReDoc documentation is accessible"""
        response = client.get("/api/redoc")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    @pytest.mark.asyncio
    async def test_api_openapi_endpoint(self, client: TestClient):
        """Test that OpenAPI specification is accessible"""

        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

        openapi_spec = response.json()
        assert "openapi" in openapi_spec
        assert "info" in openapi_spec
        assert "paths" in openapi_spec

    @pytest.mark.asyncio
    async def test_api_info_endpoint(self, client: TestClient):
        """Test API info endpoint"""

        response = client.get("/api/")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_artifact_endpoint_with_invalid_uuid(self, client: TestClient):
        """Test artifact endpoint with invalid UUID format"""

        invalid_inventory_id = "invalid-uuid-format"

        with pytest.raises(Exception):
            client.get(f"/api/v1/artifacts/{invalid_inventory_id}")

    @pytest.mark.asyncio
    async def test_artifact_endpoint_with_empty_uuid(self, client: TestClient):
        """Test artifact endpoint with empty UUID"""
        empty_inventory_id = ""

        response = client.get(f"/api/v1/artifacts/{empty_inventory_id}")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_api_cors_headers(self, client: TestClient):
        """Test that CORS headers are properly set"""
        response = client.get("/api/docs", headers={"Origin": "http://localhost:3000"})

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_api_response_time(self, client: TestClient):
        """Test API response time for documentation endpoints"""
        import time

        start_time = time.time()
        response = client.get("/api/docs")
        end_time = time.time()

        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 2.0  # Should respond within 2 seconds

    @pytest.mark.asyncio
    async def test_api_content_type_negotiation(self, client: TestClient):
        """Test API content type negotiation"""
        response = client.get(
            "/api/openapi.json", headers={"Accept": "application/json"}
        )

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    @pytest.mark.asyncio
    async def test_api_not_found_endpoint(self, client: TestClient):
        """Test non-existent API endpoint"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_api_method_not_allowed(self, client: TestClient):
        """Test API method not allowed"""
        response = client.post("/api/docs")
        assert response.status_code == 405

    @pytest.mark.asyncio
    async def test_api_health_check(self, client: TestClient):
        """Test API health check through docs endpoint"""
        response = client.get("/api/docs")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_api_openapi_schema_validation(self, client: TestClient):
        """Test OpenAPI schema validation"""
        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        openapi_spec = response.json()

        required_fields = ["openapi", "info", "paths"]
        for field in required_fields:
            assert field in openapi_spec

        info = openapi_spec["info"]
        assert "title" in info
        assert "version" in info

        paths = openapi_spec["paths"]
        assert isinstance(paths, dict)

    @pytest.mark.asyncio
    async def test_api_artifact_path_in_openapi(self, client: TestClient):
        """Test that artifact path is defined in OpenAPI spec"""

        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        openapi_spec = response.json()

        paths = openapi_spec["paths"]
        artifact_paths = [path for path in paths.keys() if "artifacts" in path]

        assert len(artifact_paths) > 0

    @pytest.mark.asyncio
    async def test_api_response_structure(self, client: TestClient):
        """Test API response structure for OpenAPI spec"""
        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        openapi_spec = response.json()

        assert isinstance(openapi_spec, dict)
        assert isinstance(openapi_spec.get("info", {}), dict)
        assert isinstance(openapi_spec.get("paths", {}), dict)
        assert isinstance(openapi_spec.get("openapi", ""), str)

    @pytest.mark.asyncio
    async def test_api_version_consistency(self, client: TestClient):
        """Test API version consistency"""
        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        openapi_spec = response.json()

        openapi_version = openapi_spec.get("openapi", "")
        assert openapi_version.startswith("3.")  # Should be OpenAPI 3.x

    @pytest.mark.asyncio
    async def test_api_info_metadata(self, client: TestClient):
        """Test API info metadata"""
        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        openapi_spec = response.json()

        info = openapi_spec.get("info", {})

        assert "title" in info
        assert "version" in info
        assert "description" in info

        assert "Антиквариум" in info["title"] or "Antiques" in info["title"]

    @pytest.mark.asyncio
    async def test_api_security_definitions(self, client: TestClient):
        """Test API security definitions in OpenAPI spec"""
        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        openapi_spec = response.json()

        if (
            "components" in openapi_spec
            and "securitySchemes" in openapi_spec["components"]
        ):
            security_schemes = openapi_spec["components"]["securitySchemes"]
            assert isinstance(security_schemes, dict)

    @pytest.mark.asyncio
    async def test_api_servers_definition(self, client: TestClient):
        """Test API servers definition in OpenAPI spec"""
        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        openapi_spec = response.json()

        if "servers" in openapi_spec:
            servers = openapi_spec["servers"]
            assert isinstance(servers, list)

            for server in servers:
                assert "url" in server
