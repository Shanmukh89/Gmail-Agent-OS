# Product Requirements Document — MailMind
**AI-Powered Email Sorting & Intelligence Platform**

Version: 0.1 (MVP)
Status: Draft
Last Updated: April 2026

---

## 1. Overview

MailMind is a personal email intelligence system that automatically classifies incoming emails into user-defined categories, selectively notifies the user based on priority rules, and surfaces actionable statistics through a lightweight dashboard. The system is powered by LangChain and LangGraph, enabling a modular, agent-based pipeline that can be extended with richer features over time (summaries, job application tracking, etc.).

---

## 2. Problem Statement

Email inboxes are noisy. Users receive dozens to hundreds of emails per day across wildly different contexts — newsletters, receipts, personal messages, work threads, job responses — and existing inbox tools offer only crude filtering. The user ends up either checking email constantly or missing something important. There is no intelligent layer that understands the *meaning* of an email, routes it appropriately, and decides whether it warrants immediate attention.

---

## 3. Goals

**Primary Goals (MVP)**
- Automatically classify every incoming email into one of the user's custom-defined categories using an LLM agent.
- Apply user-defined notification rules: some categories/senders trigger a push notification, others are silently filed.
- Provide a simple dashboard showing email counts by category, notification activity, and recent inbox activity.
- Allow the user to manage categories and notification preferences without touching code.

**Secondary Goals (Post-MVP)**
- Email summarization: one-click or automatic digest of email body.
- Job application tracker: auto-detect rejection/offer/interview emails and log them as structured data with statistics (applications sent, rejection rate, response rate, etc.).
- Weekly digest report.
- Rule suggestions based on past user corrections.

---

## 4. Non-Goals

- MailMind will NOT send emails or reply on the user's behalf (MVP).
- MailMind will NOT be a full email client; it augments existing clients via API.
- MailMind will NOT store full email bodies long-term — only metadata and classification results (privacy-first design).

---

## 5. Target User

Solo users and professionals who:
- Receive high email volume and want intelligent routing without manual filters.
- Are actively job-seeking and want passive tracking of application outcomes.
- Prefer local/personal tooling over SaaS subscriptions with unclear data policies.

---

## 6. Core Features

### 6.1 — Email Ingestion
- Connect to email via Gmail API (OAuth2) or IMAP.
- Poll for new emails on a configurable interval (default: 5 minutes) or via webhook/push notification from Gmail.
- Extract: sender, subject, snippet/body preview, timestamp, existing labels, thread ID.

### 6.2 — Classification Agent (LangGraph)
- A LangGraph state machine processes each new email through the following nodes:
  1. **Preprocess Node**: Clean and tokenize metadata + body snippet.
  2. **Classify Node**: LLM call (via LangChain) against user's current label definitions.
  3. **Confidence Check Node**: If confidence is below threshold, fall back to an "Uncategorized" bucket and flag for user review.
  4. **Notification Decision Node**: Based on category + sender rules, determine if a notification should fire.
  5. **Apply Label Node**: Write label back to Gmail/IMAP and store classification in local DB.
- User-defined labels carry an optional short description (e.g., "Work — anything from my team or manager") to ground the LLM prompt.

### 6.3 — Notification Engine
- Per-category setting: notify / silent / off.
- Per-sender override: always notify / never notify regardless of category.
- Notification delivery: local desktop notification (via system tray app or webhook to personal device).
- Notification payload: sender, subject, assigned category.

### 6.4 — Dashboard
- **Email Volume**: total emails received (today / this week / this month), breakdown by category.
- **Label Manager**: create, edit, delete labels; set label description for LLM grounding; toggle notification setting per label.
- **Notification Log**: recent emails that triggered a notification.
- **Unreviewed / Uncategorized Queue**: emails where confidence was low — user can assign correct label (used as future fine-tuning signal).
- Tech: React (Vite) frontend + FastAPI backend; SQLite for local storage MVP.

### 6.5 — Correction & Feedback Loop
- User can re-label any email from the dashboard.
- Corrections are logged and will be used as few-shot examples in future prompt calls (soft fine-tuning without model retraining).

---

## 7. Future Features (Backlog)

| Feature | Description | Priority |
|---|---|---|
| Email Summarization | LLM-generated one-paragraph summary of email body on demand | High |
| Job Tracker | Detect job-related emails (application, rejection, offer, interview) and log structured data | High |
| Job Statistics | Dashboard panel: applications logged, rejection count, response rate, avg response time | High |
| Weekly Digest | Scheduled email/notification summarizing the week's categories and counts | Medium |
| Rule Suggestions | System suggests notification rules based on user's past correction patterns | Medium |
| Multi-account Support | Connect multiple email addresses | Low |
| Export | Export classification history as CSV | Low |

---

## 8. Technical Requirements

| Requirement | Detail |
|---|---|
| LLM Orchestration | LangChain (prompt management, LLM calls, output parsers) |
| Agent Flow | LangGraph (stateful, multi-node pipeline per email) |
| LLM Provider | OpenAI GPT-4o or Anthropic Claude (configurable) |
| Email Integration | Gmail API (primary), IMAP (fallback) |
| Backend | Python 3.11+, FastAPI |
| Frontend | React + Vite, TailwindCSS |
| Database | SQLite (MVP), PostgreSQL-ready schema |
| Auth | OAuth2 for Gmail; local user session for dashboard |
| Deployment | Local (user's machine) for MVP; Docker Compose packaging |

---

## 9. User Stories

**As a user,**
- I want to define my own email categories so that the AI sorts to my mental model, not a generic one.
- I want to choose which categories are worth a notification so that I'm not pinged for newsletters.
- I want to see how many emails I've received this week by category so that I have inbox situational awareness.
- I want to correct a wrong classification so that the system gets better over time.
- I want job rejection emails automatically logged so that I can track my job search without a spreadsheet.

---

## 10. Success Metrics (MVP)

| Metric | Target |
|---|---|
| Classification accuracy (user-rated) | ≥ 85% correct on first pass |
| Notification false positive rate | < 10% (user marks notification as unnecessary) |
| Latency: email received → classified | < 30 seconds |
| Dashboard load time | < 1 second |

---

## 11. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| LLM misclassification on vague emails | Confidence threshold + Uncategorized queue for review |
| Gmail API rate limits | Exponential backoff + batch fetching |
| Privacy concern over sending email to LLM | Process only subject + sender + snippet by default; full body opt-in |
| Label creep (too many categories) | Warn user when label count exceeds 10; suggest merging |

---

## 12. Milestones

| Phase | Deliverable | Timeline |
|---|---|---|
| Phase 1 | Gmail OAuth + email ingestion + LangGraph pipeline (classify only) | Week 1-2 |
| Phase 2 | Notification engine + label manager UI | Week 3 |
| Phase 3 | Dashboard (volume stats, logs, correction queue) | Week 4 |
| Phase 4 | Job tracker + summarization (post-MVP) | Week 6+ |