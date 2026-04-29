from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from backend.preprocessing import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"


HAM_MESSAGES = [
    ("ham", "Hey, are we still meeting for lunch tomorrow?"),
    ("ham", "Please review the attached project notes when you have time."),
    ("ham", "Your invoice for March has been paid successfully."),
    ("ham", "Can you send me the presentation before the client call?"),
    ("ham", "Reminder: team sync starts at 10 AM in the main conference room."),
    ("ham", "Thanks for your help today. I really appreciate it."),
    ("ham", "The package has been delivered to your front desk."),
    ("ham", "Let's reschedule the demo to Friday afternoon."),
    ("ham", "Your appointment is confirmed for next Tuesday."),
    ("ham", "I updated the shared document with the latest numbers."),
    ("ham", "Dinner was great yesterday. Let's do it again soon."),
    ("ham", "The weekly report is ready for your review."),
    ("ham", "Can you approve the leave request in the portal?"),
    ("ham", "The build passed and the deployment is complete."),
    ("ham", "Here are the meeting minutes from today's planning session."),
    ("ham", "Your password was changed successfully."),
    ("ham", "Please find the receipt for your recent purchase attached."),
    ("ham", "I will be out of office on Monday."),
    ("ham", "The interview panel feedback has been uploaded."),
    ("ham", "Could you share your availability for next week?"),
    ("ham", "The maintenance window is scheduled for Saturday night."),
    ("ham", "Your subscription renewal reminder is due next month."),
    ("ham", "The class assignment deadline has been extended."),
    ("ham", "Thanks for registering for the webinar."),
    ("ham", "The quarterly budget spreadsheet is in the drive folder."),
    ("ham", "Your flight itinerary has been updated with the new gate number."),
    ("ham", "The support ticket has been resolved and closed."),
    ("ham", "Please sign the contract draft before end of day."),
    ("ham", "The server migration checklist is ready for approval."),
    ("ham", "I added comments to the design review document."),
    ("ham", "Your order confirmation is attached for your records."),
    ("ham", "The dentist appointment reminder is for 4 PM tomorrow."),
    ("ham", "We received your application and will respond next week."),
    ("ham", "The payment receipt for your booking is available online."),
    ("ham", "Can you join the standup call five minutes early?"),
    ("ham", "Your monthly statement is now available in the customer portal."),
    ("ham", "Please update the onboarding checklist after the training session."),
    ("ham", "The client approved the revised homepage copy."),
    ("ham", "I shared the calendar invite for the product review."),
    ("ham", "The database backup completed successfully last night."),
    ("ham", "Your library books are due next Friday."),
    ("ham", "The conference registration badge is ready for pickup."),
    ("ham", "Please send the signed NDA to the legal team."),
    ("ham", "The office Wi-Fi password changed this morning."),
    ("ham", "Your lab results are available in the patient portal."),
]

SPAM_MESSAGES = [
    ("spam", "Congratulations! You have won a free iPhone. Claim now."),
    ("spam", "URGENT: Your account has been suspended. Verify immediately."),
    ("spam", "You are selected for a $5000 cash prize. Click this link."),
    ("spam", "Limited time offer! Buy now and get 90% discount."),
    ("spam", "Earn money fast from home with no experience required."),
    ("spam", "Act now to receive your exclusive lottery winnings."),
    ("spam", "Your bank account needs verification. Send your password."),
    ("spam", "Win a brand new car today. Reply with your details."),
    ("spam", "Lowest price pills available without prescription."),
    ("spam", "Claim your free gift card before midnight."),
    ("spam", "Final notice: pay now to avoid account closure."),
    ("spam", "Get rich quickly with this secret investment trick."),
    ("spam", "Hot deal! Free vacation package waiting for you."),
    ("spam", "You have been pre-approved for an instant loan."),
    ("spam", "Click here to remove virus from your device now."),
    ("spam", "Your parcel is blocked. Pay a small fee to release it."),
    ("spam", "Double your bitcoin in 24 hours guaranteed."),
    ("spam", "Exclusive reward unlocked. Confirm identity to receive cash."),
    ("spam", "Free entry in our weekly prize draw. Text WIN now."),
    ("spam", "Cheap insurance quote available only today."),
    ("spam", "Make thousands per week using your phone."),
    ("spam", "Important security alert. Login using this link."),
    ("spam", "You've won bonus credit. Activate your reward."),
    ("spam", "No credit check payday loan approved instantly."),
    ("spam", "Secret shopper job pays $800 weekly. Apply now."),
    ("spam", "Immediate action required to unlock your frozen bank account."),
    ("spam", "Claim free crypto bonus by entering your wallet password."),
    ("spam", "Winner alert! Collect your cash reward with one click."),
    ("spam", "Your device is infected. Download this cleaner immediately."),
    ("spam", "Flash sale for miracle weight loss tablets ends tonight."),
    ("spam", "Confirm your social security number to avoid legal action."),
    ("spam", "Exclusive casino bonus waiting in your account."),
    ("spam", "Guaranteed approval for debt relief funds today."),
    ("spam", "Your email address won a lottery prize transfer."),
    ("spam", "Click to receive a free premium subscription forever."),
    ("spam", "Suspicious login detected. Verify billing details now."),
    ("spam", "Government grant approved. Pay processing fee to claim."),
    ("spam", "Free coupons available only to selected users."),
    ("spam", "Urgent refund pending. Provide bank details immediately."),
    ("spam", "Special investment doubles your money with zero risk."),
    ("spam", "Reactivate your mailbox by sharing your password."),
    ("spam", "You qualify for a limited cash bonus today."),
    ("spam", "Final warning: your antivirus has expired. Click repair."),
    ("spam", "Get paid instantly for forwarding this message."),
    ("spam", "Prize department needs your identity confirmation."),
]

TRAINING_DATA = HAM_MESSAGES + SPAM_MESSAGES


def build_dataset() -> pd.DataFrame:
    return pd.DataFrame(TRAINING_DATA, columns=["label", "message"])


def train_model() -> tuple[Pipeline, float, str]:
    data = build_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        data["message"],
        data["label"],
        test_size=0.2,
        random_state=42,
        stratify=data["label"],
    )

    model = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=clean_text,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=1,
                ),
            ),
            ("classifier", MultinomialNB(alpha=0.4)),
        ]
    )

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    return model, accuracy, report


def main() -> None:
    model, accuracy, report = train_model()
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")
    print(f"Accuracy: {accuracy:.4f}")
    print(report)


if __name__ == "__main__":
    main()
