import os

from krita import *
from PyQt5.QtGui import QIcon

from practiscope.utils import generate_available_filepath

_ICON = os.path.join(os.path.dirname(__file__), "python.png")
print(_ICON)

class PractiscopeExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def createActions(self, window):
        save_action = window.createAction("save_daily", "Practiscope - Save Current", "tools/Practiscope")
        save_action.triggered.connect(self.exportDocument)
        save_action.setIcon(QIcon(_ICON))
        create_A4 = window.createAction("create_daily", "Practiscope - Create Daily", "tools/Practiscope")
        create_A4.triggered.connect(self.createDocument)
        create_A4.setIcon(QIcon(_ICON))
        
    def setup(self):
        # NOTE: must be overriden
        self.application = Krita.instance()
    
    def createDocument(self):
        # Create A4, 300 dpi
        
        new_document = self.application.createDocument(
            4960,
            3508,
            "foo",
            "RGBA",
            "U8",
            "",
            300.0
        )
        self.application.activeWindow().addView(new_document)
        
    def exportDocument(self):
        # Get the document:
        doc =  self.application.activeDocument()
        # Saving a non-existent document causes crashes, so lets check for that first.
        if doc:
            print(doc.fileName())
            if not doc.fileName():
                doc_filepath = generate_available_filepath(number_padding=3)
                r=doc.saveAs(doc_filepath)
                print(f"Doc saved as  : {doc_filepath}")
            else : doc.save()
            
# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(PractiscopeExtension(Krita.instance()))