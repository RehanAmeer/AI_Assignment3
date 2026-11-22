import os

from fastmcp import FastMCP

from tools import ALL_TOOLS

mcp = FastMCP("cgpa")

for fn in ALL_TOOLS:
    mcp.tool(fn)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
    )
