import uvicorn
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("app:app", host="127.0.0.1", reload=True, debug=True)
