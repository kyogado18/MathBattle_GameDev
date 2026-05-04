import random

class MathGenerator:
    def __init__(self):
        self.operations = [
            ("+", lambda a, b: a + b),
            ("-", lambda a, b: a - b),
            ("*", lambda a, b: a * b),
            ("/", lambda a, b: a // b if b != 0 else 0)  # Integer division
        ]
    
    def generate_equation(self, chapter):
        op, func = self.operations[chapter]
        if chapter == 0:  # Addition
            a = random.randint(1, 10)
            b = random.randint(1, 10)
        elif chapter == 1:  # Subtraction
            a = random.randint(5, 20)
            b = random.randint(1, a)
        elif chapter == 2:  # Multiplication
            a = random.randint(1, 10)
            b = random.randint(1, 10)
        elif chapter == 3:  # Division
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
        
        answer = func(a, b)
        # For now, assume answers are single digits
        if answer > 9:
            # Regenerate if answer > 9
            return self.generate_equation(chapter)
        equation = f"{a} {op} {b} = ?"
        return equation, answer