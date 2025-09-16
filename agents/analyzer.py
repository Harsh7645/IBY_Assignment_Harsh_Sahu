class AnalyzerAgent:
    def __init__(self):
        self.events = []

    def add_event(self, agent, action, timestamp, details=None):
        self.events.append({'agent': agent, 'action': action, 'timestamp': timestamp, 'details': details})

    def get_summary(self):
        return self.events
