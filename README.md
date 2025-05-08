# 🏀 NBA Match Simulator

A Flask-based NBA match simulator deployed on AWS EC2, reverse proxied via NGINX, and SSH-authenticated. Simulates single games or best-of-7 series with emoji-based highlights and top scorer stats. Built as a hands-on DevOps and Python full-stack deployment challenge.

> 🎯 **Live Demo:** [http://54.79.168.37](http://54.79.168.37)

---

## 🚀 Features

- 🏀 Choose from 6 NBA teams: Lakers, Celtics, Warriors, Bucks, Suns, Nuggets
- 📊 Simulate single games or best-of-7 playoff series
- 🔥 Emoji-based highlights for key plays (e.g. 🔥 coast-to-coast slam!)
- 🧠 Randomized score and top scorer stats
- 📱 Responsive design (works on desktop and mobile)
- 🧵 Stateless Python/Flask backend — no database
- ☁️ Hosted on AWS EC2 with reverse proxy via NGINX
- 🔐 SSH-secured EC2 access (GitHub passwordless auth only)

---

## 🛠️ Tech Stack

| Layer        | Stack / Tool                    |
|--------------|---------------------------------|
| Frontend     | HTML + CSS (no framework)       |
| Backend      | Python 3.12 + Flask             |
| Infra        | AWS EC2 (Amazon Linux 2023)     |
| Web Server   | NGINX reverse proxy             |
| Deployment   | Manual SSH + Python venv + systemd |
| GitHub       | SSH key-based repo management   |

---

## 🧰 Project Structure

nba_simulator_web/
├── app.py # Flask app main logic
├── static/ # Optional assets (currently unused)
├── templates/
│ └── index.html # Web interface
├── venv/ # Python virtual environment (excluded in .gitignore)
└── README.md # You're reading it

---

## ⚙️ Deployment Notes

### 🖥️ EC2 Configuration

- **Instance**: `t2.micro` (Amazon Linux 2023)
- **Open ports**:
  - `22` (SSH)
  - `80` (HTTP for NGINX)
  - `5000` (Flask, internal only)

### 🔁 NGINX Proxy Setup

**File**: `/etc/nginx/nginx.conf`

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


💡 Tips from Deployment
Flask only binds to port 80 with sudo or setcap — better to reverse proxy with NGINX

Amazon Linux uses /etc/nginx/conf.d/ and nginx.conf by default

Port 5000 shouldn't be exposed publicly — use 127.0.0.1

403 Forbidden often = NGINX falling back to its default /usr/share/nginx/html root

NGINX restarts silently unless you run nginx -t before restarting (always test first)

🧪 How to Run Locally
bash
Copy
Edit
git clone git@github.com:maltrbl/nba-match-simulator.git
cd nba-match-simulator
python3 -m venv venv
source venv/bin/activate
pip install flask
python app.py
