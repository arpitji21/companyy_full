from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_active_user


def make_placeholder_router(prefix: str, tag: str, phase_note: str) -> APIRouter:
    """
    Creates a router that is wired into the app (correct prefix/tags/auth)
    but whose endpoints are not yet implemented. This lets the frontend
    point at the final URL shape now, and keeps main.py's route table
    matching the full API design from day one, without pretending modules
    are done that aren't.
    """
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.get("", summary=f"[Not yet implemented] {tag} overview")
    def not_implemented(_=Depends(get_current_active_user)):
        return {
            "status": "not_implemented",
            "module": tag,
            "message": f"{tag} endpoints are scaffolded but not built yet. {phase_note}",
        }

    return router
