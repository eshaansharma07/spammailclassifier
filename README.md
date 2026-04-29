# Spam Mail Classifier

A production-ready full-stack web app that classifies email messages as **Spam** or **Not Spam** using a Python machine learning backend and a modern React frontend.

## Folder Structure

```text
spam-classifier/
├── api/
│   └── index.py
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── model.pkl
│   ├── preprocessing.py
│   ├── requirements.txt
│   └── train.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── components/
│   │   │   └── ResultCard.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   └── tailwind.config.js
├── .gitignore
├── package.json
├── README.md
├── vercel.json
└── requirements.txt
```

## Features

- TF-IDF vectorization with Multinomial Naive Bayes
- Text preprocessing with lowercase normalization and punctuation removal
- FastAPI backend with CORS enabled
- `POST /predict` API with prediction, confidence, and top important words
- React + Tailwind CSS frontend
- Dark theme, animated gradient actions, loading states, and error handling

## Screenshots

Add screenshots here after deployment:

![Home screen placeholder](docs/screenshots/home.png)
![Result screen placeholder](docs/screenshots/result.png)

## Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..
python -m backend.train
cd backend
uvicorn main:app --reload
```

The API will run at:

```text
http://localhost:8000
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app will run at:

```text
http://localhost:5173
```

To point the frontend to a deployed backend, create `frontend/.env.local`:

```bash
VITE_API_URL=https://your-backend-url.example.com
```

## API Usage

### Request

```http
POST /predict
Content-Type: application/json
```

```json
{
  "message": "Congratulations, you won a free prize. Claim now!"
}
```

### Response

```json
{
  "prediction": "spam",
  "confidence": 0.9421,
  "important_words": ["claim", "free", "prize"]
}
```

## Deployment Notes

The project includes `api/index.py` and `vercel.json` so Vercel can serve the React frontend and route `/predict` plus `/health` to the FastAPI app.

For local frontend-only deployment against a separate backend, add:

```text
VITE_API_URL=<your deployed FastAPI backend URL>
```

For the included same-origin Vercel setup, no `VITE_API_URL` is required.

## GitHub

Target repository:

```text
https://github.com/eshaansharma07/spammailclassifier
```
