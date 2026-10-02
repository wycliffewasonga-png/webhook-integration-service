# Troubleshooting Guide

## 401 — Invalid Webhook Signature

### Symptoms

The API returns:

```json
{
  "detail": "Invalid webhook signature"
}
```

### Checks

1. Confirm the webhook secret is correct.
2. Confirm the sender is calculating an HMAC-SHA256 signature.
3. Confirm the `X-Webhook-Signature` header is present.
4. Confirm the signature is calculated from the exact request payload.

---

## 400 — Unsupported Event

### Symptoms

The API returns:

```json
{
  "detail": "Unsupported event type"
}
```

### Checks

1. Confirm the `event_type` value.
2. Confirm that the event is supported by the integration.
3. Check the customer integration documentation for the expected event type.

---

## 422 — Payload Validation Error

### Symptoms

The API rejects the request because the payload does not match the expected structure.

### Checks

Confirm that the request contains:

* `event_id`
* `event_type`
* `content_id`
* `customer_id`
* `timestamp`

Also confirm that the values are supplied in the expected format.

---

## Duplicate Event

### Symptoms

The API identifies an event as already processed.

### Checks

1. Compare the submitted `event_id` with previously processed events.
2. Confirm whether the sender retried the same webhook.
3. Check whether the duplicate is expected behaviour.

Duplicate detection prevents repeated processing of the same event.

---

## Local Development Issues

If the API does not start:

```bash
uvicorn app.main:app --reload
```

If dependencies are missing:

```bash
pip install -r requirements.txt
```

To run automated tests:

```bash
pytest -q
```

## Production Diagnostic Considerations

A production implementation should additionally provide:

* Structured application logs
* Request correlation IDs
* Monitoring and alerting
* Persistent event records
* Authentication failure logging
* Retry and failure tracking
* Operational dashboards
