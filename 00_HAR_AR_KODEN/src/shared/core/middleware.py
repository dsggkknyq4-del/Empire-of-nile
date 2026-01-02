from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List

class GeoBlockMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, blocked_countries: List[str] = None):
        super().__init__(app)
        self.blocked_countries = blocked_countries or []

    async def dispatch(self, request: Request, call_next):
        # Simulation of GeoIP. In real prod, use a DB or Nginx header.
        # Here we look for a header "X-Country-Code" which might be set by a load balancer.
        country = request.headers.get("X-Country-Code", "US") # Default to US
        
        if country in self.blocked_countries:
            return await self.block_request()
            
        return await call_next(request)

    async def block_request(self):
        # We raise HTTPException effectively by returning a Response since we can't easily raise from middleware dispatch
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Access restricted in your region."}
        )
