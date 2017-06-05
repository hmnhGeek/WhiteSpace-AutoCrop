from Tkinter import *
import cropper
from tkFileDialog import askopenfile, asksaveasfile
from PIL import Image, ImageTk

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        # defining result page here.
        class ResultPage(Page):
            def __init__(self, *args, **kwargs):
                Page.__init__(self, *args, **kwargs)

                self.config(background = "white")
                
                self.DEFAULT_FONT = ("consolas", 12)

                # Note down the last cropped image.
                self.loaded = Label(self, text = '', font = self.DEFAULT_FONT, bg = "white")
                self.loaded.pack(pady = 100)

                # Add a go back button too.
                self.gobackbutton = Button(self, text = "Go Back", command = self.goback, bg = "brown", fg = "white", bd = 0)
                self.gobackbutton.pack(pady = 10)

            def goback(self):
                hp.show()
                

        # defining home screen here.
        class Home(Page):
            def __init__(self, *args, **kwargs):
                Page.__init__(self, *args, **kwargs)

                self.config(background = "white")
                
                self.DEFAULT_FONT = ("consolas", 20)
                self.SMALL_FONT = ("consolas", 12)

                # A label to display the address of selected image.
                self.selected = Label(self, text = "No Image Chosen", font = self.SMALL_FONT, bg = "white")
                self.selected.pack(pady = 20)

                # A label to choose image, it will act like a button.
                self.choose = Label(self, text = "Step 1: Choose Image", font = self.DEFAULT_FONT, cursor = "hand2", fg = "green", bg = "white")
                self.choose.pack(pady = 10)
                self.choose.bind("<Button-1>", self.callback)

                # A label to confirm cropping.
                self.confirm = Label(self, text = "Step 2: Confirm Auto Crop", font = self.DEFAULT_FONT, cursor = "hand2", fg = "blue", bg = "white")
                self.confirm.pack(pady = 75)
                self.confirm.bind("<Button-1>", self.submitCallback)
                self.confirm.config(state = 'disabled')


            def callback(self, event):

                try:
                    # open the dialog box to ask for a file.
                    f = askopenfile()
                    filename = f.name
                    f.close()

                    # change the label of the selected image.
                    self.selected['text'] = filename

                    # Make the confirm label normal.
                    self.confirm.config(state = "normal")
                except:
                    pass


            def submitCallback(self, event):

                if self.confirm['state'] == NORMAL:
                    try:
                        # Store the image address.
                        img_adr = self.selected['text']

                        # Ask user for where the cropped file is to be saved.
                        destination = asksaveasfile()
                        final_adr = destination.name

                        # send img_adr and final_adr to cropper.py
                        cropper.autoCrop(img_adr, final_adr)

                        rp.loaded['text'] = "Image stored at: "+str(final_adr)
                        rp.show()

                    except IOError:
                        if self.selected['text'] == 'No Image Chosen':
                            rp.loaded['text'] = "No source image was chosen. Image build failed."
                        else:
                            pass
                        rp.show()
                else:
                    pass

        hp = Home(self)
        rp = ResultPage(self)
        
        self.container = Frame(self)
        self.container.pack(side = 'top', fill = 'both', expand = True)

        hp.place(in_ = self.container, x = 0, y = 0, relwidth = 1, relheight = 1)
        rp.place(in_ = self.container, x = 0, y = 0, relwidth = 1, relheight = 1)

        hp.show()

if __name__ == '__main__':
    root = Tk()

    main = MainView(root)
    main.pack(side = 'top', fill = 'both', expand = True)

    root.wm_geometry('700x300')
    root.resizable(height = 0, width = 0)

    root.title('AutoCrop')
    root.mainloop()
        
        
