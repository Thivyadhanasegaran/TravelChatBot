# 🧳 Travel Planner Chatbot (LangChain + Gemini + Python)

A smart and friendly terminal-based chatbot built with **LangChain**, **Gemini 1.5 Pro (via Generative AI SDK)**, and **Python** to help users plan their dream trips. 🌍✈️

This bot interacts with users conversationally to:
- Collect travel preferences
- Suggest destinations
- Recommend local food
- Provide travel tips
- Generate personalized itineraries
- Handle unexpected inputs gracefully

## ▶️ Live Demo

   [Watch Live Demo](https://drive.google.com/file/d/1Q0Az4WHwLLRr6jRFOuH4d7-2z6EgcU62/view?usp=drive_link)


## 🔧 Tech Stack

- **🧠 LLM**: Gemini 1.5 Pro (via Google’s Generative AI SDK)
- **🦜 LangChain**: Framework to manage conversation flow and memory
- **🐍 Python**: Core programming language
- **📦 Dependencies**: `langchain`, `google.generativeai`, `re`, `time`, and `dotenv`


## 🚀 Features

- ✅ **Welcome Message**: Friendly greeting and name collection
- ✅ **Intent Recognition**: Trip planning, food suggestions, travel tips, destination ideas
- ✅ **User Input Collection**: Destination, budget, days, and food preferences
- ✅ **Conditional Logic**: Branches based on yes/no inputs
- ✅ **Text Response Formatting**: Well-structured and readable responses
- ✅ **End Conversation**: Personalized goodbye with destination
- ✅ **Error Handling**: Prompts for missing or invalid input
- ✅ **Fallback Handling**: Creatively redirects unrelated inputs to travel themes


## 🧠 How It Works

1. Greets the user and asks for their name
2. Listens for travel-related intents like "I want to travel", "suggest food", or "tips"
3. Asks for input based on intent (e.g., destination, budget)
4. Uses Gemini 1.5 Pro to generate natural, helpful responses
5. Detects edge cases and unrelated inputs and handles them using fallback logic
6. Ends with a personalized message



