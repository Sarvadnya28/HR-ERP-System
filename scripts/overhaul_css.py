import os

file_path = r"c:\Users\HP\PycharmProjects\[A]_Project_ERP_HR\static\style.css"

old_root = """:root {
  /* Default Dark (Navy) Theme */
  --bg: #0d1b2a;
  --bg-gradient: radial-gradient(ellipse at 50% 50%, #1b2e44 0%, #0d1b2a 100%);
  --navy-light: #1b2e44;
  --navy-mid: #162232;
  --teal: #17c3b2;
  --teal-dark: #0ea89a;
  --teal-glow: rgba(23, 195, 178, 0.2);
  --accent: #f0a500;
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --white: #ffffff;
  --danger: #ef4444;
  --success: #22c55e;
  --warning: #f59e0b;

  /* Glassmorphism Specs */
  --glass-bg: rgba(27, 46, 68, 0.65);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-blur: blur(12px);
  --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);

  --radius: 16px;
  --radius-sm: 10px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}"""

new_root = """:root {
  /* High-End Pro Theme */
  --primary: #17c3b2;
  --accent: #22b391;
  --bg: #0f172a;
  --bg-deep: #020617;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --white: #ffffff;
  --card-bg: rgba(30, 41, 59, 0.7);
  --glass-border: rgba(255, 255, 255, 0.1);
  --glass-glow: rgba(23, 195, 178, 0.15);
  
  --shadow-sm: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.2);
  --shadow-premium: 0 25px 50px -12px rgba(0, 0, 0, 0.5);

  --radius-xl: 24px;
  --radius-lg: 16px;
  --radius-md: 12px;
  --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}"""

old_body = """body {
  font-family: 'Inter', Arial, sans-serif;
  font-size: 15px;
  background: var(--bg);
  background-attachment: fixed;
  background-image: var(--bg-gradient);
  color: var(--text);
  min-height: 100vh;
  line-height: 1.65;
  transition: background 0.5s ease;
}"""

new_body = """body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  font-size: 16px;
  background-color: var(--bg);
  background-image: 
    radial-gradient(at 0% 0%, hsla(173,85%,41%,0.15) 0, transparent 50%), 
    radial-gradient(at 50% 0%, hsla(217,91%,60%,0.1) 0, transparent 50%),
    radial-gradient(at 100% 0%, hsla(173,85%,41%,0.15) 0, transparent 50%);
  background-attachment: fixed;
  color: var(--text-main);
  min-height: 100vh;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}"""

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found.")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(old_root, new_root)
content = content.replace(old_body, new_body)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CSS Overhaul Applied Successfully with absolute paths.")
