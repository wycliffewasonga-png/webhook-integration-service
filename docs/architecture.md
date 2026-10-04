# Architecture

## Overview

The Webhook Integration Service receives webhook events from an external customer platform, validates the request, prevents duplicate processing, and returns a clear HTTP response.

The implementation follows this flow:

External Customer Platform  
↓  
Webhook Endpoint  
↓  
HMAC Authentication  
↓  
Payload Validation  
↓  
Event Type Validation  
↓  
Idempotency Check  
↓  
Event Processing  
↓  
Response

---

## Components

### 1. External Customer Platform

The external platform sends webhook events when customer content changes.

Example event:

```json
{
  "event_id": "evt_1001",
  "event_type": "content.published",
  "content_id": "DOC-1001",
  "customer_id": "customer-001",
  "timestamp": "2026-09-28T10:30:00Z"
}
