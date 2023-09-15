import tkinter as tk
import threading
import os
import subprocess


# Define functions to execute when buttons are clicked
def generate_mock_data():
    mock_data_thread = threading.Thread(target=lambda: os.system("python data.py"))
    mock_data_thread.start()


def openai_reviews_analysis():
    rev_analysis_thread = threading.Thread(target=lambda: os.system("python openAI_review_analysis.py"))
    rev_analysis_thread.start()


def dynamic_price_optimization():
    def run_pricing_model():
        # Execute pricing_model.py and capture its output
        try:
            output = subprocess.check_output(["python", "pricing_model.py"], universal_newlines=True)
            update_output_text(output)
        except subprocess.CalledProcessError as e:
            # Handle errors if needed
            update_output_text(f"Error: {e.output}")

    pricing_thread = threading.Thread(target=run_pricing_model)
    pricing_thread.start()


def personalized_offers():
    per_offer_thread = threading.Thread(target=lambda: os.system("python openAI_prsnlizd_pricing.py"))
    per_offer_thread.start()


def open_website():
    os.system("python webapp.py")


# Create the main window
root = tk.Tk()
root.title("OpenAI Powered Dynamic Pricing Engine")

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20, padx=20, anchor="center")

# Create and pack buttons
button1 = tk.Button(button_frame, text="Generate Mock Data", command=generate_mock_data, width=20)
button2 = tk.Button(button_frame, text="OpenAI Reviews Analysis", command=openai_reviews_analysis, width=20)
button3 = tk.Button(button_frame, text="Dynamic Price Optimization", command=dynamic_price_optimization, width=25)
button4 = tk.Button(button_frame, text="Generate Personalized Offers", command=personalized_offers, width=25)
button5 = tk.Button(button_frame, text="Open Website", command=open_website, width=15)

button1.pack(side="left", padx=10)
button2.pack(side="left", padx=10)
button3.pack(side="left", padx=10)
button4.pack(side="left", padx=10)
button5.pack(side="left", padx=10)

# Create a frame for the title
title_frame = tk.Frame(root)
title_frame.pack(pady=20, padx=20, anchor="center")

# Create and pack title label
title_label = tk.Label(title_frame, text="OpenAI Powered Dynamic Pricing Engine", font=("Helvetica", 20))
title_label.pack()

# Create a frame for the output text
output_frame = tk.Frame(root)
output_frame.pack(pady=20, padx=20, anchor="center")

# Create and pack output text widget
output_text = tk.Text(output_frame, height=5, width=50, font=("Helvetica", 12))
output_text.pack()


# Function to update output_text
def update_output_text(text):
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)


# Replace this function with your actual pricing_model.py output
def run_pricing_model():
    pricing_output = "Sales to be maximized..."
    update_output_text(pricing_output)


# Start pricing_model.py thread
pricing_thread = threading.Thread(target=run_pricing_model)
pricing_thread.start()

root.mainloop()
