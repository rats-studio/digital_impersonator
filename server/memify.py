import os
import platform

from random import randint
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


FONT_SIZE = 25
LIMIT = 50
BORDER_SIZE = 1
MEMES_FOLDER = os.path.join("client", "static", "img", "memes")
SAMPLE_PICS = os.path.join("client", "static", "img", "sample_img")
FONT_FAMILY = "Arial.ttf"


class Meme:

    def __init__(self,
                 text="default string",
                 font_size=FONT_SIZE,
                 limit=LIMIT,
                 border_size=BORDER_SIZE,
                 memes_folder=MEMES_FOLDER,
                 sample_pics=SAMPLE_PICS,
                 font_family=FONT_FAMILY
                 ):
        self.text = text
        self.font_size = font_size
        self.limit = limit
        self.border_size = border_size
        self.memes_folder = memes_folder
        self.font_family = font_family
        self.sample_pics = sample_pics

        self.img = self._get_random_image()

        self.canvas = Image.new("RGBA", self.img.size, (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.canvas)

        self._draw_border()
        self._draw_text()
        self.meme = Image.alpha_composite(self.img, self.canvas)

    def _get_text_position(self):
        """
        should return list of tree-value tuple [(x, y, text)]
        """
        width, height = self.img.size
        width = width - width + 20
        height = height - self.font_size*2
        ret_val = []

        processing_text = self.text

        while True:
            if len(processing_text) > self.limit:
                s = self.find_split(processing_text)
                ret_val.append((width, height, processing_text[:s]))
                processing_text = processing_text[s:]
                processing_text = processing_text.strip()
            else:
                ret_val.append((width, height, processing_text))
                break
        
        sentences = len(ret_val)
        real_ret_val = []  # omg this made me lol so hard. Super-hackerman

        for i in ret_val:
            x, y = (i[0], i[1])
            real_ret_val.append((x, y - (sentences*self.font_size), i[2]))
            sentences -= 1

        return real_ret_val

    def find_split(self, text):
        sub = 0
        while text.find(" ", sub+1) < self.limit and text.find(" ", sub+1) != -1:
            sub = text.find(" ", sub+1)

        return sub 

    def get_font(self):
        try:
            # choice of font depends on which OS this is running on
            o_sys = platform.system()
            
            if o_sys in ["Darwin", "Linux"]:
                fnt = ImageFont.truetype(self.font_family, self.font_size)
            if o_sys == "Windows":
                fnt = ImageFont.truetupe("Pillow/Tests/fonts/Arial.ttf", self.font_size)
        except OSError as e:
            print("Couldn't find font, loading default. Meme might not display correctly")
            fnt = ImageFont.load_default()

        return fnt

    def _resize_img(self, img):
        if img.size[0] < 740:
            return img
        else:
            return self._resize_img(
                img.resize((int(img.size[0]*0.95), int(img.size[1]*0.95)),
                           Image.ANTIALIAS)
            )

    def _get_random_image(self):

        while True:
            pics = len(os.listdir(self.sample_pics))  # how many pictures
            random_pic = os.path.join(self.sample_pics, f"trump_{randint(0, pics-2)}.jpg")
            im = Image.open(random_pic).convert("RGBA")
            
            # check that the image is not too small
            if im.size[0] > 680:
                break
            
        return self._resize_img(im)

    def _draw_text(self):
        text_pos = self._get_text_position()
        
        for i in range(len(text_pos)):
            self.draw.text(
                (text_pos[i][0], text_pos[i][1]), 
                text_pos[i][2], 
                font=self.get_font(), 
                fill=(255, 255, 255, 255)
            )

    def _draw_border(self):
        text_pos = self._get_text_position()
        font = self.get_font()
    
        for i in range(len(text_pos)):
            x, y, text = text_pos[i]

            self.draw.text((x-self.border_size, y), text, font=font, fill="black")
            self.draw.text((x+self.border_size, y), text, font=font, fill="black")
            self.draw.text((x, y-self.border_size), text, font=font, fill="black")
            self.draw.text((x, y+self.border_size), text, font=font, fill="black")

            self.draw.text(
                (x-self.border_size, y+self.border_size), text, font=font, fill="black")
            self.draw.text(
                (x-self.border_size, y-self.border_size), text, font=font, fill="black")
            self.draw.text(
                (x+self.border_size, y+self.border_size), text, font=font, fill="black")
            self.draw.text(
                (x+self.border_size, y-self.border_size), text, font=font, fill="black")

    def display(self):
        self.meme.show()

    def save(self):
        filename = f"{int(time.time())}.jpg"
        file_path = os.path.join(MEMES_FOLDER, filename)
        self.meme.convert("RGB").save(file_path)
        return filename


if __name__ == "__main__":
    meme = Meme("this is just a test-string that is somewhat longer than the other one because yeah")
    meme.display()
