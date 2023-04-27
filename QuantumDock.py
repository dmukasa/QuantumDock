# -------------------------------------------------------------------------- #
# ---------------------------- Imported Modules ---------------------------- #

# General modules
import os
import sys
# GUI Modules
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtCore import QTimer


# -------------------------------------------------------------------------- #
# ----------------------------- Gui Application ---------------------------- #

class quantumGUI(QtWidgets.QMainWindow):

    def __init__(self, folderPath = "./"):
        # Initialize the GUI application
        self.guiApp = QtWidgets.QApplication(sys.argv)  # Create a GUI, Parent Object
        super().__init__()  # Initialize QMainWindow functions.

        # Add a page/window to the GUI
        self.guiWindow = QtWidgets.QWidget()
        # Add a layout to the window
        self.guiLayout = QtWidgets.QGridLayout() # The layout that contains the text and buttons.
        self.guiLayout.setSpacing(0)
        self.guiWindow.setLayout(self.guiLayout)
        # Add scrollbar to the window
        self.scroll = QtWidgets.QScrollArea()    # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll.setWidget(self.guiWindow)

        # Specify the GUI dimensions.
        upperLeftXPos, upperLeftYPos = 50, 200   # The coordinates of the GUI from the top left hand corner.
        self.width, self.height = 1100, 700      # Specify the length, height of the GUI Window from upperLeftXPos, upperLeftYPos
        # Set window information
        self.setWindowTitle("QuantumDock")
        self.setGeometry(upperLeftXPos, upperLeftYPos, self.width, self.height)
        self.setStyleSheet("background-color : white")
        self.background = QtWidgets.QLabel(self.guiWindow)
        self.background.setGeometry(0, 0, self.width, self.height)

        # Set scrollbar properties.
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        #self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)
        self.scroll.verticalScrollBar().setStyleSheet('background: grey; margin-left: 1rem;')
        
        # Start the GUI
        self.displayWelcomePage()

        # Start the GUI
        self.show() # Display the GUI on the screen (pop-up)
        self.guiApp.exec() # Run the GUI continuosly
        
    # ---------------------------------------------------------------------- #
    # ------------------ Backend Intergration with Program ----------------- #
    
    def validateInputs(self, targetName, monomerName):
        if targetName == "" or monomerName == "":
            return False
        
        return True
    
    def _startProgram(self, targetName, monomerName, movieLabel, movie, userRelayText):
        if self.validateInputs(targetName, monomerName):
            userRelayText.setText("Program Running") #"\nTarget = '" + targetName + "'; Monomer = '" + monomerName + "'")

            # Start the movie
            movie.start()
                        
            # Specify the names of the monomer/target
            specifyTargetCommand = f"Molecule_1_name={targetName}"
            specifyMonomerCommand = f"Molecule_2_name={monomerName}"
            # Send commands to bash
            command = f"{specifyTargetCommand}; {specifyMonomerCommand}; export Molecule_1_name Molecule_2_name; sh Pose_Gen.sh"
            print("Excecuting Command:", command)
            # os.system(command)

            # Set the timeout duration to 10 seconds (10000 milliseconds)
            QTimer.singleShot(10000, lambda: self.updateMovie(movie, movieLabel, moviePath = "End Movie.gif"))
            QTimer.singleShot(10000, lambda: userRelayText.setText("Program Finished!"))
        else:
            userRelayText.setText("Invalid Inputs") #".\nTarget = '" + targetName + "'; Monomer = '" + monomerName + "'")
            print("Invalid Target/Monomer Inputs: ", targetName, monomerName)
            

    # ---------------------------------------------------------------------- #
    # ------------------------ Creating GUI Buttons ------------------------ #
    
    def clearScreen(self):
        """
        This method removes all widgets from the screen.
        """
        # Remove any background
        self.background.setMovie(None)
        self.setStyleSheet("background-image: white; background-color: white;")
        
        # Remove all objects
        for i in reversed(range(self.guiLayout.count())):
            widget = self.guiLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
            
    def setButtonAesthetics(self, widget, backgroundColor = "black", textColor = "white", fontFamily = "Arial", fontSize = 15, border = "0.5px solid black"):
        # Add color to background
        widget.setAutoFillBackground(True)
        widget.setStyleSheet(
            "background-color: " + backgroundColor + "; " + \
            "color: " + textColor + "; " + \
            "border: " + border + "; " + \
            "font-weight: 5rem; padding: 3rem 5rem; text-align: center; width: 100%; margin: 1rem 2rem;" \
        )

        # Add font information
        widget.setFont(QFont(fontFamily, fontSize))
    
    def setDimensions(self, element, minWidth, maxWidth, minHeight, maxHeight):
        # Add dynamic sizing
        if minHeight != None and minWidth != None:
            element.setMinimumSize(QSize(minWidth, minHeight));
        if maxWidth != None and maxHeight != None:
            element.setMaximumSize(QSize(maxWidth, maxHeight));
    
    def addTitleToGui(self, titleText, fontSize = 50):
        # Create the title text
        titleLabel = QtWidgets.QLabel(titleText)
        
        # Add styling to the title
        titleLabel.setAutoFillBackground(True)
        titleLabel.setFont(QFont("Arial", fontSize)) # Specify the font
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter) # Specify the alignment
        titleLabel.setStyleSheet("color: black; text-align: center; margin: 1rem auto;")
        
        # Add the title to the GUI
        self.guiLayout.addWidget(titleLabel, 0, 0, 1, 6)
    
    def setBackgroundImage(self, imagePath):    
        # Set the pixmap as the background image of a QLabel widget
        self.background.setStyleSheet(f"background-image: url({imagePath}); background-repeat: no-repeat; background-position: center center;")
    
    def inputText(self, startRow, startColumn, rows, columns, placeholderText = "Enter Text Here", onlyInt = False):
        """
        This method creates and returns a input textbox Widget with default
        styling given position and dimensions.
        
        If onlyInt is true, the widget will only accept integer values.
        
        Adds textbox to the window GUI layout and returns a QLineEdit Widget
        """
        currInput = QtWidgets.QLineEdit()
        currInput.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setDimensions(currInput, minWidth=300, maxWidth=400, minHeight=50, maxHeight=50)
        
        if onlyInt:
            # sets textbox to only accept integers between 0 and 1000.
            validator = QtGui.QIntValidator(0, 1000)
            currInput.setValidator(validator)
        
        # sets placeholder (default) text and adds stylistic choice
        currInput.setPlaceholderText(placeholderText)
        currInput.setStyleSheet("color: black; margin: 1rem 2rem; border: 0.5px solid black; padding: 1rem 3rem;")
        # Add input textbox to the GUI
        self.guiLayout.addWidget(currInput, startRow, startColumn, rows, columns, alignment=Qt.AlignmentFlag.AlignCenter)

        return currInput
    
    def updateMovie(self, movie, movieLabel, moviePath):
        # Stop the current QMovie
        movie.stop()
        # Load the new QMovie
        newMovie = QtGui.QMovie(moviePath)
        newMovie.setScaledSize(QtCore.QSize(300, 200))
        newMovie.setSpeed(200)
        # Set the new QMovie as the movie of the QLabel
        movieLabel.setMovie(newMovie)
        movieLabel.setStyleSheet("margin-top: 20px; background-color: #dbdbdb; width: 100%;")
        # Start playing the new QMovie
        newMovie.start()
        # Set the new QMovie object as the current QMovie object
        return newMovie
    
    # ---------------------------------------------------------------------- #
    # ------------------------ Creating GUI Windows ------------------------ #

    def displayWelcomePage(self):
        # Start off fresh by clearning the GUI elements.
        self.clearScreen()
        self.guiLayout.setSpacing(5)
        self.guiWindow.setLayout(self.guiLayout)
                
        # Set the background image as a GIF
        movie = QtGui.QMovie("./atom.gif")
        self.setStyleSheet("border: none; background-color: transparent")
        # movie.setScaledSize(self.background.size())
        movie.setScaledSize(QtCore.QSize(self.width, self.height))        
        movie.start()
        # Add the movie to the screen
        self.background.setMovie(movie)
       
        # Creates box for top logo
        itemBox = QtWidgets.QLabel("QuantumDock")
        itemBox.setStyleSheet("background-color: transparent; color: transparent; font-family: Arial; font-size: 50px;")
        self.setDimensions(itemBox, minWidth=None, maxWidth=None, minHeight=50, maxHeight=50)
        self.setButtonAesthetics(itemBox, backgroundColor="transparent", textColor="white", fontFamily="Arial", fontSize=50, border = "None") 
        self.guiLayout.addWidget(itemBox, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Create the start button to begin an experiment.
        addSubjectInfoButton = QtWidgets.QPushButton("Start Program")
        addSubjectInfoButton.clicked.connect(lambda: self.displaySecondPage())
        # Add button aesthetics: colors and text styles.
        self.setDimensions(addSubjectInfoButton, minWidth=200, maxWidth=200, minHeight=50, maxHeight=50)
        self.setButtonAesthetics(addSubjectInfoButton, backgroundColor="white", textColor="black", fontFamily="Arial", fontSize=15)
        self.guiLayout.addWidget(addSubjectInfoButton, self.guiLayout.rowCount(), 0, 1, -1, alignment=Qt.AlignmentFlag.AlignHCenter)
            
    def displaySecondPage(self):
        # Start off fresh by clearning the GUI elements.
        self.clearScreen()
        self.guiLayout.setSpacing(5)
        self.guiWindow.setLayout(self.guiLayout)
    
        # Set the background image as a GIF, oad the background image
        self.setBackgroundImage("grid_background.png")
    
        # Creates box for experiment buttons
        itemBox = QtWidgets.QLabel()
        itemBox.setStyleSheet("background-color: #dbdbdb; width: 100%; border: 2px solid black;")
        self.guiLayout.addWidget(itemBox, 3, 0, 4, 9)
        #self.guiLayout.addWidget(itemBox, 5, 0, 2, 9) # reduce the height value from 4 to 2

        # Creates box for experiment buttons
        headerText = QtWidgets.QLabel("""QuantumDock""")
        headerText.setWordWrap(True)
        headerText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.setDimensions(headerText, minWidth=200, maxWidth=200, minHeight=50, maxHeight=50)
        self.setDimensions(headerText, minWidth=1000, maxWidth=1000, minHeight=100, maxHeight=100)
        self.setButtonAesthetics(headerText, backgroundColor="transparent", textColor="white", fontFamily="Arial", fontSize=50)
        self.guiLayout.addWidget(headerText, 0, 0, 1, 9, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Create a QLabel widget
        label = QtWidgets.QLabel()
        # Add the movie
        movie = QtGui.QMovie("./PHE-PYR.gif")
        movie = self.updateMovie(movie, movieLabel = label, moviePath = "./PHE-PYR.gif")
        # Add the QLabel to the layout
        self.guiLayout.addWidget(label, 3, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Create textbox for target button
        targetInput_Object = self.inputText(4, 3, 1, 1, "Choose Target")
        targetInput_Object.setStyleSheet("float: right; color: black; margin: 1rem auto; border: 1px solid black; font-size: 25px;")
    
        # Creates box for experiment texts
        userRelayText = QtWidgets.QLabel("Target Molecule")
        # userRelayText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setDimensions(userRelayText, minWidth=None, maxWidth=None, minHeight=50, maxHeight=50)
        self.setButtonAesthetics(userRelayText, backgroundColor="transparent", textColor="black", fontFamily="Arial", fontSize=25)
        userRelayText.setStyleSheet("background-color: transparent; border: none; text-align: center; margin: auto; width: 50%;")
        self.guiLayout.addWidget(userRelayText, 5, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter) # row, column, rowspan, columnspan    
    
        # Create textbox for monomer button
        monomerInput_Object = self.inputText(4, 5, 1, 1, "Choose Monomer")
        monomerInput_Object.setStyleSheet("float: left; color: black; margin: 1rem auto; border: 1px solid black; font-size: 25px;")
    
        # Creates box for experiment texts
        userRelayText = QtWidgets.QLabel("Monomer Molecule")
        # userRelayText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setDimensions(userRelayText, minWidth=None, maxWidth=None, minHeight=50, maxHeight=50)
        self.setButtonAesthetics(userRelayText, backgroundColor="transparent", textColor="black", fontFamily="Arial", fontSize=25)
        userRelayText.setStyleSheet("background-color: transparent; border: none; text-align: center; margin: auto; width: 50%;")
        self.guiLayout.addWidget(userRelayText, 5, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter) # row, column, rowspan, columnspan
    
        # Creates box for experiment texts
        userRelayText = QtWidgets.QLabel("Choose your interacting system")
        userRelayText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setDimensions(userRelayText, minWidth=None, maxWidth=None, minHeight=50, maxHeight=50)
        self.setButtonAesthetics(userRelayText, backgroundColor="transparent", textColor="black", fontFamily="Arial", fontSize=25)
        userRelayText.setStyleSheet("background-color: transparent; border: none; text-align: center; margin: auto; width: 50%;")
        self.guiLayout.addWidget(userRelayText, 6, 3, 1, 3, alignment=Qt.AlignmentFlag.AlignHCenter) # row, column, rowspan, columnspan

        # Create the start button to begin an experiment.
        startExperimentButton = QtWidgets.QPushButton("Start Program")
        startExperimentButton.clicked.connect(lambda: self._startProgram(targetInput_Object.text(), monomerInput_Object.text(), label, movie, userRelayText))
        startExperimentButton.setStyleSheet("margin-top: 1000px; background-color: #dbdbdb; width: 100%;")
        # Add button aesthetics: colors and text styles.
        self.setDimensions(startExperimentButton, minWidth=150, maxWidth=200, minHeight=50, maxHeight=50)
        self.setButtonAesthetics(startExperimentButton,backgroundColor = "#7cdf91", textColor = "#000000", fontFamily = "Arial", fontSize = 23)
        # Add the quit button to the layout.
        # Add an empty label widget for spacing
        self.guiLayout.addWidget(startExperimentButton, 5, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter) # row, column, rowspan, columnspan

        # Center the input text boxes
        self.guiLayout.setAlignment(targetInput_Object, Qt.AlignmentFlag.AlignHCenter)
        self.guiLayout.setAlignment(monomerInput_Object, Qt.AlignmentFlag.AlignHCenter)


        
if __name__ == "__main__":
    # Open the questionaire GUI.
    guiObject = quantumGUI(folderPath = "./")     


