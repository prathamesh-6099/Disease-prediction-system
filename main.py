import os
import pickle
import streamlit as st
import requests
import feedparser
from streamlit_option_menu import option_menu
import google.generativeai as genai
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide", page_icon="🧑‍⚕️")

base_dir = os.path.dirname(os.path.abspath(__file__))

# Load disease prediction models
diabetes_model = pickle.load(open(os.path.join(base_dir, "diabetes_model.sav"), 'rb'))
heart_disease_model = pickle.load(open(os.path.join(base_dir, "heart_disease_model.sav"), 'rb'))
parkinsons_model = pickle.load(open(os.path.join(base_dir, "parkinsons_model.sav"), 'rb'))
parkinsons_model = pickle.load(open(os.path.join(base_dir, "parkinsons_model.sav"), 'rb'))
css_path = os.path.join(base_dir, "styles.css")

st.markdown("<style> " + open(css_path).read() + " </style>", unsafe_allow_html=True)

# Function to fetch recent healthcare articles in Hindi from RSS feeds


def get_health_articles():
    feeds = [
        "https://www.healthshots.com/hindi/rss-feeds/health-news/",
        "https://www.prabhasakshi.com/rss/health"
    ]
    articles = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            # Fetch top 5 articles from each feed
            for entry in feed.entries[:5]:
                title = entry.title
                link = entry.link
                articles.append((title, link))
        except Exception as e:
            st.error(f"Error fetching articles from {url}: {e}")
    return articles if articles else [("No articles found", "#")]

# Function to extract text from an article


def get_article_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        article_text = " ".join([para.get_text() for para in paragraphs])
        return article_text if article_text else "No meaningful text found."
    except Exception as e:
        return f"Error fetching article content: {e}"

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Multiple Disease Prediction System",
        ["General Assistance",
         "Ayurveda and Remedies",
         "Insightful Answers",
         "Diabetes Prediction",
         "Heart Disease Prediction",
         "Parkinson's Prediction",
         "Health News in Hindi"],
        menu_icon='hospital-fill',
        icons=['chat-right-heart', 'feather2', 'lightbulb',
               'activity', 'heart', 'person', 'newspaper'],
        default_index=0
    )

# Health News Section
if selected == "Health News in Hindi":
    st.title("📰 Latest Healthcare News in Hindi")
    articles = get_health_articles()

    for title, link in articles:
        if link != "#":
            st.markdown(f"### [{title}]({link})")

# General Assistance Chatbot
if selected == "General Assistance":
    st.title("💬 Healthcare Chatbot")
    st.write("Ask me anything about health!")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=os.getenv("API_KEY"))
# Suggested questions
    suggested_questions = [
        "What are the symptoms of diabetes?",
        "How can I prevent heart disease?",
        "What are the early signs of Parkinson's?",
        "How do I manage high blood pressure?",
        "What are the risk factors for breast cancer?",
    ]


# Display suggested questions as clickable buttons
    st.write("### Suggested Questions:")
    selected_question = st.radio("", suggested_questions, index=None)

# Input field with autofill when a suggestion is selected
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""

    if selected_question:
        st.session_state.user_question = selected_question

    user_input = st.text_input(
        "Your Question:", st.session_state.user_question, key="general_assistance_input")

    ask = st.button("Ask", key="general_ask")

    if ask:
        st.write(
            f"🧑‍⚕️ **Chatbot:** Here is the response to your question: _'{user_input}'_")
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("Answer in 200 words: " + str(user_input))
        st.success(response.text)

# Ayurveda Chatbot
if selected == "Ayurveda and Remedies":
    st.title("Traditional Cures")
    st.write("Gives Home Remedies for Symptoms!")
    genai.configure(api_key=os.getenv("API_KEY"))

# Suggested questions
    suggested_questions = [
        "Cough",
        "Sore Throat",
        "Indigestion",
        "Rashes",
        "Insomnia",
        "Acidity"
    ]


# Display suggested questions as clickable buttons
    st.write("### Suggested Questions:")
    selected_question = st.radio("", suggested_questions, index=None)

# Input field with autofill when a suggestion is selected
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""

    if selected_question:
        st.session_state.user_question = selected_question

    user_input = st.text_input(
        "Your symptom(s):", st.session_state.user_question, key="ayurveda_remedies_input")

    ask = st.button("Ask", key="ayurveda_ask")

    if ask:
        st.write(
            f"🧑‍⚕️ **Chatbot:** Here is some home remedies for your relief from {user_input}")
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            "With no further explanation, list ayurvedic or traditional Indian home remedies for " + str(user_input))
        st.success(response.text)

# Insightful Chatbot
if selected == "Insightful Answers":
    st.title("Ask Me More Abstract Questions for Health")
    st.write("When Wisdom is More Required than Intelligence")
    genai.configure(api_key=os.getenv("API_KEY"))
# Suggested questions
    suggested_questions = [
        'Which diet plans are the most beneficial for overall health?',
        'Yoga vs. Gym – which is better for long-term health?',
        'Which Ayurvedic and allopathic treatments can work effectively together?',
        'What is the latest healthcare technology that is most effective?',
        'What daily habits should be included for a healthier lifestyle?'
    ]


# Display suggested questions as clickable buttons
    st.write("### Suggested Questions:")
    selected_question = st.radio("", suggested_questions, index=None)

# Input field with autofill when a suggestion is selected
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""

    if selected_question:
        st.session_state.user_question = selected_question

    user_input = st.text_input(
        "Your Question:", st.session_state.user_question, key="insightful_questions_input")

    ask = st.button("Ask", key="insightful_ask")

    if ask:
        st.write(
            f"🧑‍⚕️ **Chatbot:** To answer your question: _'{user_input}'_")
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            "Provide a wise, analytical, insightful answer for the question of less than 4 paragraphs: " + str(user_input))
        st.success(response.text)

# Diabetes Prediction
if selected == "Diabetes Prediction":
    st.title("🩸 Diabetes Prediction")
    col1, col2 = st.columns(2)

    with col1:
        Pregnancies = st.slider("Number of Pregnancies", 0, 15, 1)
        Glucose = st.slider("Glucose Level", 50, 200, 100)
        BloodPressure = st.slider("Blood Pressure", 50, 150, 80)

    with col2:
        SkinThickness = st.slider("Skin Thickness", 5, 50, 20)
        Insulin = st.slider("Insulin Level", 0, 300, 100)
        BMI = st.slider("BMI", 10.0, 50.0, 25.0)

    DiabetesPedigreeFunction = st.number_input(
        "Diabetes Pedigree Function", value=0.5, format="%.2f")
    Age = st.number_input("Age", min_value=1, max_value=120, value=30)

    if st.button("Predict Diabetes"):
        user_input = [Pregnancies, Glucose, BloodPressure,
                      SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        result = diabetes_model.predict([user_input])
        st.success("Diabetic" if result[0] == 1 else "Not Diabetic")

# Heart Disease Prediction
if selected == "Heart Disease Prediction":
    st.title("❤️ Heart Disease Prediction")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    if st.button("Predict Heart Disease"):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        result = heart_disease_model.predict([user_input])
        st.success(
            "Heart Disease Detected" if result[0] == 1 else "No Heart Disease")

# Parkinson's Prediction
if selected == "Parkinson's Prediction":
    st.title("🧠 Parkinson's Disease Prediction")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    if st.button("Predict Parkinson's"):
        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                      RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
        result = parkinsons_model.predict([user_input])
        st.success("Has Parkinson's" if result[0] == 1 else "No Parkinson's")