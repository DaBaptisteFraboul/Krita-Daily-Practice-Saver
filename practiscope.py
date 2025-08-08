from krita import *

from practiscope.utils import generate_available_filepath


class PractiscopeExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def createActions(self, window):
        action = window.createAction("save_daily", "Practiscope - Save Current", "tools/Practiscope")
        action.triggered.connect(self.exportDocument)    
    
    def setup(self):
        # NOTE: must be overriden
        pass
        
    def exportDocument(self):
        # Get the document:
        doc =  Krita.instance().activeDocument()
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