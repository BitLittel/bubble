import uvicorn
import main


uvicorn.run(main.main, port=8000, host='0.0.0.0', use_colors=True)
