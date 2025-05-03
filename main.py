from fastapi import FastAPI

# Create the FastAPI app
app = FastAPI()

# Placeholder test route
@app.get("/")
def read_root():
    return {"message": "Security Headers Analyzer is live"}
# instruct server when entrypoint is run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)