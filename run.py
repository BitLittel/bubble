import uvicorn
import main


uvicorn.run(main.main, port=8000, host='127.0.0.1', use_colors=True, workers=2)
