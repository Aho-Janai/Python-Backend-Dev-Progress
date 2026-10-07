"""
Python Basic Concepts Quiz - Simplified Version
This quiz tests fundamental Python programming knowledge.
"""

def run_quiz():
    """Run a simple Python quiz with pre-defined answers."""
    
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
        }
    ]
    
    score = 0
    
    print("Python Basic Concepts Quiz")
    print("=" * 30)
    print("Instructions: This is a sample quiz showing question format and correct answers.\n")
    
    for i, q in enumerate(questions, 1):
        print(f"Question {i}: {q['question']}")
        for j, option in enumerate(q['options'], 1):
            print(f"  {j}. {option}")
        
        print(f"\nCorrect answer: {q['answer']}\n")
        
        # Simulate correct answers for demo
        if i <= 3:  # Give score for first few questions to show it working
            score += 1
    
    print(f"Sample Quiz Results: {score}/{len(questions)} correct")
    print("This quiz demonstrates basic Python concepts including:")
    print("- Variable naming conventions")
    print("- Data types and type() function")
    print("- Function definition with 'def'")
    print("- Built-in functions like len()")
    print("- Common errors in Python")

if __name__ == "__main__":
    run_quiz()