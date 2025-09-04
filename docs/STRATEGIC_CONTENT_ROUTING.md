# Strategic Content Routing System

## Overview

This system automatically differentiates between strategic planning queries and everyday insights to route users to the appropriate interface:

- **Strategic Planning Dashboard** - For quarterly strategies, long-term planning, and comprehensive strategic discussions
- **Agent Chat** - For everyday insights, tactical questions, and immediate actionable advice

## Problem Solved

Previously, quarterly strategy content was appearing in the Agent chat when it should be routed to the Strategic Planning Dashboard. Users were getting strategic planning responses mixed with everyday tactical advice, creating confusion about where to find different types of insights.

## Solution Components

### 1. Strategic Content Classifier (`backend/App/strategic_content_classifier.py`)

A sophisticated classifier that analyzes user messages and determines whether they should be routed to strategic planning or everyday insights based on:

**Strategic Planning Indicators:**
- Time-based keywords: "quarterly", "annual", "long-term", "Q1/Q2/Q3/Q4"
- Planning keywords: "strategic planning", "roadmap", "goal setting", "comprehensive strategy"
- Scope keywords: "big picture", "overall strategy", "strategic direction"
- Collaboration keywords: "team strategy", "strategic coordination"

**Everyday Insights Indicators:**
- Immediacy keywords: "today", "now", "this week", "current", "latest"
- Optimization keywords: "optimize", "improve", "fix", "boost", "quick win"
- Specific content keywords: "this video", "my latest", "recent upload"
- Tactical actions: "thumbnail test", "title optimization", "posting time"

### 2. Boss Agent Integration (`backend/App/boss_agent_core.py`)

The boss agent now includes strategic content classification in its processing pipeline:

1. Classifies user intent (existing functionality)
2. **NEW:** Checks if content should be routed to strategic planning
3. If strategic planning is detected, returns a redirect response
4. Otherwise, continues with normal agent processing

### 3. Frontend Handling (`frontend-nuxt4/components/chat/AgentChatPanel.vue`)

The agent chat interface now:

1. Makes real API calls to the backend instead of simulated responses
2. Handles strategic planning redirect responses
3. Shows special UI for strategic planning redirects with confidence indicators
4. Automatically navigates users to the Strategic Planning Dashboard when appropriate

## Classification Accuracy

Current performance metrics:
- **Strategic Examples:** 75% accuracy
- **Tactical Examples:** 100% accuracy  
- **Overall Accuracy:** 87.5%

## Usage Examples

### Strategic Planning Queries (Redirected)
- "What should my quarterly strategy be for Q2?"
- "I need help with long-term planning for my channel"
- "Can you help me create a strategic roadmap for next year?"
- "What are the strategic priorities for my channel growth?"
- "Help me with annual goal setting and planning"

### Everyday Insights Queries (Stay in Chat)
- "How can I optimize this video's thumbnail?"
- "What should I do to improve my latest video performance?"
- "Can you analyze my current analytics?"
- "How do I fix my retention rate today?"
- "Help me improve my video titles right now"

## Configuration

### Confidence Threshold
The system uses a confidence threshold of 0.4 (40%) to determine redirects. This can be adjusted in the classifier:

```python
should_redirect, analysis = classifier.should_redirect_to_strategic_planning(
    message, 
    confidence_threshold=0.4  # Adjust this value
)
```

### Customizing Keywords
Add new keywords to the classifier's keyword dictionaries to improve detection for your specific use case.

## Testing

Run the test script to verify classifier performance:

```bash
cd backend/App
python3 test_strategic_classifier.py
```

## Benefits

1. **Clear Separation of Concerns:** Strategic planning and tactical advice are now properly separated
2. **Better User Experience:** Users are automatically guided to the right interface for their needs
3. **Improved Context:** Strategic discussions happen in the strategic planning environment with appropriate tools
4. **Maintained Flexibility:** Users can still manually navigate between interfaces if needed

## Future Enhancements

1. **Machine Learning:** Train a more sophisticated ML model on user interaction data
2. **User Feedback:** Allow users to correct misclassifications to improve the system
3. **Context Awareness:** Consider conversation history and user patterns for better classification
4. **A/B Testing:** Test different confidence thresholds and keyword sets to optimize performance
