import streamlit as st
import requests
from datetime import datetime

# API endpoint configuration
API_BASE_URL = "http://localhost:8000/api"

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

def call_api(method, endpoint, data=None, params=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def main():
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = {
        "Dashboard": "dashboard",
        "Focus Timer": "focus",
        "Habits": "habits",
        "Meditation": "meditation",
        "Creative Canvas": "creativity",
        "Settings": "settings"
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()), key="main_navigation")
    st.session_state.page = pages[selection]
    
    # Main content
    if st.session_state.page == 'dashboard':
        render_dashboard()
    elif st.session_state.page == 'focus':
        render_focus_timer()
    elif st.session_state.page == 'habits':
        render_habits()
    elif st.session_state.page == 'meditation':
        render_meditation()
    elif st.session_state.page == 'creativity':
        render_creativity()
    elif st.session_state.page == 'settings':
        render_settings()

def render_dashboard():
    st.title("Your Mindful Dashboard")
    
    # Get stats from different services
    focus_stats = call_api("GET", "/focus/stats")
    habits = call_api("GET", "/habits")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        focus_hours = sum(stat["hours"] for stat in focus_stats["stats"]) if focus_stats else 0
        st.metric("Focus Time Today", f"{focus_hours:.1f}h")
    
    with col2:
        habit_count = len(habits) if habits else 0
        st.metric("Active Habits", str(habit_count))
    
    with col3:
        st.metric("Mindful Minutes", "0")  # Placeholder

def render_focus_timer():
    st.title("Focus Timer")
    
    col1, col2 = st.columns([2,1])
    with col1:
        category = st.selectbox("What are you working on?",
                              ["Study", "Work", "Reading", "Project"],
                              key="focus_category")
        
        if "current_session" not in st.session_state:
            if st.button("Start Focus Session", key="start_focus"):
                response = call_api("POST", "/focus/start", {
                    "category": category
                })
                if response:
                    st.session_state.current_session = response
                    st.rerun()
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("End Session", key="end_focus"):
                    response = call_api("POST", 
                        f"/focus/{st.session_state.current_session['id']}/end",
                        {"category": category}
                    )
                    if response:
                        st.success(f"Session completed! Duration: {response['duration_minutes']:.1f} minutes")
                        del st.session_state.current_session
                        st.rerun()

def render_habits():
    st.title("Habit Tracker")
    
    # Add new habit
    with st.expander("Add New Habit"):
        habit_name = st.text_input("Habit name", key="new_habit_name")
        category = st.selectbox("Category",
                              ["Health", "Learning", "Productivity", "Wellness"],
                              key="new_habit_category")
        frequency = st.selectbox("Target frequency",
                               ["Daily", "Weekly", "Monthly"],
                               key="new_habit_frequency")
        
        if st.button("Add Habit", key="add_habit_button"):
            response = call_api("POST", "/habits", {
                "name": habit_name,
                "category": category,
                "target_frequency": frequency
            })
            if response:
                st.success("Habit added successfully!")
                st.rerun()
    
    # List habits
    habits = call_api("GET", "/habits")
    if habits:
        for habit in habits:
            with st.expander(f"{habit['name']} ({habit['category']})"):
                streak = call_api("GET", f"/habits/{habit['id']}/streak")
                if streak:
                    st.metric("Current Streak", f"{streak['streak']} days")
                
                if st.button("Mark Complete", key=f"complete_{habit['id']}"):
                    response = call_api("POST", f"/habits/{habit['id']}/log", {
                        "habit_id": habit['id']
                    })
                    if response:
                        st.success("Progress logged!")
                        st.rerun()

def render_meditation():
    st.title("Meditation & Mindfulness")
    
    # Get daily quote
    quote = call_api("GET", "/meditation/quote")
    if quote:
        st.info(quote["quote"])
    
    # Guided sessions
    st.subheader("Guided Sessions")
    session_type = st.selectbox("Choose your practice",
                               ["breathing", "body_scan", "visualization"],
                               key="meditation_type")
    
    session = call_api("GET", f"/meditation/sessions/{session_type}")
    if session:
        st.write(f"🧘‍♀️ {session['name']} ({session['duration']} minutes)")
        
        if "instructions" in session:
            for i, instruction in enumerate(session["instructions"], 1):
                st.write(f"{i}. {instruction}")
        
        if st.button("Start Session", key="start_meditation"):
            response = call_api("POST", "/meditation/sessions", {
                "session_type": session_type,
                "duration": session["duration"]
            })
            if response:
                st.success("Session started. Find a comfortable position...")

def render_creativity():
    st.title("Creative Canvas")
    
    tab = st.sidebar.radio("Choose Section",
                          ["Write New Entry", "Browse Entries", "Search & Tags"],
                          key="creativity_section")
    
    if tab == "Write New Entry":
        title = st.text_input("Title")
        entry_type = st.selectbox("Entry Type",
                                ["Journal", "Poetry", "Story", "Ideas", "Goals"])
        content = st.text_area("Write your thoughts...", height=300)
        mood = st.select_slider("How are you feeling?",
                              ["😔", "😕", "😐", "🙂", "😊"])
        tags = st.text_input("Tags (comma separated)")
        
        if st.button("Save Entry"):
            if title and content:
                response = call_api("POST", "/creativity/entries", {
                    "entry_type": entry_type,
                    "title": title,
                    "content": content,
                    "mood": mood,
                    "tags": [tag.strip() for tag in tags.split(",")] if tags else []
                })
                if response:
                    st.success("Entry saved successfully!")
                    st.rerun()
    elif tab == "Browse Entries":
        entries = call_api("GET", "/creativity/entries")
        if entries:
            for entry in entries["entries"]:
                with st.expander(f"{entry['title']} - {entry['entry_type']}"):
                    st.write(entry['content'])
                    if entry.get('mood'):
                        st.write(f"Mood: {entry['mood']}")
                    if entry.get('tags'):
                        st.write(f"Tags: {', '.join(entry['tags'])}")

def render_settings():
    st.title("Settings")
    st.write("App settings and preferences will appear here.")

if __name__ == "__main__":
    main()
