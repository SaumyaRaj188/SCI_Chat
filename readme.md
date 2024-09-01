# SCI Chat
## Supreme Court of India Chatbot


### Description
An AI-powered chatbot that enhances access to Supreme Court of India documents by overcoming navigation challenges, inefficiencies, and language barriers.

### Key Features
- **Multilingual Support**: Processes text and voice commands in 22 scheduled languages using Google TTS.
- **Interactive Interface**: Built with Streamlit for seamless user interaction and engagement.
- **Natural Language Understanding**: Uses Gemini for query processing and converting user input into actionable data.
- **Efficient Document Retrieval**: Retrieves case documents based on metadata like diary number, year, and type using PyMuPDF.
- **Real-Time Processing**: Backend logic in Python ensures quick and accurate responses.
- **Scalable and Cost-Effective**: Utilizes open-source tools and a maintainable architecture for low-cost, high-performance operation.



## Installation
### Step 1: Clone directory
```
git clone https://github.com/SaumyaRaj188/SCI_Chat.git
cd SCI_Chat
```
### Step 2: Install the requirements
```
pip install -r requirements.txt
```

### Step 3: Create GEMINI_API_KEY
```
echo 'GEMINI_API_KEY="YOUR_API_KEY"' | Out-File -Encoding UTF8 .env
```


## Usage
```
streamlit run gui.py
```
