from app import create_app

app = create_app()
import requests
import random

if __name__ == "__main__":
    with app.app_context():
        requests.put("http://localhost:5000/processing/1", json={
            "layers":[1, 3, 7],
            "output": [random.random()*2 for _ in range(10)]
        })
