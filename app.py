from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for simplicity
assessments = {}  # userId -> assessment data

# ---------------------- Career Database ----------------------
careers_db = [
    # ---------------- Technology ----------------
    {
        "name": "Software Developer",
        "category": "Technology",
        "courses": ["Python", "JavaScript", "Algorithms"],
        "skills": ["Coding", "Problem Solving"],
        "improve": "Practice coding challenges daily and contribute to projects.",
        "platforms": ["Coursera", "Udemy", "LeetCode"],
        "roadmap": [
            "Learn programming basics (Python, JavaScript).",
            "Understand data structures and algorithms.",
            "Build projects to apply knowledge.",
            "Learn web/app development frameworks.",
            "Prepare for coding interviews."
        ]
    },
    {
        "name": "Data Scientist",
        "category": "Technology",
        "courses": ["Python", "R", "Statistics", "Machine Learning"],
        "skills": ["Analytical Thinking", "Coding"],
        "improve": "Work on real data projects and Kaggle competitions.",
        "platforms": ["Coursera", "edX", "Kaggle"],
        "roadmap": [
            "Learn Python/R and statistics.",
            "Practice data cleaning and visualization.",
            "Learn machine learning algorithms.",
            "Work on real datasets/projects.",
            "Build portfolio and practice interviews."
        ]
    },
    # ---------------- Design ----------------
    {
        "name": "Graphic Designer",
        "category": "Design",
        "courses": ["Adobe Photoshop", "Figma", "Illustrator"],
        "skills": ["Creativity", "Design Tools"],
        "improve": "Design real projects and build a portfolio.",
        "platforms": ["Udemy", "Coursera", "Skillshare"],
        "roadmap": [
            "Learn design tools (Photoshop, Illustrator, Figma).",
            "Study color theory and typography.",
            "Work on real design projects.",
            "Create a portfolio website.",
            "Apply for internships or freelance projects."
        ]
    },
    {
        "name": "UX/UI Designer",
        "category": "Design",
        "courses": ["UX Design", "Wireframing", "Prototyping"],
        "skills": ["User Research", "Creativity"],
        "improve": "Practice designing user-friendly interfaces.",
        "platforms": ["Coursera", "Interaction Design Foundation", "Udemy"],
        "roadmap": [
            "Learn UX/UI principles.",
            "Practice wireframing and prototyping.",
            "Conduct user research and testing.",
            "Build a portfolio of designs.",
            "Apply for UX/UI roles or freelance work."
        ]
    },
    # ---------------- Business ----------------
    {
        "name": "Marketing Manager",
        "category": "Business",
        "courses": ["Digital Marketing", "SEO", "Analytics"],
        "skills": ["Communication", "Marketing Knowledge"],
        "improve": "Work on marketing campaigns and case studies.",
        "platforms": ["Coursera", "Udemy", "HubSpot Academy"],
        "roadmap": [
            "Learn marketing basics and digital tools.",
            "Practice creating marketing campaigns.",
            "Analyze campaign performance using analytics.",
            "Develop leadership and communication skills.",
            "Apply for marketing roles or start projects."
        ]
    },
    {
        "name": "Business Analyst",
        "category": "Business",
        "courses": ["Excel", "SQL", "Business Analysis"],
        "skills": ["Analytical Thinking", "Communication"],
        "improve": "Work on real business data and case studies.",
        "platforms": ["Coursera", "edX", "Udemy"],
        "roadmap": [
            "Learn data analysis tools (Excel, SQL).",
            "Understand business processes.",
            "Practice analyzing real datasets.",
            "Prepare reports and dashboards.",
            "Apply for business analyst roles."
        ]
    },
    # ---------------- Healthcare ----------------
    {
        "name": "Nurse",
        "category": "Healthcare",
        "courses": ["Nursing Basics", "Patient Care", "Medical Ethics"],
        "skills": ["Caregiving", "Communication"],
        "improve": "Gain practical experience in hospitals or clinics.",
        "platforms": ["Coursera", "edX"],
        "roadmap": [
            "Complete nursing degree/diploma.",
            "Gain clinical experience.",
            "Learn patient care and medical ethics.",
            "Prepare for licensing exams.",
            "Apply for hospital/clinic roles."
        ]
    },
    {
        "name": "Physiotherapist",
        "category": "Healthcare",
        "courses": ["Anatomy", "Physiotherapy Techniques", "Rehabilitation"],
        "skills": ["Caregiving", "Physical Therapy Knowledge"],
        "improve": "Practice therapy sessions under supervision.",
        "platforms": ["Coursera", "Udemy"],
        "roadmap": [
            "Study human anatomy and physiology.",
            "Learn physiotherapy techniques.",
            "Gain hands-on experience with patients.",
            "Get licensed or certified.",
            "Start practice or work in clinics."
        ]
    },
    # ---------------- Education ----------------
    {
        "name": "Teacher",
        "category": "Education",
        "courses": ["Pedagogy", "Subject Knowledge", "Classroom Management"],
        "skills": ["Communication", "Teaching"],
        "improve": "Practice teaching and lesson planning.",
        "platforms": ["Coursera", "edX", "Udemy"],
        "roadmap": [
            "Gain degree in teaching or subject area.",
            "Learn classroom management and pedagogy.",
            "Prepare lesson plans.",
            "Practice teaching in schools or online.",
            "Apply for teaching roles or tutoring."
        ]
    },
    {
        "name": "Educational Consultant",
        "category": "Education",
        "courses": ["Curriculum Development", "Counseling", "Educational Technology"],
        "skills": ["Communication", "Analytical Thinking"],
        "improve": "Work with schools and students to improve learning outcomes.",
        "platforms": ["Coursera", "Udemy"],
        "roadmap": [
            "Understand curriculum and educational standards.",
            "Learn counseling and guidance methods.",
            "Practice educational technology tools.",
            "Advise students and institutions.",
            "Build consulting experience and portfolio."
        ]
    }
]

# ---------------------- Page Routes ----------------------
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/assessment')
def assessment_page():
    return render_template('career-assessment.html')

@app.route('/career-result.html')
def result_page():
    return render_template('career-result.html')

@app.route('/career-roadmap.html')
def roadmap_page():
    return render_template('career-roadmap.html')

# ---------------------- API Routes ----------------------
@app.route('/save-assessment', methods=['POST'])
def save_assessment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    user_id = str(len(assessments) + 1)  # simple unique ID
    assessments[user_id] = data
    return jsonify({"userId": user_id})

@app.route('/get-careers')
def get_careers():
    user_id = request.args.get("user_id")
    if not user_id or user_id not in assessments:
        return jsonify({"error": "User assessment not found"}), 404

    assessment = assessments[user_id]
    interest = assessment.get("interest")

    # Filter careers by category
    filtered_careers = [c for c in careers_db if c["category"] == interest]

    response = {
        "userId": user_id,
        "interest": interest,
        "weakSubject": assessment.get("weakSubject"),
        "skills": assessment.get("skills"),
        "personality": assessment.get("personality"),
        "careers": filtered_careers
    }
    return jsonify(response)

@app.route('/get-roadmap')
def get_roadmap():
    user_id = request.args.get("user_id")
    career_name = request.args.get("career_name")
    if not user_id or user_id not in assessments:
        return jsonify({"error": "User assessment not found"}), 404

    career = next((c for c in careers_db if c["name"] == career_name), None)
    if not career:
        return jsonify({"error": "Career not found"}), 404

    return jsonify({"roadmap": career["roadmap"]})

# ---------------------- Run Server ----------------------
if __name__ == "__main__":
    app.run(debug=True)