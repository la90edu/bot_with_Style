
import streamlit as st
import base64
from pathlib import Path
from questions2 import questions  # ייבוא השאלות מקובץ חיצוני
import time
import gd
import llm
import pathlib
from PIL import Image
# פונקציה להמרת תמונה ל-base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# המרת התמונה ל-base64
try:
    img_base64 = img_to_base64("mop_logo.jpg")
    avatar_img = f"data:image/jpeg;base64,{img_base64}"
except Exception as e:
    avatar_img = ""

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap');
    
    .main-title {
        font-family: 'Rubik', sans-serif;
        font-size: 36px;
        font-weight: 700;
        color: #1E88E5;
        text-align: right;
        padding: 20px 0;
        direction: rtl;
    }
    
    .chat-message {
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        display: flex;
        flex-direction: row;
        width: fit-content;
        max-width: 80%;
    }
    
    .user-message {
        background: #E3F2FD;
        border-radius: 15px;
        margin-left: 0;
        margin-right: auto;
        direction: rtl;
    }
    
    .bot-message {
        margin-left: auto;
        margin-right: 0;
        direction: rtl;
        display: flex;
        align-items: center;  /* מיישר את התוכן אנכית במרכז */
    }
    
    .message-text {
        font-family: 'Rubik', sans-serif;
        font-size: 16px;
        margin: 0;
    }
    
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-left: 10px;
        object-fit: cover;
    }
    
    .message-content {
        display: flex;
        flex-direction: column;
    }
    
    .timestamp {
        font-size: 12px;
        color: #666;
        margin-top: 4px;
    }
    
    .stButton button {
    direction: rtl;
    text-align: right;
    background-color: rgb(0, 110, 184, 0.8);
    border: 1px solid rgba(250, 250, 250, 0);
    color: white;
    padding: 0.5em 1em;
    border-radius: 8px;
    font-size: 1em;
    cursor: pointer;
    text-align: center;
    display: inline-block;
    text-decoration: none;
}

.stButton button:hover{
    background-color: rgb(0, 110, 184);
    color: white;
    border: 1px solid rgb(38, 39, 48);
}


.stTextInput input {
    background-color: rgb(165, 221, 234); 
    color: black; 
    border: 1px solid rgba(0, 110, 184, 0.8); /
    padding: 10px; 
}

/* יישור טקסט בתוך selectbox */
.stSelectbox div[role="combobox"] {
    direction: rtl;
    text-align: right;
    }
    
body, .css-1aumxhk, .stSelectbox > div {
        direction: rtl;
        text-align: right;
    }

    </style>
    """,
    unsafe_allow_html=True
)

def display_user_message(text):
    st.markdown(f"""
    <div class="chat-message user-message">
        <div class="message-content">
            <p class="message-text">{text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
def display_bot_message(text):
    st.markdown(f"""
    <div class="chat-message bot-message">
        <img src="{avatar_img}" class="avatar" />
        <div class="message-content">
            <p class="message-text">{text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.logo("logo1.jpg",
         size="large")
 
#questions functions
def show_closed_question(question, options, feedbacks):
    time.sleep(0.5)  # הוספת השהיה של 0.5 שניות

    # הצגת השאלה הסגורה מהבוט
   #old # with st.chat_message("assistant"):
    #old#     st.markdown(question)
    display_bot_message(question)

    # יצירת כפתורים לבחירת תשובה
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        if cols[i].button(option, key=f"{st.session_state.current_question}_{option}"):
            # הוספת השאלה והתשובה להיסטוריה
            st.session_state.messages.append({"role": "assistant", "content": question})
            st.session_state.messages.append({"role": "user", "content": option})

            # שמירת התשובה של המשתמש במשתנה user_data
            st.session_state.user_data.append(option)
            
            # הוספת הפידבק
            st.session_state.messages.append({"role": "assistant", "content": feedbacks[i]})
            st.session_state.current_question += 1
            st.rerun()

# פונקציה להצגת שאלה פתוחה
def show_open_question(question, feedback):
    # הצגת השאלה הפתוחה מהבוט
    time.sleep(0.5)  # הוספת השהיה של 0.5 שניות

    display_bot_message(question)
  #old#  with st.chat_message("assistant"):
   #old#     st.markdown(question)

# פונקציה להצגת היסטוריית השיחה
def show_chat_history():
    for message in st.session_state.messages:
        if (message["role"]=="assistant"):
            display_bot_message(message["content"])
        if (message["role"]=="user"):
            display_user_message(message["content"])
       #old# with st.chat_message(message["role"]):
            #old#st.markdown(message["content"])

# פונקציה להצגת תיבת הקלט הקבועה בתחתית
def display_input_box(disabled):
    user_input = st.chat_input("הכנס את התשובה שלך כאן", disabled=disabled)
    
    if user_input:
        # אם המשתמש מקליד לאחר סיום השאלות, נוסיף להיסטוריה בלבד
        if st.session_state.current_question >= len(questions):
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": "תודה! השיחה הסתיימה, אבל אני כאן לשמוע אם יש עוד משהו שתרצה לשתף."})
        # אם המשתמש מקליד תשובה לשאלה פתוחה
        elif not disabled:
            # הוספת התשובה להיסטוריה
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # שמירת התשובה של המשתמש במשתנה user_data
            st.session_state.user_data.append(user_input)

            # טיפול בשאלה הפתוחה או החזרה לשאלה הסגורה
            if st.session_state.current_question < len(questions):
                current_q = questions[st.session_state.current_question]

                # אם זו שאלה פתוחה, השאלה תטופל כאן
                if current_q["type"] == "open":
                    st.session_state.messages.append({"role": "assistant", "content": current_q["feedback"]})
                    st.session_state.current_question += 1
                # אם זו שאלה סגורה, השאלה תוצג מחדש כדי שהמשתמש יבחר באחת האפשרויות
                elif current_q["type"] == "closed":
                    st.session_state.messages.append({"role": "assistant", "content": current_q["question"]})
            
        st.rerun()
        
# פונקציה להצגת שאלה מסוג selectbox
def show_selectbox_question(question, options, feedbacks):
     # הצגת השאלה
    #old#st.markdown(question)
    display_bot_message(question)

    # יצירת Selectbox עבור הבחירה
    selected_option = st.selectbox("", options, key=f"{st.session_state.current_question}_selectbox",
                                   index=None,
                                   placeholder="שם בית הספר שלך...",)



    # לחצן אישור לבחירת התשובה
    if st.button("אישור", key=f"{st.session_state.current_question}_confirm"):
        # הוספת השאלה והתשובה להיסטוריה
        st.session_state.messages.append({"role": "assistant", "content": question})
        st.session_state.messages.append({"role": "user", "content": selected_option})

        # שמירת התשובה של המשתמש במשתנה user_data
        st.session_state.user_data.append(selected_option)

        # הוספת הפידבק לפי הבחירה
        feedback_index = options.index(selected_option)
        st.session_state.messages.append({"role": "assistant", "content": feedbacks})
        st.session_state.current_question += 1
        st.rerun()
    
# כותרת
st.markdown('<h1 class="main-title">צ\'אט בוט חכם</h1>', unsafe_allow_html=True)
# אתחול משתני session_state במידת הצורך
if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_question = 0
        st.session_state.finished = False
        st.session_state.user_data = []  # אתחול המשתנה לאחסון התשובות

        # הוספת משפט פתיחה
        opening_message = """
        שלום, אני ביטי הבוט של תוכנית ההייטק הלאומית. נעים מאוד!
        אני כאן כדי לשמוע על הרצון והמוטיבציה שלך להשתלב בעתיד בתפקידים שונים בתעשיית ההייטק.
        נתחיל מכמה שאלות בסיסיות.
        """
        st.session_state.messages.append({"role": "assistant", "content": opening_message})

    # הצגת היסטוריית השיחה
show_chat_history()

    # הצגת השאלה הנוכחית (אם עדיין לא סיימנו את כל השאלות)
if not st.session_state.finished:
        if st.session_state.current_question < len(questions):
            current_q = questions[st.session_state.current_question]
            if current_q["type"] == "open":
                show_open_question(current_q["question"], current_q["feedback"])
                display_input_box(disabled=False)  # הפעלת תיבת ה-input
            elif current_q["type"] == "closed":
                show_closed_question(current_q["question"], current_q["options"], current_q["feedbacks"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
            elif current_q["type"] == "selectbox":
                show_selectbox_question(current_q["question"], current_q["options"], current_q["feedbacks"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
        else:
            st.session_state.finished = True

            # summary_message = """
            # <div style="text-align: right;">
            # שמחתי לשוחח איתכם ולשמוע על רמת המוטיבציה שלכם להשתלב בתחום טכנולוגי בעתיד. 
            # אני ממליץ לכם בחום לדבר על הנושא עם מורה, הורה או איש צוות בבית הספר שיוכל לספר לכם עוד על התחום.
            # </div>
            # """
            
            summary_message = llm.summerize_conversation(st.session_state.messages)
            
            display_bot_message(summary_message)
            #old#with st.chat_message("assistant", avatar="🤖"):
             #old#   st.markdown(summary_message)
         #   st.markdown(summary_message, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": summary_message})

            # השבתת תיבת ה-input בסיום השיחה
            display_input_box(disabled=True)

            user_data = st.session_state.user_data
            gd.add_row_to_sheet(user_data)
        
