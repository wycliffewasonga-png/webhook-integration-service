import hashlib
import hmac

from fastapi.testclient import TestClient

from app.main import app, WEBHOOK_SECRET

client = TestClient(app)


def make_signature(payload: str) -> str:
    return hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_valid_webhook():
    payload = """
    {
        "event_id": "evt_test_001",
        "event_type": "content.published",
        "content_id": "DOC-1001",
        "customer_id": "customer-001",
        "timestamp": "2026-09-28T10:30:00Z"
    }
    """.strip()

    signature = make_signature(payload)

    response = client.post(
        "/webhooks/content",
        content=payload,
        headers={"X-Webhook-Signature": signature},
    )

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"


def test_invalid_signature():
    payload = """
    {
        "event_id": "evt_test_002",
        "event_type": "content.published",
        "content_id": "DOC-1002",
        "customer_id": "customer-001",
        "timestamp": "2026-09-28T10:30:00Z"
    }
    """.strip()

    response = client.post(
        "/webhooks/content",
        content=payload,
        headers={"X-Webhook-Signature": "invalid-signature"},
    )

    assert response.status_code == 401


def test_duplicate_event():
    payload = """
    {
        "event_id": "evt_duplicate_001",
        "event_type": "content.published",
        "content_id": "DOC-1003",
        "customer_id": "customer-001",
        "timestamp": "2026-09-28T10:30:00Z"
    }
    """.strip()

    signature = make_signature(payload)

    first = client.post(
        "/webhooks/content",
        content=payload,
        headers={"X-Webhook-Signature": signature},
    )

    second = client.post(
        "/webhooks/content",
        content=payload,
        headers={"X-Webhook-Signature": signature},
    )

    assert first.status_code == 202
    assert second.status_code == 200
    assert second.json()["status"] == "duplicate"


def test_unsupported_event():
    payload = """
    {
        "event_id": "evt_test_004",
        "event_type": "content.deleted",
        "content_id": "DOC-1004",
        "customer_id": "customer-001",
        "timestamp": "2026-09-28T10:30:00Z"
    }
    """.strip()

    signature = make_signature(payload)

    response = client.post(
        "/webhooks/content",
        content=payload,
        headers={"X-Webhook-Signature": signature},
    )

    assert response.status_code == 400
