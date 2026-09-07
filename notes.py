notes_data = {
    "python": """
# 🐍 Python

## Introduction
Python is a high-level, easy-to-learn programming language.

## Features
- Easy syntax
- Object-Oriented
- Open Source
- Cross Platform

## Applications
- AI
- Web Development
- Data Science
- Automation

## Advantages
- Beginner friendly
- Huge library support
- Fast development
""",

    "ai": """
# 🤖 Artificial Intelligence

## Definition
Artificial Intelligence is the simulation of human intelligence in machines.

## Types
- Narrow AI
- General AI

## Applications
- Chatbots
- Healthcare
- Self Driving Cars
- Robotics
""",

    "machine learning": """
# 📘 Machine Learning

Machine Learning is a branch of AI.

## Types
- Supervised Learning
- Unsupervised Learning
- Reinforcement Learning

## Applications
- Recommendation Systems
- Image Recognition
- Fraud Detection
"""
}

def generate_notes(topic):
    return notes_data.get(
        topic.lower(),
        f"# {topic}\n\nNo notes available for this topic yet."
    )
