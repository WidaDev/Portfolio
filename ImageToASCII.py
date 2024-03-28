from PIL import Image as Img
from resizeimage import resizeimage

taille=300
def Import(ImageEntrée):
    ImageOuverte=Img.open(ImageEntrée)
    ImageOuverte=resizeimage.resize_width(ImageOuverte,int(taille))
    ImageOuverte=ImageOuverte.convert('L')
    return ImageOuverte
Image=Import("ponton.jpg")

def ToAscii(Image):
    Result=open("data.txt", "w")
    CHAR_LIST = {0:'@', 1:'%', 2:'#', 3:'*', 4:'+', 5:'=', 6:';', 7:',', 8:'-', 9:'.', 10:' '}
    Image_dat=list(Image.getdata())
    Image_ASCII=""
    for ligne in range (int(len(Image_dat)/taille)):
        for pixelnum in range (taille):
            couleur=Image_dat[pixelnum+(ligne*taille)]
            for n in range (round(taille/110)):
                Image_ASCII+=ToCHAR(couleur, CHAR_LIST)
        Image_ASCII+= '\n'
    Result.write(Image_ASCII)
    Result.close()
    print(Image_ASCII)

def ToCHAR(couleur, CHAR_LIST):
    Inde=int(couleur/24)
    Car=CHAR_LIST.get(Inde)
    return Car

ToAscii(Image)