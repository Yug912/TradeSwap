# FastAPI Matching Service

The TradeSwap FastAPI service exposes health and reciprocal skill matching
endpoints. Matching currently uses eight fictional profiles from
`app.data.dummy_users.DUMMY_USERS`.

## Endpoints

### `GET /health`

Reports whether the service is running.

Response (`200 OK`):

```json
{"status": "ok"}
```

### `POST /match`

Validates the supplied user profile and returns reciprocal matches from the
dummy dataset. Skills match case-insensitively, and offered proficiency must
meet the requested proficiency in both directions. A valid profile with no
matches returns an empty `matches` list. Invalid request bodies return
`422 Unprocessable Entity`.

Request body (`MatchRequest`):

```json
{
  "user_id": 1,
  "teach": [{"skill": "Python", "level": "advanced"}],
  "learn": [{"skill": "Machine Learning", "level": "beginner"}]
}
```

Each skill level must be `beginner`, `intermediate`, or `advanced`. Both `teach`
and `learn` default to empty lists.

Response (`200 OK`, `MatchResponse`):

```json
{
  "matches": [{"user_id": 2, "score": 100.0}]
}
```

The current rule-based matcher returns a fixed score of `100` for each match;
it does not calculate a ranking score.

## CORS

By default, browser requests are allowed from `http://localhost:5173` and
`http://127.0.0.1:5173`. Set `FASTAPI_CORS_ORIGINS` to a comma-separated list of
explicit origins when the frontend runs elsewhere. The API does not allow every
origin.

## Run locally

From this `fastapi` directory, start the service with:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open Swagger UI at <http://127.0.0.1:8000/docs>. Expand `GET /health` or
`POST /match`, select **Try it out**, enter a request body for `/match`, and
select **Execute**. The OpenAPI schema is available at
<http://127.0.0.1:8000/openapi.json>.

Run the tests from this directory with:

```bash
python -m pytest
```
