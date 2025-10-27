# backend/tests/test_api.py
import os
os.environ["STORAGE_BACKEND"] = "memory"  # ensure clean in-memory state for this test run

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_status_and_fill_and_brew():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # initial
        r = await ac.get("/api/status")
        assert r.status_code == 200

        # fill both
        r = await ac.post("/api/fill/water", json={"amount_ml": 1000})
        assert r.status_code == 200
        r = await ac.post("/api/fill/coffee", json={"amount_g": 100})
        assert r.status_code == 200

        # brew espresso
        r = await ac.post("/api/brew", json={"type": "espresso"})
        assert r.status_code == 200
        data = r.json()
        assert "Enjoy your espresso" in data["message"]
        assert data["state"]["water_ml"] == 1000 - 24
        assert data["state"]["coffee_g"] == 100 - 8
