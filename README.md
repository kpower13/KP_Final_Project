# **MLB Chatbot Assistant**

## 📝 **Overview**
The **MLB Chatbot Assistant** is a Retrieval-Augmented Generation (RAG) chatbot designed to answer user inquiries related to Major League Baseball (MLB). The chatbot leverages a custom dataset, searches through documents for relevant information, and generates concise responses using natural language processing (NLP) models. 

The bot can handle:
- Queries about MLB teams, players, and history.
- Specific commands like **help** or **status** to provide additional functionality.
- Summarized responses from relevant documents found in its dataset.

---

## 📂 **Features**
- **Document Query:** Retrieves relevant documents from a curated MLB dataset.
- **Summarization:** Uses NLP models to generate summaries of relevant information.
- **Command Handling:** Supports special commands such as:
  - **`help`**: Provides instructions on how to use the chatbot.
  - **`status`**: Confirms if the chatbot is running properly.

---

## 🛠️ **Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kpower13/KP_Final_Project.git
   cd KP_Final_Project

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt 

---

## 🚀 **How to Run the Chatbot**

1. **Start the Flask Server: Run the following command in the project directory:**
   ```bash
   python app.py

2. **Go to the Web UI**
   ```bash
   * Serving Flask app 'app'
   * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000

   #this one below that can be found in your terminal
   * Running on http://192.168.1.181:5000
   
    Press CTRL+C to quit
   * Restarting with watchdog (fsevents)
   * Debugger is active!
   * Debugger PIN: 140-281-653

3. **Search for Key Words or Phrases**
   ```bash
    #search for single word or simple word queries
    Bobby Witt Jr
    Kansas City Royals
    Most Valuable Player
  
    #you can also search /help to see all of the built in commands
    /help
  
    Available Commands:
    /help - Show available commands
    /status - Check if the chatbot is running
    /info - Learn more about this chatbot
    /category - List available categories
    /source - View data sources
    /clear - Reset the conversation
    /time - Get the current server time
    /debug - View debug information

---

##🤟Have Fun and Happy Searching!##
