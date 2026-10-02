# Webhook Integration Service

A practical Python/FastAPI webhook service demonstrating authenticated event processing, payload validation, idempotency, error handling, automated testing, and integration documentation.

## Overview

This project simulates a customer integration where an external content platform sends webhook events to an API.

The service demonstrates an end-to-end integration workflow:

**External Platform → Webhook API → Authentication → Validation → Processing → Response**

The project focuses on implementation practices relevant to customer-facing technical integrations.

## What It Demonstrates

* REST API development with FastAPI
* Webhook event processing
* HMAC-SHA256 request authentication
* JSON payload validation
* Idempotent event handling
* Error handling
* Automated API testing
* Structured technical documentation
* Acceptance criteria
* Troubleshooting procedures

## Business Scenario

A customer content platform publishes content and sends an event to an external integration service.

The integration must:

1. Verify that the request came from the expected source.
2. Validate the incoming payload.
3. Reject unsupported events.
4. Prevent duplicate event processing.
5. Return clear HTTP responses.
6. Provide documentation for implementation and troubleshooting.

## Technology Stack

* Python
* FastAPI
* Pydantic
* HMAC-SHA256
* Pytest
* HTTPX

## Supported Event

The service currently supports:

`content.published`

Example payload:

```json
{
  "event_id": "evt_1001",
  "event_type": "content.published",
  "content_id": "DOC-1001",
  "customer_id": "customer-001",
  "timestamp": "2026-09-28T10:30:00Z"
}
```

## Authentication

Webhook requests use an HMAC-SHA256 signature.

The signature is supplied through:

`X-Webhook-Signature`

For demonstration purposes, the project uses a local development secret.

In a production environment, secrets should be stored using a secure secrets-management system rather than hard-coded.

## API Endpoints

### Health Check

`GET /health`

Returns the service health status.

### Webhook

`POST /webhooks/content`

Receives and processes content events.

## Response Behaviour

| Scenario               | HTTP Response |
| ---------------------- | ------------: |
| Valid new event        |           202 |
| Valid duplicate event  |           200 |
| Invalid signature      |           401 |
| Invalid payload        |           422 |
| Unsupported event type |           400 |

## Idempotency

Each event contains a unique `event_id`.

The service records processed event IDs and prevents the same event from being processed repeatedly.

This demonstrates a common reliability requirement in webhook integrations where external systems may retry delivery.

## Processing Flow

```text
Customer Platform
       |
       v
Webhook Request
       |
       v
Verify HMAC Signature
       |
       v
Validate Payload
       |
       v
Check event_id
       |
       +---- Duplicate ----> Return 200
       |
       v
Process Event
       |
       v
Record Event
       |
       v
Return 202
```

## Testing

The test suite covers:

* Health endpoint
* Valid webhook requests
* Invalid signatures
* Duplicate events
* Unsupported event types

Run the tests with:

```bash
pytest -q
```

## Acceptance Criteria

The implementation is considered successful when:

* Valid webhook requests are authenticated.
* Invalid signatures are rejected.
* Required payload fields are validated.
* Unsupported event types are rejected.
* Duplicate events are detected.
* Appropriate HTTP status codes are returned.
* Automated tests cover the core integration behaviour.
* Technical documentation explains setup and troubleshooting.

## Project Structure

```text
webhook-integration-service/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_webhook.py
├── docs/
│   ├── acceptance-criteria.md
│   ├── architecture.md
│   └── troubleshooting.md
├── .gitignore
├── README.md
└── requirements.txt
```

## Local Setup

Clone the repository:

```bash
git clone https://github.com/wycliffewasonga-png/webhook-integration-service.git
```

Move into the project:

```bash
cd webhook-integration-service
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Run the tests:

```bash
pytest -q
```

## Production Considerations

A production implementation would additionally require:

* External secret management
* Persistent event storage
* Structured logging
* Monitoring and alerting
* Retry handling
* Rate limiting
* Secure deployment configuration
* Authentication key rotation
* Database-backed idempotency

## What This Project Demonstrates

This project provides evidence of practical experience with:

**API implementation → authentication → structured data → validation → testing → error handling → technical documentation**

It is designed as a portfolio implementation demonstrating how a technical integration can be translated from requirements into a working and testable service.
