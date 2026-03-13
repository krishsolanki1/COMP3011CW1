"""
BMW Market Analytics MCP Server
Exposes BMW pricing API tools for use with Claude and other MCP clients.
"""

import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://krish1802.pythonanywhere.com"

mcp = FastMCP("BMW Market Analytics")


async def _get(path: str, params: dict | None = None) -> dict | list | None:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BASE_URL}{path}", params=params, timeout=30.0)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            return {"error": str(exc)}


@mcp.tool()
async def list_models(
    fuel_type: str = "",
    transmission: str = "",
    name: str = "",
    limit: int = 50,
) -> str:
    """List BMW car models with optional filtering.

    Args:
        fuel_type: Filter by exact fuel type (e.g. Diesel, Petrol, Hybrid).
        transmission: Filter by exact transmission (e.g. Automatic, Manual, Semi-Auto).
        name: Filter by model name (partial, case-insensitive).
        limit: Maximum number of results to return (1–500).
    """
    params = {"limit": limit}
    if fuel_type:
        params["fuel_type"] = fuel_type
    if transmission:
        params["transmission"] = transmission
    if name:
        params["name"] = name
    data = await _get("/models/", params)
    if isinstance(data, list):
        lines = [f"id={m['id']}  name={m['name']}  fuel={m['fuel_type']}  transmission={m['transmission']}" for m in data]
        return f"Found {len(data)} model(s):\n" + "\n".join(lines)
    return str(data)


@mcp.tool()
async def get_model(model_id: int) -> str:
    """Get full details for a single BMW model by its ID.

    Args:
        model_id: The integer ID of the car model.
    """
    data = await _get(f"/models/{model_id}")
    if isinstance(data, dict) and "error" not in data and "detail" not in data:
        return (
            f"Model #{data['id']}: {data['name']}\n"
            f"  Series:       {data.get('series') or '—'}\n"
            f"  Body style:   {data.get('body_style') or '—'}\n"
            f"  Fuel type:    {data.get('fuel_type') or '—'}\n"
            f"  Transmission: {data.get('transmission') or '—'}"
        )
    return str(data)


@mcp.tool()
async def get_average_price(model_id: int) -> str:
    """Get the average market price for a BMW model across all recorded years.

    Args:
        model_id: The integer ID of the car model.
    """
    data = await _get("/analytics/average-price", {"model_id": model_id})
    if isinstance(data, dict) and "average_price" in data:
        return (
            f"{data['model_name']} (id={data['model_id']}): "
            f"average price = £{data['average_price']:,.2f}"
        )
    return str(data)


@mcp.tool()
async def get_price_trend(model_id: int) -> str:
    """Get the year-by-year average price trend for a BMW model.

    Args:
        model_id: The integer ID of the car model.
    """
    data = await _get("/analytics/price-trend", {"model_id": model_id})
    if isinstance(data, dict) and "trend" in data:
        lines = [
            f"  {row['year']}: £{row['average_price']:,.2f}  ({row['num_records']} records)"
            for row in data["trend"]
        ]
        return f"Price trend for {data['model_name']}:\n" + "\n".join(lines)
    return str(data)


@mcp.tool()
async def get_top_models(year: int, limit: int = 5) -> str:
    """Get the top BMW models by average price for a given year.

    Args:
        year: The year to query (e.g. 2019).
        limit: Number of top models to return (default 5).
    """
    data = await _get("/analytics/top-models", {"year": year, "limit": limit})
    if isinstance(data, dict) and "results" in data:
        lines = [
            f"  {i+1}. {r['model_name']} — £{r['average_price']:,.2f}  ({r['num_records']} records)"
            for i, r in enumerate(data["results"])
        ]
        return f"Top {limit} models in {data['year']}:\n" + "\n".join(lines)
    return str(data)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
