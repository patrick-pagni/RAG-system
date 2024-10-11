from flask import Flask, render_template, request
import re
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/simple', methods=["GET", "POST"])
def simple():
    question = None
    response = None

    if request.method == "POST":
        question = request.form.get("input_text")

        try:
            result = subprocess.run(
                ['python', 'code/run.py', question],
                capture_output=True,
                text=True
            )

            response = re.sub(
                r"(/[\w-]+)+\n",
                "",
                result.stdout
            )

        except Exception as e:
            response = f"An error occurred: {e}"

    return render_template("simple.html", entered_text = question, script_output = response)

@app.route("/advanced", methods = ["GET", "POST"])
def advanced():
    return render_template("advanced.html")

if __name__ == "__main__":
    app.run(debug=True)