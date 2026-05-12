# Math Battle Game
# A game where players solve handwritten math equations to battle enemies.

## Features
- 4 chapters: Addition, Subtraction, Multiplication, Division
- Player vs Enemy battles
- Handwritten digit recognition using OpenCV preprocessing and TensorFlow/Keras
- Cross-platform with Pygame

## Requirements
- Python 3.8+
- Install dependencies: pip install -r requirements.txt

## How to Run
python main.py

## Controls
- Mouse: Draw digits in the canvas area
- Enter: Submit your handwritten answer
- Space: Start game / Select chapter / Continue after battle
- ESC: Quit full screen / exit game

## Gameplay
1. Start the game and select a chapter
2. Battle enemies by solving math equations
3. Draw the answer with your mouse in the white canvas
4. Press Enter to submit (currently auto-correct)
5. Correct answers deal full damage, wrong answers deal half
6. Win battles to unlock next chapters
7. Complete all chapters to win the game

## Notes
- The game launches in fullscreen mode by default
- The ML recognizer uses OpenCV and TensorFlow
- TensorFlow may require a compatible Python version (Python 3.11 or 3.12 is recommended)
- Drawing area is 400x300 pixels in the center
- Answers are single digits (0-9) for now
- Game is cross-platform and runs on Windows, Mac, Linux

## TODO
- Fix ML library installation (TensorFlow/PyTorch compatibility with Python 3.13)
- Re-enable handwritten digit recognition