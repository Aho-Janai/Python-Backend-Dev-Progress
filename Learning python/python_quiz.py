"""
Python Basic Concepts Quiz
This quiz tests fundamental Python programming knowledge.
"""

import random

def run_quiz():
    """Run the Python quiz and calculate score."""
    
    # Quiz questions
    questions = [
        {
            "question": "Which of these is NOT a valid Python variable name?",
            "options": ["my_var", "var2", "_private", "2var"],
            "answer": "2var"
        },
        {
            "question": "What is the output of the following code?\nprint(type(3.14))",
            "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>"],
            "answer": "<class 'float'>"
        },
        {
            "question": "Which keyword is used to create a function in Python?",
            "options": ["func", "define", "def", "function"],
            "answer": "def"
        },
        {
            "question": "What does the 'len()' function do?",
            "options": ["Converts to lowercase", "Returns length of an object", "Checks if object is empty", "Deletes an object"],
            "answer": "Returns length of an object"
        },
        {
            "question": "Which of these will throw a TypeError?",
            "options": ["'Hello' + 'World'", "5 + 3", "len([1,2,3])", "None + None"],
            "answer": "None + None"
        },
        {
            "question": "What is the output of this code?\nnumbers = [1, 2, 3]\nprint(numbers[0])",
            "options": ["1", "2", "3", "0"],
            "answer": "1"
        },
        {
            "question": "How do you comment in Python?",
            "options": ["// This is a comment", "# This is a comment", "/* This is a comment */", "-- This is a comment"],
            "answer": "# This is a comment"
        },
        {
            "question": "Which loop is used to iterate over a sequence in Python?",
            "options": ["while", "for", "do-while", "repeat"],
            "answer": "for"
        }
    ]
    
    # Shuffle questions
    random.shuffle(questions)
    
    score = 0
    
    print("Python Basic Concepts Quiz")
    print("=" * 30)
    
    for i, q in enumerate(questions[:5], 1):  # Ask first 5 questions
        print(f"\nQuestion {i}: {q['question']}")
        for j, option in enumerate(q['options'], 1):
            print(f"  {j}. {option}")
        
        while True:
            try:
                answer = int(input("Your answer (1-4): ")) - 1
                if 0 <= answer < len(q['options']):
                    if q['options'][answer] == q['answer']:
                        print("Correct!")
                        score += 1
                    else:
                        print(f"Wrong! The correct answer is: {q['answer']}")
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
    
    print(f"\nQuiz completed! Your score: {score}/5")
    percentage = (score / 5) * 100
    print(f"Percentage: {percentage:.1f}%")
    
    if percentage >= 80:
        print("Great job! You have a solid understanding of basic Python concepts.")
    elif percentage >= 60:
        print("Good effort! Keep practicing to improve your Python skills.")
    else:
        print("Keep studying Python basics. You'll get better with practice!")

if __name__ == "__main__":
    run_quiz()