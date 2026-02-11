from flask import Flask, render_template, request, redirect, url_for
import PyPDF2
import os

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

questions = []
answers = []

def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global questions, answers

    if request.method == 'POST':
        qp = request.files['question_paper']
        ak = request.files['answer_key']

        qp_path = os.path.join(app.config['UPLOAD_FOLDER'], qp.filename)
        ak_path = os.path.join(app.config['UPLOAD_FOLDER'], ak.filename)

        qp.save(qp_path)
        ak.save(ak_path)

        qp_text = extract_text_from_pdf(qp_path)
        ak_text = extract_text_from_pdf(ak_path)

        questions = qp_text.split("Q.")
        answers = ak_text.split()

        return redirect(url_for('quiz'))

    return render_template('upload.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global questions, answers

    if request.method == 'POST':
        score = 0
        user_answers = request.form.getlist('answer')

        for i in range(len(user_answers)):
            if i < len(answers) and user_answers[i].strip().upper() == answers[i].strip().upper():
                score += 1

        return f"Your Score: {score} / {len(answers)}"

    return render_template('quiz.html', questions=questions[1:])

if __name__ == '__main__':
    app.run()
