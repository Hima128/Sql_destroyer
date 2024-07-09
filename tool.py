import requests
import re
import tkinter as tk
from tkinter import messagebox
import subprocess
import random
import time

def fetch_page(url):
    # توليد User-Agent عشوائي
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        # يمكنك إضافة المزيد من User-Agent حسب الحاجة
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
    # بحث عن أنماط SQL injection في النص
    sql_injection_patterns = [
        r'\bSELECT\b.*?\bFROM\b',
        r'\bINSERT INTO\b.*?\bVALUES\b',
        r'\bUPDATE\b.*?\bSET\b',
        r'\bDELETE FROM\b.*?\bWHERE\b',
        # يمكنك إضافة أنماط إضافية حسب الحاجة
    ]
    
    vulnerabilities_found = []
    
    for pattern in sql_injection_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            vulnerabilities_found.extend(matches)
    
    return vulnerabilities_found

def run_sqlmap(url):
    # استخدام SQLMap بواسطة subprocess
    command = f"sqlmap -u {url} --batch --risk 3 --level 5 --dbs"  # قم بتعديل الخيارات حسب احتياجاتك
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

            # تشغيل SQLMap وعرض النتائج
            sqlmap_result = run_sqlmap(website_url)
            result_text.insert(tk.END, "\nSQLMap results:\n")
            result_text.insert(tk.END, sqlmap_result)
        else:
            result_text.delete(1.0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a website URL.")

# إنشاء نافذة tkinter
root = tk.Tk()
root.title("Website Security Scanner with SQLMap Integration")

# إضافة بانر أنيق
banner = """
 _____      _        _______          _ 
|  __ \    | |      |__   __|        | |
| |__) |__ | |_ _______| | ___   ___ | |
|  ___/ _ \| __|______| |/ _ \ / _ \| |
| |  | (_) | |_       | | (_) | (_) | |
|_|   \___/ \__|      |_|\___/ \___/|_|
"""
banner_label = tk.Label(root, text=banner, font=("Courier", 14))
banner_label.pack(pady=10)

# إضافة حقل إدخال لعنوان URL
url_label = tk.Label(root, text="Enter website URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# زر لبدء الفحص
scan_button = tk.Button(root, text="Scan Website", command=check_website)
scan_button.pack(pady=10)

# مربع نصي لعرض النتائج
result_text = tk.Text(root, width=80, height=20)
result_text.pack(pady=10)

root.mainloop()