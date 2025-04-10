from flask import Flask, request, redirect 
import datetime
import os
import sys
import re
import pandas as pd

app = Flask(__name__)

# Create an empty log file if it doesn't exist
if not os.path.exists('click_log.txt'):
    open('click_log.txt', 'w').close()

@app.route('/redirect')
def track_and_redirect():
    # Get parameters: user_id and destination URL 
    user_id = request.args.get('user_id', 'unknown')
    destination = request.args.get('dest', 'https://www.res4city.eu')
    
    # Log the click event into a text file
    log_entry = f"{datetime.datetime.now()} - Click from user: {user_id} redirected to {destination}\n"   
    with open('click_log.txt', 'a') as log_file:            
        log_file.write(log_entry)

    # Redirect the user to the destination
    return redirect(destination)

# [UPDATED] Export function that aggregates clicks by unique user and updates (merges) with an existing Excel file
def export_clicks_by_user(log_file_path, excel_file_path):
    """Reads the click_log.txt file, aggregates click counts by unique user,
       and updates (merges) the data into an Excel file. Existing click counts will be summed."""
    # Aggregate click counts from the log file
    click_counts = {}
    if not os.path.exists(log_file_path):
        print(f"Log file {log_file_path} does not exist.")
        return
    
    with open(log_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Expected format:
            # "YYYY-MM-DD HH:MM:SS.ssssss - Click from user: <user_id> redirected to <destination>"
            match = re.match(r'(.+?) - Click from user: (.+?) redirected to (.+)', line)
            if match:
                _, user_id, _ = match.groups()
                click_counts[user_id] = click_counts.get(user_id, 0) + 1

    # Convert the aggregated data into a DataFrame
    new_data = [{"User ID": uid, "Click Count": count} for uid, count in click_counts.items()]
    df_new = pd.DataFrame(new_data)

    # [UPDATED] Check if the Excel file already exists
    if os.path.exists(excel_file_path):
        df_existing = pd.read_excel(excel_file_path)
        # Ensure the "Click Count" column exists; if not, add it with 0
        if "Click Count" not in df_existing.columns:
            df_existing["Click Count"] = 0
        # Merge the new data with existing data on "User ID"
        df_merged = pd.merge(df_existing, df_new, on="User ID", how="outer", suffixes=('_old', '_new'))
        df_merged["Click Count_old"] = df_merged["Click Count_old"].fillna(0)
        df_merged["Click Count_new"] = df_merged["Click Count_new"].fillna(0)
        # Sum old and new counts
        df_merged["Click Count"] = df_merged["Click Count_old"] + df_merged["Click Count_new"]
        # Keep only relevant columns
        df_final = df_merged[["User ID", "Click Count"]]
    else:
        # If no existing file, use new data directly
        df_final = df_new

    # Write the final DataFrame to Excel
    df_final.to_excel(excel_file_path, index=False)
    print(f"Unique user click log exported/updated to {excel_file_path}")

if __name__ == '__main__':
    # If the script is run with "--export", export the click log instead of running the server.
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_clicks_by_user('click_log.txt', 'click_log.xlsx')
    else:
        app.run(debug=True, host='0.0.0.0', port=5050)