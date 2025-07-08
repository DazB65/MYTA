from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
# Import from the same directory
from ai_services import get_ai_response, extract_channel_info, update_user_context

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    user_id: str = "default_user"

@app.post("/api/agent/chat")
async def chat(message: ChatMessage):
    """Endpoint to handle chat messages from the user"""
    try:
        # Extract any channel info from the message
        extract_channel_info(message.user_id, message.message)
        
        # Get AI response with context
        response = await get_ai_response(message.message, message.user_id)
        return {"response": response}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

@app.get("/api/agent/status")
def agent_status():
    """Endpoint to check if the AI agent is running"""
    return {
        "status": "online",
        "version": "1.0.0",
        "model": "gpt-4o"
    }
class ChannelInfo(BaseModel):
    name: str = "Unknown"
    niche: str = "Unknown"
    content_type: str = "Unknown"
    subscriber_count: int = 0
    avg_view_count: int = 0
    ctr: float = 0
    retention: float = 0
    upload_frequency: str = "Unknown"
    video_length: str = "Unknown"
    monetization_status: str = "Unknown"
    primary_goal: str = "Unknown"
    notes: str = ""
    user_id: str = "default_user"

@app.post("/api/agent/set-channel-info")
async def set_channel_info(channel_info: ChannelInfo):
    """Endpoint to manually set channel information"""
    try:
        # Extract channel info fields
        info = {
            "name": channel_info.name,
            "niche": channel_info.niche,
            "content_type": channel_info.content_type,
            "subscriber_count": channel_info.subscriber_count,
            "avg_view_count": channel_info.avg_view_count,
            "ctr": channel_info.ctr,
            "retention": channel_info.retention,
            "upload_frequency": channel_info.upload_frequency,
            "video_length": channel_info.video_length,
            "monetization_status": channel_info.monetization_status,
            "primary_goal": channel_info.primary_goal,
            "notes": channel_info.notes
        }
        
        # Update user context
        update_user_context(channel_info.user_id, "channel_info", info)
        
        return {"status": "success", "message": "Channel information updated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Add a health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
@app.get("/api/agent/status")
def agent_status():
    """Endpoint to check if the AI agent is running"""
    return {
        "status": "online",
        "version": "1.0.0",
        "model": "gpt-4o"
    }
# Mount static files - update the path to point to the frontend directory
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")