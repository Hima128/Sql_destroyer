# SQL Destroyer 

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Code Explanation](#code-explanation)
   - [fetch_page Function](#fetch_page-function)
   - [find_sql_injection_vulnerabilities Function](#find_sql_injection_vulnerabilities-function)
   - [run_sqlmap Function](#run_sqlmap-function)
   - [check_website Function](#check_website-function)
   - [add_proxy Function](#add_proxy-function)
6. [User Interface](#user-interface)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

The Website Security Scanner with SQLMap Integration is a Python-based tool that helps in identifying SQL injection vulnerabilities in websites. It allows users to:
- Fetch and analyze web pages for potential SQL injection patterns.
- Integrate and run SQLMap to further assess vulnerabilities.
- Add and manage proxies for requests.

## Requirements

- Python 3.x
- `requests` library
- `tkinter` library (usually included with Python)
- `subprocess` library (part of the standard library)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required libraries:**
   ```bash
   pip install requests
   ```

3. **Ensure SQLMap is installed:**
   SQLMap should be installed and accessible from the command line. You can download it from [SQLMap's official website](http://sqlmap.org/).

## Usage

Run the script using Python:
```bash
python3 tool.py
```
A GUI window will appear allowing you to enter a website URL, add proxies, and scan for SQL injection vulnerabilities.

## Code Explanation

### fetch_page Function

```python
def fetch_page(url):
    """
    Fetch the HTML content of the given URL using a random User-Agent and optional proxies.
    """
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
        proxy = random.choice(proxies) if proxies else None
        response = requests.get(url, headers=headers, proxies=proxy)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch page: {e}")
        return None
```
This function fetches the HTML content of a URL using a random User-Agent and optional proxies.

### find_sql_injection_vulnerabilities Function

```python
def find_sql_injection_vulnerabilities(html_content):
    """
    Search for SQL injection patterns in the provided HTML content.
    """
    sql_injection_patterns = [
        r'\bSELECT\b.*?\bFROM\b',
        r'\bINSERT INTO\b.*?\bVALUES\b',
        r'\bUPDATE\b.*?\bSET\b',
        r'\bDELETE FROM\b.*?\bWHERE\b',
        r'\bUNION\b.*?\bSELECT\b',
        r'\bOR\b.*?\b1=1\b',
        # Add more patterns as needed
    ]

    vulnerabilities_found = []

    for pattern in sql_injection_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            vulnerabilities_found.extend(matches)

    return vulnerabilities_found
```
This function searches for common SQL injection patterns in the provided HTML content.

### run_sqlmap Function

```python
def run_sqlmap(url):
    """
    Run SQLMap on the provided URL and return the output.
    """
    command = f"sqlmap -u {url} --batch --risk 3 --level 5 --dbs"
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running SQLMap: {e.stderr}"
```
This function runs SQLMap on the provided URL and returns the output.

### check_website Function

```python
def check_website():
    """
    Check the given website for SQL injection vulnerabilities and run SQLMap.
    """
    website_url = url_entry.get()
    if not website_url:
        messagebox.showwarning("Warning", "Please enter a website URL.")
        return

    html_content = fetch_page(website_url)
    if not html_content:
        return

    vulnerabilities = find_sql_injection_vulnerabilities(html_content)
    result_text.delete(1.0, tk.END)
    if vulnerabilities:
        result_text.insert(tk.END, "SQL Injection vulnerabilities found:\n")
        for vulnerability in vulnerabilities:
            result_text.insert(tk.END, vulnerability + "\n")
    else:
        result_text.insert(tk.END, "No SQL Injection vulnerabilities found.\n")

    # Run SQLMap and display results
    sqlmap_result = run_sqlmap(website_url)
    result_text.insert(tk.END, "\nSQLMap results:\n")
    result_text.insert(tk.END, sqlmap_result)
```
This function checks the website for SQL injection vulnerabilities and runs SQLMap, displaying the results in the GUI.

### add_proxy Function

```python
def add_proxy():
    """
    Add a new proxy to the list from the user input.
    """
    proxy = proxy_entry.get()
    if proxy:
        proxies.append({'http': f'http://{proxy}', 'https': f'http://{proxy}'})
        proxy_list_text.insert(tk.END, f'{proxy}\n')
        proxy_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a proxy.")
```
This function allows users to add a new proxy to the list from the user input.

## User Interface

- **Enter website URL**: Input field for entering the website URL to be scanned.
- **Enter proxy (IP:Port)**: Input field for entering a proxy in the format IP:Port.
- **Add Proxy**: Button to add the entered proxy to the list.
- **Proxies**: Text box displaying the list of added proxies.
- **Scan Website**: Button to initiate the scan.
- **Results**: Text box displaying the results of the scan and SQLMap output.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.