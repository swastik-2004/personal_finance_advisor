import pandas as pd
import joblib
import os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

TRAINING_DATA = [
    # Food
    ("grocery run at walmart", "Food"),
    ("whole foods grocery", "Food"),
    ("supermarket shopping", "Food"),
    ("lunch at restaurant", "Food"),
    ("dinner out with family", "Food"),
    ("coffee shop latte", "Food"),
    ("pizza delivery order", "Food"),
    ("food delivery swiggy", "Food"),
    ("zomato food order", "Food"),
    ("bakery purchase", "Food"),
    ("vegetable market", "Food"),
    ("meat and dairy groceries", "Food"),
    ("fast food burger", "Food"),
    ("breakfast cafe", "Food"),
    ("weekly grocery run", "Food"),
    # Rent
    ("monthly rent payment", "Rent"),
    ("house rent due", "Rent"),
    ("apartment rent", "Rent"),
    ("rent paid to landlord", "Rent"),
    ("room rent transfer", "Rent"),
    ("housing rent", "Rent"),
    ("flat rent monthly", "Rent"),
    # Travel
    ("uber ride to office", "Travel"),
    ("lyft airport pickup", "Travel"),
    ("flight ticket booking", "Travel"),
    ("airbnb hotel stay", "Travel"),
    ("taxi cab fare", "Travel"),
    ("train ticket purchase", "Travel"),
    ("bus pass recharge", "Travel"),
    ("fuel petrol station", "Travel"),
    ("gas station fill up", "Travel"),
    ("metro card recharge", "Travel"),
    ("cab to airport", "Travel"),
    ("road trip fuel", "Travel"),
    # Shopping
    ("amazon online purchase", "Shopping"),
    ("flipkart order delivery", "Shopping"),
    ("clothing store shirt", "Shopping"),
    ("shoe purchase nike", "Shopping"),
    ("electronics gadget buy", "Shopping"),
    ("mall shopping spree", "Shopping"),
    ("online shopping order", "Shopping"),
    ("new laptop purchase", "Shopping"),
    ("mobile phone accessories", "Shopping"),
    ("fashion outlet clothes", "Shopping"),
    # Health
    ("doctor consultation fee", "Health"),
    ("pharmacy medicine purchase", "Health"),
    ("gym membership monthly", "Health"),
    ("dental checkup appointment", "Health"),
    ("hospital bill payment", "Health"),
    ("health insurance premium", "Health"),
    ("medical test lab fee", "Health"),
    ("eye checkup glasses", "Health"),
    ("vitamin supplements pharmacy", "Health"),
    # Entertainment
    ("netflix subscription monthly", "Entertainment"),
    ("spotify premium music", "Entertainment"),
    ("movie tickets cinema", "Entertainment"),
    ("concert event tickets", "Entertainment"),
    ("youtube premium subscription", "Entertainment"),
    ("gaming purchase steam", "Entertainment"),
    ("streaming service renewal", "Entertainment"),
    ("amusement park entry", "Entertainment"),
    ("book purchase fiction", "Entertainment"),
    # Utilities
    ("electricity bill payment", "Utilities"),
    ("water bill monthly", "Utilities"),
    ("internet broadband bill", "Utilities"),
    ("phone mobile bill", "Utilities"),
    ("gas utility bill", "Utilities"),
    ("wifi bill payment", "Utilities"),
    ("cable tv subscription", "Utilities"),
    ("postpaid mobile recharge", "Utilities"),
    # Other
    ("miscellaneous expense", "Other"),
    ("cash withdrawal atm", "Other"),
    ("bank transfer payment", "Other"),
    ("unknown transaction", "Other"),
    ("general purchase", "Other"),
]

def train_classifier():
    df = pd.DataFrame(TRAINING_DATA, columns=["description", "category"])

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ('clf', LogisticRegression(max_iter=1000, random_state=42))
    ])
    pipeline.fit(df["description"], df["category"])

    joblib.dump(pipeline, os.path.join(MODEL_DIR, "classifier.pkl"))
    print(f"Classifier trained on {len(df)} samples and saved.")

if __name__ == "__main__":
    train_classifier()
