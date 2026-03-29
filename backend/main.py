from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserData(BaseModel):
    income: float
    expenses: float
    savings: float
    goal: str

@app.get("/")
def home():
    return {"message": "AI Money Mentor Backend Running"}

@app.post("/analyze")
def analyze(data: UserData):
    savings_rate = (data.income - data.expenses) / data.income

    score = int(savings_rate * 100)
    score = max(0, min(score, 100))

    # AI-style personalized response
    if score < 30:
        advice = f"""
⚠️ Financial Risk Detected

You are spending more than you save. This may lead to financial stress.

Recommendations:
- Reduce unnecessary expenses
- Build an emergency fund (₹{int(data.income * 3)})
- Avoid loans/credit dependency
"""
    elif score < 60:
        advice = f"""
🟡 Moderate Financial Health

You're managing okay but missing growth opportunities.

Recommendations:
- Start SIP of ₹{int(data.income * 0.15)}
- Track monthly expenses
- Increase savings gradually
"""
    else:
        advice = f"""
🟢 Strong Financial Health

Great job! You're financially disciplined.

Recommendations:
- Diversify investments (stocks, mutual funds)
- Increase SIP to ₹{int(data.income * 0.25)}
- Plan long-term wealth creation
"""

    return {
        "score": score,
        "advice": advice,
        "goal_plan": f"🎯 To achieve {data.goal}, invest ₹{int(data.income * 0.2)} per month."
    }