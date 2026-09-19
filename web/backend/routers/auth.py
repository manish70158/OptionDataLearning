"""Upstox OAuth callback router.

Flow:
1. User clicks "Authorise Upstox" in the UI → GET /api/auth/upstox/authorize
2. We redirect to Upstox's login dialog with ``client_id`` + ``redirect_uri``.
3. Upstox redirects back to /api/auth/upstox/callback?code=...
4. We POST the code to Upstox's token endpoint, receive ``access_token``,
   store it in the DB, and reload the fetcher's in-memory token.

Env vars required on the server:
- ``UPSTOX_API_KEY`` — the app's OAuth client_id
- ``UPSTOX_API_SECRET`` — the app's OAuth client_secret
- ``UPSTOX_REDIRECT_URI`` — must exactly match the redirect URI configured
   in the Upstox app settings, e.g.
   ``https://manishkumar.qzz.io/api/auth/upstox/callback``.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse

from web.backend.data.cache import init_db, upsert_upstox_credentials, get_upstox_credentials

logger = logging.getLogger(__name__)
router = APIRouter(tags=["auth"])

_AUTH_URL = "https://api.upstox.com/v2/login/authorization/dialog"
_TOKEN_URL = "https://api.upstox.com/v2/login/authorization/token"


def _redirect_uri(request_url: str | None = None) -> str:
    """Prefer the explicit env var; otherwise derive from the current request."""
    configured = os.environ.get("UPSTOX_REDIRECT_URI")
    if configured:
        return configured
    if request_url:
        # Trim the query string / trailing path — expected shape is host + /api/auth/upstox/callback
        from urllib.parse import urlparse
        u = urlparse(request_url)
        return f"{u.scheme}://{u.netloc}/api/auth/upstox/callback"
    return ""


@router.get("/auth/upstox/authorize")
async def upstox_authorize():
    """Redirect the browser to Upstox's OAuth login dialog."""
    api_key = os.environ.get("UPSTOX_API_KEY")
    redirect = _redirect_uri()
    if not api_key or not redirect:
        raise HTTPException(
            status_code=500,
            detail=(
                "UPSTOX_API_KEY or UPSTOX_REDIRECT_URI env vars not set on the server. "
                "Configure them and redeploy before triggering OAuth."
            ),
        )
    params = {
        "client_id": api_key,
        "redirect_uri": redirect,
        "response_type": "code",
    }
    return RedirectResponse(f"{_AUTH_URL}?{urlencode(params)}")


@router.get("/auth/upstox/callback")
async def upstox_callback(code: str = Query(...)):
    """Exchange the authorization code for an access token and persist it."""
    api_key = os.environ.get("UPSTOX_API_KEY")
    api_secret = os.environ.get("UPSTOX_API_SECRET")
    redirect = _redirect_uri()
    if not (api_key and api_secret and redirect):
        raise HTTPException(status_code=500, detail="Upstox app not configured on server")

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            _TOKEN_URL,
            data={
                "code": code,
                "client_id": api_key,
                "client_secret": api_secret,
                "redirect_uri": redirect,
                "grant_type": "authorization_code",
            },
            headers={"Accept": "application/json"},
        )
    if r.status_code != 200:
        return HTMLResponse(
            f"<h2>Upstox token exchange failed ({r.status_code})</h2>"
            f"<pre>{r.text}</pre>",
            status_code=r.status_code,
        )
    payload = r.json()
    access_token = payload.get("access_token")
    if not access_token:
        return HTMLResponse(f"<h2>No access_token in response</h2><pre>{payload}</pre>", status_code=502)

    # Upstox tokens expire the next trading day at 3:30 AM IST — persist an
    # approximate expiry so the UI can show freshness.
    expires_in = payload.get("expires_in")
    if isinstance(expires_in, (int, float)) and expires_in > 0:
        expires_at = (datetime.utcnow() + timedelta(seconds=expires_in)).isoformat()
    else:
        expires_at = None

    await init_db()
    await upsert_upstox_credentials(
        access_token=access_token,
        refresh_token=payload.get("refresh_token"),
        expires_at=expires_at,
    )

    # Reload the pricing engine's shared fetcher so subsequent requests use the new token.
    try:
        from web.backend.engine import pricing
        if pricing._fetcher is not None:
            await pricing._fetcher.reload_access_token()
    except Exception as e:
        logger.warning(f"Could not hot-reload pricing fetcher: {e}")

    return HTMLResponse(
        "<h2 style='font-family:sans-serif'>Upstox authorised ✓</h2>"
        "<p>Access token stored. You can close this tab and return to the app.</p>"
        "<p><a href='/'>Go to app</a></p>"
    )


@router.get("/auth/upstox/status")
async def upstox_status():
    """Return whether the app has a stored Upstox token and when it was updated."""
    await init_db()
    row = await get_upstox_credentials()
    if not row:
        return {"authorised": False}
    return {
        "authorised": True,
        "updated_at": row.get("updated_at"),
        "expires_at": row.get("expires_at"),
    }
