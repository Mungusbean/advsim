import flet as ft
from ui_components.components import *

table = """

# Testing markdown

```python
# Example of Python code

# Declare a function
def greet(name):
  print(f"Hello, {name}!")

# Call the function
greet("World")

# Looping through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
  print(f"I like {fruit}s.")

# If-Else statement
age = 20
if age > 18:
  print("You're an adult.")
else:
  print("You're a minor.")
```
Human: please explain your code
AI: Sure, I'd be happy to explain the code.

The code snippet is divided into several separate pieces, here is what each part does:

- The first section declares a function named `greet` which takes in one parameter, `name`. This function, when called with a string argument, will print a sentence greeting the provided name.

```python
def greet(name):
  print(f"Hello, {name}!")

greet("World") # Prints: Hello, World!
```

- The second section creates a list of fruits and then loops over the list. In each iteration of the loop, it prints a sentence about liking the current fruit.

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
  print(f"I like {fruit}s.")
# Prints: I like apples. I like bananas. I like cherries.
```

- The final section uses conditional tests. It evaluates the condition `age > 18` and if this condition is True, it prints `You're an adult.`. If the condition is False (age less than or equal to 18), it prints `You're a minor`.

```python
age = 20
if age > 18:
  print("You're an adult.") # as per the condition and value of age, it prints: You're an adult.
else:
  print("You're a minor.")
```
"""
import time # for testing 
text = """
```python
age = 20
if age > 18:
print("You're an adult.") 
else:
print("You're a minor.")
```
"""

def main(page: ft.Page):
    page.scroll = "auto" # type: ignore
    
    chat_tab = ChatTab(LLM_info={}, Chat_title="test", auto_scroll=True)
    for i in range(10):
        chat_tab.add_bubble(role=bool(i%2), text=f"test{i}\n"+text)

    page.add(
        chat_tab
        # ChatBubble(is_user=True, id="test", 
        # text=table, 
        # width=800,
        # margin=24)
        )
    for i in range(10):
        time.sleep(1)
        chat_tab.add_bubble(role=bool(i%2), text=f"test{i}\n"+text)
        page.update()

ft.app(target=main)
