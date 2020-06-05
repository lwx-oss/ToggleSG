import sys
import xbmc

def searchInput(heading = 'Search for a show'):
    keyboard = xbmc.Keyboard('default', 'heading', True)
    keyboard.setHeading(heading)
    keyboard.setDefault('')
    keyboard.setHiddenInput(False)
    keyboard.doModal()

    inputValue = None

    if(keyboard.isConfirmed()):
        inputValue = keyboard.getText()
    
    return inputValue