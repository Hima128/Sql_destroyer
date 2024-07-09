
---

## Website Security Scanner with SQLMap Integration

### Overview
This tool is designed to scan a given website for SQL injection vulnerabilities. It integrates basic web page fetching and SQL injection pattern matching. Additionally, it leverages SQLMap, a powerful penetration testing tool, to provide more advanced security checks.

### Features
- Fetches web page content using requests library.
- Identifies potential SQL injection vulnerabilities using regex patterns.
- Integrates SQLMap for in-depth SQL injection testing.
- Provides a simple graphical user interface (GUI) for ease of use.

### Requirements
- Python 3.x
- `requests` library (`pip install requests`)
- SQLMap (installed separately)

### Installation
1. Install Python 3.x from [python.org](https://www.python.org/downloads/).
2. Install required Python libraries:
   ```
   pip install requests
   ```
3. Install SQLMap. Download and installation instructions are available at [sqlmap.org](https://sqlmap.org/).

### Usage
1. Launch the application:
   ```
   python app.py
   ```
2. Enter the URL of the website you want to scan in the provided input field.
3. Click on the "Scan Website" button to initiate the scan.

### Example
```python
import requests
import re
import tkinter as tk
from tkinter import messagebox
import subprocess
import random

# Function definitions here...

# GUI initialization and event loop (mainloop) here...
```

### Notes
- Ensure proper permissions and legal authorization before scanning websites you do not own.
- Results from SQLMap should be interpreted carefully and used responsibly.

### Future Enhancements
- Proxy support for bypassing stricter firewalls.
- Enhanced error handling and logging.
- Integration with additional security testing tools for comprehensive testing.
---


