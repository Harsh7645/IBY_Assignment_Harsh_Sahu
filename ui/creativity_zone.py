import streamlit as st
from datetime import datetime, timedelta

def creativity_zone(creativity_agent):
    zone = CreativityZone(creativity_agent)
    zone.render()

class CreativityZone:
    def __init__(self, creativity_agent):
        self.creativity = creativity_agent

    def render(self):
        st.title("Creative Canvas")
        
        # Sidebar for navigation
        tab = st.sidebar.radio("Choose Section", 
                              ["Write New Entry", "Browse Entries", "Search & Tags"],
                              key="creativity_section")
        
        if tab == "Write New Entry":
            self.render_new_entry()
        elif tab == "Browse Entries":
            self.render_browse_entries()
        else:
            self.render_search()

    def render_new_entry(self):
        st.subheader("New Entry")
        
        title = st.text_input("Title")
        entry_type = st.selectbox("Entry Type", 
                                 ["Journal", "Poetry", "Story", "Ideas", "Goals"])
        
        # Mood selector with emojis
        mood = st.select_slider("How are you feeling?",
                              ["😔", "😕", "😐", "🙂", "😊"])
        
        # Tags input
        tags = st.text_input("Tags (comma separated)")
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
        
        content = st.text_area("Write your thoughts...", height=300)
        
        if st.button("Save Entry"):
            if title and content:
                self.creativity.add_entry(entry_type, title, content, 
                                        mood=mood, tags=tag_list)
                st.success("Entry saved successfully!")
            else:
                st.error("Please fill in title and content")

    def render_browse_entries(self):
        st.subheader("Your Entries")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            entry_type = st.selectbox("Filter by type", 
                                    ["All", "Journal", "Poetry", "Story", "Ideas", "Goals"])
        with col2:
            timeframe = st.selectbox("Time period", 
                                   ["All time", "This month", "This week", "Today"])
        
        # Get entries based on filters
        start_date = None
        if timeframe != "All time":
            start_date = datetime.now()
            if timeframe == "This month":
                start_date = start_date.replace(day=1, hour=0, minute=0, second=0)
            elif timeframe == "This week":
                start_date -= timedelta(days=start_date.weekday())
            else:  # Today
                start_date = start_date.replace(hour=0, minute=0, second=0)
        
        entries = self.creativity.get_entries(
            entry_type=None if entry_type == "All" else entry_type,
            start_date=start_date
        )
        
        # Display entries
        for entry in entries:
            with st.expander(f"{entry[2]} - {entry[6][:10]}"):
                st.write(f"Type: {entry[1]}")
                if entry[4]:  # mood
                    st.write(f"Mood: {entry[4]}")
                st.write(entry[3])  # content
                
                # Edit/Delete buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_{entry[0]}"):
                        st.session_state.editing_entry = entry[0]
                with col2:
                    if st.button("Delete", key=f"delete_{entry[0]}"):
                        self.creativity.delete_entry(entry[0])
                        st.experimental_rerun()

    def render_search(self):
        st.subheader("Search Entries")
        
        search_term = st.text_input("Search by title or content")
        tag_search = st.text_input("Search by tag")
        
        if search_term or tag_search:
            entries = self.creativity.get_entries(tag=tag_search)
            
            if not entries:
                st.info("No entries found matching your search.")
            else:
                for entry in entries:
                    with st.expander(f"{entry[2]} - {entry[6][:10]}"):
                        st.write(f"Type: {entry[1]}")
                        st.write(entry[3])  # content
