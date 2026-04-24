# MailMind (Gmail Agent OS)

Automate your inbox with AI-powered email sorting, intelligent routing rules, and an agentic classification pipeline.

MailMind is a personal email intelligence system built with a React frontend and a Python FastAPI backend powered by LangChain and LangGraph. It helps users automatically classify incoming emails into custom-defined categories, selectively notify based on priority rules, and surface actionable statistics. The system reads your unread Gmail messages, evaluates them against your custom prompts using an LLM agent, and applies labels directly in your inbox.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)

## Features

**Agentic Email Classification**  
Automatically classify every incoming email into one of your custom-defined categories using a LangGraph-based LLM agent.

**Custom Routing Rules & Prompts**  
Define categories with natural language descriptions (e.g., "Receipts, bills, and financial docs") to ground the LLM prompt and ensure accurate sorting based on your mental model.

**Gmail API Integration**  
Securely connects to your Gmail via OAuth2. It fetches unread emails, analyzes them, and automatically applies the correct labels back to your Gmail account.

**Smart Notification Engine**  
Set per-category notification rules so you only get pinged for important threads, while newsletters and receipts are silently filed away.

**Minimalist Dashboard**  
A clean, utilitarian React interface to manage your routing rules, trigger manual syncs, and monitor the intelligence pipeline without unnecessary clutter.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, TypeScript, Tailwind CSS |
| UI Components | Lucide React, Glassmorphism UI |
| Backend API | Python, FastAPI, Uvicorn |
| AI / Agents | LangChain, LangGraph, OpenAI |
| Database | SQLite, SQLAlchemy |
| Integrations | Gmail API, Google OAuth2 |

## Project Structure

```bash
Gmail-Agent-OS/
├── backend/
│   ├── agent.py               # LangGraph state machine & classification agent
│   ├── database.py            # SQLite database setup & sessions
│   ├── email_service.py       # Gmail API integration (OAuth flow, fetch, label)
│   ├── main.py                # FastAPI entry point & API endpoints
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic schemas for data validation
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main dashboard & routing rules UI
│   │   ├── index.css          # Tailwind & custom CSS styles
│   │   └── main.tsx           # React entry point
│   ├── package.json           # Node dependencies
│   └── vite.config.ts         # Vite bundler configuration
├── prd.md                     # Product Requirements Document
└── README.md                  # Project documentation
```

## System Architecture

```text
User defines routing rules
        |
        v
┌─────────────────────┐
│ React Frontend      │
│ Rule Management UI  │
└─────────┬───────────┘
          |
          v
┌─────────────────────┐
│ FastAPI Backend     │
│ Database (SQLite)   │
└─────────┬───────────┘
          | Trigger Sync
          v
┌───────────────────────────┐
│ LangGraph Agent Pipeline  │
│ 1. Fetch unread emails    │
│ 2. Preprocess text        │
│ 3. Classify via LLM       │
│ 4. Apply Gmail label      │
└─────────┬─────────────────┘
          |
          v
┌─────────────────────┐
│ Gmail API (OAuth2)  │
│ Token management    │
└─────────────────────┘
```

## Getting Started

### Prerequisites

| Requirement | Details |
|---|---|
| Node.js | Version 18 or higher |
| npm | Version 9 or higher |
| Python | Version 3.10 or higher |
| Google Cloud | A project with the Gmail API enabled and OAuth credentials |
| OpenAI API Key | Required for the classification agent |

### Setup

1. Clone the repository

```bash
git clone https://github.com/Shanmukh89/Gmail-Agent-OS.git
cd Gmail-Agent-OS
```

2. Install backend dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies

```bash
cd ../frontend
npm install
```

## Environment Variables

### Backend (`backend/.env`)

Create a `.env` file in the `backend/` directory:

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Required | OpenAI API key for email classification |

### Google Credentials (`backend/credentials.json`)

You must download your OAuth 2.0 Client IDs from the Google Cloud Console and save the file as `backend/credentials.json`. When you run the sync for the first time, the app will prompt you to log in and generate a `token.json` file.

## Running the Application

1. Start the FastAPI backend:

```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

2. Start the React frontend in a separate terminal:

```bash
cd frontend
npm run dev
```

The app will be available at `http://localhost:5173`.

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/categories/` | Retrieve all active routing rules |
| `POST` | `/categories/` | Create a new routing rule |
| `PUT` | `/categories/{id}` | Update an existing rule (e.g., toggle notifications) |
| `DELETE` | `/categories/{id}` | Delete a routing rule |
| `POST` | `/sync/` | Trigger the LangGraph agent to fetch and categorize unread emails |
