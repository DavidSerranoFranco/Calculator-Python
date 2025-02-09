import math
import re
import os
import tkinter as tk

# Configure Tcl/Tk routes (only required on some systems)
os.environ['TCL_LIBRARY'] = r"C:\Users\david\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\david\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

# Create the main window
window = tk.Tk()
window.title('Calculator version 1.2')

# Customize window size
window.minsize(300, 500)
window.maxsize(1200, 800)

# Customize the window background color
window.configure(bg='#152640')

# Customize the window icon
path_icon = 'D:/PythonProjects/CalculatorProject/calico.ico'
window.iconbitmap(path_icon)

# Set rows and columns to expand with the window
for i in range(6):  # Six rows
    window.grid_rowconfigure(i, weight=1)

for j in range(4):  # Four columns
    window.grid_columnconfigure(j, weight=1)

# Global variables to control the expression and state of the viewer
expression = ''
show_result = False

# Variable for the viewer
visor_text = tk.StringVar()

# Function to validate input
def validate_entry(text):
    # Allows numbers, operators, decimal points, parentheses, and the root symbol
    if text == '':
        return True
    # Check that there are no multiple decimal points in a number
    parts = text.split('.')
    if len(parts) > 2:  # More than one decimal point
        return False
    # Verify that the characters are valid
    return all(char.isdigit() or char in '+-*/.√%()' for char in text)

# Configure validation in the Entry
validation = window.register(validate_entry)

# Create the viewer with Entry
visor = tk.Entry(
    window,
    textvariable=visor_text,
    font=('Arial', 20),
    justify='right',
    bd=0,
    insertwidth=4,
    bg='#152640',  # Same color as the window background
    fg='#08d49f',  # Text in aqua blue
    insertbackground='#08d49f',  # Cursor in aqua blue
    validate='key',
    validatecommand=(validation, '%P')
)
visor.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

# Viewfinder cleaning function
def clear():
    global expression, show_result
    expression = ''
    visor_text.set(expression)
    show_result = False

# Function to evaluate the expression
def evaluate_expression():
    global expression, show_result
    try:
        # Replace square root symbol with `math.sqrt()`
        temp_expr = expression
        # Use a regular expression to replace √number with math.sqrt(number)
        temp_expr = re.sub(r'√(\d+\.?\d*)', r'math.sqrt(\1)', temp_expr)
        # Evaluate the expression with access to the library `math`
        result = eval(temp_expr, {"math": math})
        # Convert to integer if result is an integer
        if result == int(result):
            result = int(result)
        expression = str(result)  # Convert result to string
        show_result = True  # Update result status
    except ZeroDivisionError:
        expression = 'Error: División entre cero'
        show_result = False
    except Exception as e:
        expression = f'Error: {str(e)}'  # Show error message
        show_result = False
    visor_text.set(expression)  # Update the viewer

# Function to handle button clicks
def on_button_click(value):
    global expression, show_result

    if value == 'C':  # Clean the viewfinder
        clear()
    elif value == '=':  # Evaluate the expression
        evaluate_expression()
    else:
        if show_result:  # If a result is displayed
            if value.isdigit():  # If the value is a number
                expression = value  # Start a new expression
                show_result = False  # Reset the result indicator
            else:
                # If you are a operator, continue with the current operator
                expression = visor_text.get() + value
                show_result = False  # Reset the result indicator
        else:
            # Avoid multiple decimal points in a number
            if value == '.':
                last_number_match = re.search(r'(\d+\.?\d*)$', expression)
                if last_number_match and '.' in last_number_match.group(1):
                    return  # Don´t add another decimal point
            expression += value  # Add the number or operator

        visor_text.set(expression)  # Update the viewer

# Function to create stylish buttons
def create_button(text, row, col, bg_color, fg_color, hover_bg=None, hover_fg=None, columnspan=1):
    button = tk.Button(
        window,
        text=text,
        font=('Arial', 12),
        bg=bg_color,
        fg=fg_color,
        bd=0,
        activebackground=hover_bg if hover_bg else bg_color,
        activeforeground=hover_fg if hover_fg else fg_color,
        relief='flat',
        command=lambda: on_button_click(text)  # Call function on click
    )
    button.grid(row=row, column=col, columnspan=columnspan, sticky='nsew', padx=5, pady=5)
    return button

# Create buttons with specific styles
# First row: circular buttons (simulated with background color)
create_button('C', 1, 0, '#152640', '#00daa1')  # Navy blue, aqua blue text
create_button('√', 1, 1, '#152640', '#00daa1')  # Navy blue, aqua blue text
create_button('%', 1, 2, '#152640', '#00daa1')  # Navy blue, aqua blue text
create_button('/', 1, 3, '#00daa1', '#152640')  # Aqua blue, navy text

# Middle buttons: transparent background, with text and hover effect
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2),
    ('0', 5, 0), ('.', 5, 1)
]

for text, row, col in buttons:
    create_button(text, row, col, '#253652', '#ffffff', hover_bg='#00daa1', hover_fg='#152640')

# Last column: blue buttons except the last one
create_button('*', 2, 3, '#152640', '#00daa1')  # Navy blue, aqua blue text
create_button('-', 3, 3, '#152640', '#00daa1')  # Navy blue, aqua blue text
create_button('+', 4, 3, '#152640', '#00daa1')  # Navy blue, aqua blue text
create_button('=', 5, 3, '#00daa1', '#152640')  # Aqua blue, navy text

# Function to handle keyboard events
def on_key_press(event):
    key = event.char
    if key in '0123456789+-*/.√%=':  # Allowed characters
        on_button_click(key)
    elif event.keysym == 'Return':  # Press Enter to calculate
        on_button_click('=')
    elif event.keysym == 'BackSpace':  # Delete with Backspace key
        global expression
        if expression:  # Only delete if there is something in the expression
            expression = expression[:-1]  # Delete last character
            visor_text.set(expression)

# Bind keyboard events to the window
window.bind('<Key>', on_key_press)

# Run the window
window.mainloop()