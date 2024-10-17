#Help from ChatGPT

from flask import Flask, request, render_template, jsonify
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class DocumentQueryModel:
    def __init__(self, data):
        self.data = data

    def query(self, user_input, top_n=3):
        """Search the dataset for relevant entries."""
        # Search for matches in the title
        title_matches = self.data[self.data['title'].str.contains(user_input, case=False)]

        if not title_matches.empty:
            return title_matches.head(top_n)  # Return top_n title matches

        # If no title matches, search in the document
        document_matches = self.data[self.data['document'].str.contains(user_input, case=False)]
        return document_matches.head(top_n)  # Return top_n document matches

class LLMProvider:
    def __init__(self, model_name='gpt2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer, device=-1)

    def summarize(self, text):
        """Summarize the provided text."""
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        return summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

# Initialize Flask app
app = Flask(__name__)

# Load dataset
data = pd.read_parquet("data/Power-midterm.parquet")

# Ensure case-insensitive matching by converting specific columns to lowercase
columns_to_lowercase = ['category', 'subcategory', 'title']
data[columns_to_lowercase] = data[columns_to_lowercase].apply(lambda x: x.str.lower().astype(str))

# Initialize instances of query model and language model
dqm = DocumentQueryModel(data)
llm = LLMProvider()

@app.route('/')
def index():
    """Render the HTML interface."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handle user input from the chatbot interface."""
    user_input = request.json.get('user_input', '').lower().strip()

    # Debugging: Print user input to the console
    print("User Input:", user_input)

    # Handle Commands
    if user_input.startswith("/"):
        return handle_command(user_input)

    # Query relevant documents if it's not a command
    relevant_data = dqm.query(user_input)

    # Debugging: Print relevant data
    print("Relevant Data:", relevant_data)

    if not relevant_data.empty:
        # Extract the first relevant document entry
        entry = relevant_data.iloc[0]
        document_text = entry['document']
        source_url = entry['source']

        # Summarize the document
        summarized_text = llm.summarize(document_text)

        return jsonify({
            'response': summarized_text,
            'source': source_url
        })
    else:
        return jsonify({
            'response': "Sorry, I don't have the necessary information for that query.",
            'source': None
        })

def handle_command(user_input):
    """Handle specific commands from the user."""
    if user_input == "/help":
        return jsonify({
            'response': (
                "Available Commands:\n"
                "/help - Show available commands\n"
                "/status - Check if the chatbot is running\n"
                "/info - Learn more about this chatbot\n"
                "/category - List available categories\n"
                "/source - View data sources\n"
                "/clear - Reset the conversation\n"
                "/time - Get the current server time\n"
                "/debug - View debug information"
            ),
            'source': None
        })

    elif user_input == "/info":
        return jsonify({
            'response': (
                "This chatbot provides information and summaries related to MLB. "
                "Ask about players, teams, games, and history, or use commands like /help for more options."
            ),
            'source': None
        })

    elif user_input == "/category":
        return jsonify({
            'response': (
                "The available categories are:\n"
                "- Team History\n"
                "- Players\n"
                "- Statistic Types\n"
                "- Awards\n"
                "- Ballparks\n"
                "- Hall of Fame Inductees\n"
                "- World Series Winners\n"
                "- #1 Draft Picks\n"
                "- Managers\n"
                "- MLB Power Rankings 2024"
            ),
            'source': None
        })

    elif user_input == "/source":
        return jsonify({
            'response': (
                "The information provided by the chatbot comes from the MLB dataset, curated for this project. "
                "Each response includes data from real sources, which you can explore further using the provided links."
            ),
            'source': None
        })

    elif user_input == "/clear":
        return jsonify({
            'response': "The conversation has been reset. Ask me anything, and I’ll do my best to help!",
            'source': None
        })

    elif user_input == "/time":
        from datetime import datetime
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({
            'response': f"The current server time is {current_time} (UTC).",
            'source': None
        })

    elif user_input == "/debug":
        return jsonify({
            'response': (
                "Debug Information:\n"
                "- Model: gpt2\n"
                "- Dataset Size: 100 entries\n"
                "- Last Query: Not available"
            ),
            'source': None
        })

    elif user_input == "/status":
        return jsonify({
            'response': "The chatbot is running smoothly. How can I assist you today?",
            'source': None
        })

    else:
        return jsonify({
            'response': f"Unknown command: {user_input}. Type /help for a list of commands.",
            'source': None
        })

if __name__ == "__main__":
    # Run the app in debug mode for easier troubleshooting
    app.run(host="0.0.0.0", port=5000, debug=True)

