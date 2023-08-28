import uvicorn
import main

# git ls-files | grep '\.py' | xargs wc -l
uvicorn.run(main.main, port=8000, host='0.0.0.0', use_colors=True)
