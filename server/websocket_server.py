import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import whisper

app = FastAPI()

model = whisper.load_model("tiny")


# Replace this with your actual transcription model/function
def transcribe_audio_chunk(audio_chunk: bytes) -> str:
    # Example: return "Transcribed text"
    # TODO: Implement your model inference here
    result = model.transcribe("audio.mp3")
    return "Transcribed text"


@app.websocket("/TranscribeStreaming")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_open = True
    final_transcript = ""

    try:
        while websocket_open:
            message = await websocket.receive()
            if message["type"] == "websocket.receive":
                if "bytes" in message:
                    audio_chunk = message["bytes"]
                    transcript = transcribe_audio_chunk(audio_chunk)
                    final_transcript += transcript + " "
                    await websocket.send_text(transcript)
                elif "text" in message:
                    text_message = message["text"]
                    logging.info(f"Received message: {text_message}")
                    if text_message == "submit_response":
                        websocket_open = False
                        await websocket.send_text(
                            f"Final Transcript: {final_transcript.strip()}"
                        )
                        break
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, ws_ping_interval=None)
