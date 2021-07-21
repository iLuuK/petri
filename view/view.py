import tkinter.messagebox
import tkinter
from shared.iController import IController
from shared.iModel import IModel
from shared.iColor import IColor
from shared.iCell import ICell
from shared.action import Action
import json


def rgbToHex(red: int, green: int, blue: int):
    return f'#{red:02x}{green:02x}{blue:02x}'


def colorToHex(color: IColor):
    return rgbToHex(color.getRed(), color.getGreen(), color.getBlue())


class View:
    def __init__(self, controller: IController, model: IModel):
        self.__controller = controller
        self.__model = model
        self.__knowCells: [int] = []
        self.__createWindow()
        self.__loadConf()

    def __createWindow(self):
        self.__window = tkinter.Tk()
        self.__window.title("Petri Python")
        self.__window.geometry("800x800")
        self.__canvas = tkinter.Canvas(self.__window)
        self.__canvas.configure(bg="black")
        self.__canvas.pack(fill="both", expand=True)
        self.__window.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__window.bind("<KeyPress>", self.__keyPress)
        self.__window.deiconify()
        self.__window.update()

    def __keyPress(self, *args):
        self.__controller.performAction(Action.play)
        self.show()

    def show(self):
        totalCells = len(self.__model.getCells())
        totalKnowCells = len(self.__knowCells)
        print("Cells new : ", totalCells - totalKnowCells, " old : ", totalKnowCells)
        for cell in self.__model.getCells():
            if not cell.getId() in self.__knowCells:
                self.__knowCells.append(cell.getId())
                if self.__petriPythonConf["drawCellBorder"] == 0:
                    __outline = colorToHex(cell.getColor())
                else:
                    __outline = "white"
                self.__canvas.create_rectangle(self.__cellGetX0Scaled(cell),
                                               self.__cellGetY0Scaled(cell),
                                               self.__cellGetX1Scaled(cell),
                                               self.__cellGetY1Scaled(cell),
                                               fill=colorToHex(cell.getColor()),
                                               outline=__outline)
        self.__window.update()

    def __cellGetX0Scaled(self, cell: ICell):
        return cell.getX() * (self.__window.winfo_width() / cell.getPetri().getWidth())

    def __cellGetX1Scaled(self, cell: ICell):
        return (cell.getX() + 1) * (self.__window.winfo_width() / cell.getPetri().getWidth())

    def __cellGetY0Scaled(self, cell: ICell):
        return cell.getY() * (self.__window.winfo_height() / cell.getPetri().getHeight())

    def __cellGetY1Scaled(self, cell: ICell):
        return (cell.getY() + 1) * (self.__window.winfo_height() / cell.getPetri().getHeight())

    def __on_closing(self):
        self.__controller.performAction(Action.close)
        self.__window.destroy()

    def __loadConf(self):
        with open('conf/petriPython.json') as jsonfile:
            self.__petriPythonConf = json.load(jsonfile)
