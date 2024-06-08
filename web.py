import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import eventlet
from crewai import Agent, Task, Crew, Process

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key (if needed)
os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize Flask application
app = Flask(__name__, static_url_path='/templates', static_folder='templates')
CORS(app)
socketio = SocketIO(app, async_mode='eventlet')

# Function to determine agreement
def check_agreement(response):
    # Request agreement determination from LLM
    agent = Agent(
        role='Agreement Checker',
        goal='Determine if the response indicates agreement or not',
        verbose=True,
        memory=False,
        model_name='gpt-4o',  # Specific model
        backstory="You are an impartial observer tasked with determining whether a given response indicates agreement.",
        tools=[]
    )

    check_task = Task(
        description=(
            f"Review the following response and determine if it indicates agreement overall:\n{response}\n"
            "Respond with 'agree' if it indicates agreement, otherwise respond with 'disagree'."
        ),
        expected_output="A response indicating either 'agree' or 'disagree'.",
        tools=[],
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[check_task],
        process=Process.sequential
    )

    agreement_response = crew.kickoff(inputs={})
    if 'disagree' in agreement_response.lower():
        return False
    elif 'agree' in agreement_response.lower():
        return True

# Set up interactive session
def interactive_session(topic, proposer_backstory, opposer_backstory, max_iterations=5):
    proposer_agent = Agent(
        role='Proposer',
        goal='Propose new standardization items in {topic}',
        verbose=True,
        memory=True,
        model_name='gpt-4o',  # Specific model
        backstory=proposer_backstory,
        tools=[],
        allow_delegation=False
    )

    opposer_agent = Agent(
        role='Opposer',
        goal='Provide counterarguments to new standardization proposals in {topic}',
        verbose=True,
        memory=True,
        model_name='gpt-4o',  # Specific model
        backstory=opposer_backstory,
        tools=[],
        allow_delegation=False
    )

    for iteration in range(max_iterations):
        proposer_task = Task(
            description=(
                f"Propose a new standardization item related to {topic}. "
                "Explain why this item is important and how it will benefit the industry."
            ),
            expected_output=f"A proposal for a new standardization item in {topic} with explanations.",
            tools=[],
            agent=proposer_agent,
        )

        # Proposer agent performs task
        crew = Crew(
            agents=[proposer_agent],
            tasks=[proposer_task],
            process=Process.sequential
        )

        proposer_response = crew.kickoff(inputs={'topic': topic})
        print(f"Iteration {iteration + 1} - Proposer's proposal: {proposer_response}")
        socketio.emit('response', {'role': 'Proposer', 'iteration': iteration + 1, 'response': proposer_response})

        opposition_task = Task(
            description=(
                f"Review the proposal:\n{proposer_response}\nProvide counterarguments."
            ),
            expected_output=f"A list of counterarguments against the new standardization proposal in {topic}.",
            tools=[],
            agent=opposer_agent,
        )

        # Opposer agent performs task
        crew = Crew(
            agents=[opposer_agent],
            tasks=[opposition_task],
            process=Process.sequential
        )

        opposer_response = crew.kickoff(inputs={'topic': topic, 'proposer_response': proposer_response})
        print(f"Iteration {iteration + 1} - Opposer's response: {opposer_response}")
        socketio.emit('response', {'role': 'Opposer', 'iteration': iteration + 1, 'response': opposer_response})

        # Determine agreement
        if check_agreement(opposer_response):
            print("Agreement reached!")
            socketio.emit('response', {'role': 'Final', 'response': 'Agreement reached!'})
            return

        # Update topic for proposer's next iteration
        topic = f"Refined proposal based on counterarguments:\n{opposer_response}"

        # Brief pause (may be needed for asynchronous network processing)
        eventlet.sleep(0)
    
    # If no agreement was reached after all iterations
    print("No agreement reached after maximum iterations.")
    socketio.emit('response', {'role': 'Final', 'response': 'No agreement reached after maximum iterations.'})

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Handle start interaction event
@socketio.on('start_interaction')
def handle_interaction(data):
    topic = data['topic']
    max_iterations = int(data['max_iterations'])
    proposer_backstory = data['proposer_backstory']
    opposer_backstory = data['opposer_backstory']
    
    eventlet.spawn(interactive_session, topic, proposer_backstory, opposer_backstory, max_iterations)

# Run the web application
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5002)
