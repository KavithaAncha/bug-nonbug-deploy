from flask import Flask, request, jsonify, render_template
import joblib, os

app = Flask(__name__)
MODEL_PATH = os.getenv("MODEL_PATH", "app/model/bug_classifier_pipeline.pkl")
model = joblib.load(MODEL_PATH)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok", model_loaded=True), 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    title = data.get("title", "")
    description = data.get("description", "")
    text = f"{title}\n\n{description}".strip()

    pred = model.predict([text])[0]
    proba = None
    if hasattr(model, "predict_proba"):
        proba = float(max(model.predict_proba([text])[0]))

    return jsonify({"prediction": pred, "confidence": proba}), 200

@app.route("/predict:batch", methods=["POST"])
def predict_batch():
    data = request.get_json(force=True)
    items = data.get("items", [])
    results = []
    for i, item in enumerate(items):
        title = item.get("title", "")
        description = item.get("description", "")
        text = f"{title}\n\n{description}".strip()
        pred = model.predict([text])[0]
        proba = None
        if hasattr(model, "predict_proba"):
            proba = float(max(model.predict_proba([text])[0]))
        results.append({"index": i, "prediction": pred, "confidence": proba})
    return jsonify({"results": results}), 200

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
