import streamlit as st
import requests
import json

st.title("HC-01 Ambient Clinical Note Generator")

tab1, tab2 = st.tabs(["From text", "From audio (mp3)"])

with tab1:
    st.write("Paste a sample doctor-patient conversation transcript below.")

    default_text = """Doctor: Hello, what brings you in today?
Patient: I've had a headache for the last three days, mostly on the right side.
Doctor: Any fever or blurred vision?
Patient: Mild fever yesterday, no blurred vision.
Doctor: Okay, I'll examine you and may start you on simple pain relief and hydration first."""

    transcript_input = st.text_area("Conversation transcript", value=default_text, height=200)

    if st.button("Generate Note from Text"):
        with st.spinner("Calling backend and local LLM..."):
            resp = requests.post(
                "http://localhost:8000/generate-from-text",
                json={"transcript": transcript_input}
            )

        if resp.status_code == 200:
            data = resp.json()
            st.subheader("Transcript used")
            st.text_area("Transcript", data["transcript"], height=150)

            st.subheader("Model output (raw)")
            st.code(data["result"], language="json")

            try:
                parsed = json.loads(data["result"])
                soap = parsed.get("soap", {})

                st.subheader("SOAP Note (Readable)")
                st.write("**Subjective**")
                st.write(soap.get("subjective", ""))
                st.write("**Objective**")
                st.write(soap.get("objective", ""))
                st.write("**Assessment**")
                st.write(soap.get("assessment", ""))
                st.write("**Plan**")
                st.write(soap.get("plan", ""))

                st.checkbox("Doctor has reviewed and approves this note")
            except Exception:
                st.error("Could not parse JSON from model. Showing raw response above.")
        else:
            st.error(f"Backend error: {resp.status_code} - {resp.text}")

with tab2:
    st.write("Upload a short doctor-patient consultation audio (mp3).")

    audio_file = st.file_uploader("Upload mp3", type=["mp3"])

    if audio_file is not None and st.button("Generate Note from Audio"):
        with st.spinner("Uploading audio and transcribing..."):
            files = {"file": (audio_file.name, audio_file.getvalue(), "audio/mpeg")}
            resp = requests.post("http://localhost:8000/upload-audio", files=files)

        if resp.status_code == 200:
            data = resp.json()
            st.subheader("Transcript from audio")
            st.text_area("Transcript", data["transcript"], height=150)

            st.subheader("Model output (raw)")
            st.code(data["result"], language="json")

            try:
                parsed = json.loads(data["result"])
                soap = parsed.get("soap", {})

                st.subheader("SOAP Note (Readable)")
                st.write("**Subjective**")
                st.write(soap.get("subjective", ""))
                st.write("**Objective**")
                st.write(soap.get("objective", ""))
                st.write("**Assessment**")
                st.write(soap.get("assessment", ""))
                st.write("**Plan**")
                st.write(soap.get("plan", ""))

                st.checkbox("Doctor has reviewed and approves this note")
            except Exception:
                st.error("Could not parse JSON from model. Showing raw response above.")
        else:
            st.error(f"Backend error: {resp.status_code} - {resp.text}")

