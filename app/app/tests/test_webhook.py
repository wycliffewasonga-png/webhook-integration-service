import hashlib
import hmac

from fastapi.testclient import TestClient

from app.main import app, WEBHOOK_SECRET


client = TestClient(app)


def create_signature(payload: str) -> str:
    return hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_valid_webhook():
    payload = {
        "event_id": "evt_1001",
        "event_type": "content.published",
        "content_id": "DOC-1001",
        "customer_id": "customer-001",
        "timestamp": "2026-09-28T10:30:00Z"
    }

    from app.main import WebhookEvent

    event = WebhookEvent(**payload)
    signature = create_signature(event.model_dump_json())

    response = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": signature}
    )

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"


def test_invalid_signature():
    payload = {
        "event_id": "evt_invalid",
        "event_type": "content.published",
        "content_id": "DOC-1002",
        "customer_id": "customer-001",
        "timestamp": "2026-09-28T10:30:00Z"
    }

    response = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": "invalid-signature"}
    )

    assert response.status_code == 401


def test_unsupported_event():
    payload = {
        "event_id": "evt_unsupported",
        "event_type": "content.deleted",
        "content_id": "DOC-1003",
        "customer_id": "customer-001",
        "timestamp": "2026-09-28T10:30:00Z"
    }

    from app.main import WebhookEvent

    event = WebhookEvent(**payload)
    signature = create_signature(event.model_dump_json())

    response = client.post(
        "/webhooks/content",
        json=payload,
        headers={"X-Webhook-Signature": signature}
    )

    assert response.status_code == 400
