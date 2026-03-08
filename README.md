# hc01-ambient-note-Adaengapa-4-paeru-

hc01-ambient-note (Adaengapa 4 paeru) – Hackathon project

# HC-01 Ambient Clinical Note Generator (Hackathon 2025)

This project implements the **HC-01: Ambient Clinical Note Generator from Doctor–Patient Conversations** problem statement from the Healthcare domain.[file:1]

## What it does

- Takes a doctor–patient conversation **as text** (demo input).
- Uses a **local LLM** (Llama via Ollama) to generate a structured **SOAP note**:
  - Subjective
  - Objective
  - Assessment
  - Plan
- Returns the SOAP note as JSON and shows it in a simple Streamlit UI for the doctor to review instead of writing from scratch.[file:1]

> In a full version, a speech-to-text module (e.g. Whisper) would convert live audio to text. For this hackathon demo we focus on the core LLM-powered note generation pipeline.[file:1]

## Tech stack

- Backend: FastAPI (Python), connects to local Ollama (`llama3` model).
- Frontend: Streamlit (Python).
- AI: Local LLM only (no paid API usage).

## How to run (local)

1. Install Python 3 on Windows.

2. Install backend dependencies:
## How to run (local)

1. Install Python 3 on Windows.

2. Install backend dependencies:
  
   ```
   cd backend
   py -m pip install fastapi uvicorn requests 
3.Install frontend dependencies:

  ```
   cd ../frontend
   py -m pip install streamlit requests

```
4.Install and run Ollama:

Download from: https://ollama.com

First time (downloads model):
```
ollama run llama3
```
Then, in another terminal:
```
ollama serve
```
5.Start backend:
```
cd backend
py main.py
```
6.Start frontend:
```
cd frontend
py -m streamlit run app.py
```
7.Open the browser (Streamlit will show a local URL), paste a sample conversation, and click Generate Note.



   





