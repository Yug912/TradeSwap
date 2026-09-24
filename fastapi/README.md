# FastAPI Matching Service

The FastAPI service provides the Day 1 foundation for TradeSwap matching:

- `GET /health` reports service health.
- `POST /match` validates the agreed matching request and returns a placeholder response.
- `GET /docs` provides Swagger documentation.
- Pytest covers health, valid matching requests, and validation errors.

The matching algorithm is intentionally not implemented yet. Start the service
from this directory with:

```bash
uvicorn app.main:app --reload --port 8001
```