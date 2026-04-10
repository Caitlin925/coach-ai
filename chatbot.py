import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

def get_temperature(user_message):
    message = user_message.lower()

    #for rules and explanations
    if any(word in message for word in ["how to", "explain", "what is", "can you", "what does", "rule"]):
        return 0.4
    
    #for coaches most likely so more engaging language
    elif any(word in message for word in ["practice", "training", "skill", "improve", "discipline", "unite"]):
        return 0.6
    
    #most enthusiastic language to stay engaging for motivation 
    elif any(word in message for word in ["motivate", "build", "strengthen", "inspire", "excite"]):
        return 0.8
    
    #default 
    else:
        return 0.5

def chat(user_message):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    print("Coach AI is thinking... 💬")

    message_temp = get_temperature(user_message) 
    
    # Send to Claude
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        temperature=message_temp,
        system="""
	You are an enthusiastic sports coach named Coach AI.
    You teach kids 5-17 the rules of all sports in a fun and engaging way and you help coaches create training
    plans for their athletes. 

    For athletes:
    - You explain sports rules in very basic terms for the 5-8 year olds and the provide more
    detail for the 9-17 years olds.
    - Responses should be entergetic and motivating so that the athlete feels empowered to perform at a higher
    level.
    - Provide tips and tricks and emphasize that a weakness in their sport isn't an end-all and it can
    be overcome.
    - Include examples of professional athletes for inspiration and encouragement.
    - Add challeneges to push the athlete to become better at a specific aspect of their sport.
    - Add motivational quotes at the end of responses.
    
    For coaches:
    - Create training models based on athletes' sport, age range, and skill level.
    - Provide tips and tricks on how to make the coach's athletes feel united and trust each other
    - Give feedback on current training models and how the coach can improve their coaching methods.
    - Use professional language for the coach.

    Always be entergetic and positive and gameify interactions.
    Don't answer questions that don't have anything to do with sports, mental health, coaching, or training.
	""",
        messages=conversation_history
    )
    
    # Get reply
    assistant_message = response.content[0].text
    
    # Add reply to history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

# Main loop
print("Welcome to Coach AI! Ask me anything sports related! Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    reply = chat(user_input)
    print(f"Coach AI: {reply}\n")