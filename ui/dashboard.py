import streamlit as st
from datetime import datetime, timedelta

class Dashboard:
    def __init__(self, habit_tracker, study_timer, meditation, creativity):
        self.habit_tracker = habit_tracker
        self.study_timer = study_timer
        self.meditation = meditation
        self.creativity = creativity

    def render(self):
        st.title("Your Mindful Dashboard")
        
        # Top metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            study_stats = self.study_timer.get_session_stats('today')
            focus_hours = study_stats[0][2] if study_stats else 0
            st.metric("Focus Time Today", 
                     f"{focus_hours:.1f}h",
                     "Track your progress")
                     
        with col2:
            habits = len(self.habit_tracker.get_all_habits())
            st.metric("Active Habits", 
                     str(habits),
                     "Build consistency")
                     
        with col3:
            meditation_stats = self.meditation.get_stats('today')
            mindful_mins = meditation_stats[0][2] if meditation_stats else 0
            st.metric("Mindful Minutes", 
                     str(mindful_mins),
                     "Breathe & reflect")

        # Daily Schedule
        st.subheader("Today's Focus")
        schedule_col, progress_col = st.columns([2,1])
        
        with schedule_col:
            now = datetime.now()
            st.write(f"📅 {now.strftime('%A, %B %d')}")
            
            # Get today's habits
            habits = self.habit_tracker.get_all_habits()
            for habit in habits:
                completed = "✅" if self.habit_tracker.get_streak(habit[0]) > 0 else "⭕"
                st.write(f"{completed} {habit[1]}")
            
            # Get scheduled study sessions
            sessions = self.study_timer.get_session_stats('today')
            if sessions:
                st.write(f"📚 Study Sessions: {len(sessions)} completed")
            
            # Today's meditation
            st.write("🧘‍♀️ Daily Meditation")
            st.info(self.meditation.get_daily_quote())
            
        with progress_col:
            # Day progress
            hour = now.hour
            progress = (hour * 100) / 24
            st.progress(progress/100, "Day Progress")
            
            # Quick actions
            st.button("Start Focus Session")
            st.button("Quick Meditation")
            st.button("Write Journal")
        
    def show_activity_timeline(self, timeframe='today'):
        activities = []
        
        # Get study sessions
        study_sessions = self.study_timer.get_session_stats(timeframe)
        for session in study_sessions:
            activities.append({
                'timestamp': session[0],
                'type': 'Study',
                'description': f'{session[2]:.1f} hours of {session[1]}'
            })
            
        # Get meditation sessions
        meditation_sessions = self.meditation.get_stats(timeframe)
        for session in meditation_sessions:
            activities.append({
                'timestamp': session[0],
                'type': 'Meditation',
                'description': f'{session[2]} minutes of mindfulness'
            })
            
        display_timeline(activities, timeframe)


def display_timeline(activities, timeframe='today'):
    st.subheader("Activity Timeline")
    
    if timeframe == 'today':
        start_date = datetime.now().replace(hour=0, minute=0, second=0)
    elif timeframe == 'week':
        start_date = datetime.now() - timedelta(days=7)
    else:
        start_date = datetime.now() - timedelta(days=30)

    if not activities:
        st.info("No activities to display for the selected timeframe.")
        return

    for activity in sorted(activities, key=lambda x: x.get('timestamp', datetime.now()), reverse=True):
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(activity.get('timestamp').strftime('%H:%M'))
            with col2:
                st.write(f"**{activity.get('type')}**: {activity.get('description')}")


def show_notifications(notifications):
    if notifications:
        with st.sidebar:
            st.subheader("Notifications")
            for notif in notifications:
                st.info(notif.get('message', ''))
    else:
        with st.sidebar:
            st.subheader("Notifications")
            st.write("No new notifications")
