# TradeSwap

TradeSwap is a skill-exchange platform where users can teach skills to each
other instead of exchanging money.

## Architecture

```text
React + TypeScript
        ↓
Django + DRF
        ↓
PostgreSQL
```

Django will communicate with a separate FastAPI service for matching and AI
functionality.

## Current Status

Day 1:

- Django backend initialized
- DRF configured
- CORS configured for `http://localhost:5173`
- Users and skills apps created
- PostgreSQL configuration prepared
