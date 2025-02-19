import mysql.connector
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(_name_)

# MySQL Connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root@localhost",
    password="ADIAMIT@123",
    database="ai_exam_evaluation"
)
cursor = db.cursor()

# Function to store evaluation results in MySQL
def save_result(student_name, roll_no, score):
    query = "INSERT INTO results (student_name, roll_no, score) VALUES (%s, %s, %s)"
    values = (student_name, roll_no, score)
    cursor.execute(query, values)
    db.commit()

# AI Model: TF-IDF Similarity for Answer Evaluation
def evaluate_answer(model_answer, student_answer):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([model_answer, student_answer])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0] * 100  # Convert to percentage
    return round(similarity, 2)

# API to Evaluate Answers
@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    model_answer = data['model_answer']
    student_answer = data['student_answer']
    student_name = data['student_name']
    roll_no = data['roll_no']

    score = evaluate_answer(model_answer, student_answer)
    save_result(student_name, roll_no, score)

    return jsonify({'student_name': student_name, 'roll_no': roll_no, 'score': score})

# API to Retrieve Results
@app.route('/results', methods=['GET'])
def get_results():
    cursor.execute("SELECT student_name, roll_no, score FROM results")
    data = cursor.fetchall()
    results = [{"student_name": row[0], "roll_no": row[1], "score": row[2]} for row in data]
    return jsonify(results)

if _name_ == '_main_':
    app.run(debug=True)
