from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import json
import re
import tempfile
from pydub import AudioSegment
import speech_recognition as sr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def call_llm(transcript: str) -> str:
    prompt = f"""
You are a clinical scribe.
Given this doctor-patient conversation transcript, create:
1) A SOAP note in JSON with keys: subjective, objective, assessment, plan.

Return ONLY valid JSON, no explanations, in this exact format:

{{
  "soap": {{
    "subjective": "...",
    "objective": "...",
    "assessment": "...",
    "plan": "..."
  }}
}}

Transcript:
{transcript}
"""

    ollama_payload = {
        "model": "llama3",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    ollama_resp = requests.post("http://localhost:11434/v1/chat/completions", json=ollama_payload)
    ollama_resp.raise_for_status()
    data = ollama_resp.json()
    content = data["choices"][0]["message"]["content"]

    # Try to extract JSON block
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return match.group(0)
    return content

@app.post("/generate-from-text")
async def generate_from_text(body: dict):
    transcript = body.get("transcript", "")
    result_json = call_llm(transcript)
    return {"transcript": transcript, "result": result_json}

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    # 1. Save uploaded mp3 to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        content = await file.read()
        tmp.write(content)
        mp3_path = tmp.name

    # 2. Convert mp3 -> wav
    wav_path = mp3_path.replace(".mp3", ".wav")
    audio = AudioSegment.from_file(mp3_path)
    audio.export(wav_path, format="wav")

    # 3. Transcribe wav with SpeechRecognition (Google Web Speech)
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
    transcript = recognizer.recognize_google(audio_data)  # needs internet[web:40][web:45]

    # 4. Call LLM to get SOAP
    result_json = call_llm(transcript)

    return {
        "transcript": transcript,
        "result": result_json
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


