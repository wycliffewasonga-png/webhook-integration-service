from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import hashlib
import hmac

app = FastAPI(
    title="Webhook Integration Service",
    version="1.0.0",
)

WEBHOOK_SECRET = "demo-webhook-secret"
SUPPORTED_EVENT = "content.published"

processed_events = set()


class WebhookEvent(BaseModel):
    event_id: str
    event_type: str
    content_id: str
    customer_id: str
    timestamp: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/webhooks/content", status_code=202)
def receive_webhook(
    event: WebhookEvent,
    x_webhook_signature: str = Header(...)
):
    payload = event.model_dump_json()

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(
        x_webhook_signature,
        expected_signature
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature"
        )

    if event.event_type != SUPPORTED_EVENT:
        raise HTTPException(
            status_code=400,
            detail="Unsupported event type"
        )

    if event.event_id in processed_events:
        return JSONResponse(
            status_code=200,
            content={
                "status": "duplicate",
                "event_id": event.event_id
            }
        )

    processed_events.add(event.event_id)

    return {
        "status": "accepted",
        "event_id": event.event_id,
        "event_type": event.event_type
    }
