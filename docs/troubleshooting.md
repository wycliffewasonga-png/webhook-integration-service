# Troubleshooting Guide

## Purpose

This guide provides a structured approach to diagnosing common webhook integration failures.

The goal is to identify the failure stage before changing the implementation.

---

## 1. HTTP 401 — Invalid Webhook Signature

### Symptom

The webhook request returns:

```text
401 Unauthorized
