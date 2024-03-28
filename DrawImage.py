#Par Timothé Kalinka (Wida)
#PS: Il peut être nécessaire de modifié la taille de la fenêtre ou la brosse, pour cela augmenter le temps à la ligne 163

from PIL import Image
import time
from pynput import mouse
from pynput.keyboard import Key, Controller
import os

start = time.time()

currentSupport = "Paint10"

color_supports = {"Paint10" : [0, 0, 0, 127, 127, 127, 136, 0, 21, 237, 28, 36, 255, 127, 39, 255, 242, 0, 34, 177,
                            76, 0, 162, 232, 63, 72, 204, 163, 73, 164, 255, 255, 255, 195, 195, 195, 185, 122, 87,
                            255, 174, 201, 255, 201, 14, 239, 228, 176, 181, 230, 29, 153, 217, 234, 112, 146, 190, 200,
                            191, 231],
                 "Paint3D" : [255,255,255, 195,195,195, 88,88,88, 0, 0, 0, 136,0,27, 228,28,36, 255,127,39, 255,
                            202, 24, 253, 236, 166, 255, 242, 0, 196, 255, 14, 14, 209, 69, 140, 255,251,  0,168,243,
                            63,72,204, 184, 61, 186, 255, 174,200, 185,122,86],
                 "Paint11" : [0, 0, 0, 127, 127, 127, 136, 0, 21, 237, 28, 36, 255, 127, 39, 255, 242, 0, 34, 177,
                            76, 0, 162, 232, 63, 72, 204, 163, 73, 164, 255, 255, 255, 195, 195, 195, 185, 122, 87,
                            255, 174, 201, 255, 201, 14, 239, 228, 176, 181, 230, 29, 153, 217, 234, 112, 146, 190, 200,
                            191, 231]
                 }

coord_supports = {"Paint10" : [(882,60),(901,58),(924,60),(948,61),(966,59),(995,59),(1013,57),(1034,61),(1054,60),
                              (1077,59),(883,85),(902,81),(928,84),(945,83),(968,84),(991,84),(1014,84),(1034,84),
                              (1056,83),(1079,85)],
                  "Paint3D": [(1681, 880), (1732, 872), (1768, 873), (1812, 876), (1848, 874), (1873, 872), (1697, 916),
                              (1734, 919), (1771, 917), (1806, 916), (1841, 913), (1871, 912), (1698, 949), (1732, 950),
                              (1769, 950), (1810, 947), (1841, 953), (1879, 954)],
                  "Paint11" : [(850,90), (875,90), (900,90), (925,90), (950,90), (975,90), (1000,90), (1025,90), (1050,90),
                              (1075,90), (850,115), (875,115), (900,115), (925,115), (950,115), (975,115), (1000,115),
                              (1025,115), (1050,115), (1075,115)]
                  }

coord_start = {"Paint10" : (200,200), 'Paint11' : (263,90)}
colorsId = color_supports[currentSupport]
colorsCoord = coord_supports[currentSupport]

class DataPreparation:
    def __init__(self):
        self.SourceImage = Image.open("Lycee.jpg")

        self.xWantedSize = 900
        self.yWantedSize = 1700

        self.Palette = Image.new("P", (21, 1))

        self.grey = False

    def sizeModification(self):
        global x_size, y_size
        x_size, y_size = self.SourceImage.size
        y_optimal_size = int((y_size * self.xWantedSize) / x_size)
        x_optimal_size = int((x_size * self.yWantedSize) / y_size)

        if x_size > self.xWantedSize:
            self.SourceImage = self.SourceImage.resize((self.xWantedSize, y_optimal_size))

        elif y_size > self.yWantedSize:
            self.SourceImage = self.SourceImage.resize((x_optimal_size, self.yWantedSize))

        x_size, y_size = self.SourceImage.size

    def colorModification(self):
        self.sizeModification()
        self.Palette.putpalette(colorsId)
        self.SourceImage = self.SourceImage.convert("RGB")

        if self.grey:
            self.SourceImage = self.SourceImage.convert("L")

        self.quantizedImage = self.SourceImage.quantize(palette=self.Palette)
        self.quantizedImage.save("quantizedImage.png")
        return self.quantizedImage


class ImagePrinter:
    def __init__(self):
        self.colorsBrutData = list(Datas.colorModification().getdata())
        self.comboTrue = 0
        self.comboFalse = 0
        self.startByColor = []
        self.order = []
        self.basePosition = 200
        self.mouse = mouse.Controller()
        self.colorsByLineData = [self.colorsBrutData[i:i + x_size] for i in range(0, len(self.colorsBrutData), x_size)]

    def list_modification(self, color):
        self.order = []
        self.startByColor = []
        for lines in range(len(self.colorsByLineData)):
            orderLine = []
            if self.colorsByLineData[lines][0] == color:
                self.startByColor.append(True)
            else:
                self.startByColor.append(False)

            for i in range (x_size):

                if self.colorsByLineData[lines][i] == color:
                    if self.comboFalse != 0:
                        orderLine.append(self.comboFalse)
                        self.comboFalse = 0
                    self.comboTrue += 1

                else:
                    if self.comboTrue != 0:
                        orderLine.append(self.comboTrue)
                        self.comboTrue = 0
                    self.comboFalse += 1

            if self.comboFalse != 0:
                orderLine.append(self.comboFalse)
                self.comboFalse = 0
            elif self.comboTrue != 0:
                orderLine.append(self.comboTrue)
                self.comboTrue = 0

            self.order.append(orderLine)

    def goToColor(self, valeure):
        self.mouse.position=(colorsCoord[valeure][0], colorsCoord[valeure][1])#Se dépelace vers la couleure voulue
        time.sleep(0.1)
        self.mouse.press(mouse.Button.left)
        self.mouse.release(mouse.Button.left)


    def drawing(self):
        for color in range (len(colorsCoord)):
            self.list_modification(color)
            time.sleep(0.1)
            self.goToColor(color)
            time.sleep(0.1)

            for lines in range(len(self.order)):
                self.mouse.position = (self.basePosition, self.basePosition  + lines)
                time.sleep(0.001)
                xStep = 0
                for nbOfChanging in range(len(self.order[lines])):
                    xStep += self.order[lines][nbOfChanging]
                    if (nbOfChanging%2 == 0 and self.startByColor[lines]) or (nbOfChanging%2 != 0 and self.startByColor[lines] == False):
                        self.mouse.press(mouse.Button.left)
                        self.mouse.position = ((self.basePosition + xStep), self.basePosition + (lines))
                        self.mouse.release(mouse.Button.left)
                        time.sleep(0.001)

                    else:
                        self.mouse.release(mouse.Button.left)
                        self.mouse.position = ((self.basePosition + xStep), self.basePosition + (lines))
                        time.sleep(0.001)


                    self.mouse.move(1, 0)


mouseControl = mouse.Controller()
keyboardControl = Controller()

os.system('start /max mspaint')
time.sleep(2)

mouseControl.position = coord_start[currentSupport]
mouseControl.click(mouse.Button.left)


Datas = DataPreparation()
Printer = ImagePrinter()
Printer.drawing()

print(f"Temps d'éxécution : {round(time.time()-start, 3)} secondes")