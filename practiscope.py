from krita import *
from PyQt5.QtWidgets import QWidget

from practiscope.utils import (
    generate_available_filepath,
    get_get_practice_directory,
    get_icon
)


_FILEDIALOG_FILTER = "Krita (*.kra) ;; Images (*.png *.xpm *.jpg);; Photoshop (*.psd)"
_PYTHON_ICON = get_icon(name="python.png")
_IMPORT_ICON = get_icon(name="import.png")


class PractiscopeExtension(Extension):

    def __init__(self, parent) -> None:
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self) -> None :
        # NOTE: must be overriden
        self.application = Krita.instance()

    def createActions(self, window:QWidget) -> None:
        save_action = window.createAction(
            "save_daily", #id
            "Practiscope - Save Current", #name
            "tools/Practiscope" #menuLocation
        )
        save_action.triggered.connect(self.save_doc_as_practice)
        save_action.setIcon(get_icon(name="python.png"))
        
        create_A4 = window.createAction(
            "create_daily",
            "Practiscope - Create Daily",
            "tools/Practiscope"
        )
        create_A4.triggered.connect(self.create_a4_document)
        create_A4.setIcon(_PYTHON_ICON)
        
        import_practice = window.createAction(
            "import_daily",
            "Practiscope - Import Practice",
            "tools/Practiscope"
        )
        import_practice.triggered.connect(self.import_from_practice)
        import_practice.setIcon(_IMPORT_ICON)

    def create_a4_document(self) -> None:
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
        
    def save_doc_as_practice(self) -> None:
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
    
    def import_from_practice(self) -> None:
        """
        Load all files selected in the practice directory
        """
        current_practice_dir = get_get_practice_directory()
        filenames, _ext = QFileDialog.getOpenFileNames(
            parent=None,
            caption="Open Select Files To Open",
            directory=current_practice_dir,
            filter=_FILEDIALOG_FILTER
        )
        if filenames :
            for _file in filenames :
                print(_file)
                import_doc = self.application.openDocument(
                    _file
                )
                self.application.activeWindow().addView(import_doc)
             

# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(PractiscopeExtension(Krita.instance()))