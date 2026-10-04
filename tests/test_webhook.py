import hashlib
import hmac

from fastapi.testclient import TestClient

from app.main import app, WEBHOOK_SECRET, WebhookEvent

client = TestClient(app)


def make_signature(payload: str) -> str:
    return hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()


def create_payload(event_id: str, event_type: str = "content.published"):
    return {
        "event_id": event_id,
        "event_type": event_type,
        "content_id": "DOC-1001",
        "customer_id": "customer-001",
        "timestamp": "2026-09-28T10:30:00Z",
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_valid_webhook():
    payload = create_payload("evt_test_001")
    event = WebhookEvent(**payload)

    signature = make_signature(event.model_dump_json())

    response = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": signature},
    )

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"


def test_invalid_signature():
    payload = create_payload("evt_test_002")

    response = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": "invalid-signature"},
    )

    assert response.status_code == 401


def test_duplicate_event():
    payload = create_payload("evt_duplicate_001")
    event = WebhookEvent(**payload)

    signature = make_signature(event.model_dump_json())

    first = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": signature},
    )

    second = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": signature},
    )

    assert first.status_code == 202
    assert second.status_code == 200
    assert second.json()["status"] == "duplicate"


def test_unsupported_event():
    payload = create_payload(
        "evt_test_004",
        event_type="content.deleted",
    )

    event = WebhookEvent(**payload)
    signature = make_signature(event.model_dump_json())

    response = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": signature},
    )

    assert response.status_code == 400


def test_invalid_payload():
    payload = {
        "event_id": "evt_test_005",
        "event_type": "content.published",
        "content_id": "DOC-1005",
    }

    response = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": "invalid"},
    )

    assert response.status_code == 422
