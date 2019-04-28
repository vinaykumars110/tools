import ui
from PIL import Image

def next_button_tapped(sender):
    #sender.title = 'Hello'
    view.close()
    img = Image.open('IMG_6294.JPG')
    img.show()
    
    
# view1 - screen displays a word and two options 
#	Next
# Image
# Meaning
view = ui.View()                                      # [1]
view.name = 'Demo'                                    # [2]
view.background_color = 'black'                       # [3]
button_reveal = ui.Button(title='Reveal')  
button_next = ui.Button(title='Next')                 # [4]
button_reveal.center = (view.width * 0.5, view.height * 0.7) 
#button_reveal.font = '20'
button_next.center = (view.width * 0.5, view.height * 0.5)
# [5]
button_reveal.flex = 'LRTB'    
button_next.flex = 'LRTB'                              # [6]
button_reveal.action = button_tapped                          # [7]
view.add_subview(button_reveal)    
view.add_subview(button_next)                          # [8]
#view.present('sheet')                                 # [

view= ui.load_view('swipe')

