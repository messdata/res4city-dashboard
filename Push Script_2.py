import pandas as pd
import os
import threading
from email_structure import send_creative_email, get_html_template, get_plain_text_template
from CTR import app as ctr_app  # Import the Flask app from CTR.py

def load_and_filter_data(excel_file):
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None, None

    required_columns = ['user_id', 'email', 'Course_Code', 'Hours_Since_Course_Signup',
                        'Course_Completed', 'prediction(Course_Completed)']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing columns in the Excel file: {missing_columns}")
        return None, None

    # Identify profile incomplete rows (e.g., where Course_Code is missing)
    incomplete_profiles = df[df['Course_Code'].isnull() | (df['Course_Code'].astype(str).str.strip() == '') | df['email'].isnull() | (df['email'].astype(str).str.strip() == '')]
    
    users_to_notify = df[
        (df['Course_Completed'].str.lower() == 'no') &
        (df['prediction(Course_Completed)'].str.lower() == 'no') &
        (df['Hours_Since_Course_Signup'] > 90) &
        (~df.index.isin(incomplete_profiles.index))
    ]
    return users_to_notify, incomplete_profiles

# Function to start the CTR Flask app in a separate thread
def start_ctr_app():
    port = int(os.getenv("CTR_PORT", 5050))
    ctr_app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)

def notify_users(excel_file):
    users, incomplete_profiles = load_and_filter_data(excel_file)
    if users is None:
        print("Error in loading data.")
        return

    if users.empty and incomplete_profiles.empty:
        print("No users to notify and no incomplete profiles.")
        return

    if not users.empty:
        print("Users who need to be notified:")
        print(users[['user_id', 'email', 'Hours_Since_Course_Signup']])
        print(f"\n📬 Total emails to be sent: {len(users)}\n")
    else:
        print("No users to notify based on filter criteria.")

    if not incomplete_profiles.empty:
        print("\nPROFILE INCOMPLETE (missing Course_Code):")
        print(incomplete_profiles[['user_id', 'email']])
    else:
        print("\nAll profiles complete.")

    subject = "We Miss You at Res4City"
    logo_path = "/Users/chinmaypatil/Desktop/Assesments/Sem -2/Analytics Live /Res4city - 8C/logo1.png"
    print(f"Logo path: {logo_path}")
    print("Logo exists:", os.path.exists(logo_path))

    results = []
    for _, row in users.iterrows():
        user_name = row.get('user_id')
        user_email = row.get('email')
        hours_since_signup = row.get('Hours_Since_Course_Signup')
        course_code = row.get('Course_Code')

        html_content = get_html_template(user_name, hours_since_signup, user_email, course_code)
        plain_text_content = get_plain_text_template(user_name, hours_since_signup, course_code)

        result = send_creative_email(user_email, subject, html_content, plain_text_content, logo_path=logo_path)
        from datetime import datetime
        #timestamp 
        result["send_time"] = datetime.now()
        results.append(result)



    output_dir = "/Users/chinmaypatil/Desktop/Assesments/Sem -2/Analytics Live /Res4city - 8C"
    os.makedirs(output_dir, exist_ok=True)
    output_excel = os.path.join(output_dir, "Sent_log.xlsx")
    results_df = pd.DataFrame(results)
    results_df.to_excel(output_excel, index=False)

# --- Auto Push to GitHub after updating logs ---
def auto_push_logs():
    print("\n📤 Syncing logs to GitHub...")
    os.system("git add ./Sent_log.xlsx ./click_log.txt")
    os.system("git commit -m 'Auto log sync from Push Script_2.py'")
    os.system("git push origin main")
    print(" Logs synced to GitHub successfully.")

if __name__ == "__main__":
    ctr_thread = threading.Thread(target=start_ctr_app)
    ctr_thread.start()

    excel_file = "Model_Output.xlsx"
    notify_users(excel_file)


    # ctr_thread.join()
  

    auto_push_logs()
  # ctr_thread.join()

 

