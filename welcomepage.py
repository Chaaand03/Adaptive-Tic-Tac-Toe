import taipy as tp
from taipy.gui import Gui
import taipy.gui.builder as tgb

pdf_file = None

def on_pdf_upload(state):
    global pdf_file
    pdf_file = state.value
    if pdf_file:
        if pdf_file.name.endswith(".pdf"):
            tp.Notification(text="PDF file uploaded successfully.", gui=gui).show()
        else:
            tp.Notification(text="Please upload a PDF file.", gui=gui).show()

with tgb.Page() as page:
    tgb.text("# Upload PDF File", mode="md")
    tgb.file_selector("{content}", label="Select PDF File", on_action=on_pdf_upload, extensions=".pdf", drop_message="Drop PDF file here")

gui = Gui(page)
gui.run(title="PDF Upload", dark_mode=True, debug=True)