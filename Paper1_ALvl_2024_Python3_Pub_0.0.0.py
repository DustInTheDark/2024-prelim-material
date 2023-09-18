#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

import random
import os

# Main function to start the puzzle game
def Main():
    Again = "y" # Initialize the variable 'Again' to 'y' to start the loop
    Score = 0 # Initialize the player's score to 0
    while Again == "y": # Loop to keep playing the game until the user decides to stop
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ") # Prompt the user to either start a standard puzzle or load a puzzle from a file
        if len(Filename) > 0: # If the user provides a filename, load the puzzle from that file
            MyPuzzle = Puzzle(Filename + ".txt")
        else: # If the user presses Enter without providing a filename, start a standard puzzle
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle() # Attempt the puzzle and store the score
        print("Puzzle finished. Your score was: " + str(Score)) # Display the user's score after attempting the puzzle
        Again = input("Do another puzzle? ").lower() # Ask the user if they want to play another puzzle

class Puzzle(): # Puzzle class to handle the game logic, including loading puzzles, checking patterns, and managing the game state.
    def __init__(self, *args): # Constructor to initialize the puzzle. It can either load a puzzle from a file or create a new one based on given dimensions.
        if len(args) == 1: # Check if only one argument is provided, which would be the filename to load the puzzle from
 
            #  Initialize score, symbols left, grid size, grid, allowed patterns, and allowed symbols to their default values
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0]) # Load the puzzle from the provided filename

        else: # If more than one argument is provided, create a new puzzle based on the given dimensions
            self.__Score = 0 # set score to 0
            self.__SymbolsLeft = args[1] # set symbols left
            self.__GridSize = args[0] # set grid size (based on passed arguments)
            
            self.__Grid = [] # initialize the grid for the puzzle
            for Count in range(1, self.__GridSize * self.__GridSize + 1): # propulate the grid with cells - most cells are standard, but some are blocked
                if random.randrange(1, 101) < 90: # 90% chance to add a standard cell
                    C = Cell()
                else: # 10% chance to add a blocked cell.
                    C = BlockedCell()
                self.__Grid.append(C)
            
            # initialize the lists that will store the allowed patterns and symbols for the puzzle
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            
            QPattern = Pattern("Q", "QQ**Q**QQ") # define the default pattersn + symbols for puzzle
            self.__AllowedPatterns.append(QPattern) # add the "Q" pattern to the list of allowed patterns
            self.__AllowedSymbols.append("Q") # add the "Q" symbols to the list of allowed symbols
            
            XPattern = Pattern("X", "X*X*X*X*X") # define the default patterns + symbols for the puzzle
            self.__AllowedPatterns.append(XPattern) # add the "X" pattern to the list of allowed patterns
            self.__AllowedSymbols.append("X") # add the "X" symbol to the list of allowed symbols
            
            TPattern = Pattern("T", "TTT**T**T") # define the default patterns + symbols for the puzzle
            self.__AllowedPatterns.append(TPattern) # add the "T" pattern to the list of allowed patterns
            self.__AllowedSymbols.append("T") # add the "T" symbol to the list of allowed symbols

    # Private method to load a puzzle from a specified file.
    def __LoadPuzzle(self, Filename):
        # Try to open and read the specified file.
        try:
            with open(Filename) as f:
                # Read the number of symbols from the file.
                NoOfSymbols = int(f.readline().rstrip())
                
                for Count in range(1, NoOfSymbols + 1): # Iterate through the number of patterns specified in the file.
                    Items = f.readline().rstrip().split(",") # Split each line by comma to separate the pattern symbol from its sequence.
                    P = Pattern(Items[0], Items[1]) # Create a new Pattern object using the symbol and its sequence.
                    self.__AllowedPatterns.append(P) # Add the newly created pattern to the allowed patterns list.

                self.__GridSize = int(f.readline().rstrip()) # Read the grid size for the puzzle from the file.

                for Count in range(1, self.__GridSize * self.__GridSize + 1): # Iterate through each cell in the grid based on the grid size.
                    Items = f.readline().rstrip().split(",") # Split each line by comma to separate cell details.
                    if Items[0] == "@": # Check if the cell is a blocked cell (represented by "@").
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else: # If the cell is not blocked, load its details.
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0]) # Set the symbol for the cell
                        for CurrentSymbol in range(1, len(Items)): # Add any symbols that are not allowed in this cell
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C) # Add the cell to the grid.

                # Read and set the current score and the number of symbols left to be placed in the puzzle.
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        
        # If there's an error in reading the file or processing its contents, display an error message.
        except:
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        Finished = False # Initialize a flag to check if the puzzle is completed.
        while not Finished: # Continue the loop until the puzzle is finished.
            self.DisplayPuzzle() # Display the current state of the puzzle.
            
            print("Current score: " + str(self.__Score)) # Display the current score.
            
            Row = -1 # Get a valid row number from the user.
            Valid = False
            while not Valid: # Loop to ensure the user provides a valid row number.
                try:
                    Row = int(input("Enter row number: ")) # Attempt to get an integer input for the row number.
                    Valid = True # If successful, set the Valid flag to True.
                except: 
                    pass # If the input is not a valid integer, continue prompting the user.

            Valid = False # Reset the Valid flag for the next input.

            while not Valid: # Loop to ensure the user provides a valid column number.
                try:
                    Column = int(input("Enter column number: ")) # Attempt to get an integer input for the column number.
                    Valid = True # If successful, set the Valid flag to True.
                except:
                    pass # If the input is not a valid integer, continue prompting the user.

            Symbol = self.__GetSymbolFromUser() # Get the desired symbol from the user.

            self.__SymbolsLeft -= 1 # Decrement the count of symbols left to be placed in the puzzle.

            CurrentCell = self.__GetCell(Row, Column) # Retrieve the specific cell based on the user's provided row and column.

            if CurrentCell.CheckSymbolAllowed(Symbol): # Check if the chosen symbol can be placed in the selected cell
                CurrentCell.ChangeSymbolInCell(Symbol) # Place the symbol in the cell
                
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column) # Determine if placing the symbol results in a matching pattern.
                
                if AmountToAddToScore > 0: # If a match is found, update the score.
                    self.__Score += AmountToAddToScore

            if self.__SymbolsLeft == 0: # If all symbols have been placed, the puzzle is considered finished.
                Finished = True

            # Display the final state of the puzzle.
            print()
            self.DisplayPuzzle()
            print()

            # Return the player's final score.
            return self.__Score

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1 # Calculate the index of the cell in the grid based on the provided row and column.
        if Index >= 0: # If the calculated index is valid (non-negative), return the cell at that index.
            return self.__Grid[Index]
        else: # If the index is invalid (negative), raise an IndexError exception.
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        # Begin iterating over a 3x3 grid. The iteration starts from two rows above the provided Row 
        # and goes downwards, and spans from two columns to the left of the provided Column to the column itself.
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    
                    PatternString = "" # Initialize an empty string to represent the pattern formed by the symbols in the 3x3 grid.
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()# Concatenate the symbol from the top-left cell of the 3x3 grid to the PatternString.
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol() # Concatenate the symbol from the cell to the right of the top-left cell.
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol() # Concatenate the symbol from the top-right cell of the 3x3 grid.
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol() # Move one row down and concatenate the symbol from the rightmost cell.
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol() # Move another row down and concatenate the symbol from the rightmost cell.
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol() # Concatenate the symbol from the cell to the left of the bottom-right cell.
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol() # Concatenate the symbol from the bottom-left cell of the 3x3 grid.
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol() # Move one row up and concatenate the symbol from the leftmost cell.
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol() # Concatenate the symbol from the center cell of the 3x3 grid.
                    for P in self.__AllowedPatterns: # Iterate through the list of predefined allowed patterns.
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol() # Iterate through the list of predefined allowed patterns.
                        
                        # Check if the constructed pattern (PatternString) matches the current allowed pattern (P) 
                        # and if the symbol in the specified cell is the one being checked in the pattern.
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            # If there's a match, the current symbol is added to a list of symbols that 
                            # are not allowed to be placed in each cell of the 3x3 grid. This is to ensure 
                            # that the same pattern doesn't get repeated in subsequent moves.
                            # Mark the top-left cell of the 3x3 grid.
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            # ... (similar lines for other cells in the 3x3 grid) ...
                            # Mark the center cell of the 3x3 grid.
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            # If a valid pattern match is found, the function returns a score of 10 
                            # indicating a successful match and exits.
                            return 10
                # If there's an exception, like trying to access a cell that's out of the bounds 
                # of the grid, the exception is caught and the loop continues to the next iteration.
                except:
                    pass

        # If the function hasn't returned by this point, it means no valid pattern matches 
        # were found in the entire grid. Therefore, it returns a score of 0.
        return 0

    def __GetSymbolFromUser(self):
        Symbol = "" # Initialize an empty string for the symbol.
        while not Symbol in self.__AllowedSymbols: # Continuously prompt the user until a valid symbol from the allowed list is entered.
            Symbol = input("Enter symbol: ")
        return Symbol # Return the valid symbol entered by the user.

    def __CreateHorizontalLine(self):
        Line = "  " # Initialize a string with two spaces for the line's starting point.
        for Count in range(1, self.__GridSize * 2 + 2): # Loop through a range based on the grid size to construct the horizontal line.
            Line = Line + "-"
        return Line # Return the constructed horizontal line.

    def DisplayPuzzle(self):
        print() # Start with a blank line for visual separation when displaying the puzzle.
        if self.__GridSize < 10: # If the grid size is single-digit (less than 10), we adjust the column headers accordingly.
            print("  ", end='') # Print two spaces to align the column numbers with the grid.
            for Count in range(1, self.__GridSize + 1): # Loop through the grid size to print each column number.
                print(" " + str(Count), end='') # Print each column number with a space before it for alignment.
        print()
        
        # Print a horizontal line to visually separate the header from the grid.
        # This line is constructed using the __CreateHorizontalLine method.
        print(self.__CreateHorizontalLine())
        
        for Count in range(0, len(self.__Grid)): # Iterate through the entire grid to print each cell's symbol.
            if Count % self.__GridSize == 0 and self.__GridSize < 10:# At the beginning of each row, and if the grid size is less than 10,
                row_number = self.__GridSize - ((Count + 1) // self.__GridSize) # calculate row number - based on current cell's position
                print(str(row_number) + " ", end='') # print row number
            print("|" + self.__Grid[Count].GetSymbol(), end='') # Print the symbol of the current cell enclosed by vertical bars.

            # At the end of each row, close the row with a vertical bar, 
            # move to the next line, and print a horizontal line to separate rows.
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

class Pattern():
    def __init__(self, SymbolToUse, PatternString): # Constructor for the Pattern class.
        self.__Symbol = SymbolToUse # Store the symbol associated with this pattern.
        self.__PatternSequence = PatternString # Store the sequence or layout of the pattern as a string.

    def MatchesPattern(self, PatternString, SymbolPlaced):
        # First, we check if the symbol that was placed (SymbolPlaced) is the same as the symbol 
        # associated with this particular pattern. If not, the pattern cannot match, and we return False.
        if SymbolPlaced != self.__Symbol:
            return False
        
        # We then iterate through each character position in our pattern sequence.
        for Count in range(0, len(self.__PatternSequence)):
            try:
                # For each position, we check two things:
                # 1. If the character in our pattern sequence is the pattern's symbol.
                # 2. If the corresponding character in the provided PatternString is NOT the pattern's symbol.
                # If both conditions are met, it means the PatternString does not match our pattern at this position.
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                # If there's an exception, it's likely due to an out-of-bounds access (i.e., the provided PatternString 
                # might be shorter than our pattern sequence). In such cases, we print a detailed error message 
                # to help with debugging.
                print(f"EXCEPTION in MatchesPattern: {ex}")
        
        # If we've gone through the entire pattern sequence without returning False, it means the provided PatternString 
        # matches our pattern sequence for the given symbol. Therefore, we return True.
        return True

def GetPatternSequence(self): # This function returns the private attribute __PatternSequence.
    return self.__PatternSequence # The __PatternSequence represents the sequence or layout of the pattern as a string.

class Cell():
    def __init__(self): # Constructor for the Cell class.
        self._Symbol = "" # initialize _Symbole attribute to an empty string - attribute represents symbol currently present in the cell
        self.__SymbolsNotAllowed = [] # initialize the __SymbolsNotAllowed list as an empty list - stores symbols that are not allowed to be placed in this cell

    def GetSymbol(self):
        if self.IsEmpty(): # Check if the cell is empty using the IsEmpty() method.
            return "-" # If the cell is empty, return a dash ("-") as a placeholder.
        else:
            return self._Symbol # If the cell is not empty, return the symbol currently present in the cell.
    
    def IsEmpty(self):
        if len(self._Symbol) == 0: # Check the length of the _Symbol attribute.
            return True # If the length is 0, it means the cell does not contain any symbol and is considered empty.
        else:
            return False # If the length is not 0, the cell contains a symbol and is not empty.

    def ChangeSymbolInCell(self, NewSymbol):
        # Update the _Symbol attribute of the cell with the provided NewSymbol.
        # This effectively changes or sets the symbol currently present in the cell.
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        for Item in self.__SymbolsNotAllowed: # Iterate through each symbol in the __SymbolsNotAllowed list.
            if Item == SymbolToCheck: # If the symbol being checked (SymbolToCheck) is found in the list,
                return False # it means this symbol is not allowed in the cell.
        # If the loop completes without finding the symbol in the list,
        return True # it means the symbol is allowed in the cell.

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        self.__SymbolsNotAllowed.append(SymbolToAdd) # Add the provided symbol (SymbolToAdd) to the __SymbolsNotAllowed list.
        # This ensures that the symbol will not be allowed in this cell in the future.

    def UpdateCell(self):
        # This is a placeholder method, currently doing nothing.
        # It's likely intended to be filled in with functionality to update the cell in the future.
        pass

class BlockedCell(Cell):
    def __init__(self): # Constructor for the BlockedCell class, which inherits from the Cell class
        super(BlockedCell, self).__init__() # Call the constructor of the parent Cell class to initialize inherited attributes
        # This indicates that the cell is blocked and cannot be modified
        self._Symbol = "@" # Override the _Symbol attribute with the "@" symbol
        # This indicates that the cell is blocked and cannot be modified

    def CheckSymbolAllowed(self, SymbolToCheck): # This method always returns False, indicating that no symbol is allowed in this cell.
        return False # This behavior is consistent with the nature of a BlockedCell, which should not accept any symbols.

if __name__ == "__main__":
    # This conditional checks if the script is being run as the main program.
    # If it is, then the Main() function is called to execute the primary logic of the script.
    # This structure is commonly used in Python scripts to allow for both standalone execution 
    # and the possibility to import the script as a module in other scripts without running the main logic.
    Main()