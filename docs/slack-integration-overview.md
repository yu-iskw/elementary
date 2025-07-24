# Slack Integration Overview

This document summarizes how Slack integrations are currently implemented in the repository and lists the Slack API methods/endpoints that are used.

## Implementations

The codebase contains two main implementations:

1. **SlackWebMessagingIntegration** (`elementary/messages/messaging_integrations/slack_web.py`)
   - Uses `slack_sdk.WebClient`.
   - Supports sending messages and replies in Block Kit format.
   - Caches email to user ID lookups.
   - Handles rate limiting via `ratelimit` decorators.

2. **SlackWebhookMessagingIntegration** (`elementary/messages/messaging_integrations/slack_webhook.py`)
   - Uses `slack_sdk.WebhookClient` to post messages to an incoming webhook.
   - Does not support replies or Slack actions.

A legacy client implementation exists under `elementary/clients/slack/client.py` with `SlackWebClient` and `SlackWebhookClient` classes. These classes contain similar logic for sending messages, uploading files and resolving user IDs.

## Slack API Methods / Endpoints

The following Slack API methods are invoked across the implementations:

| Method | File & Usage |
|-------|--------------|
| `chat_postMessage` | Sending messages in `slack_web.py` and `client.py` |
| `files_upload_v2` | Uploading files in `client.py` |
| `users_lookupByEmail` | Resolving user IDs from emails in `slack_web.py` and `client.py` |
| `conversations_list` | Listing channels during channel lookup in `slack_web.py` and `client.py` |
| `conversations_join` | Attempting to join a channel if not already a member in `slack_web.py` and `client.py` |
| Incoming webhook POST (`WebhookClient.send`) | Posting messages through a webhook in `slack_webhook.py` and `client.py` |

## Message Formatting

Message formatting is handled through helper classes:

- `SlackMessageBuilder` (`elementary/clients/slack/slack_message_builder.py`) – builds messages with blocks and attachments.
- `SlackAlertMessageBuilder` (`elementary/monitor/data_monitoring/alerts/integrations/slack/message_builder.py`) – constructs alert-specific blocks.
- `block_kit.py` (`elementary/messages/formats/block_kit.py`) – converts generic message blocks to Slack Block Kit format.

## Caching & Rate Limiting

- Email-to-user-id mappings are cached in dictionaries inside the Slack clients to reduce API calls.
- API calls are wrapped with the `ratelimit` library to comply with Slack rate limits (e.g., 1 call per second for posting messages, 50 calls per minute for `users_lookupByEmail`).

## Error Handling

- Slack API errors raise `MessagingIntegrationError` with user-friendly messages.
- In some cases (e.g., `not_in_channel`), the code attempts to join the channel before retrying.

---
This summary captures the current state of the Slack integration for reference while refactoring.
