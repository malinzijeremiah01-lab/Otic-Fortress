# Otic Fortress API Documentation

## Overview

The Otic Fortress API provides a secure interface for interacting with the platform's core services, including authentication, user management, AI agents, and system monitoring.

This document is the main entry point for all API-related documentation.

---

## Base Information

- Base URL: `https://api.otic-fortress.com` (to be confirmed)
- API Version: `v1`
- Protocol: HTTPS
- Data Format: JSON

---

## Authentication

All API requests require a valid Bearer Token.

### Example Header

```http
Authorization: Bearer <access_token>

## Authentication API

The Authentication API handles user identity, login, registration, session management, and token lifecycle.

All authentication endpoints are prefixed with:

## Users API

The Users API manages user accounts, profiles, roles, and permissions within the Otic Fortress system.

All endpoints are prefixed with:

## Organizations API

The Organizations API manages multi-tenant structures within Otic Fortress.

An organization represents a company, team, or group that contains users, AI agents, and resources.

All endpoints are prefixed with:

## AI Agents API

The AI Agents API manages the lifecycle, configuration, and execution of AI agents within Otic Fortress.

AI agents are intelligent entities that perform tasks, respond to events, and interact with users and systems on behalf of an organization.

All endpoints are prefixed with:

## AI Shadow API

The AI Shadow API is responsible for monitoring, logging, and analyzing all AI agent activities within Otic Fortress.

It provides transparency, auditability, and behavioral insights for AI systems operating inside an organization.

All endpoints are prefixed with:

## Events API

The Events API provides access to system events generated throughout the Otic Fortress platform.

Events allow services to communicate asynchronously and provide an audit trail for important activities.

All endpoints are prefixed with:

```
/api/v1/events
```

---

## 1. List Events

Returns a list of recent events.

### Endpoint

```http
GET /api/v1/events
```

### Headers

```http
Authorization: Bearer <access_token>
```

### Optional Query Parameters

| Parameter | Description |
|------------|-------------|
| organizationId | Filter events by organization |
| agentId | Filter events for a specific AI agent |
| type | Filter by event type |
| limit | Maximum number of events to return |

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": "evt_001",
      "type": "agent.created",
      "timestamp": "2026-01-01T10:00:00Z",
      "organizationId": "org_123",
      "actor": "user_456"
    }
  ],
  "message": "Events retrieved successfully"
}
```

---

## 2. Get Event Details

Returns information about a specific event.

### Endpoint

```http
GET /api/v1/events/{id}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": "evt_001",
    "type": "agent.created",
    "description": "Support Agent was created.",
    "timestamp": "2026-01-01T10:00:00Z"
  }
}
```

---

## 3. Publish Event

Creates a new event.

### Endpoint

```http
POST /api/v1/events
```

### Request Body

```json
{
  "type": "agent.updated",
  "organizationId": "org_123",
  "resourceId": "agent_123",
  "description": "Support Agent configuration updated"
}
```

### Response

```json
{
  "success": true,
  "message": "Event published successfully"
}
```

---

## Common Event Types

| Event | Description |
|--------|-------------|
| user.created | A new user was created |
| user.updated | User profile updated |
| user.deleted | User removed |
| organization.created | Organization created |
| organization.updated | Organization updated |
| agent.created | AI agent created |
| agent.updated | AI agent updated |
| agent.deleted | AI agent deleted |
| login.success | Successful user login |
| login.failed | Failed login attempt |

---

## Security Rules

- All requests require authentication.
- Events are visible only within the user's organization.
- Sensitive event information should only be accessible to authorized users.
- Event records should be treated as immutable for audit purposes.

---

## Notes

- Events support auditing and monitoring across the platform.
- AI Shadow may consume event data for monitoring and compliance.
- Additional event types may be introduced as new platform features are developed.






