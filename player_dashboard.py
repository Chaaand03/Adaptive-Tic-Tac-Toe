from taipy import Gui

from taipy.gui import Gui
import taipy.gui.builder as tgb
import plotly.graph_objects as go
from taipy.gui import Gui, Markdown
import taipy.gui.builder as tgb


import pandas as pd


from taipy.gui import Markdown

text = "Welcome to the user dashboard!"



home_md = Markdown("""
<|navbar|>

# Home

<|{text}|>
""")



data = {
    "Topic": ["Geometry", "Calculas", "Trigonometry"],
    "Total Questions": ["12","25","40"],
    "Correct Answers": ["2", "10", "20"],
    "Wrong Answers": ["10","15","20"],
    "Accuracy": [16.67, 40, 50],
}
score_table = pd.DataFrame(data)

table_md = Markdown("""# User Dashboard - Tabular Data
<|{score_table}|table|>
""")

chart_data = {
    "Topic": ["Geometry", "Calculas", "Trigonometry"],
    "Questions" : [12, 25, 40]
}

tgb.chart(f"{chart_data}", type="pie", values="Area", labels="Topics")

property_chart = {"type":"bar"
                 }


page = """# User Dashboard - Chart Data
<|{dataframe}|chart|properties={property_chart}|>
"""
dataframe = pd.DataFrame(chart_data)


chart_md = Markdown(page)


# from taipy.gui import Gui, Markdown
# import pandas as pd
#
# food_df = pd.DataFrame({
#     "Meal": ["Lunch", "Dinner", "Lunch", "Lunch", "Breakfast", "Breakfast", "Lunch", "Dinner"],
#     "Category": ["Food", "Food", "Drink", "Food", "Food", "Drink", "Dessert", "Dessert"],
#     "Name": ["Burger", "Pizza", "Soda", "Salad", "Pasta", "Water", "Ice Cream", "Cake"],
#     "Calories": [300, 400, 150, 200, 500, 0, 400, 500],
# })
#
# main_md = Markdown("<|{food_df}|table|>")
#
# Gui(page=main_md).run(debug=True,port=8000)

pages = {
    "/": "<|navbar|>",
    "table": table_md,
    "chart": chart_md
}

Gui(pages=pages).run(debug=True,port=8000)