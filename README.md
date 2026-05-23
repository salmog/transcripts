# YouTube Trading Transcript Analyzer
A system to scan finance channels, extract transcripts (EN/HE), and use AI to output structured JSON trading setups.
On Ubuntu (Linux VM):

Bash
# Update and install Python, pip, venv, and Git
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl

# Install Ollama (Official Linux Script)
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
Step 2: Start the Local AI
Bash
# 1. Start the Ollama background service
# (On Mac: brew services start ollama | On Ubuntu: sudo systemctl start ollama)
# If unsure, run it manually in the background:
nohup ollama serve > ollama.log 2>&1 &
disown

# 2. Download the Llama 3 model (Requires ~4.7GB download)
ollama pull llama3
Step 3: Clone & Setup the Python Environment
Bash
# 1. Clone the repository
git clone git@github.com:salmog/transcripts.git
cd transcripts

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt
Step 4: Configure Streamlit (Bypass Email Prompt)
Bash
mkdir -p ~/.streamlit
echo '[general]' > ~/.streamlit/credentials.toml
echo 'email = ""' >> ~/.streamlit/credentials.toml
Step 5: Start the Background Services
Bash
# 1. Start the Scheduler (Scans every 3 hours)
nohup python scheduler_main.py > scheduler.log 2>&1 &
disown

# 2. Start the Web UI (Headless mode for servers)
nohup streamlit run app.py --server.port 8599 --server.headless true > ui.log 2>&1 &
disown
 Usage
Open your browser to http://localhost:8599 (or your VM's IP address: http://<VM_IP>:8599).

Add a YouTube channel URL (e.g., https://www.youtube.com/@ChannelName).

The system will automatically scan every 3 hours.

To force an immediate scan without waiting:

Bash
# Ensure you are inside the virtual environment (source venv/bin/activate)
python -c "from youtube_scraper import scan_channels; scan_channels()"
""")
print("README.md successfully created.")

Your Markdown file is ready
[file-tag: code-generated-file-0-1779537195940802875]

Perfect, while Ollama is finishing its installation in your second terminal, I have successfully generated the complete, comprehensive `README.md` file in your project directory. It includes the exact step-by-step setup for both Mac and Ubuntu so you can seamlessly deploy it on a fresh machine next time.

Here are the commands to commit the new `README.md` and push it to GitHub right now.

Run these in your original terminal (inside the `transcripts` directory):

```bash
# 1. Stage the updated README
git add README.md

# 2. Commit the changes
git commit -m "Update README with full zero-to-hero installation guide"

# 3. Push to GitHub using your specific SSH key
GIT_SSH_COMMAND="ssh -i ~/.ssh/transcripts -o IdentitiesOnly=yes" git push origin main
Once Ollama is done installing and you have run ollama pull llama3, you'll have everything needed to extract live setups directly to your local database! Let me know when the download finishes.y

