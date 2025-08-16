# bug-nonbug-deploy

This project deploys a machine learning model that classifies software issue reports as **Bug** or **Non-Bug**.  
It uses **Flask** for the API and is containerized with **Docker** for portability.  

##  Live Demo

🔗 [Click here to try the live app](https://bug-nonbug-deploy.onrender.com)

You can enter the issue title and description on the homepage to receive a classification: **Bug** or **Non-Bug**.

You can also use the `/predict` endpoint directly:

### POST /predict

**Request Example**:
json
{
  "title": "Submit button crash",
  "description": "App crashes when clicking submit with empty form"
}

{
  "prediction": "Bug"
}
---
This project deploys a machine learning model that classifies software issue reports as **Bug** or **Non-Bug**.  
It uses **Flask** for the API and is containerized with **Docker** for portability.  

---

##  Features
- `/health` → Health check endpoint  
- `/predict` → Predict a single issue report  
- `/predict_batch` → Predict multiple issue reports  
- Simple **HTML frontend** at `/` for quick testing  
- Packaged with **Docker** for easy deployment  

---

##  Project Structure
bug-nonbug-deploy/
├── app/
│ ├── app.py # Main Flask application
│ ├── model/ # Trained model (.pkl)
│ └── templates/
│ └── index.html # Simple UI
├── requirements.txt # Python dependencies
├── Dockerfile # Container setup
└── README.md # Project documentation


##  Setup (Local)

1. **Clone the repo**
   ```bash
2. Create virtual environment & install deps
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
3. Run the app
   python -m app.app
    ##App will be available at → http://127.0.0.1:5000

## Run with Docker

1.Build the image
  docker build -t bug-nonbug:1.0 .
2.Run the container
   docker run --rm --name bugapp \
  -e MODEL_PATH=/app/app/model/bug_classifier_pipeline.pkl \
  -p 8000:5000 bug-nonbug:1.0
  ##App will be available at → http://127.0.0.1:8000

## API Endpoints
➤ Health check
   curl http://127.0.0.1:8000/health
  Response:
   {"status": "ok", "model_loaded": true}
➤ Single prediction
   curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"title": "Submit button crash", "description": "App crashes when clicking submit"}'
 Response:
   {"prediction": "Bug", "confidence": 0.87}
➤ Batch prediction
   curl -X POST http://127.0.0.1:8000/predict_batch \
  -H "Content-Type: application/json" \
  -d '{"items": [{"title": "UI alignment", "description": "Minor text alignment issue"}]}'
Response:
   {"results":[{"index":0,"prediction":"Non-Bug","confidence":0.65}]}
   
## Documentation
  API implemented in app/app.py using Flask
  Simple frontend in app/templates/index.html
  Extendable with Swagger or Postman for more robust API testing

