import taipy.gui.builder as tgb
import plotly.graph_objects as go

num_correct = 75
num_incorrect = 25

# Create a pie chart
fig = go.Figure(data=go.Pie(labels=['Correct', 'Incorrect'], values=[num_correct, num_incorrect]))

with tgb.Page() as page:
    tgb.chart(figure=fig)

page.show()
