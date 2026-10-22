from flask import Flask, render_template, request
import os

app = Flask(__name__)

INBOX_FOLDER = "inbox"
SPAM_FOLDER = "spam_folder"

os.makedirs(INBOX_FOLDER, exist_ok=True)
os.makedirs(SPAM_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    inbox_file = os.path.join(INBOX_FOLDER, "normal_email.txt")
    spam_file = os.path.join(SPAM_FOLDER, "spam_email.txt")

    if request.method == "POST":

        sender = request.form["sender"]
        subject = request.form["subject"]
        email = request.form["email"]

        # Spam words
        spam_words = [
            "win", "winner", "prize", "free",
            "money", "offer", "lottery", "click",
            "urgent", "congratulations"
        ]

        # Sender + Subject + Message check
        complete_email = sender + " " + subject + " " + email
        complete_email = complete_email.lower()

        # Spam score
        score = 0

        for word in spam_words:
            if word in complete_email:
                score += 1

        # 2 ya usse zyada spam words = Spam
        if score >= 2:

            result = "🚨 This email is SPAM"

            file_path = spam_file

        else:

            result = "✅ This email is NOT SPAM"

            file_path = inbox_file

        # Email save karo
        with open(file_path, "a", encoding="utf-8") as file:

            file.write("From: " + sender + "\n")
            file.write("Subject: " + subject + "\n")
            file.write("Message: " + email + "\n")
            file.write("-" * 50 + "\n")


    # Inbox count
    inbox_count = 0

    if os.path.exists(inbox_file):

        with open(inbox_file, "r", encoding="utf-8") as file:
            inbox_count = file.read().count("From:")


    # Spam count
    spam_count = 0

    if os.path.exists(spam_file):

        with open(spam_file, "r", encoding="utf-8") as file:
            spam_count = file.read().count("From:")


    return render_template(
        "index.html",
        result=result,
        inbox_count=inbox_count,
        spam_count=spam_count
    )


@app.route("/inbox")
def inbox():

    emails = ""

    file_path = os.path.join(
        INBOX_FOLDER,
        "normal_email.txt"
    )

    if os.path.exists(file_path):

        with open(file_path, "r", encoding="utf-8") as file:
            emails = file.read()

    return render_template(
        "inbox.html",
        emails=emails
    )


@app.route("/spam")
def spam():

    emails = ""

    file_path = os.path.join(
        SPAM_FOLDER,
        "spam_email.txt"
    )

    if os.path.exists(file_path):

        with open(file_path, "r", encoding="utf-8") as file:
            emails = file.read()

    return render_template(
        "spam.html",
        emails=emails
    )


if __name__ == "__main__":
    app.run(debug=True)