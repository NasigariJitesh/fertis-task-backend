### Create a virtual env
    python -m venv venv
    
### Activate virtual env
    source venv/bin/activate

### Install dependencies
    pip install -r requirements.txt

### Start the server
    uvicorn server.main:app --reload --host 0.0.0.0 --port 9000

