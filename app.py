import streamlit as st
from datetime import datetime

from config import init_db
from agents.habit_tracker import HabitTracker
from agents.study_timer import StudyTimer
from agents.meditation import MeditationModule
from agents.creativity import CreativityAgent
from ui.dashboard import Dashboard, display_timeline, show_notifications
from ui.creativity_zone import creativity_zone

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    # Initialize database if not already done
    init_db()

def main():
    initialize_session_state()
    
    # Initialize agents
    habit_tracker = HabitTracker()
    study_timer = StudyTimer()
    meditation = MeditationModule()
    creativity = CreativityAgent()
    
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
        dashboard = Dashboard(habit_tracker, study_timer, meditation, creativity)
        dashboard.render()
        
    elif st.session_state.page == 'creativity':
        creativity_zone(creativity)
        
    elif st.session_state.page == 'focus':
        st.title("Focus Timer")
        
        col1, col2 = st.columns([2,1])
        with col1:
            category = st.selectbox("What are you working on?",
                                  ["Study", "Work", "Reading", "Project"],
                                  key="focus_category")
            
            if not study_timer.current_session:
                if st.button("Start Focus Session", key="start_focus"):
                    study_timer.start_session(category)
                    st.rerun()
            else:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Pause", key="pause_focus"):
                        study_timer.pause_session()
                        st.rerun()
                with col2:
                    if st.button("End Session", key="end_focus"):
                        duration = study_timer.end_session()
                        st.success(f"Session completed! Duration: {duration/60:.1f} minutes")
                        
        with col2:
            st.subheader("Recent Sessions")
            sessions = study_timer.get_session_stats()
            if sessions:
                for category, count, hours in sessions:
                    if hours is not None:
                        st.write(f"{category}: {count} sessions ({hours:.1f}h)")
                    else:
                        st.write(f"{category}: {count} sessions (0.0h)")
            else:
                st.write("No sessions recorded yet")
                
    elif st.session_state.page == 'habits':
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
                habit_tracker.add_habit(habit_name, category, frequency)
                st.success("Habit added successfully!")
                
        # List and track habits
        habits = habit_tracker.get_all_habits()
        for habit in habits:
            with st.expander(f"{habit[1]} ({habit[2]})"):
                streak = habit_tracker.get_streak(habit[0])
                st.metric("Current Streak", f"{streak} days")
                
                if st.button("Mark Complete", key=f"complete_{habit[0]}"):
                    habit_tracker.log_habit(habit[0])
                    st.success("Progress logged!")
                    
                # Show stats
                stats = habit_tracker.get_habit_stats(habit[0])
                st.write(f"Completed {len(stats)} times in the last week")
                
    elif st.session_state.page == 'meditation':
        st.title("Meditation & Mindfulness")
        
        # Daily quote
        st.info(meditation.get_daily_quote())
        
        # Guided sessions
        st.subheader("Guided Sessions")
        session_type = st.selectbox("Choose your practice",
                                  ["breathing", "body_scan", "visualization"],
                                  key="meditation_type")
        
        session = meditation.get_session(session_type)
        st.write(f"🧘‍♀️ {session['name']} ({session['duration']} minutes)")
        
        if 'instructions' in session:
            for i, instruction in enumerate(session['instructions'], 1):
                st.write(f"{i}. {instruction}")
                
        if st.button("Start Session", key="start_meditation"):
            meditation.log_session(session_type, session['duration'])
            st.success("Session started. Find a comfortable position...")
            
    elif st.session_state.page == 'settings':
        st.title("Settings")
        st.write("App settings and preferences will appear here.")

if __name__ == "__main__":
    main()
