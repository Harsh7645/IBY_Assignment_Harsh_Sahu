import streamlit as st
import requests
import time
import random
from datetime import datetime

# API endpoint configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Custom CSS styling with your color scheme
def apply_custom_styling():
    st.markdown("""
    <style>
    :root {
        --primary-color: #5873C6;
        --secondary-color: #B49FCC;
        --background-color: #F6F6F2;
        --card-color: #E3EAF2;
        --button-color: #8ED081;
        --highlight-color: #FFD6A5;
        --supportive-color: #F6A6B2;
        --text-color: #30404D;
    }
    
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    .stSidebar {
        background-color: var(--card-color);
        color: var(--text-color);
    }
    
    .stSidebar .stSelectbox label,
    .stSidebar .stButton label,
    .stSidebar h1, .stSidebar h2, .stSidebar h3,
    .stSidebar p, .stSidebar div {
        color: var(--text-color) !important;
    }
    
    .stButton > button {
        background-color: var(--button-color);
        color: var(--text-color);
        border: none;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-color);
        color: white;
    }
    
    .stSelectbox > div > div {
        background-color: var(--card-color);
        border: 1px solid var(--primary-color);
        color: var(--text-color);
    }
    
    .stSelectbox label {
        color: var(--text-color) !important;
    }
    
    .stTextInput > div > div > input {
        background-color: var(--card-color);
        border: 1px solid var(--primary-color);
        color: var(--text-color);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6B7280 !important;
        opacity: 0.8;
    }
    
    .stTextArea > div > div > textarea {
        background-color: var(--card-color);
        border: 1px solid var(--primary-color);
        color: var(--text-color);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #6B7280 !important;
        opacity: 0.8;
    }
    
    .stMetric {
        background-color: var(--card-color);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
        color: var(--text-color);
    }
    
    .stMetric label, .stMetric div {
        color: var(--text-color) !important;
    }
    
    .stExpander {
        background-color: var(--card-color);
        border: 1px solid var(--secondary-color);
        border-radius: 8px;
        color: var(--text-color);
    }
    
    .stExpander summary, .stExpander div, .stExpander p {
        color: var(--text-color) !important;
    }
    
    .stSuccess {
        background-color: var(--button-color);
        color: var(--text-color);
    }
    
    .stInfo {
        background-color: var(--highlight-color);
        color: var(--text-color);
    }
    
    .stError {
        background-color: var(--supportive-color);
        color: var(--text-color);
    }
    
    h1, h2, h3 {
        color: var(--primary-color);
    }
    
    .stRadio > div {
        background-color: var(--card-color);
        padding: 0.5rem;
        border-radius: 8px;
        color: var(--text-color);
    }
    
    .stRadio label, .stRadio div {
        color: var(--text-color) !important;
    }
    
    /* Additional styling for form elements */
    .stTextInput label, .stTextArea label, .stSlider label,
    .stNumberInput label, .stDateInput label, .stTimeInput label {
        color: var(--text-color) !important;
    }
    
    /* Ensure all content areas have dark text on light backgrounds */
    .stMarkdown, .stWrite, .element-container {
        color: var(--text-color);
    }
    
    /* Style for containers and columns */
    .stColumn > div, .stContainer > div {
        color: var(--text-color);
    }
    
    /* Additional comprehensive styling for light backgrounds */
    .stNumberInput > div > div > input {
        background-color: var(--card-color);
        border: 1px solid var(--primary-color);
        color: var(--text-color);
    }
    
    .stNumberInput > div > div > input::placeholder {
        color: #6B7280 !important;
        opacity: 0.8;
    }
    
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background-color: var(--card-color);
        border: 1px solid var(--primary-color);
        color: var(--text-color);
    }
    
    .stSlider > div > div > div {
        color: var(--text-color);
    }
    
    .stSelectSlider > div {
        color: var(--text-color);
    }
    
    /* Checkbox and multiselect styling */
    .stCheckbox > label {
        color: var(--text-color) !important;
    }
    
    .stMultiSelect > div > div {
        background-color: var(--card-color);
        border: 1px solid var(--primary-color);
        color: var(--text-color);
    }
    
    .stMultiSelect label {
        color: var(--text-color) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: var(--card-color);
        border: 1px solid var(--primary-color);
        color: var(--text-color);
    }
    
    .stFileUploader label {
        color: var(--text-color) !important;
    }
    
    /* Progress bar and spinner styling */
    .stProgress > div {
        color: var(--text-color);
    }
    
    /* Tab styling */
    .stTabs > div > div > div {
        color: var(--text-color);
    }
    
    /* Code block styling */
    .stCode {
        background-color: var(--card-color);
        color: var(--text-color);
        border: 1px solid var(--primary-color);
    }
    
    /* Table styling */
    .stDataFrame {
        background-color: var(--card-color);
        color: var(--text-color);
    }
    
    /* Warning and info boxes */
    .stWarning {
        background-color: var(--highlight-color);
        color: var(--text-color) !important;
    }
    
    .stAlert {
        color: var(--text-color) !important;
    }
    
    /* General text elements */
    p, span, div, label {
        color: var(--text-color);
    }
    
    /* Override any white text on light backgrounds */
    .stApp [data-testid="stAppViewContainer"] * {
        color: var(--text-color);
    }
    
    /* Specific override for any elements that might inherit light text */
    .stApp * {
        color: inherit;
    }
    
    .stApp .main * {
        color: var(--text-color);
    }
    </style>
    """, unsafe_allow_html=True)

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
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def main():
    apply_custom_styling()
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
    
    # Generate synthetic data for demonstration
    import random
    
    # Synthetic focus data
    synthetic_focus = {
        "today_hours": round(random.uniform(1.5, 4.2), 1),
        "yesterday_minutes": random.randint(45, 180),
        "trees_planted": random.randint(8, 25),
        "sessions_today": random.randint(2, 6)
    }
    
    # Synthetic meditation data
    synthetic_meditation = {
        "today_minutes": random.randint(15, 45),
        "weekly_days": random.randint(4, 7),
        "streak_days": random.randint(3, 18)
    }
    
    # Updated synthetic habits data with different examples
    synthetic_habits_count = random.randint(7, 15)
    
    # Try to get real data, but fall back to synthetic if API fails
    focus_progress = call_api("GET", "/api/focus/daily-progress") or synthetic_focus
    habits_response = call_api("GET", "/api/habits")
    top_streaks_response = call_api("GET", "/api/habits/top-streaks")
    meditation_progress = call_api("GET", "/api/meditation/daily-progress") or synthetic_meditation
    
    # Main metrics row - now including meditation
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        focus_hours = focus_progress.get('today_hours', synthetic_focus['today_hours'])
        yesterday_delta = focus_hours - (focus_progress.get('yesterday_minutes', synthetic_focus['yesterday_minutes']) / 60)
        st.metric(
            "Focus Time Today", 
            f"{focus_hours}h",
            delta=f"+{yesterday_delta:.1f}h from yesterday" if yesterday_delta > 0 else f"{yesterday_delta:.1f}h from yesterday"
        )
    
    with col2:
        habit_count = len(habits_response.get("habits", [])) if habits_response else synthetic_habits_count
        st.metric("Active Habits", str(habit_count))
    
    with col3:
        mindful_minutes = meditation_progress.get('today_minutes', synthetic_meditation['today_minutes'])
        st.metric("Mindful Minutes", f"{mindful_minutes} min")
    
    with col4:
        trees_planted = focus_progress.get('trees_planted', synthetic_focus['trees_planted'])
        st.metric("Trees Planted", f"{trees_planted}")
    
    # Top Habit Streaks Section
    if top_streaks_response and top_streaks_response.get("top_streaks"):
        st.subheader("Top Habit Streaks")
        
        top_streaks = top_streaks_response["top_streaks"]
        
        # Create streak cards
        if len(top_streaks) >= 3:
            streak_cols = st.columns(3)
        else:
            streak_cols = st.columns(len(top_streaks))
        
        for idx, streak in enumerate(top_streaks[:3]):  # Only show top 3
            with streak_cols[idx]:
                # Medal emoji and colors based on position
                if idx == 0:
                    medal = "🥇"
                    gradient = "linear-gradient(135deg, #FFD700, #FFA500)"
                elif idx == 1:
                    medal = "🥈"
                    gradient = "linear-gradient(135deg, #C0C0C0, #A8A8A8)"
                else:
                    medal = "🥉"
                    gradient = "linear-gradient(135deg, #CD7F32, #A0522D)"
                
                st.markdown(f"""
                <div style="
                    background: {gradient};
                    border-radius: 15px;
                    padding: 25px;
                    text-align: center;
                    margin-bottom: 20px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                    border: 2px solid rgba(255,255,255,0.3);
                ">
                    <div style="font-size: 32px; margin-bottom: 12px;">{medal}</div>
                    <img src="{streak['icon']}" 
                         style="width: 32px; height: 32px; margin-bottom: 12px; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));"
                         alt="{streak['category']} icon">
                    <div style="font-weight: 700; color: white; margin-bottom: 6px; font-size: 16px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                        {streak['name'][:25]}{'...' if len(streak['name']) > 25 else ''}
                    </div>
                    <div style="font-size: 28px; font-weight: bold; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.4);">
                        {streak['streak']} days
                    </div>
                    <div style="font-size: 12px; color: rgba(255,255,255,0.9); text-transform: uppercase; font-weight: 600;">
                        {streak['category']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Updated synthetic top streaks with different examples
        st.subheader("🔥 Top Habit Streaks")
        
        synthetic_streaks = [
            {"name": "Evening Workout", "streak": 28, "category": "Exercise"},
            {"name": "Practice Piano", "streak": 22, "category": "Learning"},
            {"name": "Journal Writing", "streak": 19, "category": "Wellness"}
        ]
        
        streak_cols = st.columns(3)
        
        for idx, streak in enumerate(synthetic_streaks):
            with streak_cols[idx]:
                if idx == 0:
                    medal = "🥇"
                    gradient = "linear-gradient(135deg, #FFD700, #FFA500)"
                elif idx == 1:
                    medal = "🥈"
                    gradient = "linear-gradient(135deg, #C0C0C0, #A8A8A8)"
                else:
                    medal = "🥉"
                    gradient = "linear-gradient(135deg, #CD7F32, #A0522D)"
                
                st.markdown(f"""
                <div style="
                    background: {gradient};
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 20px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                    border: 2px solid rgba(255,255,255,0.3);
                ">
                    <div style="font-size: 28px; margin-bottom: 10px;">{medal}</div>
                    <div style="font-weight: 600; color: white; margin-bottom: 5px; font-size: 14px;">
                        {streak['name']}
                    </div>
                    <div style="font-size: 24px; font-weight: bold; color: white;">
                        {streak['streak']} days
                    </div>
                    <div style="font-size: 11px; color: rgba(255,255,255,0.9);">
                        {streak['category']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Additional progress widgets
    st.subheader("📈 Today's Progress")
    
    # Progress indicators with synthetic data
    col_prog1, col_prog2, col_prog3 = st.columns(3)
    
    with col_prog1:
        focus_sessions = focus_progress.get('sessions_today', synthetic_focus['sessions_today'])
        st.info(f"🎯 Completed {focus_sessions} focus sessions today")
        
        # Focus progress bar
        daily_focus_goal = 4.0  # 4 hours goal
        focus_progress_pct = min(focus_hours / daily_focus_goal, 1.0)
        st.progress(focus_progress_pct, text=f"Daily Focus Goal: {focus_progress_pct*100:.0f}%")
    
    with col_prog2:
        weekly_meditation = meditation_progress.get('weekly_days', synthetic_meditation['weekly_days'])
        st.success(f"🧘‍♀️ Meditated {weekly_meditation} days this week")
        
        # Weekly meditation progress
        weekly_goal = 7
        weekly_progress_pct = weekly_meditation / weekly_goal
        st.progress(weekly_progress_pct, text=f"Weekly Meditation: {weekly_progress_pct*100:.0f}%")
    
    with col_prog3:
        meditation_streak = meditation_progress.get('streak_days', synthetic_meditation['streak_days'])
        st.warning(f"🔥 Meditation streak: {meditation_streak} days")
        
        # Streak visualization
        streak_goal = 30  # 30 day streak goal
        streak_progress_pct = min(meditation_streak / streak_goal, 1.0)
        st.progress(streak_progress_pct, text=f"Streak Goal: {streak_progress_pct*100:.0f}%")
    
    # Daily Summary
    if focus_hours >= 2 or mindful_minutes >= 20:
        st.subheader("🌟 Today's Summary")
        
        summary_messages = []
        if focus_hours >= 3:
            summary_messages.append(f"Outstanding focus today with {focus_hours} hours!")
        elif focus_hours >= 2:
            summary_messages.append(f"Great focus session totaling {focus_hours} hours!")
        
        if mindful_minutes >= 30:
            summary_messages.append(f"Excellent mindfulness practice with {mindful_minutes} minutes!")
        elif mindful_minutes >= 15:
            summary_messages.append(f"Good meditation habit with {mindful_minutes} minutes!")
        
        if trees_planted >= 15:
            summary_messages.append(f"Impressive productivity - you've planted {trees_planted} trees!")
        
        for message in summary_messages:
            st.success(message)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #E8F0F8, #F0F8F8); 
                    border-radius: 15px; margin: 20px 0;">
            <div style="font-size: 48px; margin-bottom: 15px;">🌟</div>
            <h4 style="color: #5873C6; margin-bottom: 8px;">Ready to Start Your Day?</h4>
            <p style="color: #6B7280;">Begin your first focus session to see your progress bloom!</p>
        </div>
        """, unsafe_allow_html=True)

def render_tree_animation(stage, duration_minutes):
    """Render animated tree based on progress stage"""
    # Tree grows based on stage (0-4)
    tree_height = 50 + (stage * 50)  # Base height + growth
    tree_width = 40 + (stage * 20)   # Base width + growth
    
    # Color progression using our palette
    colors = {
        0: "#F6F6F2",  # Empty pot
        1: "#8ED081",  # Small sapling
        2: "#5873C6",  # Growing tree
        3: "#B49FCC",  # Full tree
        4: "#FFD6A5"   # Tree with fruits
    }
    
    progress_percent = min((stage / 4) * 100, 100)
    
    # Create SVG tree
    tree_svg = f"""
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <svg width="200" height="200" viewBox="0 0 200 200">
            <!-- Pot -->
            <rect x="75" y="160" width="50" height="30" fill="#8B4513" stroke="#654321" stroke-width="2"/>
            
            <!-- Tree trunk (appears from stage 1) -->
            {f'<rect x="95" y="{160-tree_height//3}" width="10" height="{tree_height//3}" fill="#8B4513"/>' if stage >= 1 else ''}
            
            <!-- Tree leaves/crown (appears from stage 2) -->
            {f'<circle cx="100" cy="{160-tree_height//2}" r="{tree_width//2}" fill="{colors[min(stage, 4)]}" opacity="0.8"/>' if stage >= 2 else ''}
            
            <!-- Additional foliage (stage 3+) -->
            {f'<circle cx="85" cy="{160-tree_height//2-10}" r="{tree_width//3}" fill="{colors[min(stage, 4)]}" opacity="0.6"/>' if stage >= 3 else ''}
            {f'<circle cx="115" cy="{160-tree_height//2-10}" r="{tree_width//3}" fill="{colors[min(stage, 4)]}" opacity="0.6"/>' if stage >= 3 else ''}
            
            <!-- Fruits (stage 4) -->
            {f'<circle cx="90" cy="{160-tree_height//2}" r="4" fill="#FF6B6B"/>' if stage >= 4 else ''}
            {f'<circle cx="110" cy="{160-tree_height//2-5}" r="4" fill="#FF6B6B"/>' if stage >= 4 else ''}
            {f'<circle cx="100" cy="{160-tree_height//2+10}" r="4" fill="#FF6B6B"/>' if stage >= 4 else ''}
            
            <!-- Progress indicator -->
            <text x="100" y="190" text-anchor="middle" font-size="12" fill="#30404D">
                {progress_percent:.0f}% Complete
            </text>
        </svg>
    </div>
    """
    
    return tree_svg

def render_focus_timer():
    st.title("Focus Timer")
    
    # Get daily targets for task selection
    targets_response = call_api("GET", "/api/focus/targets")
    targets = targets_response.get("targets", []) if targets_response else []
    
    # Check for active session
    active_session_response = call_api("GET", "/api/focus/active-session")
    active_session = active_session_response if active_session_response and active_session_response.get("session_id") else None
    
    # Main layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Get Ready to Focus")
        
        # Duration selection
        duration_options = [15, 25, 30, 45, 60, 90, 120]
        selected_duration = st.selectbox(
            "Focus Duration (minutes)",
            duration_options,
            index=1,  # Default to 25 minutes
            key="focus_duration"
        )
        
        # Target selection (optional)
        target_options = ["No specific target"] + [target["target_description"] for target in targets]
        selected_target = st.selectbox(
            "What are you working on? (Optional)",
            target_options,
            key="focus_target"
        )
        
        # Pomodoro break options
        st.subheader("Break Settings")
        break_enabled = st.checkbox("Enable Pomodoro breaks", value=True, key="break_enabled")
        if break_enabled:
            break_duration = st.selectbox("Break duration", [5, 15], index=0, key="break_duration")
        else:
            break_duration = 0
        
        # Start/Control buttons
        if not active_session:
            if st.button("🎯 Start Focus Session", type="primary", key="start_focus"):
                task_selected = selected_target if selected_target != "No specific target" else None
                
                response = call_api("POST", "/api/focus/start-session", {
                    "duration_minutes": selected_duration,
                    "task_selected": task_selected,
                    "break_enabled": break_enabled,
                    "break_duration": break_duration
                })
                
                if response:
                    st.session_state.focus_session_id = response["session_id"]
                    st.session_state.focus_start_time = time.time()
                    st.session_state.focus_duration = selected_duration * 60  # Convert to seconds
                    st.session_state.focus_paused = False
                    st.success("Focus session started! 🌱")
                    st.rerun()
        else:
            st.info("Focus session in progress...")
            
            col_pause, col_end = st.columns(2)
            with col_pause:
                if st.session_state.get("focus_paused", False):
                    if st.button("▶️ Resume", key="resume_focus"):
                        st.session_state.focus_paused = False
                        st.rerun()
                else:
                    if st.button("⏸️ Pause", key="pause_focus"):
                        st.session_state.focus_paused = True
                        st.rerun()
            
            with col_end:
                if st.button("🛑 End Session", key="end_focus"):
                    # Calculate completed duration
                    if hasattr(st.session_state, 'focus_start_time'):
                        elapsed_time = time.time() - st.session_state.focus_start_time
                        completed_minutes = int(elapsed_time / 60)
                        
                        # Update session as completed
                        update_response = call_api("PUT", f"/api/focus/session/{active_session['session_id']}", {
                            "status": "completed",
                            "completed_duration": completed_minutes,
                            "tree_stage": min(4, int((completed_minutes / selected_duration) * 4))
                        })
                        
                        if update_response:
                            st.success(f"Session completed! You focused for {completed_minutes} minutes 🎉")
                            # Clear session state
                            for key in ['focus_session_id', 'focus_start_time', 'focus_duration', 'focus_paused']:
                                if key in st.session_state:
                                    del st.session_state[key]
                            st.rerun()
    
    with col2:
        st.subheader("Focus Progress")
        
        # Focus timer display for demo purposes
        if st.button("Start Focus Timer", key="focus_timer"):
            st.session_state.show_focus_timer = True
            st.session_state.focus_start_time = time.time()
            st.session_state.focus_minutes = random.randint(15, 45)
            st.session_state.focus_seconds = random.randint(0, 59)
        
        if st.session_state.get("show_focus_timer"):
            # Generate countdown
            if not hasattr(st.session_state, 'last_focus_update') or time.time() - st.session_state.last_focus_update > 1:
                if st.session_state.focus_seconds > 0:
                    st.session_state.focus_seconds -= 1
                elif st.session_state.focus_minutes > 0:
                    st.session_state.focus_minutes -= 1
                    st.session_state.focus_seconds = 59
                else:
                    st.session_state.show_focus_timer = False
                    st.balloons()
                    st.success("🎉 Focus session completed! You grew a beautiful tree! 🌳")
                
                st.session_state.last_focus_update = time.time()
            
            # Timer display with tree
            minutes = st.session_state.focus_minutes
            seconds = st.session_state.focus_seconds
            progress = 1 - (minutes * 60 + seconds) / (45 * 60)  # Assuming max 45 min
            
            # Large timer display
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-size: 3rem; font-weight: bold; color: #5873C6; margin-bottom: 10px;">
                    {minutes:02d}:{seconds:02d}
                </div>
                <div style="font-size: 1.2rem; color: #30404D;">
                    🎯 Focusing Intensely
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            st.progress(min(progress, 1.0), text=f"Progress: {min(progress*100, 100):.0f}%")
            
            # Animated tree based on progress
            tree_stage = min(int(progress * 4), 4)
            tree_emojis = ["🌱", "🌿", "🌳", "🌲", "🌟🌲🌟"]
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-size: 4rem; margin: 20px 0;">
                    {tree_emojis[tree_stage]}
                </div>
                <div style="color: #5873C6; font-weight: 500;">
                    Tree Growth: Stage {tree_stage + 1}/5
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-refresh for countdown
            if st.session_state.show_focus_timer:
                time.sleep(0.5)
                st.rerun()
        else:
            # Show demo statistics
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: #F8F9FA; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #5873C6; margin-bottom: 15px;">📊 Today's Focus Stats</h4>
                <div style="font-size: 1.5rem; font-weight: bold; color: #30404D;">2h 35m</div>
                <div style="color: #6B7280;">Total Focus Time</div>
                <div style="margin-top: 10px; font-size: 1.2rem;">🌳 Trees Grown: 3</div>
            </div>
            """, unsafe_allow_html=True)
            tree_html = render_tree_animation(0, 0)
            st.markdown(tree_html, unsafe_allow_html=True)
    
    # Targets of the Day section
    st.subheader("🎯 Targets of the Day")
    
    # Add new target
    with st.expander("Add New Target"):
        new_target = st.text_input("Target description", key="new_target_desc")
        target_category = st.selectbox(
            "Category",
            ["Study", "Work", "Personal", "Skill Development", "Research"],
            key="new_target_category"
        )
        target_priority = st.selectbox(
            "Priority",
            ["high", "medium", "low"],
            key="new_target_priority"
        )
        
        if st.button("Add Target", key="add_target"):
            if new_target:
                response = call_api("POST", "/api/focus/targets", {
                    "target_description": new_target,
                    "category": target_category,
                    "priority": target_priority
                })
                if response:
                    st.success("Target added successfully!")
                    st.rerun()
    
    # Display existing targets
    if targets:
        for target in targets:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                status_icon = "✅" if target["is_completed"] else "📌"
                priority_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}[target["priority"]]
                st.write(f"{status_icon} {priority_color} {target['target_description']}")
                st.caption(f"Category: {target['category']}")
            
            with col2:
                if not target["is_completed"]:
                    if st.button("Mark Complete", key=f"complete_{target['id']}"):
                        response = call_api("PUT", f"/api/focus/targets/{target['id']}/complete")
                        if response:
                            st.success("Target completed!")
                            st.rerun()
            
            with col3:
                st.caption(f"Priority: {target['priority']}")
    else:
        st.info("No targets set for today. Add some targets to stay focused!")

def render_habits():
    st.title("Habit Tracker")
    
    # Compact "Add New Habit" section with smaller padding
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4A5B8C, #5873C6); 
                padding: 15px; border-radius: 12px; margin-bottom: 25px;
                box-shadow: 0 4px 15px rgba(88, 115, 198, 0.3);
                border: 2px solid #30404D;">
        <h4 style="color: white; margin: 0 0 5px 0; font-weight: 600; text-align: center; line-height: 1.2;">
            Build New Habit
        </h4>
        <p style="color: #E3EAF2; margin: 0; text-align: center; font-size: 14px;">
            Small steps, big changes
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add new habit form - directly without extra container
    col1, col2 = st.columns(2)
    
    with col1:
        habit_name = st.text_input("Habit name", 
                                 placeholder="e.g., Read for 30 minutes daily",
                                 key="new_habit_name")
        category = st.selectbox("Category",
                              ["Health", "Learning", "Productivity", "Wellness", "Exercise", "Mindfulness"],
                              key="new_habit_category")
    
    with col2:
        frequency = st.selectbox("Target frequency",
                               ["Daily", "Weekly", "Monthly"],
                               key="new_habit_frequency")
        
        # Add habit button
        if st.button("Create Habit", type="primary", key="add_habit_button", use_container_width=True):
            if habit_name:
                response = call_api("POST", "/habits", {
                    "name": habit_name,
                    "category": category,
                    "target_frequency": frequency
                })
                if response:
                    st.success("Habit created successfully!")
                    st.rerun()
            else:
                st.error("Please enter a habit name")
    
    # Get habits from API
    habits_response = call_api("GET", "/api/habits")
    habits = habits_response.get("habits", []) if habits_response else []
    
    if habits:
        st.subheader("Your Active Habits")
        
        # Create habit cards in grid layout
        cols = st.columns(2)  # 2 habits per row
        
        for idx, habit in enumerate(habits):
            with cols[idx % 2]:
                # Check if this card is selected/expanded
                is_selected = st.session_state.get(f"selected_habit", None) == habit['id']
                
                # Card styling based on selection
                if is_selected:
                    card_bg = "#D1F2D1"  # Light green when selected
                    border_color = "#8ED081"
                    box_shadow = "0 4px 16px rgba(142, 208, 129, 0.4)"
                else:
                    card_bg = "#E3EAF2"  # Default card color
                    border_color = "#B49FCC"
                    box_shadow = "0 2px 8px rgba(0,0,0,0.1)"
                
                # Habit card HTML - clean design without excessive emojis
                card_html = f"""
                <div style="
                    background-color: {card_bg};
                    border: 2px solid {border_color};
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 20px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: {box_shadow};
                    position: relative;
                ">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; flex: 1;">
                            <img src="{habit['icon']}" 
                                 style="width: 40px; height: 40px; margin-right: 15px; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));"
                                 alt="{habit['category']} icon">
                            <div>
                                <div style="font-weight: 700; font-size: 18px; color: #30404D; margin-bottom: 4px; line-height: 1.2;">
                                    {habit['name']}
                                </div>
                                <div style="font-size: 13px; color: #6B7280; font-weight: 500;">
                                    {habit['category']} • {habit['target_frequency']}
                                </div>
                            </div>
                        </div>
                        <div style="text-align: center; min-width: 80px; background-color: rgba(88, 115, 198, 0.1); 
                                    border-radius: 10px; padding: 10px;">
                            <div style="font-weight: bold; font-size: 24px; color: #5873C6;">
                                {habit['streak']}
                            </div>
                            <div style="font-size: 11px; color: #6B7280; text-transform: uppercase; font-weight: 600;">
                                DAY STREAK
                            </div>
                        </div>
                    </div>
                </div>
                """
                
                # Display the card
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Clickable area to expand/collapse
                button_label = "Mark Complete" if not is_selected else "Hide Actions"
                button_type = "primary" if not is_selected else "secondary"
                
                if st.button(button_label, key=f"manage_{habit['id']}", use_container_width=True, type=button_type):
                    if is_selected:
                        st.session_state.selected_habit = None
                    else:
                        st.session_state.selected_habit = habit['id']
                    st.rerun()
                
                # Expanded section for mark complete
                if is_selected:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #F0F8F0, #E8F5E8);
                        border: 2px solid #8ED081;
                        border-radius: 12px;
                        padding: 20px;
                        margin-top: 15px;
                        margin-bottom: 25px;
                        box-shadow: 0 4px 12px rgba(142, 208, 129, 0.2);
                    ">
                        <h6 style="color: #30404D; margin-bottom: 15px; font-weight: 600; text-align: center;">
                            Quick Actions for "{habit['name']}"
                        </h6>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action buttons
                    action_col1, action_col2 = st.columns([2, 1])
                    
                    with action_col1:
                        if st.button(f"Complete Today's Goal", 
                                   key=f"complete_{habit['id']}", 
                                   type="primary",
                                   use_container_width=True):
                            response = call_api("POST", f"/api/habits/{habit['id']}/log")
                            if response:
                                st.success("Habit completed for today!")
                                st.rerun()
                            else:
                                st.warning("Already completed today or error occurred")
                    
                    with action_col2:
                        if habit['last_completed']:
                            st.info(f"Last: {habit['last_completed']}")
                        else:
                            st.info("First time!")
                
                # Add spacing between cards
                st.markdown("<br>", unsafe_allow_html=True)
    
    else:
        # Clean empty state without excessive emojis
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #F0F4F8, #E8F0F8); 
                    border-radius: 15px; margin: 30px 0;">
            <h4 style="color: #5873C6; margin-bottom: 12px; font-weight: 600;">Ready to Build Great Habits?</h4>
            <p style="color: #6B7280; font-size: 16px;">
                Start your habit journey today and track your progress!
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_meditation():
    st.title("Meditation & Mindfulness")
    
    # Get motivational quote
    quote_response = call_api("GET", "/api/meditation/quote")
    if quote_response:
        st.markdown(f"""
        <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #E8F0F8, #F0F8F8); 
                    border-radius: 15px; margin: 20px 0; border: 2px solid #B49FCC;">
            <h3 style="color: #5873C6; font-style: italic; margin: 0; font-weight: 500; line-height: 1.4;">
                "{quote_response['quote']}"
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Meditation illustration - Using multiple image options for better compatibility
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 30px 0;">
        <div style="width: 150px; height: 150px; 
                    background: linear-gradient(135deg, #E8F0F8, #F0F8F8); 
                    border-radius: 50%; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    font-size: 60px;">
            🧘‍♀️
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Descriptive text
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <p style="color: #6B7280; font-size: 16px; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Take a moment to center yourself and find inner peace. Meditation helps reduce stress, 
            improve focus, and cultivate mindfulness in your daily life.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for active session
    active_session_response = call_api("GET", "/api/meditation/active-session")
    active_session = active_session_response if active_session_response and active_session_response.get("id") else None
    
    # Meditation controls
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Start Your Practice")
        
        # Duration selection with varied options
        duration_options = [2, 3, 5, 8, 10, 15, 20]
        selected_duration = st.selectbox(
            "Choose duration (minutes)",
            duration_options,
            index=2,  # Default to 5 minutes
            key="meditation_duration_select"
        )
        
        # Meditation session controls
        if not active_session:
            if st.button("Begin Meditation", type="primary", key="start_meditation", use_container_width=True):
                response = call_api("POST", "/api/meditation/start-session", {
                    "duration_minutes": selected_duration
                })
                
                if response:
                    st.session_state.meditation_session_id = response["session_id"]
                    st.session_state.meditation_start_time = time.time()
                    st.session_state.meditation_duration = selected_duration * 60  # Convert to seconds
                    st.session_state.meditation_paused = False
                    st.success("Meditation session started. Close your eyes and breathe...")
                    st.rerun()
        else:
            st.info("Meditation session in progress...")
            
            col_pause, col_end = st.columns(2)
            with col_pause:
                if st.session_state.get("meditation_paused", False):
                    if st.button("Resume", key="resume_meditation"):
                        st.session_state.meditation_paused = False
                        st.rerun()
                else:
                    if st.button("Pause", key="pause_meditation"):
                        st.session_state.meditation_paused = True
                        st.rerun()
            
            with col_end:
                if st.button("End Session", key="end_meditation"):
                    # Complete the session
                    complete_response = call_api("PUT", f"/api/meditation/complete-session/{active_session['id']}", {})
                    
                    if complete_response:
                        st.success("Meditation session completed! How do you feel?")
                        # Clear session state
                        for key in ['meditation_session_id', 'meditation_start_time', 'meditation_duration', 'meditation_paused']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.session_state.show_reflection = True
                        st.rerun()
    
    with col2:
        st.subheader("Session Progress")
        
        # Meditation timer for demo
        if st.button("Start Meditation Timer", key="meditation_timer"):
            st.session_state.show_meditation_timer = True
            st.session_state.meditation_start_time = time.time()
            st.session_state.meditation_minutes = random.randint(3, 20)
            st.session_state.meditation_seconds = random.randint(0, 59)
        
        if st.session_state.get("show_meditation_timer"):
            # Generate countdown
            if not hasattr(st.session_state, 'last_meditation_update') or time.time() - st.session_state.last_meditation_update > 1:
                if st.session_state.meditation_seconds > 0:
                    st.session_state.meditation_seconds -= 1
                elif st.session_state.meditation_minutes > 0:
                    st.session_state.meditation_minutes -= 1
                    st.session_state.meditation_seconds = 59
                else:
                    st.session_state.show_meditation_timer = False
                    st.balloons()
                    st.success("🧘‍♀️ Meditation completed! You feel peaceful and centered! ✨")
                
                st.session_state.last_meditation_update = time.time()
            
            # Timer display in circular format
            minutes = st.session_state.meditation_minutes
            seconds = st.session_state.meditation_seconds
            progress = 1 - (minutes * 60 + seconds) / (20 * 60)  # Assuming max 20 min
            
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin: 30px 0;">
                <div style="
                    width: 150px; height: 150px; border-radius: 50%; 
                    border: 8px solid #E3EAF2; 
                    display: flex; flex-direction: column; align-items: center; justify-content: center;
                    background: linear-gradient(135deg, #F0F8F0, #E8F5E8);
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    position: relative;
                ">
                    <div style="font-size: 2.5rem; font-weight: bold; color: #5873C6; margin-bottom: 5px;">
                        {minutes:02d}:{seconds:02d}
                    </div>
                    <div style="font-size: 14px; color: #30404D; text-align: center;">
                        Meditating ✨
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            st.progress(min(progress, 1.0), text=f"Progress: {min(progress*100, 100):.0f}%")
            
            # Meditation mood indicator
            mood_stages = ["😌", "😊", "😇", "🧘‍♀️", "✨🧘‍♀️✨"]
            mood_stage = min(int(progress * 4), 4)
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-size: 3rem; margin: 15px 0;">
                    {mood_stages[mood_stage]}
                </div>
                <div style="color: #5873C6; font-weight: 500;">
                    Mindfulness Level: {mood_stage + 1}/5
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-refresh for countdown
            if st.session_state.show_meditation_timer:
                time.sleep(0.5)
                st.rerun()
        else:
            # Show demo statistics
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: #F8F9FA; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #5873C6; margin-bottom: 15px;">🧘‍♀️ Today's Mindful Minutes</h4>
                <div style="font-size: 1.5rem; font-weight: bold; color: #30404D;">45 min</div>
                <div style="color: #6B7280;">Meditation Time</div>
                <div style="margin-top: 10px; font-size: 1.2rem;">✨ Sessions: 3</div>
                <div style="margin-top: 5px; font-size: 1.2rem;">🧘‍♀️ Mindfulness Streak: 7 days</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Post-meditation reflection section (optional)
    if st.session_state.get("show_reflection", False):
        st.subheader("Reflection Time")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F0F8F0, #E8F5E8); 
                    padding: 20px; border-radius: 12px; margin: 20px 0;">
            <p style="color: #30404D; margin: 0; text-align: center;">
                Take a moment to reflect on your meditation. Writing down your thoughts 
                can help you process any feelings or insights that arose during your practice.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mood rating
        mood_rating = st.slider(
            "How do you feel after meditation? (1=Anxious/Cluttered, 5=Peaceful/Clear)",
            min_value=1, max_value=5, value=3, key="meditation_mood"
        )
        
        # Motivational message based on mood
        if mood_rating <= 2:
            st.warning("It's okay to feel this way. Meditation takes practice. Consider writing about what's on your mind - it often helps to get thoughts out of your head.")
        elif mood_rating >= 4:
            st.success("Wonderful! You're experiencing the benefits of meditation. Feel free to capture this peaceful state in writing.")
        
        # Thoughts text area
        thoughts = st.text_area(
            "Share your thoughts, feelings, or any insights (optional)",
            placeholder="What came up during your meditation? Any worries, insights, or feelings you'd like to note down...",
            height=150,
            key="meditation_thoughts"
        )
        
        col_save, col_skip = st.columns(2)
        
        with col_save:
            if st.button("Save Reflection", type="primary", key="save_reflection"):
                if thoughts.strip() or mood_rating != 3:
                    # Only save meaningful reflections, delete generic ones for privacy
                    if len(thoughts.strip()) > 10:  # Only save substantial thoughts
                        response = call_api("POST", "/api/meditation/reflection", {
                            "mood_rating": mood_rating,
                            "thoughts": thoughts
                        })
                    
                    st.success("Thank you for reflecting! Your session is complete.")
                    st.session_state.show_reflection = False
                    st.rerun()
        
        with col_skip:
            if st.button("Skip Reflection", key="skip_reflection"):
                st.session_state.show_reflection = False
                st.rerun()

def render_creativity():
    st.title("✨ Creative Canvas")
    
    # Initialize session state for creativity features
    if 'current_entry_type' not in st.session_state:
        st.session_state.current_entry_type = "Journal"
    if 'canvas_content' not in st.session_state:
        st.session_state.canvas_content = ""
    if 'canvas_title' not in st.session_state:
        st.session_state.canvas_title = ""
    if 'drawing_mode' not in st.session_state:
        st.session_state.drawing_mode = False
    if 'current_tool' not in st.session_state:
        st.session_state.current_tool = "🖊️ Pen"
    if 'current_color' not in st.session_state:
        st.session_state.current_color = "#000000"
    if 'brush_size' not in st.session_state:
        st.session_state.brush_size = 3
    if 'background_pattern' not in st.session_state:
        st.session_state.background_pattern = "📄 Blank"
    
    # Main navigation tabs with better styling
    st.sidebar.markdown("### 📚 Creative Sections")
    main_tab = st.sidebar.radio(
        "Navigation",
        ["✍️ New Entry", "📚 Browse Entries", "🔍 Search & Filter"],
        key="creativity_main_tab",
        label_visibility="collapsed"
    )
    
    if main_tab == "✍️ New Entry":
        render_new_entry_canvas()
    elif main_tab == "📚 Browse Entries":
        render_entry_browser()
    else:
        render_search_filter()

def render_new_entry_canvas():
    """Enhanced canvas for creating new entries with rich features"""
    
    # Header with date and entry type selector
    st.markdown("### ✨ Create New Entry")
    
    # Create better spaced header layout
    header_col1, header_col2, header_col3 = st.columns([3, 3, 2])
    
    with header_col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E8F0FE, #F0F8FF); 
                    padding: 20px; border-radius: 12px; margin-bottom: 20px;
                    border-left: 4px solid #5873C6; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;">
            <h4 style="color: #5873C6; margin: 0; font-weight: 600;">📅 Today's Date</h4>
            <p style="color: #30404D; margin: 8px 0 0 0; font-size: 18px; font-weight: 500;">{datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        st.markdown("**📋 Entry Type**")
        entry_types = ["Journal", "Poems", "Stories", "Special Memories", "Drawings"]
        st.session_state.current_entry_type = st.selectbox(
            "Entry Type Selection",
            entry_types,
            index=entry_types.index(st.session_state.current_entry_type),
            key="entry_type_selector",
            label_visibility="collapsed"
        )
    
    with header_col3:
        st.markdown("**💾 Save**")
        if st.button("💾 Save Entry", type="primary", key="save_entry_btn", use_container_width=True):
            save_current_entry()
    
    st.markdown("---")
    
    # Title input with better styling
    st.markdown("**📝 Entry Title**")
    st.session_state.canvas_title = st.text_input(
        "Entry Title Input",
        value=st.session_state.canvas_title,
        placeholder="Give your entry a meaningful title...",
        key="canvas_title_input",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Canvas area with tools
    render_canvas_interface()

def render_canvas_interface():
    """Main canvas interface with drawing and text tools"""
    
    # Create main layout: sidebar tools + canvas with better spacing
    tools_col, canvas_col = st.columns([1, 3])
    
    with tools_col:
        st.markdown("### 🎨 Tools Panel")
        render_drawing_tools()
    
    with canvas_col:
        st.markdown("### 📝 Canvas")
        render_main_canvas()

def render_drawing_tools():
    """Side toolbar with all drawing and formatting tools"""
    
    # Mode toggle with better styling
    st.markdown("#### 📝 Mode")
    mode = st.radio(
        "Canvas Mode",
        ["✍️ Text", "🎨 Draw"],
        horizontal=True,
        key="canvas_mode",
        label_visibility="collapsed"
    )
    st.session_state.drawing_mode = (mode == "🎨 Draw")
    
    st.markdown("---")
    
    if st.session_state.drawing_mode:
        # Drawing tools section
        st.markdown("#### 🖊️ Drawing Tools")
        current_tool = st.selectbox(
            "Tool Selection",
            ["🖊️ Pen", "🖍️ Pencil", "🖌️ Brush", "📝 Marker", "✏️ Highlighter", "🧹 Eraser"],
            index=["🖊️ Pen", "🖍️ Pencil", "🖌️ Brush", "📝 Marker", "✏️ Highlighter", "🧹 Eraser"].index(st.session_state.current_tool) if st.session_state.current_tool in ["🖊️ Pen", "🖍️ Pencil", "🖌️ Brush", "📝 Marker", "✏️ Highlighter", "🧹 Eraser"] else 0,
            key="drawing_tool_selector",
            label_visibility="collapsed"
        )
        st.session_state.current_tool = current_tool
        
        st.markdown("#### 🎨 Colors")
        
        # Color palette with better layout
        colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", 
                 "#FF00FF", "#00FFFF", "#FFA500", "#800080", "#FFC0CB"]
        
        # Create a more organized color grid
        color_grid_cols = st.columns(5)
        for i, color in enumerate(colors):
            col_idx = i % 5
            with color_grid_cols[col_idx]:
                if st.button("●", key=f"color_{i}", help=color, use_container_width=True):
                    st.session_state.current_color = color
        
        # Custom color picker
        st.markdown("**Custom Color**")
        current_color = st.color_picker(
            "Custom Color Picker",
            value=st.session_state.current_color,
            key="custom_color_picker",
            label_visibility="collapsed"
        )
        st.session_state.current_color = current_color
        
        # Brush size with better styling
        st.markdown("#### 📏 Brush Size")
        brush_size = st.slider(
            "Brush Size Slider",
            1, 20, st.session_state.brush_size,
            key="brush_size_selector",
            label_visibility="collapsed"
        )
        st.session_state.brush_size = brush_size
        st.markdown(f"*Size: {brush_size}px*")
        
    else:
        # Text formatting tools with better organization
        st.markdown("#### 📝 Text Format")
        
        # Text formatting buttons in a grid
        format_col1, format_col2 = st.columns(2)
        
        with format_col1:
            if st.button("**B**", key="bold_btn", help="Bold", use_container_width=True):
                pass  # Will implement text formatting
            if st.button("*U*", key="underline_btn", help="Underline", use_container_width=True):
                pass
        
        with format_col2:
            if st.button("*I*", key="italic_btn", help="Italic", use_container_width=True):
                pass
            if st.button("**H**", key="highlight_btn", help="Highlight", use_container_width=True):
                pass
        
        # Text colors with better layout
        st.markdown("#### 🌈 Text Colors")
        text_colors = ["#000000", "#FF0000", "#00AA00", "#0066CC", "#AA00AA"]
        text_color_cols = st.columns(len(text_colors))
        
        for i, color in enumerate(text_colors):
            with text_color_cols[i]:
                if st.button("●", key=f"text_color_{color}", help=f"Text color {color}", use_container_width=True):
                    pass
    
    st.markdown("---")
    
    # Background patterns with better styling
    st.markdown("#### 📄 Background")
    background_pattern = st.selectbox(
        "Background Pattern Selection",
        ["📄 Blank", "📏 Lined", "📊 Graph", "📓 Dotted"],
        index=["📄 Blank", "📏 Lined", "📊 Graph", "📓 Dotted"].index(st.session_state.background_pattern),
        key="background_pattern_selector",
        label_visibility="collapsed"
    )
    st.session_state.background_pattern = background_pattern
    
    # Media upload with better styling
    st.markdown("#### 📸 Media Upload")
    uploaded_file = st.file_uploader(
        "Upload Image File",
        type=['png', 'jpg', 'jpeg', 'gif'],
        key="media_uploader",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", width=120)

def render_main_canvas():
    """Main canvas area for content creation"""
    
    # Canvas background styling based on selected pattern
    background_styles = {
        "📄 Blank": "background: white;",
        "📏 Lined": """
            background: white;
            background-image: 
                linear-gradient(transparent 24px, #E3E6EA 24px, #E3E6EA 26px, transparent 26px);
            background-size: 100% 26px;
        """,
        "📊 Graph": """
            background: white;
            background-image: 
                linear-gradient(#E3E6EA 1px, transparent 1px),
                linear-gradient(90deg, #E3E6EA 1px, transparent 1px);
            background-size: 20px 20px;
        """,
        "📓 Dotted": """
            background: white;
            background-image: radial-gradient(circle, #E3E6EA 1px, transparent 1px);
            background-size: 20px 20px;
        """
    }
    
    canvas_bg = background_styles.get(st.session_state.background_pattern, background_styles["📄 Blank"])
    
    # Entry type specific templates
    if st.session_state.current_entry_type == "Drawings":
        render_drawing_canvas(canvas_bg)
    else:
        render_text_canvas(canvas_bg)

def render_text_canvas(background_style):
    """Text-focused canvas with rich formatting"""
    
    st.markdown(f"""
    <div style="
        {background_style}
        min-height: 450px; 
        padding: 30px; 
        border-radius: 15px; 
        border: 2px solid #E3E6EA;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05), 0 4px 20px rgba(0,0,0,0.1);
        position: relative;
        margin: 20px 0;
    ">
        <div style="position: absolute; top: 15px; right: 20px; color: #AAB2C6; font-size: 14px; font-weight: 500;">
            {st.session_state.current_entry_type} Entry
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Rich text area with better styling
    if st.session_state.current_entry_type == "Poems":
        placeholder = "Write your verses here...\n\nLine by line,\nLet your thoughts flow,\nIn rhythm and rhyme..."
        height = 350
    elif st.session_state.current_entry_type == "Stories":
        placeholder = "Once upon a time...\n\nBegin your story here. Let your imagination run wild and create characters, settings, and adventures that captivate readers..."
        height = 400
    elif st.session_state.current_entry_type == "Special Memories":
        placeholder = "This special moment...\n\nDescribe the memory that means so much to you. What made it special? Who was there? How did it make you feel?"
        height = 300
    else:  # Journal
        placeholder = "Dear Diary...\n\nWhat's on your mind today? Share your thoughts, feelings, experiences, and reflections..."
        height = 300
    
    st.session_state.canvas_content = st.text_area(
        "Content Area",
        value=st.session_state.canvas_content,
        placeholder=placeholder,
        height=height,
        key="main_content_area",
        label_visibility="collapsed"
    )
    
    # Add spacing before formatting options
    st.markdown("---")
    st.markdown("#### 🛠️ Quick Insert Tools")
    
    # Better organized formatting options
    format_row1 = st.columns(3)
    format_row2 = st.columns(3)
    
    with format_row1[0]:
        if st.button("📝 Add Quote", key="add_quote", use_container_width=True):
            st.session_state.canvas_content += '\n\n"Quote goes here"\n- Author\n'
            st.rerun()
    
    with format_row1[1]:
        if st.button("📋 Add List", key="add_list", use_container_width=True):
            st.session_state.canvas_content += '\n\n• Item 1\n• Item 2\n• Item 3\n'
            st.rerun()
    
    with format_row1[2]:
        if st.button("💭 Add Thought", key="add_thought", use_container_width=True):
            st.session_state.canvas_content += '\n\n💭 Reflection: \n'
            st.rerun()
    
    with format_row2[0]:
        if st.button("⭐ Add Highlight", key="add_highlight", use_container_width=True):
            st.session_state.canvas_content += '\n\n⭐ Important: \n'
            st.rerun()
    
    with format_row2[1]:
        if st.button("🎯 Add Goal", key="add_goal", use_container_width=True):
            st.session_state.canvas_content += '\n\n🎯 Goal: \n'
            st.rerun()
    
    with format_row2[2]:
        if st.button("🔥 Add Insight", key="add_insight", use_container_width=True):
            st.session_state.canvas_content += '\n\n🔥 Insight: \n'
            st.rerun()

def render_drawing_canvas(background_style):
    """Pure drawing canvas for sketches and artwork"""
    
    st.markdown(f"""
    <div style="
        {background_style}
        min-height: 500px; 
        padding: 30px; 
        border-radius: 15px; 
        border: 2px solid #E3E6EA;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05), 0 4px 20px rgba(0,0,0,0.1);
        position: relative;
        margin: 20px 0;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    ">
        <div style="position: absolute; top: 15px; right: 20px; color: #AAB2C6; font-size: 14px; font-weight: 500;">
            Drawing Canvas
        </div>
        <div style="color: #5873C6; margin-bottom: 20px;">
            <h3 style="margin-bottom: 15px;">🎨 Interactive Drawing Area</h3>
            <p style="color: #6B7280; font-size: 16px; margin-bottom: 10px;">HTML5 Canvas will be implemented here</p>
            <div style="background: #F8F9FA; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="color: #30404D; margin: 0; font-weight: 500;">Current Tool: {st.session_state.current_tool}</p>
                <p style="color: #30404D; margin: 5px 0 0 0;">Color: {st.session_state.current_color}</p>
                <p style="color: #30404D; margin: 5px 0 0 0;">Brush Size: {st.session_state.brush_size}px</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Drawing notes section with better spacing
    st.markdown("#### 📝 Drawing Notes & Description")
    st.session_state.canvas_content = st.text_area(
        "Sketch Description or Notes",
        value=st.session_state.canvas_content,
        placeholder="Describe your drawing, add notes about your artwork, or write about your creative process...",
        height=120,
        key="drawing_notes"
    )

def render_entry_browser():
    """Grid view for browsing saved entries"""
    
    st.markdown("### 📚 Your Creative Collection")
    
    # Filter options
    filter_cols = st.columns(4)
    with filter_cols[0]:
        filter_type = st.selectbox("Filter by Type", ["All", "Journal", "Poems", "Stories", "Special Memories", "Drawings"])
    
    with filter_cols[1]:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Title A-Z", "Title Z-A"])
    
    with filter_cols[2]:
        date_filter = st.date_input("Filter by Date", value=None, key="date_filter")
    
    with filter_cols[3]:
        search_term = st.text_input("🔍 Search entries", placeholder="Search titles, content...")
    
    # Mock entry data for demonstration
    mock_entries = [
        {
            "id": 1,
            "title": "My First Day",
            "type": "Journal",
            "date": "2024-09-18",
            "preview": "Today was an amazing day. I started my new journal and I'm excited to document my journey...",
            "mood": "Happy",
            "thumbnail": "📔"
        },
        {
            "id": 2,
            "title": "Sunset Thoughts",
            "type": "Poems",
            "date": "2024-09-17",
            "preview": "Golden rays fade away, Into the night they say, Tomorrow brings new light...",
            "mood": "Peaceful",
            "thumbnail": "🌅"
        },
        {
            "id": 3,
            "title": "Adventure Begins",
            "type": "Stories",
            "date": "2024-09-16",
            "preview": "Once upon a time, in a land far away, there lived a young explorer who dreamed of discovering...",
            "mood": "Excited",
            "thumbnail": "📖"
        },
        {
            "id": 4,
            "title": "Family Reunion",
            "type": "Special Memories",
            "date": "2024-09-15",
            "preview": "The best day ever! Our whole family came together after so long. Uncle John told his famous stories...",
            "mood": "Joyful",
            "thumbnail": "👨‍👩‍👧‍👦"
        },
        {
            "id": 5,
            "title": "Abstract Art",
            "type": "Drawings",
            "date": "2024-09-14",
            "preview": "A colorful abstract piece expressing my emotions through bold strokes and vibrant colors...",
            "mood": "Creative",
            "thumbnail": "🎨"
        }
    ]
    
    # Apply filters
    filtered_entries = mock_entries
    if filter_type != "All":
        filtered_entries = [e for e in filtered_entries if e["type"] == filter_type]
    
    if search_term:
        filtered_entries = [e for e in filtered_entries if search_term.lower() in e["title"].lower() or search_term.lower() in e["preview"].lower()]
    
    # Display entries in grid
    if filtered_entries:
        # Create grid layout
        entries_per_row = 2
        for i in range(0, len(filtered_entries), entries_per_row):
            cols = st.columns(entries_per_row)
            
            for j, col in enumerate(cols):
                if i + j < len(filtered_entries):
                    entry = filtered_entries[i + j]
                    
                    with col:
                        # Entry card
                        with st.container():
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
                                border: 1px solid #E3E6EA;
                                border-radius: 15px;
                                padding: 20px;
                                margin: 10px 0;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                                transition: transform 0.2s;
                                height: 280px;
                                display: flex;
                                flex-direction: column;
                            ">
                                <div style="text-align: center; font-size: 2rem; margin-bottom: 10px;">
                                    {entry['thumbnail']}
                                </div>
                                <h5 style="color: #5873C6; margin-bottom: 8px; font-weight: 600;">
                                    {entry['title'][:25]}{'...' if len(entry['title']) > 25 else ''}
                                </h5>
                                <div style="color: #AAB2C6; font-size: 12px; margin-bottom: 10px;">
                                    {entry['type']} • {entry['date']} • {entry['mood']}
                                </div>
                                <div style="color: #30404D; font-size: 14px; line-height: 1.4; flex-grow: 1; overflow: hidden;">
                                    {entry['preview'][:120]}{'...' if len(entry['preview']) > 120 else ''}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Action buttons
                            btn_cols = st.columns(3)
                            with btn_cols[0]:
                                if st.button("👁️", key=f"view_{entry['id']}", help="View"):
                                    st.session_state.viewing_entry = entry
                            
                            with btn_cols[1]:
                                if st.button("✏️", key=f"edit_{entry['id']}", help="Edit"):
                                    load_entry_for_editing(entry)
                            
                            with btn_cols[2]:
                                if st.button("🗑️", key=f"delete_{entry['id']}", help="Delete"):
                                    confirm_delete_entry(entry)
    else:
        st.info("No entries found matching your criteria.")

def render_search_filter():
    """Advanced search and filtering interface"""
    
    st.markdown("### 🔍 Search & Filter Your Entries")
    
    search_cols = st.columns(2)
    
    with search_cols[0]:
        st.markdown("**🔍 Search Options**")
        search_text = st.text_input("Search in content", placeholder="Enter keywords...")
        search_title = st.text_input("Search in titles", placeholder="Enter title keywords...")
        
        st.markdown("**📅 Date Range**")
        date_range = st.date_input("Select date range", value=[], key="date_range_filter")
        
    with search_cols[1]:
        st.markdown("**📂 Filter Options**")
        selected_types = st.multiselect(
            "Entry Types",
            ["Journal", "Poems", "Stories", "Special Memories", "Drawings"],
            default=["Journal", "Poems", "Stories", "Special Memories", "Drawings"]
        )
        
        mood_filter = st.multiselect(
            "Mood Filter",
            ["Very Happy", "Happy", "Neutral", "Sad", "Very Sad", "Excited", "Peaceful", "Creative", "Joyful"]
        )
    
    if st.button("🔍 Search", type="primary"):
        st.success("Search functionality will be implemented with backend integration!")
    
    # Quick stats
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    stats_cols = st.columns(4)
    with stats_cols[0]:
        st.metric("Total Entries", "23")
    with stats_cols[1]:
        st.metric("This Month", "8")
    with stats_cols[2]:
        st.metric("Favorite Type", "Journal")
    with stats_cols[3]:
        st.metric("Writing Streak", "12 days")

def save_current_entry():
    """Save the current entry to database"""
    if st.session_state.canvas_title and st.session_state.canvas_content:
        # This will be connected to the backend API
        entry_data = {
            "title": st.session_state.canvas_title,
            "type": st.session_state.current_entry_type,
            "content": st.session_state.canvas_content,
            "date": datetime.now().isoformat(),
            "background_pattern": st.session_state.background_pattern
        }
        
        # Mock save for now
        st.success(f"✅ '{st.session_state.canvas_title}' saved successfully!")
        
        # Clear the canvas for new entry
        st.session_state.canvas_content = ""
        st.session_state.canvas_title = ""
        st.rerun()
    else:
        st.error("Please add a title and some content before saving.")

def load_entry_for_editing(entry):
    """Load an existing entry for editing"""
    st.session_state.canvas_title = entry["title"]
    st.session_state.canvas_content = entry["preview"]
    st.session_state.current_entry_type = entry["type"]
    st.info(f"Loaded '{entry['title']}' for editing.")

def confirm_delete_entry(entry):
    """Confirm and delete an entry"""
    st.warning(f"Are you sure you want to delete '{entry['title']}'?")
    if st.button("Yes, Delete", key=f"confirm_delete_{entry['id']}"):
        st.success(f"Deleted '{entry['title']}'")

def render_settings():
    st.title("Settings")
    st.write("App settings and preferences will appear here.")

if __name__ == "__main__":
    main()
