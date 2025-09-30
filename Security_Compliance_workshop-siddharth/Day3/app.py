from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

# Hardcoded secret - Gitleaks should find this
API_KEY = "sk_abcdefghijklmnopqrstuvwxyz1234567890"

# Insecure dependency (vulnerable version of Flask) is in requirements.txt

@app.route('/')
def home():
    return "Welcome to the Vulnerable Flask App!"

# Insecure Code (Command Injection) - Bandit and Semgrep should find this
@app.route('/file')
def get_file():
    filename = request.args.get('name', 'test.txt')
    # Vulnerable to command injection
    subprocess.call(f"cat {filename}", shell=True)
    return f"Contents of {filename} displayed."

if __name__ == '__main__':
    # Use port 8080 as a common practice in cloud environments
    app.run(debug=False, host='0.0.0.0', port=8080)