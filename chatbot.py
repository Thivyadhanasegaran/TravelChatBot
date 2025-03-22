import re
# Custom wrapper to interface with Gemini 1.5 Pro
from gemini_llm_wrapper import GeminiLLM
import time

# Instantiate Gemini LLM
llm = GeminiLLM()

# Memory to store user data
user_memory = {
    "name": None,
    "destination": None,
    "budget": None,
    "days": None,
    "food_preferences": None
}

# Function to extract the destination city from user input using alias matching
def extract_destination(text):
    text = text.lower()
    text_clean = re.sub(r"[^\w\s]", "", text)
    city_aliases = {
        "Paris": ["paris"], "New York": ["newyork", "new york", "nyc"],
        "London": ["london"], "Tokyo": ["tokyo"], "Dubai": ["dubai"],
        "Rome": ["rome"], "Sydney": ["sydney"], "Bali": ["bali"],
        "Barcelona": ["barcelona"], "Bangkok": ["bangkok"], "Amsterdam": ["amsterdam"]
    }
    for city, aliases in city_aliases.items():
        for alias in aliases:
            if alias in text_clean:
                return city
    return None

# Function to clean and format LLM response for better readability in terminal
def format_response(text):
    formatted = "\n============================================================\n"
    formatted += "🤖 Bot Response:\n\n"

     # Clean formatting issues (bold markers, lists, day headers)
    text = re.sub(r"^\s*[\*\-]\s+(?!.*?:\*\*)", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"(\d+\.\s.+?:)(?!\n\n)", r"\1\n", text)
    text = re.sub(r"\*?(Day\s+\d+:.*?)\*\*", r"\n\n**\1**\n" + "-" * 40, text)

     # Format headers for clarity
    for header in ["Accommodation", "Food Budget", "Transportation", "Activities & Entry Fees",
                   "Food to Try", "Tips for", "Helpful Tips", "Budget Breakdown"]:
        text = re.sub(rf"(?<!\n){header}(.*?:)", rf"\n\n**{header}\1**", text)

    # Improve spacing and newlines
    text = re.sub(r"(\n)([A-Z].+?:)", r"\1\n\2", text)
    text = re.sub(r"(?<=[a-z\.])\n(?=[A-Z])", "\n\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    formatted += text.strip()
    formatted += "\n\n============================================================"
    return formatted

# Intent recognition to classify what the user wants
def recognize_intent(user_input):
    user_input = user_input.lower()
    detected_destination = extract_destination(user_input)
    if detected_destination:
        user_memory["destination"] = detected_destination

    # Check for keywords to determine the intent
    if "plan" in user_input and "trip" in user_input:
        return "trip_plan"
    elif any(phrase in user_input for phrase in ["planning to travel", "planning a vacation", "want to travel",
        "going on a trip", "traveling soon", "plan to travel", "want to explore"]):
        return "trip_plan"
    elif any(word in user_input for word in ["suggest", "destination", "place"]):
        return "destination_suggestion"
    elif any(word in user_input for word in ["food", "eat", "dish", "cuisine"]):
        return "food_recommendation"
    elif any(word in user_input for word in ["tip", "advice", "how to", "tips"]):
        return "travel_tip"
    elif any(word in user_input for word in ["bye", "exit", "thanks", "thank you"]):
        return "exit"
    else:
        return "fallback"

# If the input doesn't match any known intent, generate a friendly fallback response
def handle_fallback(user_input):
    try:
        prompt = (
            f"You are a friendly travel assistant named TravelBot speaking to {user_memory['name']}.\n"
            f"They just typed: '{user_input}'.\n"
            f"Even though their question isn’t directly about travel, find a creative way to relate it to travel or exploration. "
            f"Respond warmly and helpfully. Greet them by name, keep it fun and positive, and gently guide them to ask about a planning a trip, destination, getting travel tips, choosing a destination, food, or itinerary planning."       
        )
        response = llm._call(prompt)
        print(f"{format_response(response)}\n")
    except Exception:
        print("🤖 Hmm, I didn’t quite get that — but I’d love to help! Try asking about your trip or destination.")

# Utility function to keep prompting the user until valid input is received
def ask_until_valid(prompt_text, validator=lambda x: bool(x.strip()), error_msg="⚠️ Please enter something!"):
    while True:
        response = input(prompt_text).strip()
        if validator(response):
            return response
        else:
            print(error_msg)

# Extract travel preference like beach, nature, city, or adventure from user input
def extract_preference(text):
    text = text.lower()
    for word in ["beach", "nature", "city", "adventure"]:
        if word in text:
            return word
    return None

# Main function to run the Travel Planner Assistant bot
def travel_bot():
    print("🌍 Hi there! I’m your Travel Planner Assistant. ✨")
    print("I can help you plan amazing trips, recommend unique destinations, and share travel tips.\n")

    # Ask for user name until provided
    while not user_memory["name"]:
        user_memory["name"] = input("👋 Hello, may I know your name? ").strip().title()
        if not user_memory["name"]:
            print("⚠️ A name helps me personalize your experience! Try again.\n")

    # Welcome message  
    print(f"\nNice to meet you, {user_memory['name']}! Let's get started. ✈️\n")
    print("Here are a few things I can help you with:")
    print("1️⃣  Plan a trip (budget, days, itinerary)")
    print("2️⃣  Suggest destinations (beach, nature, city, adventure)")
    print("3️⃣  Recommend local foods")
    print("4️⃣  Share travel tips and safety advice")
    print("5️⃣  Answer general travel questions")
    print("\nJust type your question to get started! 😄\n")

    # Chat loop
    while True:
        user_input = input(f"{user_memory['name']}: ").strip()
        print()

        if not user_input:
            print("⚠️ Please enter something so I can help you better! \n")
            continue

        # Recognize user intent
        intent = recognize_intent(user_input)

        # Handle trip planning flow
        if intent == "trip_plan":
            proceed = ask_until_valid(f"📋 Would you like to plan a trip now? (yes/no): ").lower()
            if proceed.startswith("y"):
                # Reset memory for new trip
                user_memory["destination"] = None
                user_memory["budget"] = None
                user_memory["days"] = None

                # Try extracting destination again if available
                new_destination = extract_destination(user_input)
                if new_destination:
                    user_memory["destination"] = new_destination

                if not user_memory["destination"]:
                    user_memory["destination"] = ask_until_valid("🌍 Where are you planning to go? ")

                # Collect budget and days
                user_memory["budget"] = ask_until_valid("💰 What's your travel budget? (e.g., under $500, $1000-$2000): ")
                user_memory["days"] = ask_until_valid("🗓️ How many days will you be traveling? ")

                # Prompt to LLM
                prompt = (
                    f"{user_memory['name']} is planning a {user_memory['days']}-day trip to {user_memory['destination']} "
                    f"with a budget of {user_memory['budget']}. "
                    f"Suggest a friendly and fun travel itinerary including places to visit, foods to try, and any helpful tips."
                )
                try:
                    response = llm._call(prompt)
                    time.sleep(1)
                    print(f"{format_response(response)}\n")
                except Exception:
                    print("🤖 Sorry, I couldn't create your travel plan right now. Please try again later.\n")
            else:
                print(f"No worries, {user_memory['name']}! You can ask me for destination ideas, food suggestions, or travel tips anytime. 😊\n")
        # Handle food recommendation flow
        elif intent == "food_recommendation":
            new_destination = extract_destination(user_input)
            if new_destination:
                user_memory["destination"] = new_destination

            if not user_memory["destination"]:
                user_memory["destination"] = ask_until_valid("🌎 Which city or country are you asking about? ")

            if not user_memory["food_preferences"]:
                user_memory["food_preferences"] = ask_until_valid("🍽️ What kind of food do you like? (Street food, fine dining, local specialties?) ").lower()

            prompt = (
                f"{user_memory['name']} loves {user_memory['food_preferences']} food and is visiting {user_memory['destination']}. "
                f"Suggest famous and local food they must try."
            )
            try:
                response = llm._call(prompt)
                time.sleep(1)
                print(f"{format_response(response)}\n")
            except Exception:
                print("🤖 Oops, I couldn’t find food suggestions. Try again later.\n")
        # Handle destination suggestion flow
        elif intent == "destination_suggestion":
            preference = extract_preference(user_input)
            while not preference:
              preference_input = ask_until_valid("🌟 Do you prefer beach, nature, city, or adventure destinations? ").lower()
              preference = extract_preference(preference_input)
            prompt = (
                 f"You are a helpful and creative travel expert assisting {user_memory['name']}."
                 f"They are looking for great {preference} destinations to visit."
                 f"Suggest 3 to 5 amazing {preference} places around the world. For each destination, give 1–2 sentences on what makes it special and ideal for {preference.lower()} lovers."
                 f"Make sure the places are diverse and interesting, and write in a friendly tone."
            )
            try:
                response = llm._call(prompt)
                if not response.strip():
                 raise ValueError("Empty response from LLM.")
                time.sleep(1)
                print(f"{format_response(response)}\n")
            except Exception:
                print("🤖 Sorry, I couldn't find suggestions right now. Please try again in a moment.\n")
        # Handle travel tips flow
        elif intent == "travel_tip":
            prompt = f"Share practical travel tips for {user_memory['name']} such as packing, budgeting, and safety."
            try:
                response = llm._call(prompt)
                time.sleep(1)
                print(f"{format_response(response)}\n")
            except Exception:
                print("🤖 Couldn't fetch tips right now.\n")
        # Exit the conversation
        elif intent == "exit":
            print(f"👋 It was wonderful helping you, {user_memory['name']}! Have a fantastic journey to {user_memory['destination'] or 'your dream destination'}! 🌍✈️\n")
            break

        else:
            handle_fallback(user_input)
# Run the bot
if __name__ == "__main__":
    travel_bot()
