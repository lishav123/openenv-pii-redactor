import uvicorn
from openenv_core.env_server import create_fastapi_app

# Robust imports to handle both direct execution and module execution
try:
    from server.environment import PiiRedactorEnvironment
    from models import PiiRedactorAction, PiiRedactorObservation
except (ImportError, ValueError):
    from .environment import PiiRedactorEnvironment
    from ..models import PiiRedactorAction, PiiRedactorObservation

# Pass the CLASS directly (no parentheses!), not an instance
app = create_fastapi_app(PiiRedactorEnvironment, PiiRedactorAction, PiiRedactorObservation)

# uv run server looks for this exact main() function
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()