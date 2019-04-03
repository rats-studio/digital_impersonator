import os

from random import randint
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


FONT_SIZE = 25
LIMIT = 27
BORDER_SIZE = 1
MEMES_FOLDER = os.path.join("client", "static", "img", "memes")
SAMPLE_PICS = os.path.join("client", "static", "img", "sample_img")
FONT_FAMILY = "Arial.ttf"


class Meme:

    def __init__(self,
                 text = "default string",
                 font_size = FONT_SIZE,
                 limit = LIMIT,
                 border_size = BORDER_SIZE,
                 memes_folder = MEMES_FOLDER,
                 sample_pics = SAMPLE_PICS,
                 font_family = FONT_FAMILY
    ):
        self.text = text
        self.font_size = font_size
        self.limit = limit
        self.border_size = border_size
        self.memes_folder = memes_folder
        self.font_family = font_family
        self.sample_pics = sample_pics

        self.img = self._get_random_image()

        self.canvas = Image.new("RGBA", self.img.size, (255, 255 ,255 ,0))
        self.draw = ImageDraw.Draw(self.canvas)

        self._draw_border()
        self._draw_text()
        self.meme = Image.alpha_composite(self.img, self.canvas)

    #TODO: need to break up long sentences into multiple lines
    def _get_text_position(self, img, txt):
        width, height = img.size
        width = width - width + 20
        height = height - self.font_size*2

        if len(txt) > LIMIT:
            # break up sentence
            pass

        return (width, height)

    #TODO: different font for windows
    def get_font(self):
        try:
            fnt = ImageFont.truetype(self.font_family, self.font_size)
        except OSError as e:
            print("Couldn't find font, loading default. Meme might not display correctly")
            fnt = ImageFont.load_default() 

        return fnt

    def _resize_img(self, img):
        if img.size[1] < 420:
            return img
        else:
            return self._resize_img(
                img.resize((int(img.size[0]*0.95), int(img.size[1]*0.95)), 
                Image.ANTIALIAS)
            )
     
    def _get_random_image(self):
        pics = len(os.listdir(self.sample_pics))  # how many pictures
        random_pic = os.path.join(self.sample_pics, f"trump_{randint(0, pics-2)}.jpg")
        im = Image.open(random_pic).convert("RGBA")
        return self._resize_img(im)

    def _draw_text(self):
        self.draw.text(
            self._get_text_position(self.img, self.text), 
            self.text, 
            font=self.get_font(), 
            fill=(255,255,255,255)
        )

    #TODO: this method is begging for a loop.
    def _draw_border(self):
        x, y = self._get_text_position(self.img, self.text)
        font = self.get_font()

        self.draw.text((x-self.border_size, y), self.text, font=font, fill="black")
        self.draw.text((x+self.border_size, y), self.text, font=font, fill="black")
        self.draw.text((x, y-self.border_size), self.text, font=font, fill="black")
        self.draw.text((x, y+self.border_size), self.text, font=font, fill="black")

        self.draw.text(
            (x-self.border_size, y+self.border_size), self.text, font=font, fill="black")
        self.draw.text(
            (x-self.border_size, y-self.border_size), self.text, font=font, fill="black")
        self.draw.text(
            (x+self.border_size, y+self.border_size), self.text, font=font, fill="black")
        self.draw.text(
            (x+self.border_size, y-self.border_size), self.text, font=font, fill="black")

    def display(self):
        self.meme.show()

    def save(self):
        filename = f"{int(time.time())}.jpg"
        file_path = os.path.join(MEMES_FOLDER, filename)
        self.meme.convert("RGB").save(file_path)
        print("LOOKIE HERE FROM memify", filename)
        return filename


if __name__ == "__main__":
    meme = Meme("this is just a test-string")
    meme.display()

