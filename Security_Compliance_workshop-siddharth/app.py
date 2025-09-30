import subprocess
from flask import Flask, request, render_template_string
import requests
import sqlite3

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret key (will be detected by Gitleaks and Semgrep)
app.config['SECRET_KEY'] = 'supersecret123'


# VULNERABILITY 2: SQL Injection vulnerability (will be detected by Bandit and Semgrep)
def get_user_by_id(user_id):
    conn = sqlite3.connect('app.db')
    query = "SELECT * FROM users WHERE id = '%s'" % user_id  # Unsafe string formatting
    cursor = conn.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result


# VULNERABILITY 3: Command injection (will be detected by Bandit)
@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        ip = request.form.get('ip', '')
        # Dangerous: direct execution of user input
        command = f"ping -c 3 {ip}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"<h1>Ping Results</h1><pre>{result.stdout}</pre>"

    return """
    <form method="POST">
        <input type="text" name="ip" placeholder="Enter IP address">
        <input type="submit" value="Ping">
    </form>
    """


# VULNERABILITY 4: XSS vulnerability (will be detected by static analysis)
@app.route('/')
def index():
    name = request.args.get('name', 'World')
    # Unsafe template rendering - no escaping
    return render_template_string(f'<h1>Hello, {name}!</h1>')


# VULNERABILITY 5: Debug mode enabled (will be detected by Bandit)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
