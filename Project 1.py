#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/  AIRPLANE PASSENGER SEAT SELECTION  \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

# NAME: Michael Gage

# PROGRAM DESCRIPTION: This program assists passengers in selecting and purchasing airplane seats. It reads
# seat data from a file, allows seat booking, displays seat statistics, and suggests nearby seats if the
# requested one is taken.



#--------------------------------------------------CONSTANT VARIABLES---------------------------------------------------
ROWS = 10  # Number of rows on the plane
COLS = 4   # Number of columns on the plane



#----------------------------------------FUNCTIONS WITH ASSOCIATED INPUT/OUTPUT-----------------------------------------

#-----------------SEAT LAYOUT------------------
def display(seats):
    '''
    Display the current layout of the seats.
    :param seats: Python data structure with all the seat information (list of lists)
    :return: None
    '''
    print("\nSeating Chart: ")
    print("   A  B    C  D")
    for i in range(ROWS):
        row_str = f"{i + 1:2} "  # Row number starts from 1, using 2 characters for alignment
        for j in range(COLS):
            if j == 2:
                row_str += "  "  # Space for aisle between columns C and D
            row_str += f"{seats[i][j]}  "  # Seat status (either 'X' or '.')
        print(row_str)



#-------------OCCUPANCY STATISTICS---------------
def statistics(seats):
    '''
    Compute and display percentage of occupancy.
    :param seats: Python data structure with all the seat information
    :return: None
    '''
    total_seats = 0
    occupied_seats = 0

    # Loop through the seats to count total seats and occupied seats ('X')
    for row in seats:
        for seat in row:
            if seat == 'X':
                occupied_seats += 1
            if seat == 'X' or seat == '.':
                total_seats += 1

    # Calculate the occupancy percentage
    occupancy_percentage = (occupied_seats / total_seats) * 100

    # Print the statistics with one decimal place
    print(f"Plane occupancy: {occupancy_percentage:.1f}%")



#------------------PURCHASING SEATS------------------
def purchase(seats):
    '''
    Allow the user to purchase a seat and mark the seat as taken (replace . with X).
    :param seats: Python data structure with all the seat information
    :return: True if successfully assigned and updated the dataset and file; else False
    '''
    while True:
        # Ask the user for input (e.g., 1A, 5C, etc.)
        user_input = input("Enter your row number and column letter (ex. 1A): ").strip().upper()

        # Validate input length (row number + column letter)
        if len(user_input) != 2 and len(user_input) != 3:
            print("Invalid input. Please enter a row number and column letter (e.g., 1A).")
            continue

        # Extract row and column
        row_input = user_input[:-1]  # All characters except the last one for row
        column = user_input[-1]  # The last character should be the column letter

        # Validate row input
        if not row_input.isdigit():
            print("Invalid row number. Please try again.")
            continue

        row = int(row_input) - 1  # Convert row to 0-indexed (1 -> 0, 10 -> 9)

        # Validate row and column range
        if row < 0 or row >= ROWS:
            print("Invalid row number. Please try again.")
            continue
        if column not in ['A', 'B', 'C', 'D']:
            print("Invalid column letter. Please try again.")
            continue

        # Map column letter to index
        column_idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3}[column]

        # Check if the seat is available
        if seats[row][column_idx] == 'X':
            print(f"Seat {user_input} is not available.")
            # Suggest nearby seats if the selected seat is taken
            if not suggest_nearby_seats(seats, row, column_idx):
                print("No nearby available seats. Please try again later.")
            continue

        # Assign the seat and mark it as taken ('X')
        seats[row][column_idx] = 'X'
        print(f"Seat {user_input} has been successfully booked!")

        # Update the seat data in the text file
        try:
            with open("seats.txt", "w") as file:
                for r in range(ROWS):
                    file.write("".join(seats[r]) + "\n")
        except Exception as e:
            print(f"Error updating seat data file: {e}")
            return False

        return True



#--------------------SUGGESTING SEATS---------------------
def suggest_nearby_seats(seats, row, column_idx):
    '''
    Suggests nearby available seats based on the nearest neighbor search.
    :param seats: Python data structure with all the seat information
    :param row: The row number of the selected seat (0-indexed)
    :param column_idx: The column index (0 for A, 1 for B, 2 for C, 3 for D)
    :return: True if nearby seats are found, False if no seats are available
    '''
    found_seat = False

    # Define directions to check: [top, bottom, left, right, diagonal directions]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    # Diagonals (top-left, top-right, bottom-left, bottom-right) for non-window seats
    if column_idx != 0 and column_idx != 3:
        directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

    # Loop over all possible directions
    for dx, dy in directions:
        new_row = row + dx
        new_column = column_idx + dy

        # Check if the new position is valid (within bounds of the seating chart)
        if 0 <= new_row < ROWS and 0 <= new_column < COLS:
            # Check if the seat is available
            if seats[new_row][new_column] == '.':
                # Print the suggestion for available nearby seat
                print(f"Nearby available seat: {new_row + 1}{'ABCD'[new_column]}")
                found_seat = True

    return found_seat



#-------------------ASSIGNING SEATS AS TAKEN--------------------
def assign_seat(seats, row, column):
    '''
    Set an available seat as taken based on given row number and column letter.
    :param seats: Python data structure with all the seat information
    :param row: row to be booked
    :param column: column to be booked
    :return: True if successfully assigned the seat and updated all necessary data structures and files; else False
    '''
    if seats[row][column] == 'X':  # Seat already taken
        return False
    seats[row][column] = 'X'  # Mark as taken
    with open('seats.txt', 'w') as file:
        for r in seats:
            file.write(''.join(r) + '\n')  # Update the file
    return True



#----------------------------MENU DISPLAY--------------------------
def menu(seats):
    '''
    Display menu and handle user input.
    :param seats: Python data structure with all the seat information
    :return: None
    '''
    while True:
        print("\nSelect choice from menu:")
        print("D to display seat chart")
        print("P to purchase a seat")
        print("S to compute statistics")
        print("Q to quit\n")
        choice = input("Enter your choice: ").upper()

        if choice == 'D':
            display(seats)
        elif choice == 'P':
            purchase(seats)
        elif choice == 'S':
            statistics(seats)
        elif choice == 'Q':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")



#---------------------FILE LOAD/PROGRAM START-----------------------
def main():
    '''
    Main function to read the seat data from the file and start the menu.
    :return: None
    '''
    # Reading the seat layout from the file
    seats = []
    try:
        with open('seats.txt', 'r') as file:
            for line in file:
                seats.append(list(line.strip()))  # Load seat layout into a 2D list
    except FileNotFoundError:
        print("Error: seats.txt not found.")
        return

    menu(seats)  # Start the menu interface

if __name__ == "__main__":
    main()