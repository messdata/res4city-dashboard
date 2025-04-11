import dash
from dash import html, dcc, dash_table, Output, Input
import pandas as pd
import datetime
import os
import re

sent_log_path = "/Users/chinmaypatil/Desktop/Assesments/Sem -2/Analytics Live /Res4city - 8C/Sent_log.xlsx"
click_log_path = "click_log.txt"

app = dash.Dash(__name__)
app.title = "Res4City | Engagement Dashboard"

app.layout = html.Div([
    html.Div([
        html.Img(src="https://www.res4city.eu/wp-content/uploads/2023/03/res4city-logo-1.svg", style={"height": "60px", "marginRight": "20px"}),
        html.H1("Res4City Email Engagement Dashboard", style={"color": "#002f5b", "fontWeight": "bold", "fontSize": "28px"}),
    ], style={"display": "flex", "alignItems": "center", "padding": "20px 30px", "backgroundColor": "#f9f9f9", "borderBottom": "2px solid #002f5b"}),

    html.Div([
        html.Button("🔄 Refresh", id="refresh-btn", n_clicks=0, style={"margin": "20px 0", "padding": "10px 20px", "fontSize": "16px", "backgroundColor": "#00a3e0", "color": "white", "border": "none", "borderRadius": "6px"}),
        dcc.Interval(id="auto-refresh", interval=30 * 1000, n_intervals=0),
        html.Div(id="stats"),
        html.Hr(style={"borderColor": "#ccc"}),
        html.H2("📋 User Click Logs", style={"marginTop": "20px", "color": "#002f5b"}),
        html.Div(id="table-div")
    ], style={"padding": "30px", "fontFamily": "'Segoe UI', sans-serif", "backgroundColor": "#f4f6f8"})
])

def load_data():
    if not os.path.exists(sent_log_path):
        return None, None

    sent_log = pd.read_excel(sent_log_path)

    click_data = []
    if os.path.exists(click_log_path):
        with open(click_log_path, "r") as f:
            for line in f:
                match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?) - Click from user: (\S+?) redirected", line)
                if match:
                    timestamp, email = match.groups()
                    click_data.append({"timestamp": timestamp, "email": email})

    click_df = pd.DataFrame(click_data)
    if not click_df.empty:
        click_df["timestamp"] = pd.to_datetime(click_df["timestamp"])

    if "user_email" in sent_log.columns:
        sent_log["clicked"] = sent_log["user_email"].isin(click_df["email"])
    else:
        sent_log["clicked"] = False

    merged_df = pd.merge(sent_log, click_df, how="left", left_on="user_email", right_on="email")

    if "send_time" in merged_df.columns:
        merged_df["send_time"] = pd.to_datetime(merged_df["send_time"], errors='coerce')
        merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"], errors='coerce')
        merged_df["time_to_click"] = (merged_df["timestamp"] - merged_df["send_time"]).dt.total_seconds() / 60
    else:
        merged_df["time_to_click"] = None

    return sent_log, merged_df

@app.callback(
    Output("stats", "children"),
    Output("table-div", "children"),
    Input("refresh-btn", "n_clicks"),
    Input("auto-refresh", "n_intervals")
)
def update_dashboard(n_clicks, n_intervals):
    sent_log, merged_df = load_data()

    if sent_log is None or merged_df is None:
        return html.Div("❌ Data not available"), html.Div("")

    stat_box_style = {
        "width": "24%",
        "display": "inline-block",
        "backgroundColor": "white",
        "padding": "15px",
        "margin": "10px",
        "borderRadius": "8px",
        "boxShadow": "0 1px 4px rgba(0, 0, 0, 0.1)",
        "textAlign": "center",
        "borderLeft": "5px solid #00a3e0"
    }

    stats = html.Div([
        html.Div([
            html.H4("Emails Sent", style={"color": "#555"}),
            html.H2(len(sent_log), style={"color": "#002f5b"})
        ], style=stat_box_style),

        html.Div([
            html.H4("Total Clicks", style={"color": "#555"}),
            html.H2(merged_df["clicked"].sum(), style={"color": "#002f5b"})
        ], style=stat_box_style),

        html.Div([
            html.H4("Click Rate", style={"color": "#555"}),
            html.H2(f"{(merged_df['clicked'].mean() * 100):.2f}%", style={"color": "#002f5b"})
        ], style=stat_box_style),

        html.Div([
            html.H4("Avg. Time to Click (min)", style={"color": "#555"}),
            html.H2(f"{merged_df['time_to_click'].mean():.2f}" if merged_df["time_to_click"].notnull().any() else "—", style={"color": "#002f5b"})
        ], style=stat_box_style)
    ], style={"display": "flex", "flexWrap": "wrap", "justifyContent": "space-around"})

    table = dash_table.DataTable(
        data=merged_df.fillna("").to_dict("records"),
        columns=[{"name": i, "id": i} for i in merged_df.columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto", "border": "1px solid #ccc"},
        style_cell={"textAlign": "left", "padding": "10px", "backgroundColor": "#fff"},
        style_header={"backgroundColor": "#002f5b", "color": "white", "fontWeight": "bold"}
    )

    return stats, table
    # if __name__ == "__main__":
#     app.run(debug=True, port=8050)

    app = dash.Dash(__name__)
application = app.server  # For Render/Gunicorn  # For WSGI


