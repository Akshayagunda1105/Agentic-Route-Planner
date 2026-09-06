# Agentic Route Planner

Plan a multi-stop Telangana route from natural language, assess weather at the
selected stops, and show the resulting road route on an OpenStreetMap map.

## Free setup

1. Create a free OpenRouteService API key at https://openrouteservice.org/dev/#/signup.
2. Copy `.env.example` to `.env` and fill in the three API keys.
3. Start the API with `uvicorn app.api.main:app --reload`.
4. In `frontend`, run `npm install` then `npm run dev`.

The map uses OpenStreetMap tiles and includes the required attribution. The
public tile service is for light interactive use only; do not bulk-download or
prefetch tiles.
