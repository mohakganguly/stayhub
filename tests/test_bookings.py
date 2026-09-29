def get_auth_headers(client, email="bookinguser@example.com"):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Booking User",
            "email": email,
            "password": "BookingPass123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "BookingPass123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def create_test_listing(client):
    response = client.post(
        "/api/v1/listings",
        json={
            "title": "Booking Test Villa",
            "description": "A villa created specifically for booking tests.",
            "location": "Manali",
            "price_per_night": 5000,
            "max_guests": 4,
            "rating": 4.5,
            "category": "Mountain",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_create_booking(client):
    headers = get_auth_headers(
        client,
        "booking1@example.com",
    )

    property_id = create_test_listing(client)

    response = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "property_id": property_id,
            "check_in": "2027-01-10",
            "check_out": "2027-01-13",
            "guests": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["property_id"] == property_id
    assert data["guests"] == 2
    assert data["status"] == "PENDING"
    assert "id" in data


def test_booking_total_price(client):
    headers = get_auth_headers(
        client,
        "booking2@example.com",
    )

    property_id = create_test_listing(client)

    response = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "property_id": property_id,
            "check_in": "2027-02-10",
            "check_out": "2027-02-15",
            "guests": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    # 5 nights × ₹5000
    assert data["total_price"] == 25000


def test_booking_property_not_found(client):
    headers = get_auth_headers(
        client,
        "booking3@example.com",
    )

    response = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "property_id": 999999,
            "check_in": "2027-03-10",
            "check_out": "2027-03-13",
            "guests": 2,
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Property not found"


def test_booking_guest_limit(client):
    headers = get_auth_headers(
        client,
        "booking4@example.com",
    )

    property_id = create_test_listing(client)

    response = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "property_id": property_id,
            "check_in": "2027-04-10",
            "check_out": "2027-04-13",
            "guests": 5,
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Property allows a maximum of 4 guests"


def test_overlapping_booking(client):
    headers1 = get_auth_headers(
        client,
        "booking5a@example.com",
    )

    headers2 = get_auth_headers(
        client,
        "booking5b@example.com",
    )

    property_id = create_test_listing(client)

    first_response = client.post(
        "/api/v1/bookings",
        headers=headers1,
        json={
            "property_id": property_id,
            "check_in": "2027-05-10",
            "check_out": "2027-05-15",
            "guests": 2,
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/bookings",
        headers=headers2,
        json={
            "property_id": property_id,
            "check_in": "2027-05-12",
            "check_out": "2027-05-17",
            "guests": 2,
        },
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["detail"] == (
        "Property is already booked for the selected dates"
    )

def test_get_my_bookings(client):
    headers = get_auth_headers(
        client,
        "mybookings@example.com",
    )

    property_id = create_test_listing(client)

    create_response = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "property_id": property_id,
            "check_in": "2027-06-10",
            "check_out": "2027-06-13",
            "guests": 2,
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/bookings/me",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert any(
        booking["property_id"] == property_id
        for booking in data
    )

def test_get_booking(client):
    headers = get_auth_headers(
        client,
        "specificbooking@example.com",
    )

    property_id = create_test_listing(client)

    create_response = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "property_id": property_id,
            "check_in": "2027-07-10",
            "check_out": "2027-07-13",
            "guests": 2,
        },
    )

    assert create_response.status_code == 201

    booking_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/bookings/{booking_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == booking_id
    assert data["property_id"] == property_id

def test_cancel_booking(client):
    headers = get_auth_headers(
        client,
        "cancelbooking@example.com",
    )

    property_id = create_test_listing(client)

    create_response = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "property_id": property_id,
            "check_in": "2027-08-10",
            "check_out": "2027-08-13",
            "guests": 2,
        },
    )

    assert create_response.status_code == 201

    booking_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/bookings/{booking_id}/cancel",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == booking_id
    assert data["status"] == "CANCELLED"

def test_cancel_already_cancelled_booking(client):
    headers = get_auth_headers(
        client,
        "doublecancel@example.com",
    )

    property_id = create_test_listing(client)

    create_response = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "property_id": property_id,
            "check_in": "2027-09-10",
            "check_out": "2027-09-13",
            "guests": 2,
        },
    )

    assert create_response.status_code == 201

    booking_id = create_response.json()["id"]

    first_cancel = client.patch(
        f"/api/v1/bookings/{booking_id}/cancel",
        headers=headers,
    )

    assert first_cancel.status_code == 200

    second_cancel = client.patch(
        f"/api/v1/bookings/{booking_id}/cancel",
        headers=headers,
    )

    assert second_cancel.status_code == 409

    data = second_cancel.json()

    assert data["detail"] == "Booking is already cancelled"

def test_cancel_booking_unauthorized(client):
    owner_headers = get_auth_headers(
        client,
        "bookingowner@example.com",
    )

    other_user_headers = get_auth_headers(
        client,
        "otheruser@example.com",
    )

    property_id = create_test_listing(client)

    create_response = client.post(
        "/api/v1/bookings",
        headers=owner_headers,
        json={
            "property_id": property_id,
            "check_in": "2027-10-10",
            "check_out": "2027-10-13",
            "guests": 2,
        },
    )

    assert create_response.status_code == 201

    booking_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/bookings/{booking_id}/cancel",
        headers=other_user_headers,
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == (
        "You are not allowed to modify this booking"
    )