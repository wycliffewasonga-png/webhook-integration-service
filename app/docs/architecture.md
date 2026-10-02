# Architecture

## Overview

The service receives webhook events from an external customer platform and processes them through a sequence of authentication, validation, event checking, and processing steps.

## Request Flow

```text
External Customer Platform
          |
          v
   POST /webhooks/content
          |
          v
   HMAC Authentication
          |
          v
    Payload Validation
          |
          v
   Event Type Validation
          |
          v
   Idempotency Check
          |
          v
     Event Processing
          |
          v
      HTTP Response
```

## Components

### FastAPI Application

Provides the HTTP API and webhook endpoint.

### Pydantic Model

Validates the structure and required fields of incoming webhook payloads.

### HMAC Authentication

Uses HMAC-SHA256 to verify that webhook requests contain a valid signature.

### Event Processor

Checks whether the event type is supported and whether the event has already been processed.

### Idempotency Store

The current implementation uses an in-memory set of event IDs.

A production implementation would use persistent storage such as a database or distributed cache.

## Design Considerations

The implementation separates the major integration concerns:

* Authentication
* Validation
* Business-rule checks
* Duplicate detection
* Response handling

This makes the integration easier to test, troubleshoot, and extend.

## Production Extensions

A production implementation could add:

* Persistent event storage
* Queue-based processing
* Retry handling
* Structured logging
* Monitoring
* Rate limiting
* Secret rotation
* Distributed idempotency
* Dead-letter processing for failed events
