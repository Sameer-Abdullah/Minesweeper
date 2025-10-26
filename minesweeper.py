import tkinter  as tk
import random
buttons = []

# Cretes the Window
def create_window(rows, cols):
    window = tk.Tk()
    window.title("Minesweeper")

    width = (rows * 3) * 12
    height = (cols * 1) * 30
    window.geometry(f"{width}x{height}")
    window.resizable(False,False)
    return window

# Creates a grid with buttons centered
def create_grid(window, rows, cols):
    global buttons
    buttons = []

    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor="center") # Center all buttons in a frame
    
    for r in range(rows):
        row_buttons = []
        for c in range(cols):
            btn = tk.Button(frame, width=3, height=1, command=lambda r=r, c=c: on_click(r, c))
            btn.grid(row=r, column=c)
            row_buttons.append(btn)
        buttons.append(row_buttons)


# Assigns mine if random value is 1 or not mine for 0
def mine_or_not():
    return random.randint(0,1)

# Generating a minefield
def generate_minefield(rows, cols):
    global minefield
    minefield = []
    for r in range(rows):
        row_data = []
        for c in range(cols):
            cell_value = mine_or_not()
            row_data.append(cell_value)
        minefield.append(row_data)

def count_adjacent_mines(minefield, rows, cols):
    global numbers
    numbers = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if minefield[r][c] == 1:
                numbers[r][c] = -1  # mark this cell as a mine
                continue

            count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue  # skip the cell itself
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and minefield[nr][nc] == 1:
                        count += 1
            numbers[r][c] = count

    return numbers

def reveal_cell(r, c):
    # Out of bounds or already revealed
    if r < 0 or r >= len(minefield) or c < 0 or c >= len(minefield[0]):
        return
    if buttons[r][c]['state'] == 'disabled':
        return
    if minefield[r][c] == 1:
        return  # stop if it's a mine

    # Reveal current cell
    n = numbers[r][c]
    if n == 0:
        buttons[r][c].config(text="", bg="gray25", state="disabled")
    else:
        buttons[r][c].config(text=str(n), bg="gray25", fg="white", state="disabled")

    # If this cell is 0, recursively reveal all neighbors
    if n == 0:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                reveal_cell(r + dr, c + dc)


def on_click(r, c):
    if minefield[r][c] == 1:
        # Show bomb
        buttons[r][c].config(text="💣", bg="red", fg="white", state="disabled")
        # Optionally reveal all other mines
        for i in range(len(minefield)):
            for j in range(len(minefield[0])):
                if minefield[i][j] == 1 and buttons[i][j]['state'] != 'disabled':
                    buttons[i][j].config(text="💣", bg="red", fg="white", state="disabled")
        print("💥 Game Over!")
        return

    # Safe cell → reveal it and expand if 0
    reveal_cell(r, c)



# Main funtion
def main():
    rows, cols = 10,10
    generate_minefield(rows, cols)
    count_adjacent_mines(minefield, rows, cols)
    window = create_window(rows, cols)
    create_grid(window, rows, cols)
    window.mainloop()


    
if __name__== "__main__":
    main()
