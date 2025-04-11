# import pandas as pd
# import os
# import threading
# from creative_email import send_creative_email, get_html_template, get_plain_text_template
# from CTR import app as ctr_app  # Import the Flask app from CTR.py

# def load_and_filter_data(csv_file):
#     try:
#         df = pd.read_csv(csv_file)
#     except Exception as e:
#         print(f"Error reading the CSV file: {e}")
#         return None

#     required_columns = ['user_name', 'user_email', 'avg_learning_time', 'completion_rate_threshold']
#     missing_columns = [col for col in required_columns if col not in df.columns]
#     if missing_columns:
#         print(f"Missing columns in the CSV file: {missing_columns}")
#         return None

#     users_to_notify = df[df['avg_learning_time'] < df['completion_rate_threshold']]
#     return users_to_notify

# # Function to start the CTR Flask app in a separate thread
# def start_ctr_app():
#     # Start CTR Flask app on port specified by environment variable or default to 5050
#     port = int(os.getenv("CTR_PORT", 5050))
#     ctr_app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)

# def notify_users(csv_file):
#     users = load_and_filter_data(csv_file)
#     if users is None or users.empty:
#         print("No users to be notified.")
#         return

#     print("Users who need to be notified:")
#     print(users[['user_name', 'user_email', 'avg_learning_time']])
#     subject = "We Miss You at Res4City"

#     # Use absolute logo path (update if needed)
#     logo_path = "/Users/chinmaypatil/Desktop/Assesments/Sem -2/Analytics Live /Res4city - 8C/logo1.png"
#     print(f"Logo path: {logo_path}")
#     print("Logo exists:", os.path.exists(logo_path))

#     results = []  # To collect sent email results
#     for _, row in users.iterrows():
#         user_name = row['user_name']
#         user_email = row['user_email']
#         avg_learning_time = row['avg_learning_time']

#         # Pass user_email to the HTML template for tracking links
#         html_content = get_html_template(user_name, avg_learning_time, user_email)
#         plain_text_content = get_plain_text_template(user_name, avg_learning_time)

#         result = send_creative_email(user_email, subject, html_content, plain_text_content, logo_path=logo_path)
#         results.append(result)

#     # Save email send results to Excel
#     output_dir = "/Users/chinmaypatil/Desktop/Assesments/Sem -2/Analytics Live /Res4city - 8C"
#     os.makedirs(output_dir, exist_ok=True)
#     output_excel = os.path.join(output_dir, "Sent_log.xlsx")
#     results_df = pd.DataFrame(results)
#     results_df.to_excel(output_excel, index=False)
#     # print(f"Email log written to {output_excel}")

# if __name__ == "__main__":
#     # Start the CTR Flask app in a separate thread so it's available to track clicks
#     ctr_thread = threading.Thread(target=start_ctr_app)
#     # Do not set daemon=True, so the CTR app stays running
#     ctr_thread.start()

#     # Run the email sending process
#     csv_file = "/Users/chinmaypatil/Desktop/Assesments/Sem -2/Analytics Live /Res4city - 8C/testdata.csv"
#     notify_users(csv_file)

#     # Block the main thread so that the CTR Flask app remains running
#     ctr_thread.join()