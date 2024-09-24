import tkinter as tk
from tkinter import messagebox
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

# Function to extract features from a password
def extract_features(password):
    features = {
        'length': len(password),
        'uppercase': sum(1 for c in password if c.isupper()),
        'lowercase': sum(1 for c in password if c.islower()),
        'digits': sum(1 for c in password if c.isdigit()),
        'special': sum(1 for c in password if not c.isalnum()),
    }
    return features

# Train a simple model (you would need a proper dataset for real-world use)
def train_model():
    # This is a very small sample dataset for demonstration purposes
    passwords = [
        "password123", "P@ssw0rd!", "qwerty", "1234567890",
        "StrongP@ssword123!", "WeakPwd", "C0mpl3x!P@ssw0rd"
    ]
    strengths = [0, 1, 0, 0, 1, 0, 1]  # 0 for weak, 1 for strong

    vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))
    X = vectorizer.fit_transform(passwords)
    
    model = RandomForestClassifier()
    model.fit(X, strengths)
    
    return model, vectorizer

# Function to check password strength
def check_password_strength(password, model, vectorizer):
    features = extract_features(password)
    X = vectorizer.transform([password])
    strength = model.predict(X)[0]
    
    if strength == 1:
        return "Strong password"
    else:
        return "Weak password"

class PasswordStrengthCheckerGUI:
    def __init__(self, master):
        self.master = master
        master.title("AI Password Strength Checker")

        self.model, self.vectorizer = train_model()

        self.label = tk.Label(master, text="Enter a password:")
        self.label.pack()

        self.entry = tk.Entry(master, show="*")
        self.entry.pack()

        self.check_button = tk.Button(master, text="Check Strength", command=self.check_strength)
        self.check_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def check_strength(self):
        password = self.entry.get()
        result = check_password_strength(password, self.model, self.vectorizer)
        self.result_label.config(text=result)

        if result == "Weak password":
            tips = "Tips to improve:\n"
            if len(password) < 12:
                tips += "- Make it at least 12 characters long\n"
            if not re.search(r'[A-Z]', password):
                tips += "- Include uppercase letters\n"
            if not re.search(r'[a-z]', password):
                tips += "- Include lowercase letters\n"
            if not re.search(r'\d', password):
                tips += "- Include numbers\n"
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                tips += "- Include special characters\n"
            messagebox.showinfo("Password Strength Tips", tips)

def main():
    root = tk.Tk()
    gui = PasswordStrengthCheckerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

