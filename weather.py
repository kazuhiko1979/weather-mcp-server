from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-mcp/1.0"

mcp = FastMCP("weather")


async def make_nws_request(
    url: str,
    *,
    params: dict[str, str] | None = None,
) -> dict[str, Any] | None:
    """NWS API にリクエストし、JSONレスポンスを返す。"""
    headers = {
        "Accept": "application/geo+json",
        "User-Agent": USER_AGENT,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError):
        return None


@mcp.tool()
async def get_weather(state: str) -> str:
    """
    Get active weather alerts for a US state.

    Args:
        state: Two-letter US state abbreviation, such as CA or NY.
    """
    state = state.strip().upper()
    if len(state) != 2 or not state.isalpha():
        return "Please provide a two-letter US state abbreviation, such as CA or NY."

    data = await make_nws_request(
        f"{NWS_API_BASE}/alerts/active",
        params={"area": state},
    )

    features = data.get("features", []) if data else []
    if not features:
        return f"No active weather alerts found for {state}."

    headlines = [
        alert.get("properties", {}).get("headline", "Untitled alert")
        for alert in features
    ]
    return "\n---\n".join(headlines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
