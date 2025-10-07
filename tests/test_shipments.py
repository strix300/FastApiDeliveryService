import pytest

@pytest.mark.asyncio
async def test_get_shipments(client):
    response = await client.get("v1/shipments/")
    assert response.status_code == 200
    
    data = response.json()
    for key in ("page", "limit", "total", "items"):
        assert key in data, f"Missing key: {key}"
    
    assert isinstance(data["items"], list)
    
@pytest.mark.asyncio
async def test_get_types(client):
    response = await client.get("v1/types/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_create_shipments_and_types(client):
    type_data = {"id": 1, "name": "test_type"}
    type_response = await client.post("v1/types/", json=type_data)
    assert type_response.status_code == 200
    type_id = type_response.json()
    print(type_id)

    shipment_data = {
        "name": "Test shipment",
        "weight": 2.5,
        "content_cost": 1000,
        "type_id": 1,
    }
    response = await client.post("v1/shipments/", json=shipment_data)
    assert response.status_code == 200
    shipment = response.json()
    assert shipment["name"] == "Test shipment"

    list_response = await client.get("v1/shipments/")
    assert list_response.status_code == 200
    data = list_response.json()
    assert len(data["items"]) >= 1