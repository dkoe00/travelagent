from typing import Any

from agents import Runner
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from travelagent.api.events import sse_format, translate_stream
from travelagent.api.sessions import ChatSession, create_session, delete_session, get_session
from travelagent.config import APP_CONFIG
from travelagent.runtime import configure_agents_sdk

configure_agents_sdk(APP_CONFIG)

app = FastAPI(title="Travel Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SessionResponse(BaseModel):
    session_id: str
    language: str


class MessageRequest(BaseModel):
    content: str


_COMPLETED_MESSAGE = {
    "de": "Die Planung ist bereits abgeschlossen.",
    "en": "The planning session is already complete.",
}


@app.post("/api/sessions", response_model=SessionResponse)
def post_session() -> SessionResponse:
    session = create_session()
    return SessionResponse(session_id=session.session_id, language=APP_CONFIG.language)


@app.delete("/api/sessions/{session_id}", status_code=204)
def remove_session(session_id: str) -> None:
    delete_session(session_id)


@app.post("/api/sessions/{session_id}/messages")
async def post_message(session_id: str, message: MessageRequest) -> StreamingResponse:
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Unknown session")

    async def event_stream() -> Any:
        async with session.lock:
            if session.completed:
                completed_message = _COMPLETED_MESSAGE.get(APP_CONFIG.language, _COMPLETED_MESSAGE["de"])
                yield sse_format("final", {"text": completed_message})
                yield sse_format("done", {})
                return

            run_input = session.history + [{"role": "user", "content": message.content}]
            result = Runner.run_streamed(session.agent, run_input, context=session.state)
            async for chunk in translate_stream(result):
                yield chunk
            session.agent = result.last_agent
            try:
                session.history = result.to_input_list()
            except Exception:
                pass
            if session.state.should_exit:
                session.completed = True

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
