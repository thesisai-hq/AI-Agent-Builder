"""Application entry point"""

import uvicorn
from agent_builder.api.app import create_app
from agent_builder.core.config import Config

if __name__ == "__main__":
    config = Config.from_env()
    app = create_app(config)
    
    print(f"🚀 Starting AI Agent Builder API")
    print(f"   Server: {config.host}:{config.port}")
    print(f"   Docs: http://localhost:{config.port}/docs")
    
    uvicorn.run(app, host=config.host, port=config.port, log_level="info")
