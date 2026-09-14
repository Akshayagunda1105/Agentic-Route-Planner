# Agentic Route Planner

An intelligent multi-stop route planning application that converts natural-language travel requests into optimized road routes, evaluates weather risk, and presents route alternatives when critical weather conditions are detected.

The application combines **LLM-based intent understanding**, **deterministic route optimization**, **road-network routing**, **weather analysis**, and **human-in-the-loop decision making**.

## Features

- Natural-language route planning
- Multi-stop route optimization
- Location disambiguation for places with the same name
- Road-network routing using OpenRouteService
- Nearest Neighbor + 2-opt optimization
- Distance, duration, and weather-aware planning objectives
- Weather information for route stops
- Deterministic weather-risk scoring
- Critical-weather detection
- Human-in-the-loop route selection
- Lower-weather-risk alternative generation
- Interactive OpenStreetMap-based route visualization
- Input validation and error handling
- Automated backend test suite

## Architecture

```text
USER
  │
  ▼
INPUT GUARDRAIL
  │
  ▼
INTENT AGENT
  │
  │  Natural language → structured route request
  ▼
OUTPUT GUARDRAIL
  │
  ▼
LOCATION AGENT
  │
  │  Resolve and disambiguate locations
  ▼
PLANNING AGENT
  ├──────────────► ROUTING AGENT ──► OpenRouteService
  │
  ├──────────────► WEATHER AGENT ──► OpenWeather
  │
  └──────────────► CONSTRAINT ENGINE
  │
  ▼
OPTIMIZATION AGENT
  │
  ├── Road-network cost
  ├── Nearest Neighbor
  ├── 2-opt improvement
  ├── Weather-aware cost
  └── Route constraints
  │
  ▼
VERIFICATION / REFLECTION AGENT
  │
  ├── PASS ───────────────► RESULT
  │
  ├── RETRY ──────────────► OPTIMIZER
  │
  └── CRITICAL WEATHER ──► ROUTE ALTERNATIVES
                              │
                              ▼
                       HUMAN SELECTION
                              │
                              ▼
                           RESULT
```

## How It Works

### 1. Natural-Language Input

The user describes the journey in natural language.

Example:

```text
Plan a weather-aware route from Hyderabad to Warangal via Nalgonda and Suryapet.
```

### 2. Intent Understanding

The intent agent uses an LLM to extract structured information such as:

- Start location
- Destination
- Waypoints
- Optimization objective
- Weather sensitivity
- Route constraints
- Departure time

The LLM is intentionally limited to **language understanding** rather than making routing or safety decisions.

### 3. Location Resolution

Locations are resolved to geographic coordinates.

If multiple locations have the same name, the application asks the user to select the intended location using additional administrative information such as:

- Subdistrict
- District

The selected location is then used for route planning.

### 4. Road Routing

The application uses **OpenRouteService** to obtain road-network distances, durations, route geometry, and leg information.

### 5. Route Optimization

For multi-stop routes, the planner uses a deterministic:

```text
Nearest Neighbor → 2-opt
```

strategy to determine an efficient waypoint order.

The optimization can consider:

- Distance
- Duration
- Weather-aware cost

The algorithm is heuristic and therefore does not claim global optimality.

### 6. Weather Analysis

Weather information is retrieved for the locations along the planned route.

A deterministic weather-risk engine calculates a risk score using factors such as:

- Weather condition
- Wind speed
- Humidity
- Temperature

The resulting risk is classified as:

```text
Low
Medium
High
Critical
```

### 7. Verification and Reflection

A deterministic reflection agent verifies the generated result.

It checks conditions such as:

- Route availability
- Valid distance and duration
- Duplicate locations
- Weather availability
- Valid weather-risk scores
- Weather severity

If a recoverable planning issue is detected, the graph can retry optimization.

### 8. Critical Weather Handling

When critical weather risk is detected, the system does **not silently change the user's route**.

Instead, it presents:

- **Route A** — the requested/primary optimized route
- **Route B** — a lower-weather-risk alternative, when one can be generated

The user chooses which route to take.

This makes the critical-weather decision **human-in-the-loop** rather than allowing the system to make a safety decision on behalf of the user.

## Technology Stack

### Backend

- Python
- FastAPI
- LangGraph
- Pydantic

### AI

- Gemini / LLM for natural-language intent parsing

### Routing & Maps

- OpenRouteService
- OpenStreetMap

### Weather

- OpenWeather

### Frontend

- React
- Vite
- Tailwind CSS
- Axios

### Testing

- Pytest

## Project Structure

```text
Agentic-Route-Planner/
│
├── app/
│   ├── agents/
│   ├── api/
│   ├── graph/
│   ├── models/
│   ├── services/
│   ├── state/
│   └── strategies/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── services/
│       └── App.jsx
│
├── tests/
│
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

Make sure the following are installed:

- Python 3.x
- Node.js and npm

### 1. Clone the Repository

```bash
git clone https://github.com/Akshayagunda1105/Agentic-Route-Planner.git

cd Agentic-Route-Planner
```

### 2. Create the Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Add the required API credentials to `.env`.

See `.env.example` for the exact variable names.

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Backend

From the project root:

```bash
uvicorn app.api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 5. Install Frontend Dependencies

Open another terminal:

```bash
cd frontend
npm install
```

### 6. Start the Frontend

```bash
npm run dev
```

Open the local URL displayed by Vite in your browser.

## API

### POST `/plan-route`

Accepts a natural-language route-planning request.

Example request:

```json
{
  "query": "Plan a route from Hyderabad to Warangal via Nalgonda and Suryapet",
  "selections": {}
}
```

The API returns route optimization results, weather analysis, reflection information, and, when critical weather is detected, available route options for human selection.

## Optimization Strategy

The route optimizer uses a heuristic approach:

```text
1. Build road-network cost matrix
2. Generate an initial route using Nearest Neighbor
3. Improve the waypoint order using 2-opt
4. Calculate the final road route
```

For weather-aware planning, weather risk can also contribute to the optimization cost.

This approach provides a practical balance between computational simplicity and route quality for multi-stop planning.

It is a heuristic optimization strategy and **does not guarantee the globally optimal route**.

## Weather Risk Model

Weather risk is calculated deterministically rather than generated by the LLM.

The risk score combines contributions from:

```text
Condition Risk
      +
Wind Risk
      +
Humidity Risk
      +
Temperature Risk
      =
Weather Risk Score
```

The resulting score is mapped to a risk level and recommendation.

This makes the safety-related logic:

- Explainable
- Deterministic
- Testable
- Independent of LLM decisions

## Human-in-the-Loop Design

The system deliberately keeps safety-sensitive route decisions under user control.

When critical weather is detected:

```text
Critical Weather
       │
       ▼
Generate Primary Route
       │
       ├──────────────► Route A
       │
       ▼
Generate Alternative
       │
       ▼
Evaluate Weather Risk
       │
       ▼
Route B: Lower Weather Risk
       │
       ▼
     USER
   /       \
Route A   Route B
```

The application does not automatically select the lower-weather-risk route for the user.

## Testing

Run the backend test suite from the project root:

```bash
python -m pytest
```

The current test suite covers route planning, optimization, weather analysis, reflection, and route-alternative behavior.

## External Services

The application uses external APIs for:

- **OpenRouteService** — road routing and route information
- **OpenWeather** — weather information
- **Gemini / LLM provider** — natural-language intent parsing
- **OpenStreetMap** — map data and map tiles

API keys are required for the corresponding services.

**Do not commit your `.env` file or API keys to the repository.**

## Limitations

- Nearest Neighbor + 2-opt is a heuristic and does not guarantee global optimality.
- Weather analysis is performed for the locations available to the weather agent rather than providing a complete meteorological analysis of every point on the road.
- Alternative routes depend on having multiple waypoints that allow a distinct waypoint ordering to be generated.
- Route planning depends on the availability of the configured external APIs.
- Traffic conditions and real-time road closures are not currently modeled.

## Future Improvements

Possible future improvements include:

- Real-time traffic integration
- Road-closure and incident data
- More advanced route optimization algorithms
- Caching of external API responses
- Additional travel modes
- More detailed weather-segment analysis
- Production deployment
- Authentication and user accounts

## License

This project is intended for educational and portfolio purposes.