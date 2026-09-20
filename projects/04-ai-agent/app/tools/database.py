from app.tools.base import BaseTool


class DatabaseLookupTool(BaseTool):
    """Database query tool (placeholder).

    TODO: Integrate a real database connection:
    - SQL: SQLAlchemy with async support
    - NoSQL: motor (MongoDB), redis

    Example integration:
        from sqlalchemy.ext.asyncio import create_async_engine
        engine = create_async_engine(settings.DATABASE_URL)

        async with engine.connect() as conn:
            result = await conn.execute(text(query))
            return result.fetchall()
    """

    @property
    def name(self) -> str:
        return "database_lookup"

    @property
    def description(self) -> str:
        return (
            "Queries a database for information. "
            "Input should be a natural language question about the data."
        )

    def execute(self, query: str = "", **kwargs) -> dict:
        """Execute a database query.

        TODO: Replace with real database integration.
        Consider:
        - Natural language to SQL conversion
        - Query validation and sanitization
        - Read-only access for safety
        """
        # Mock response for testing
        return {
            "query": query,
            "columns": ["id", "name", "value"],
            "rows": [
                {"id": 1, "name": "Mock Entry 1", "value": 100},
                {"id": 2, "name": "Mock Entry 2", "value": 200},
            ],
            "row_count": 2,
            "note": "This is mock data. Integrate a real database connection.",
        }
