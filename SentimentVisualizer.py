import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class SentimentVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.polarity_data = []
        self.subjectivity_data = []
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=1000)
        self.batch_id = 0

    def update_plot(self, i):
        self.ax.clear()
        self.ax.plot(self.polarity_data, label='Polarity')
        self.ax.plot(self.subjectivity_data, label='Subjectivity')
        self.ax.set_ylim(-1, 1)
        self.ax.set_title(f'Real-time Sentiment Analysis - Batch: {self.batch_id}')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Sentiment Score')
        self.ax.legend()

    def add_data(self, polarity, subjectivity, batch_id):
        self.polarity_data.append(polarity)
        self.subjectivity_data.append(subjectivity)
        self.batch_id = batch_id

    def show_plot(self):
        plt.show()