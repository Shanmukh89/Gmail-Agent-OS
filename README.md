# Neubox

Practice mock interviews with AI-generated questions, multimodal session capture, and structured per-question feedback.

Neubox is a full-stack interview preparation platform built with Next.js, Supabase, and a Python FastAPI processing backend. It helps users run realistic interview sessions, generate job-description-aware or company-specific questions, record answers with camera and microphone, and review detailed feedback for each response. The current application supports transcript-driven analysis, session scoring, temporary recording storage, and a product architecture that can expand into full audio and video ML evaluation.

## Live Demo

[View Live Application](https://interview-feedback-system.vercel.app/)

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Deployment](#deployment)

## Features

**AI-Powered Question Generation**  
Generate mock interview questions from a job description or company name using OpenAI-backed Next.js API routes. The system supports role-aware and domain-aware question sets for realistic interview practice.

**Live Interview Session Flow**  
Users can run structured interview sessions with preparation time, answer timers, question progression, live transcript capture, waveform feedback, and automatic session advancement when time expires.

**Transcript-Driven Answer Analysis**  
Each response is analyzed using the transcript, question, role, difficulty, and duration. The app produces content, delivery, and presence-style scores, plus strengths and improvement suggestions for every answered question.

**Detailed Results Review**  
The results page shows actual questions asked during the session, expandable per-question transcript panels, answer metrics, estimated pace, question-level scoring, and coaching-style feedback for each response.

**Temporary Recording Storage**  
Interview recordings can be uploaded to a private Supabase Storage bucket and accessed through signed URLs for replay and download after evaluation. The project is designed around short-lived recordings rather than permanent raw media retention.

**Supabase-Backed Product Core**  
Supabase handles authentication, database storage, row-level-secured user data, session persistence, response metadata, and storage integration for recordings.

**Extensible Multimodal ML Architecture**  
A dedicated Python FastAPI backend is included as the future home for heavy audio and video ML tasks such as gesture analysis, voice feature extraction, posture scoring, and deeper multimodal evaluation workflows.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| UI Components | Custom UI primitives, Lucide React, Framer Motion |
| Backend API | Next.js App Router API routes |
| ML Processing Backend | Python, FastAPI, Uvicorn |
| Database | Supabase PostgreSQL |
| Authentication | Supabase Auth |
| Storage | Supabase Storage |
| LLM | OpenAI GPT-4o-mini |
| Speech and Analysis | OpenAI-powered transcript analysis with app-side orchestration |
| Future ML Pipeline | Python audio and video processing stack via FastAPI |

## Project Structure

```bash
InterviewFeedbackSystem/
├── app/
│   ├── api/
│   │   ├── account/
│   │   │   └── delete/route.ts               # Account deletion endpoint
│   │   ├── ai/
│   │   │   ├── aggregate-session/route.ts    # Session-level score aggregation
│   │   │   ├── analyze-response/route.ts     # Transcript-based response scoring
│   │   │   ├── chat/route.ts                 # AI chat endpoint
│   │   │   ├── company-questions/route.ts    # Company-specific question generation
│   │   │   └── jd-questions/route.ts         # JD-based question generation
│   │   ├── cron/
│   │   │   └── cleanup-recordings/route.ts   # Expired recording cleanup endpoint
│   │   ├── profile/
│   │   │   └── upsert/route.ts               # Profile save/update endpoint
│   │   └── recordings/
│   │       └── signed-url/route.ts           # Signed playback URL for recordings
│   ├── analytics/
│   │   └── page.tsx                          # Analytics dashboard
│   ├── dashboard/
│   │   └── page.tsx                          # Main user dashboard
│   ├── login/
│   │   └── page.tsx                          # Login screen
│   ├── onboarding/
│   │   └── page.tsx                          # Onboarding flow
│   ├── practice/
│   │   ├── page.tsx                          # Practice mode selection
│   │   ├── setup/page.tsx                    # Interview setup and configuration
│   │   └── session/page.tsx                  # Live interview experience
│   ├── register/
│   │   └── page.tsx                          # Registration page
│   ├── results/
│   │   └── page.tsx                          # Detailed interview review
│   ├── settings/
│   │   └── page.tsx                          # User settings
│   ├── globals.css                           # Global styles
│   ├── layout.tsx                            # App layout shell
│   └── page.tsx                              # Landing page
├── backend/
│   ├── api/
│   │   └── main.py                           # FastAPI processing backend scaffold
│   └── requirements.txt                      # Python backend dependencies
├── components/
│   ├── layout/
│   │   ├── sidebar.tsx                       # Sidebar navigation
│   │   └── topbar.tsx                        # Top navigation
│   └── ui/
│       ├── button.tsx                        # Button component
│       ├── card.tsx                          # Card component
│       ├── input.tsx                         # Input component
│       ├── multi-select.tsx                  # Multi-select component
│       └── toast.tsx                         # Toast system
├── lib/
│   ├── job-roles.ts                          # Supported job roles
│   ├── practice-results.ts                   # Session result storage helpers
│   ├── practice-store.ts                     # Practice session state helpers
│   ├── profile.ts                            # Profile and settings helpers
│   ├── supabase-admin.ts                     # Admin Supabase client
│   └── supabase.ts                           # Browser Supabase client
├── supabase/
│   ├── migrations/
│   │   ├── 20260411_feature_persistence.sql  # Feature persistence migration
│   │   └── 20260413_supabase_storage.sql     # Recording storage migration
│   ├── schema.sql                            # Main schema definition
│   └── seed-questions.sql                    # Seed question bank data
├── .env.example
├── .gitignore
├── next.config.mjs
├── package-lock.json
├── package.json
├── postcss.config.js
├── tailwind.config.ts
└── tsconfig.json
```

## System Architecture

```text
User selects interview mode
        |
        v
┌─────────────────────┐
│ Next.js Frontend    │
│ Practice UI         │
│ Camera + Mic        │
└─────────┬───────────┘
          |
          v
┌─────────────────────┐
│ Next.js API Routes  │
│ Question generation │
│ Response analysis   │
│ Aggregation         │
└─────────┬───────────┘
          |
          v
┌─────────────────────┐
│ Supabase            │
│ Auth                │
│ PostgreSQL          │
│ Storage             │
└───────┬───────┬─────┘
        |       |
        |       v
        |  ┌─────────────────────┐
        |  │ Signed Recording    │
        |  │ Playback URLs       │
        |  └─────────────────────┘
        |
        v
┌─────────────────────┐
│ Results Page        │
│ Transcript review   │
│ Question scores     │
│ Recording replay    │
└─────────────────────┘

Future ML path
        |
        v
┌─────────────────────┐
│ FastAPI Backend     │
│ Audio ML            │
│ Video ML            │
│ Gesture analysis    │
│ Voice analysis      │
└─────────────────────┘
```

## Getting Started

### Prerequisites

| Requirement | Details |
|---|---|
| Node.js | Version 18 or higher |
| npm | Version 9 or higher |
| Python | Version 3.10 or higher if using the FastAPI backend |
| Supabase | A project with database and storage enabled |
| OpenAI API Key | Required for AI question generation and transcript analysis |

### Setup

1. Clone the repository

```bash
git clone https://github.com/your-username/InterviewFeedbackSystem.git
cd InterviewFeedbackSystem
```

2. Install frontend and Next.js dependencies

```bash
npm install
```

3. Prepare the Python backend if you want the FastAPI processing service available

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

4. Configure the database

Run `supabase/schema.sql` in the Supabase SQL editor, then run the SQL files in `supabase/migrations/` to enable the latest response, storage, and recording-retention structures.

5. Create environment files

Create `.env.local` in the project root using the variables listed below. Keep `.env.example` as the template committed to the repository.

## Environment Variables

### Root (`.env.local`)

| Variable | Required | Description |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Required | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Required | Supabase anonymous public key |
| `SUPABASE_SERVICE_ROLE_KEY` | Required | Supabase service role key for admin API routes |
| `OPENAI_API_KEY` | Required | OpenAI API key for question generation and transcript analysis |
| `OPENAI_MODEL` | Optional | OpenAI model name. Defaults to `gpt-4o-mini` |
| `NEXT_PUBLIC_APP_URL` | Optional | App base URL. Defaults to `http://localhost:3000` |
| `CRON_SECRET` | Optional | Secret used by the recording cleanup cron endpoint |

### Optional Python Backend

If you run the FastAPI backend separately, you can also provide Python-specific environment variables later for ML models, queues, or external processing services. The current scaffold only requires standard Python runtime setup.

## Running the Application

Start the Next.js development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

Start the optional FastAPI backend in a separate terminal if you are extending the ML pipeline:

```bash
cd backend
venv\Scripts\activate
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Build

```bash
npm run build
npm start
```

## API Reference

| Method | Endpoint | Description | Request Body |
|---|---|---|---|
| `POST` | `/api/ai/jd-questions` | Generate interview questions from a job description | `{ "jdText": "string", "domains": [], "targetJobTitle": "string", "totalQuestions": 5 }` |
| `POST` | `/api/ai/company-questions` | Generate company-specific interview questions | `{ "companyName": "string", "domains": [], "targetJobTitle": "string", "totalQuestions": 5 }` |
| `POST` | `/api/ai/analyze-response` | Analyze a transcript and enrich a response with scores and feedback | `{ "responseId": "uuid", "transcript": "string", "question": "string", "role": "string", "difficulty": "string", "duration": 90 }` |
| `POST` | `/api/ai/aggregate-session` | Aggregate completed question responses into session-level scores | `{ "sessionId": "uuid" }` |
| `POST` | `/api/recordings/signed-url` | Return a signed playback URL for a stored recording | `{ "videoPath": "string" }` |
| `POST` | `/api/cron/cleanup-recordings` | Delete expired recordings and mark them as removed | None |

## Deployment

The application can be deployed on a standard Next.js hosting platform with Supabase as the managed backend.

**Frontend and App API**  
Deploy the Next.js app to Vercel, Netlify, Render, or any Node.js-compatible platform. Ensure all required environment variables are configured in the hosting dashboard.

**Database and Storage**  
Use Supabase for PostgreSQL, authentication, and private recording storage. Run the schema and migration SQL before using the deployed app.

**Recording Retention**  
If you use temporary interview recordings, configure a scheduled trigger to call the cleanup endpoint and remove expired recordings automatically.

**Python ML Backend**  
If you expand into true audio and video ML, deploy the FastAPI backend as a separate Python service and let the Next.js app or Supabase-triggered jobs hand off heavy processing work to it.
