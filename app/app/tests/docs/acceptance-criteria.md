# Acceptance Criteria

## Webhook Integration Service

### AC-01 — Authentication

**Given** a webhook request is received
**When** the signature is invalid
**Then** the API must reject the request with HTTP `401`.

### AC-02 — Payload Validation

**Given** a webhook request is received
**When** required fields are missing or invalid
**Then** the API must reject the request with an appropriate validation response.

### AC-03 — Supported Events

**Given** a valid authenticated request
**When** the event type is unsupported
**Then** the API must return HTTP `400`.

### AC-04 — Event Processing

**Given** a valid authenticated supported event
**When** the event has not been processed before
**Then** the API must accept the event with HTTP `202`.

### AC-05 — Idempotency

**Given** an event has already been processed
**When** the same `event_id` is submitted again
**Then** the API must identify it as a duplicate and avoid processing it again.

### AC-06 — Health Check

**Given** the service is running
**When** `GET /health` is requested
**Then** the API must return a healthy status.

### AC-07 — Testing

The core authentication, validation, event-processing, and error-handling behaviours must have automated tests.
