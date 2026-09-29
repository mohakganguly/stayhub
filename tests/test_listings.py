def test_create_listing(client):
    response = client.post(
        "/api/v1/listings",
        json={
            "title": "Test Mountain Villa",
            "description": "A beautiful villa with mountain views.",
            "location": "Manali",
            "price_per_night": 5000,
            "max_guests": 4,
            "rating": 4.5,
            "category": "Mountain",
            "images": [
                {
                    "image_url": "https://example.com/villa.jpg",
                    "position": 0,
                }
            ],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["title"] == "Test Mountain Villa"
    assert data["location"] == "Manali"
    assert data["price_per_night"] == 5000
    assert data["max_guests"] == 4
    assert data["rating"] == 4.5
    assert data["category"] == "Mountain"

    assert len(data["images"]) == 1
    assert data["images"][0]["image_url"] == (
        "https://example.com/villa.jpg"
    )

def test_get_listing(client):
    create_response = client.post(
        "/api/v1/listings",
        json={
            "title": "Get Test Villa",
            "description": "A comfortable villa for testing.",
            "location": "Goa",
            "price_per_night": 4000,
            "max_guests": 3,
            "rating": 4.2,
            "category": "Beach",
        },
    )

    assert create_response.status_code == 201

    listing_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/listings/{listing_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == listing_id
    assert data["title"] == "Get Test Villa"
    assert data["location"] == "Goa"
    assert data["price_per_night"] == 4000

def test_get_nonexistent_listing(client):
    response = client.get(
        "/api/v1/listings/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Listing not found"

def test_update_listing(client):
    create_response = client.post(
        "/api/v1/listings",
        json={
            "title": "Original Villa",
            "description": "Original description for testing.",
            "location": "Jaipur",
            "price_per_night": 3000,
            "max_guests": 2,
            "rating": 4.0,
            "category": "Heritage",
        },
    )

    assert create_response.status_code == 201

    listing_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/listings/{listing_id}",
        json={
            "title": "Updated Villa",
            "price_per_night": 4500,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == listing_id
    assert data["title"] == "Updated Villa"
    assert data["price_per_night"] == 4500

    # Fields we didn't update should remain unchanged
    assert data["location"] == "Jaipur"
    assert data["max_guests"] == 2
    assert data["category"] == "Heritage"

def test_delete_listing(client):
    create_response = client.post(
        "/api/v1/listings",
        json={
            "title": "Delete Test Villa",
            "description": "A temporary villa for deletion testing.",
            "location": "Pune",
            "price_per_night": 2500,
            "max_guests": 2,
            "rating": 3.8,
            "category": "City",
        },
    )

    assert create_response.status_code == 201

    listing_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/listings/{listing_id}"
    )

    assert delete_response.status_code == 204

    # Verify the resource no longer exists
    get_response = client.get(
        f"/api/v1/listings/{listing_id}"
    )

    assert get_response.status_code == 404

def test_search_listings_by_location(client):
    client.post(
        "/api/v1/listings",
        json={
            "title": "Goa Beach House",
            "description": "Beautiful beach house near the sea.",
            "location": "Goa",
            "price_per_night": 5000,
            "max_guests": 4,
            "rating": 4.5,
            "category": "Beach",
        },
    )

    client.post(
        "/api/v1/listings",
        json={
            "title": "Delhi Apartment",
            "description": "Modern apartment in central Delhi.",
            "location": "Delhi",
            "price_per_night": 3000,
            "max_guests": 3,
            "rating": 4.0,
            "category": "City",
        },
    )

    response = client.get(
        "/api/v1/listings",
        params={"location": "Goa"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    for listing in data["items"]:
        assert listing["location"] == "Goa"

def test_listings_pagination(client):
    for i in range(3):
        response = client.post(
            "/api/v1/listings",
            json={
                "title": f"Pagination Villa {i}",
                "description": "A villa created for pagination testing.",
                "location": "Kolkata",
                "price_per_night": 2000 + i,
                "max_guests": 2,
                "rating": 4.0,
                "category": "City",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/api/v1/listings",
        params={
            "page": 1,
            "page_size": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) <= 2
    assert data["total_pages"] >= 1

def test_create_listing_invalid_data(client):
    response = client.post(
        "/api/v1/listings",
        json={
            "title": "A",
            "description": "Too short",
            "location": "Goa",
            "price_per_night": -100,
            "max_guests": 0,
            "rating": 7,
            "category": "B",
        },
    )

    assert response.status_code == 422

def test_create_listing_with_multiple_images(client):
    response = client.post(
        "/api/v1/listings",
        json={
            "title": "Multi Image Villa",
            "description": "Villa containing multiple listing images.",
            "location": "Udaipur",
            "price_per_night": 6000,
            "max_guests": 5,
            "rating": 4.8,
            "category": "Luxury",
            "images": [
                {
                    "image_url": "https://example.com/image1.jpg",
                    "position": 0,
                },
                {
                    "image_url": "https://example.com/image2.jpg",
                    "position": 1,
                },
                {
                    "image_url": "https://example.com/image3.jpg",
                    "position": 2,
                },
            ],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert len(data["images"]) == 3

    assert data["images"][0]["position"] == 0
    assert data["images"][1]["position"] == 1
    assert data["images"][2]["position"] == 2