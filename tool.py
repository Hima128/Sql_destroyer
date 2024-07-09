import requests
import re
import tkinter as tk
from tkinter import messagebox
import subprocess
import random
import time

def fetch_page(url):
    # Generate a random User-Agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        # Add more User-Agents as needed
    ]
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch page: {e}")
        return None

def find_sql_injection_vulnerabilities(html_content):
    # Search for SQL injection patterns in the text
    sql_injection_patterns = [
        r'\bSELECT\b.*?\bFROM\b',
        r'\bINSERT INTO\b.*?\bVALUES\b',
        r'\bUPDATE\b.*?\bSET\b',
        r'\bDELETE FROM\b.*?\bWHERE\b',
        # Add more patterns as needed
    ]
    
    vulnerabilities_found = []
    
    for pattern in sql_injection_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            vulnerabilities_found.extend(matches)
    
    return vulnerabilities_found

def run_sqlmap(url):
    # Use SQLMap via subprocess
    command = f"sqlmap -u {url} --batch --risk 3 --level 5 --dbs"  # Adjust options as needed
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running SQLMap: {e.stderr}"

def check_website():
    website_url = url_entry.get()
    if website_url:
        html_content = fetch_page(website_url)
        if html_content:
            vulnerabilities = find_sql_injection_vulnerabilities(html_content)
            if vulnerabilities:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "SQL Injection vulnerabilities found:\n")
                for vulnerability in vulnerabilities:
                    result_text.insert(tk.END, vulnerability + "\n")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "No SQL Injection vulnerabilities found.\n")

            # Run SQLMap and display results
            sqlmap_result = run_sqlmap(website_url)
            result_text.insert(tk.END, "\nSQLMap results:\n")
            result_text.insert(tk.END, sqlmap_result)
        else:
            result_text.delete(1.0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a website URL.")

# Create tkinter window
root = tk.Tk()
root.title("Website Security Scanner with SQLMap Integration")

# Add a nice banner
banner = """   _____ ____    __         ____  _____________________  ______  ____________ 
  / ___// __ \  / /        / __ \/ ____/ ___/_  __/ __ \/ __ \ \/ / ____/ __ \
  \__ \/ / / / / /        / / / / __/  \__ \ / / / /_/ / / / /\  / __/ / /_/ /
 ___/ / /_/ / / /___     / /_/ / /___ ___/ // / / _, _/ /_/ / / / /___/ _, _/ 
/____/\___\_\/_____/____/_____/_____//____//_/ /_/ |_|\____/ /_/_____/_/ |_|  
                  /_____/                                                     """
banner_label = tk.Label(root, text=banner, font=("Courier", 14))
banner_label.pack(pady=10)

# Add URL input field
url_label = tk.Label(root, text="Enter website URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Scan button
scan_button = tk.Button(root, text="Scan Website", command=check_website)
scan_button.pack(pady=10)

# Text box to display results
result_text = tk.Text(root, width=80, height=20)
result_text.pack(pady=10)

root.mainloop()