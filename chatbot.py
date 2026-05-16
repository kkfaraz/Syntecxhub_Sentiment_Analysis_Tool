#!/usr/bin/env python3
"""
Enhanced Rule-Based Chatbot
A professional AI/ML assistant with improved pattern matching and human-like responses.
"""

import json
import re
import os
from datetime import datetime
import random
import math


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colorize(text, color):
    return f"{color}{text}{Colors.ENDC}"


def print_header(title):
    print(colorize("\n" + "═" * 70, Colors.CYAN))
    print(colorize(f"  {title}", Colors.BOLD + Colors.CYAN))
    print(colorize("═" * 70, Colors.CYAN))


def print_section(title):
    print(colorize(f"\n── {title} ", Colors.YELLOW) + colorize("─" * 50, Colors.YELLOW))


# ============================================================================
# ENHANCED INTENT PATTERNS AND RESPONSES
# ============================================================================

GREETING_PATTERNS = [
    r'\bhi\b', r'\bhello\b', r'\bhey\b', r'\bhiya\b', r'\bgreetings\b',
    r'\bgood morning\b', r'\bgood afternoon\b', r'\bgood evening\b',
    r'\bhowdy\b', r'\bwhat\'s up\b', r'\bwhat up\b', r'\bsup\b',
    r'\bhi there\b', r'\bhello there\b', r'\bhey there\b', r'\bhiya there\b'
]

GREETING_RESPONSES = [
    "Hello! It's great to meet you. I'm here to help you explore the fascinating world of AI and Machine Learning. What would you like to learn about today?",
    "Hi there! I'm excited to chat with you about AI and ML. Whether you're just starting out or looking to deepen your knowledge, I'm here to help!",
    "Hey! Welcome! Feel free to ask me anything about artificial intelligence, machine learning, or related technologies. I'm here to assist!",
    "Greetings! It's wonderful to have you here. I can help you understand concepts in AI, machine learning, deep learning, and more. What interests you?",
    "Hello! I hope you're having a great day. I'd be happy to help you discover more about AI and machine learning. What would you like to know?"
]

GOODBYE_PATTERNS = [
    r'\bbye\b', r'\bgoodbye\b', r'\bsee you\b', r'\bsee ya\b', r'\btake care\b',
    r'\bfarewell\b', r'\blater\b', r'\bgood night\b', r'\bgotta go\b',
    r'\bhave to go\b', r'\bneed to leave\b', r'\btalk to you later\b',
    r'\bsweetheart\b', r'\buntil next time\b', r'\bbot bye\b'
]

GOODBYE_RESPONSES = [
    "Goodbye! It was wonderful chatting with you. Don't hesitate to return whenever you have more questions about AI and ML. Take care!",
    "Farewell! I hope I was helpful today. Feel free to come back anytime you want to explore more about artificial intelligence. Have a great day!",
    "Take care! It was a pleasure assisting you. Remember, the world of AI and machine learning is always evolving, so keep curious!",
    "Bye for now! I enjoyed our conversation. If you ever want to learn more about AI topics, just return and I'll be here to help!",
    "Goodbye! Thank you for stopping by. I hope you found the information helpful. Come back anytime!"
]

HELP_PATTERNS = [
    r'\bhelp\b', r'\bhelp me\b', r'\bwhat can you do\b', r'\bhow do you work\b',
    r'\bwhat can i ask\b', r'\bcapabilities\b', r'\btell me what you know\b',
    r'\bwhat topics\b', r'\bwhat subjects\b', r'\bhow can you help\b',
    r'\bwhat are you good at\b', r'\bguide\b', r'\binstructions\b'
]

HELP_RESPONSES = [
    """I specialize in explaining concepts related to Artificial Intelligence and Machine Learning. Here's what I can help you with:

▸ Core AI Concepts: AI, Machine Learning, Deep Learning, Neural Networks
▸ ML Techniques: Supervised, Unsupervised, Reinforcement Learning
▸ NLP & Computer Vision: Language processing, Image recognition
▸ Popular Frameworks: TensorFlow, PyTorch, Keras, scikit-learn
▸ Model Training: Overfitting, Underfitting, Cross-validation
▸ Advanced Topics: Transformers, GANs, Transfer Learning
▸ Practical Applications: Chatbots, Autonomous Vehicles, Recommenders

Just ask me something like "What is machine learning?" or "Explain neural networks" and I'll do my best to help!""",

    """Think of me as your AI/ML study companion! Here's how I can assist you:

📚 I can explain fundamental concepts in detail
🔍 I can help you understand technical terminology
💡 I can provide examples and real-world applications
📖 I can discuss the latest trends in AI/ML
❓ I can answer questions about specific algorithms or frameworks

Go ahead and ask me anything about artificial intelligence, machine learning, or data science!"""
]

THANKS_PATTERNS = [
    r'\bthank(s| you| ya)?\b', r'\bthanks\b', r'\bappreciate\b', r'\bthx\b',
    r'\bty\b', r'\bmuch appreciated\b', r'\bthank you very much\b',
    r'\bthank you so much\b', r'\bbig thanks\b', r'\bgrateful\b'
]

THANKS_RESPONSES = [
    "You're absolutely welcome! I'm glad I could help. Feel free to ask if you have any more questions!",
    "My pleasure! That's what I'm here for. Don't hesitate to reach out if you need clarification on anything.",
    "Glad I could be of assistance! If you want to explore more topics, just let me know.",
    "You're welcome! I enjoyed helping you understand that concept. Let me know if there's anything else!",
    "Happy to help! Learning about AI and ML is an exciting journey, and I'm here to support you along the way!"
]

SMALL_TALK_PATTERNS = [
    r'\bhow are you\b', r'\bhow do you do\b', r'\bhow\'s it going\b',
    r'\bwhat\'s new\b', r'\bhow\'s your day\b', r'\bhow have you been\b',
    r'\byou doing okay\b', r'\bhow things\b', r'\bwhat have you been up to\b'
]

SMALL_TALK_RESPONSES = [
    "I'm doing wonderfully, thank you for asking! I'm always excited to share knowledge about AI and machine learning. How can I assist you today?",
    "I'm great! There's nothing I enjoy more than discussing artificial intelligence and helping people learn. What's on your mind?",
    "Fantastic, thanks for checking! I'm here and ready to help you explore any AI or ML topic you're curious about.",
    "I'm doing well! Every conversation is an opportunity to help someone discover the fascinating world of AI. What would you like to know?"
]

NAME_PATTERNS = [
    r'\bwhat is your name\b', r'\bwho are you\b', r'\bwhat should i call you\b',
    r'\byour name\b', r'\bcall you\b', r'\bwho are you\b'
]

NAME_RESPONSES = [
    "I'm your AI/ML Assistant! Think of me as a knowledgeable friend who's always ready to help you understand artificial intelligence and machine learning concepts. I don't have a fancy name, but I'm here to assist you!",
    "You can call me your AI Companion! I'm designed to help you learn about artificial intelligence, machine learning, and related technologies in an easy-to-understand way."
]

REPEAT_PATTERNS = [
    r'\bsay that again\b', r'\brepeat\b', r'\bwhat did you say\b',
    r'\bcould you repeat\b', r'\bsay again\b'
]

NOT_UNDERSTAND_PATTERNS = [
    r'\b(i don\'t|i do not) understand\b', r'\bconfused\b', r'\bdon\'t get it\b',
    r'\bexplain further\b', r'\bclarify\b', r'\bmore details\b'
]

REPEAT_RESPONSES = [
    "Of course! Could you please tell me which part you'd like me to clarify? I'm happy to explain in more detail.",
    "Absolutely! Let me know which specific part you'd like me to elaborate on, and I'll do my best to clarify."
]

NOT_UNDERSTAND_PATTERNS = [
    r'\bwhat\b', r'\bwho\b', r'\bwhere\b', r'\bwhen\b', r'\bwhy\b', r'\bhow\b',
    r'\bi don\'t understand\b', r'\bconfused\b', r'\bdon\'t get it\b',
    r'\bexplain\b', r'\bclarify\b'
]

EXIT_COMMANDS = ['quit', 'exit', 'bye', 'q', 'goodbye', 'leave', 'stop']


# ============================================================================
# FUZZY MATCHING FOR BETTER ACCURACY
# ============================================================================

def tokenize(text):
    """Convert text to lowercase and split into words."""
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return set(text.split())


def calculate_similarity(input_tokens, pattern_tokens):
    """Calculate similarity between two sets of tokens using Jaccard similarity."""
    if not input_tokens or not pattern_tokens:
        return 0.0

    intersection = len(input_tokens & pattern_tokens)
    union = len(input_tokens | pattern_tokens)

    if union == 0:
        return 0.0

    return intersection / union


def fuzzy_match(user_input, patterns, threshold=0.3):
    """Fuzzy match user input against patterns."""
    user_tokens = tokenize(user_input)

    for pattern in patterns:
        pattern_tokens = tokenize(pattern)
        similarity = calculate_similarity(user_tokens, pattern_tokens)

        if similarity >= threshold:
            return True

    return False


def detect_intent(user_input):
    """Enhanced intent detection with fuzzy matching."""
    user_lower = user_input.lower()

    if user_lower in EXIT_COMMANDS:
        return 'exit', 1.0

    intents = [
        ('greeting', GREETING_PATTERNS),
        ('goodbye', GOODBYE_PATTERNS),
        ('help', HELP_PATTERNS),
        ('thanks', THANKS_PATTERNS),
        ('small_talk', SMALL_TALK_PATTERNS),
        ('name', NAME_PATTERNS),
        ('repeat', REPEAT_PATTERNS),
    ]

    for intent_name, patterns in intents:
        for pattern in patterns:
            if re.search(pattern, user_lower):
                return intent_name, 1.0

        if fuzzy_match(user_lower, patterns, 0.4):
            return intent_name, 0.8

    has_ai_keywords = any(word in user_lower for word in
        ['ai', 'ml', 'machine learning', 'deep learning', 'neural', 'artificial',
         'python', 'tensorflow', 'pytorch', 'nlp', 'computer vision', 'algorithm',
         'model', 'training', 'data', 'learning', 'intelligence'])

    return 'domain', 0.9 if has_ai_keywords else 0.0


# ============================================================================
# ENHANCED KNOWLEDGE BASE FUNCTIONS
# ============================================================================

def load_knowledge_base(filepath='knowledge_base.json'):
    """Load the knowledge base from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(colorize(f"⚠ Knowledge base not found: {filepath}", Colors.RED))
        return {}
    except json.JSONDecodeError as e:
        print(colorize(f"⚠ Invalid JSON: {e}", Colors.RED))
        return {}


def preprocess_input(user_input):
    """Clean and preprocess user input for better matching."""
    user_input = user_input.lower()

    question_words = ['what is', 'what are', 'what does', 'what do', 'what can',
                     'define', 'explain', 'tell me about', 'describe', 'how does',
                     'how do', 'why is', 'why does', 'who is', 'who are']

    for word in question_words:
        user_input = user_input.replace(word, ' ')

    user_input = re.sub(r'[^\w\s]', ' ', user_input)
    user_input = re.sub(r'\s+', ' ', user_input).strip()

    return user_input


def search_knowledge_base(user_input, knowledge_base):
    """Enhanced search with multiple matching strategies."""
    user_lower = user_input.lower()
    user_preprocessed = preprocess_input(user_input)
    user_tokens = set(user_preprocessed.split())

    best_match = None
    best_score = 0

    for question, answer in knowledge_base.items():
        question_clean = preprocess_input(question)
        question_tokens = set(question_clean.split())

        intersection = len(user_tokens & question_tokens)

        if intersection > 0:
            score = intersection / max(len(user_tokens), len(question_tokens))

            if 'explain' in user_preprocessed or 'define' in user_preprocessed:
                score *= 1.2

            if question_clean in user_preprocessed:
                score = 1.0

            if score > best_score:
                best_score = score
                best_match = answer

    if best_score >= 0.2:
        return best_match

    single_keywords = ['transformer', 'gan', 'lstm', 'rnn', 'cnn', 'nlp', 'ml', 'ai',
                       'nlp', 'gpt', 'bert', 'keras', 'pytorch', 'tensorflow']

    for keyword in single_keywords:
        if keyword in user_lower:
            for question, answer in knowledge_base.items():
                if keyword in question:
                    return answer

    for question, answer in knowledge_base.items():
        if question in user_lower:
            return answer

    for question, answer in knowledge_base.items():
        question_words = question.split()
        for word in question_words:
            if len(word) > 4 and word in user_lower:
                return answer

    return None


# ============================================================================
# ENHANCED RESPONSE SYSTEM
# ============================================================================

def get_greeting_response():
    return random.choice(GREETING_RESPONSES)


def get_goodbye_response():
    return random.choice(GOODBYE_RESPONSES)


def get_help_response():
    return random.choice(HELP_RESPONSES)


def get_thanks_response():
    return random.choice(THANKS_RESPONSES)


def get_small_talk_response():
    return random.choice(SMALL_TALK_RESPONSES)


def get_name_response():
    return random.choice(NAME_RESPONSES)


def get_repeat_response():
    return random.choice(REPEAT_RESPONSES)


FALLBACK_RESPONSES = [
    "That's an interesting question! While I specialize in AI and Machine Learning topics, I might not have information on that specific area. Try asking me about concepts like 'What is machine learning?' or 'Explain neural networks'!",
    "I see you're curious about that topic! My expertise is focused on artificial intelligence and machine learning. Would you like to explore something like 'What is deep learning?' or 'How do neural networks work?'?",
    "That's beyond my current knowledge base, which focuses on AI and ML. I'd be happy to help if you ask about topics like 'What is TensorFlow?' or 'Explain reinforcement learning'!",
    "Hmm, I don't have information on that particular topic. My strength is explaining AI and machine learning concepts. Perhaps you'd like to know about 'What is a transformer?' or 'How does NLP work?'?",
    "I'm not able to help with that specific question, but I'm great at discussing AI and machine learning! Try asking about topics like classification, overfitting, or computer vision."
]


def get_bot_response(user_input, knowledge_base):
    """Generate an intelligent response based on intent and context."""
    intent, confidence = detect_intent(user_input)

    if intent == 'exit':
        return get_goodbye_response()

    response_handlers = {
        'greeting': get_greeting_response,
        'goodbye': get_goodbye_response,
        'help': get_help_response,
        'thanks': get_thanks_response,
        'small_talk': get_small_talk_response,
        'name': get_name_response,
        'repeat': get_repeat_response,
    }

    if intent in response_handlers:
        return response_handlers[intent]()

    knowledge_answer = search_knowledge_base(user_input, knowledge_base)
    if knowledge_answer:
        return knowledge_answer

    return random.choice(FALLBACK_RESPONSES)


# ============================================================================
# CONVERSATION LOGGING
# ============================================================================

def log_conversation(user_input, bot_response, log_file='conversation_log.txt'):
    """Log conversation with enhanced formatting."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}]\n")
            f.write(f"  USER: {user_input}\n")
            f.write(f"  BOT:  {bot_response}\n")
            f.write("─" * 60 + "\n\n")

    except Exception as e:
        print(colorize(f"⚠ Log error: {e}", Colors.YELLOW))


# ============================================================================
# MAIN CHATBOT
# ============================================================================

def print_welcome():
    """Display welcome message with ASCII art."""
    print(colorize("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     ██████╗ ███████╗ ██████╗██╗██╗     ███████╗██╗  ██╗      ║
    ║     ██╔══██╗██╔════╝██╔════╝██║██║     ██╔════╝╚██╗██╔╝      ║
    ║     ██████╔╝█████╗  ██║     ██║██║     █████╗   ╚███╔╝       ║
    ║     ██╔══██╗██╔══╝  ██║     ██║██║     ██╔══╝   ██╔██╗       ║
    ║     ██║  ██║███████╗╚██████╗██║███████╗███████╗██╔╝ ██╗      ║
    ║     ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝      ║
    ║                                                              ║
    ║              🤖 AI & MACHINE LEARNING ASSISTANT             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """, Colors.CYAN))

    print(colorize("  Your intelligent companion for exploring AI and ML concepts", Colors.BLUE))
    print(colorize("  Type 'help' for available topics or 'quit' to exit\n", Colors.BLUE))


def print_topic_suggestions():
    """Show suggested topics for users to explore."""
    print_section("Popular Topics You Can Ask About")
    topics = [
        ("Core Concepts", ["Artificial Intelligence", "Machine Learning", "Deep Learning"]),
        ("Techniques", ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"]),
        ("Neural Networks", ["Neural Networks", "CNN", "RNN", "LSTM", "Transformers"]),
        ("Frameworks", ["TensorFlow", "PyTorch", "Keras", "scikit-learn"]),
        ("Applications", ["NLP", "Computer Vision", "Chatbots", "Autonomous Vehicles"]),
    ]

    for category, items in topics:
        print(f"  {colorize(category, Colors.CYAN)}: {', '.join(items)}")


def main():
    """Main chatbot loop."""
    print_welcome()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    kb_path = os.path.join(script_dir, 'knowledge_base.json')

    if not os.path.exists(kb_path):
        kb_path = 'knowledge_base.json'

    knowledge_base = load_knowledge_base(kb_path)

    if knowledge_base:
        print(colorize(f"  ✓ Knowledge base loaded successfully", Colors.GREEN))
    else:
        print(colorize("  ⚠ Warning: Knowledge base not loaded!", Colors.RED))

    print_topic_suggestions()

    print(colorize("\n" + "─" * 70, Colors.CYAN))
    print(colorize("  Ready to help! Ask me anything about AI and ML.", Colors.GREEN))
    print(colorize("─" * 70, Colors.CYAN))

    conversation_count = 0

    while True:
        try:
            user_input = input(colorize("\n➤ ", Colors.BOLD + Colors.CYAN)).strip()

            if not user_input:
                continue

            if user_input.lower() in EXIT_COMMANDS:
                print(colorize(f"\n  Bot: {get_goodbye_response()}", Colors.GREEN))
                print(colorize(f"\n  Session stats: {conversation_count} messages exchanged", Colors.BLUE))
                break

            bot_response = get_bot_response(user_input, knowledge_base)
            print(colorize(f"\n  Bot: {bot_response}", Colors.GREEN))

            log_conversation(user_input, bot_response)
            conversation_count += 1

        except KeyboardInterrupt:
            print(colorize("\n\n  Bot: Goodbye! Have a wonderful day!", Colors.GREEN))
            break
        except Exception as e:
            print(colorize(f"\n  ⚠ Oops! Something went wrong: {e}", Colors.RED))


if __name__ == "__main__":
    main()
