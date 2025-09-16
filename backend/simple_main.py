"""
Simple FastAPI backend for testing the pre-production analysis feature
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import time

app = FastAPI(title="MYTA Simple Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class PreProductionAnalysisRequest(BaseModel):
    description: str
    pillar: str
    contentIdea: str = ""

class AgentSuggestion(BaseModel):
    agent: str
    suggestion: str
    confidence: float
    reasoning: str

# Removed - using plain dict response to match frontend expectations

# Mock agent responses
def get_mock_agent_suggestions(description: str, pillar: str) -> List[AgentSuggestion]:
    """Generate mock suggestions from each agent"""
    
    suggestions = []
    
    # Alex (Content Agent) - Orange
    suggestions.append(AgentSuggestion(
        agent="Alex",
        suggestion="Structure your tutorial with clear sections: Introduction (30s), Environment Setup (2-3 min), Core Development (8-10 min), Deployment (2-3 min), and Conclusion (30s). Use code snippets and visual demonstrations.",
        confidence=0.92,
        reasoning="Tutorial content performs best with clear structure and practical demonstrations. Your topic covers full-stack development which benefits from step-by-step progression."
    ))
    
    # Levi (Audience Agent) - Blue  
    suggestions.append(AgentSuggestion(
        agent="Levi",
        suggestion="Your target audience is intermediate developers (65%) and beginners (35%). Focus on explaining concepts clearly while maintaining good pacing. Best upload time: Tuesday 2:00 PM PST for maximum engagement.",
        confidence=0.88,
        reasoning="Tech tutorial audiences prefer comprehensive explanations. Your pillar indicates educational content which performs well mid-week when developers are actively learning."
    ))
    
    # Maya (SEO Agent) - Purple
    suggestions.append(AgentSuggestion(
        agent="Maya",
        suggestion="Optimize for keywords: 'React MongoDB tutorial', 'full stack web development', 'MERN stack guide'. Include these in title, description, and tags. Estimated search volume: 45K monthly searches.",
        confidence=0.95,
        reasoning="Full-stack tutorials have high search demand. Your combination of React, Node.js, and MongoDB targets the popular MERN stack which has strong SEO potential."
    ))
    
    # Zara (Competitive Agent) - Yellow
    suggestions.append(AgentSuggestion(
        agent="Zara",
        suggestion="3 competitors covered similar topics recently. Differentiate by focusing on deployment strategies and real-world project structure. Avoid generic todo apps - build something practical like a blog or e-commerce site.",
        confidence=0.87,
        reasoning="Market analysis shows oversaturation of basic MERN tutorials. Your competitive advantage lies in practical application and deployment focus."
    ))
    
    # Kai (Monetization Agent) - Green
    suggestions.append(AgentSuggestion(
        agent="Kai",
        suggestion="High monetization potential. Include affiliate links for hosting services (Vercel, Netlify), development tools, and courses. Consider creating a follow-up paid course series. Estimated revenue: $200-500 per video.",
        confidence=0.91,
        reasoning="Technical tutorials have strong monetization potential through affiliate marketing and course sales. Your comprehensive approach supports premium content creation."
    ))
    
    return suggestions

@app.get("/")
async def root():
    return {"message": "MYTA Simple Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/workflows/pre-production-analysis")
async def pre_production_analysis(request: PreProductionAnalysisRequest):
    """
    Analyze content idea and provide coordinated suggestions from all agents
    """
    try:
        # Simulate processing time
        time.sleep(2)
        
        # Get mock suggestions from all agents
        suggestions = get_mock_agent_suggestions(request.description, request.pillar)
        
        # Generate optimized content suggestions
        optimized_title = "Complete MERN Stack Tutorial: Build & Deploy a Real Web App (React, Node.js, MongoDB)"
        optimized_description = f"""Learn to build a complete web application from scratch using the MERN stack! 

{request.description}

🚀 What You'll Learn:
• React frontend development with hooks and components
• Node.js backend API creation
• MongoDB database integration
• Full deployment to production

⏰ Timestamps:
00:00 Introduction & Project Overview
02:30 Environment Setup
05:00 MongoDB Database Design
12:00 Node.js Backend Development
25:00 React Frontend Creation
40:00 API Integration
50:00 Deployment & Production Setup
55:00 Next Steps & Resources

💻 Source Code: [Link in description]
🔗 Useful Links:
• MongoDB Atlas: [affiliate link]
• Vercel Deployment: [affiliate link]
• React Documentation: [link]

#ReactJS #NodeJS #MongoDB #WebDevelopment #FullStack #MERN #Tutorial #JavaScript"""

        optimized_tags = [
            "React tutorial", "Node.js", "MongoDB", "MERN stack", "full stack development",
            "web development", "JavaScript", "React hooks", "API development", "deployment"
        ]
        
        # Structure the response
        response_data = {
            "analysisId": f"analysis_{int(time.time())}",
            "timestamp": time.time(),
            "suggestions": {
                "title": {
                    "optimized": optimized_title,
                    "alternatives": [
                        "Build a Complete Web App: MERN Stack Tutorial for Beginners",
                        "React + Node.js + MongoDB: Full Stack Development Guide",
                        "MERN Stack Project: From Zero to Deployment"
                    ],
                    "source": "AI Generated"
                },
                "description": {
                    "optimized": optimized_description,
                    "source": "AI Generated"
                },
                "tags": {
                    "optimized": optimized_tags,
                    "source": "AI Generated"
                },
                "structure": {
                    "recommended": "Tutorial format with clear sections and timestamps",
                    "duration": "55-60 minutes",
                    "source": "AI Generated"
                }
            },
            "agentInsights": [
                {
                    "agent": suggestion.agent,
                    "suggestion": suggestion.suggestion,
                    "confidence": suggestion.confidence,
                    "reasoning": suggestion.reasoning
                }
                for suggestion in suggestions
            ],
            "performanceForecast": {
                "expectedViews": "15,000 - 35,000",
                "engagementRate": "6.2%",
                "confidence": "88%",
                "bestUploadTime": "Tuesday 2:00 PM PST"
            },
            "competitiveAnalysis": {
                "marketSaturation": "Medium",
                "differentiationOpportunity": "High",
                "recommendedFocus": "Practical deployment and real-world project structure"
            },
            "monetizationPotential": {
                "rating": "High",
                "estimatedRevenue": "$200-500",
                "opportunities": ["Affiliate marketing", "Course creation", "Sponsored content"]
            }
        }
        
        return {
            "status": "success",
            "data": response_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
