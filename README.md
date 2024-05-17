# Clone the repository to your local machine
; git clone git@https://github.com/neily2nd/Chitter.git YOUR_PROJECT_NAME

# Enter the directory
; cd YOUR_PROJECT_NAME

# Activate the virtual environment
.venv/script/activate 

# Install dependencies
pip install -r requirements.txt

# Seed the development database
; python seeds/seed.py

# Run the app
(html-application-starter-venv); python app.py
# Now visit http://localhost:5000 in your browser
