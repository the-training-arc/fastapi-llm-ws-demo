# AI-Powered Wellness Profiling Platform

This project implements an AI-powered wellness profiling platform that conducts real-time conversational interviews to build comprehensive user wellness profiles. The solution demonstrates proficiency in Python backend development, LLM integration, **hybrid communication architecture**, and intelligent data management.

---

## Architecture

The application follows a [Clean Architecture](http://blog.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/) pattern with clear separation of concerns:

```
app/
├── main.py                # FastAPI application entry point
├── controllers/           # API endpoints and WebSocket routes
├── usecases/              # Business logic and orchestration
├── models/                # Pydantic data models and schemas
├── repositories/          # Data persistence and state management
└── constants/             # Enums and constant definitions
```

---

## Key Features

### 1. **Hybrid Communication Architecture**
* **RESTful API**: Client-to-server communication for all user interactions
  - `POST /profile/initialize/{session_id}` - Initialize profiling session
  - `POST /profile/userAnswer/{session_id}` - Submit user responses with instant acknowledgment
* **WebSocket Communication**: Unidirectional server-to-client messaging for real-time updates
  - `WebSocket /ws/wellness_profile/{session_id}` - Receive live assistant responses
* **Unified State Management**: Seamless integration between REST and WebSocket communications

### 2. Real-time Conversational Interface

* WebSocket communication for real-time, conversation flow
* Session management with unique identifiers for concurrent users
* Structured message types: `INIT_PROFILE`, `USER_ANSWER`, `ASSISTANT_QUESTION`, `PROFILE_COMPLETE`, `MAX_REPLIES_REACHED`

### 3. Intelligent Wellness Profiling

* Comprehensive schema: captures age, gender, activity level, dietary preferences, sleep quality, stress level, and health goals
* Adaptive questioning: LLM-powered dynamic question generation based on user responses and conversation history
* Confidence scoring: tracks confidence levels for each profile field

### 4. LLM Integration

* AWS Bedrock (Anthropic Claude): uses Sonnet for reasoning
* Instructor framework for structured, validated LLM responses
* Contextual analysis of entire conversation history
* Retry logic and robust error handling 3 times maximum

### 5. Smart Data Management

* Pydantic validation and serialization
* Progressive profile building: intelligently merges new information with existing profile data
* State persistence: maintains conversation history and profile state across WebSocket connections

---

## Technical Requirements Fulfilled

* **Backend API**: FastAPI with asynchronous endpoints, WebSocket support, and RESTful structure
* **Hybrid Communication Endpoints**:

  **RESTful API:**
  * `POST /profile/initialize/{session_id}` - Initialize session with immediate response
  * `POST /profile/userAnswer/{session_id}` - Submit answers with instant acknowledgment

  **WebSocket:**
  * `WebSocket /ws/wellnessProfile/{session_id}` – Real-time profiling conversation
  * Supports: `INIT_PROFILE`, `USER_ANSWER`, `ASSISTANT_QUESTION`, `PROFILE_COMPLETE`, `MAX_REPLIES_REACHED`

* **Intelligent Profiling Schema**:

  ```python
  class WellnessProfile(BaseModel):
      age: Optional[int] = Field(ge=1, le=100)
      gender: Optional[Gender]                   # male/female/other
      activityLevel: Optional[ActivityLevel]     # sedentary/moderate/active
      dietaryPreference: Optional[DietaryPreference]  # vegan/vegetarian/keto/paleo/omnivore/no_preference
      sleepQuality: Optional[SleepQuality]       # poor/average/good
      stressLevel: Optional[StressLevel]         # low/medium/high
      healthGoals: Optional[str]                 # free text
  ```
* **LLM Integration**:

  * Anthropic Claude (Sonnet 3.5) via AWS Bedrock
  * Adaptive questioning (max 5 questions per session)
  * Context-aware, structured output extraction and validation
* **Data Integrity**:

  * Pydantic validation for all data structures
  * Intelligent profile merging without data loss
  * Confidence tracking for each field
* **Containerization**:

  * Docker support (multi-stage builds)
  * UV for fast dependency resolution

---

## Technology Stack

* Framework: FastAPI (WebSockets, async)
* LLM: Anthropic Claude via AWS Bedrock
* AI Framework: Instructor (structured LLM outputs)
* Validation: Pydantic v2
* Package Management: UV
* Containerization: Docker (slim Python images)
* Logging: structlog

---

## Getting Started

### Prerequisites

* Python 3.12+
* Docker
* .env file


### Local Development

```bash
docker compose -f docker-compose.yml up --build
```

### Production Deployment

```bash
docker-compose -f docker-compose.prod.yml up --build
```

---

## API Usage

### **API Documentation**

Interactive API documentation is available via Swagger UI at:
**http://127.0.0.1:8000/swagger#/**
or via redoc
**http://127.0.0.1:8000/redoc#/**

This provides a complete reference for all REST endpoints with request/response examples and the ability to test endpoints directly from the browser.

### **Hybrid REST + WebSocket Architecture**

This application uses a sophisticated hybrid approach where:
- **Client → Server**: All communication via REST API (immediate responses)
- **Server → Client**: All communication via WebSocket (real-time updates)

**Key Benefits:**
- **Immediate Feedback**: REST endpoints provide instant acknowledgment for all user actions
- **Real-time Updates**: WebSocket delivers live assistant responses without polling
- **Reliable Communication**: REST ensures no user input is lost, WebSocket provides seamless real-time experience
- **Clean Separation**: Clear distinction between user actions (REST) and system responses (WebSocket)

**Architecture Details:**
* **RESTful API for All Client Actions**:
  - Session initialization with instant confirmation
  - User answer submission with immediate acknowledgment
  - Better error handling and status reporting
  - Ensures no user input is lost due to connection issues

* **WebSocket for Real-Time Server Updates**:
  - Live assistant responses without polling
  - Natural conversation flow with minimal latency
  - Real-time profile completion notifications
  - Efficient unidirectional server-to-client communication

* **Unified State Management**: Both communication methods share the same session state and business logic
* **Optimal User Experience**: Immediate feedback on actions + real-time conversation flow
* **Scalability**: REST endpoints can be load-balanced independently of WebSocket connections


```js
// 1. Initialize session via REST API (immediate response)
const initResponse = await fetch('http://127.0.0.1:8000/profile/initialize/user123', {
    method: 'POST'
});
console.log(await initResponse.json()); // {"status": "success", "message": "Wellness Profile Initialized"}

// 2. Connect to WebSocket for real-time server updates
const ws = new WebSocket('ws://127.0.0.1:8000/ws/wellness_profile/user123');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.event === 'ASSISTANT_QUESTION') {
        console.log('Assistant:', data.message);
    } else if (data.event === 'PROFILE_COMPLETE') {
        console.log('Profile Complete:', JSON.parse(data.message));
    }
};

// 3. Send user responses via REST API (immediate acknowledgment)
const sendAnswer = async (answer) => {
    const response = await fetch('http://127.0.0.1:8000/profile/userAnswer/user123', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: answer })
    });
    console.log(await response.json()); // {"status": "success", "message": "User Answer Sent"}
};

// Usage
await sendAnswer("I'm 28 years old and I try to exercise 3 times a week");
```

### **Communication Flow**

**Hybrid REST + WebSocket Flow:**
1. Client → `POST /profile/initialize/{session_id}` → Server (immediate response)
2. Server → `ASSISTANT_QUESTION` → Client (via WebSocket)
3. Client → `POST /profile/userAnswer/{session_id}` → Server (immediate acknowledgment)
4. Server → `ASSISTANT_QUESTION` → Client (via WebSocket)
5. Repeat steps 3–4 until profile is complete
6. Server → `PROFILE_COMPLETE` → Client (via WebSocket)

---

## Key Implementation Highlights

### Intelligent Question Generation

* The LLM analyzes the entire conversation history to:

  * Extract information from any user message
  * Assess completeness of profile fields
  * Generate contextually appropriate follow-up questions
  * Determine when the profile is complete

### Progressive Profile Building

```python
def __merge_wellness_profile(self, existing: WellnessProfile, new: WellnessProfile) -> WellnessProfile:
    """Merge profiles, preferring new non-None values over existing data."""
    merged_data = existing.model_dump()
    new_data = new.model_dump()
    for key, value in new_data.items():
        if value is not None:
            merged_data[key] = value
    return WellnessProfile(**merged_data)
```

### Confidence-Based Completion

* Tracks confidence levels for each profile field, ensuring data quality before marking the profile as complete.

---

## Testing and Error Handling

* Comprehensive error handling and logging
* Robust WebSocket connection management (cleanup/disconnect logic)

---

## Architecture Decisions
* Clean architecture with strict separation of concerns
* Event-driven design via WebSocket events
* In-memory state management (for demonstration)
* Incremental profile building for user experience
