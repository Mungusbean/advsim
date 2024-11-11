import flet as ft
import utils.endpoints.endpoint as ep
import utils.utilfunctions as ufuncs

class GeneralPopUp(ft.AlertDialog):
    pass

class ConfirmationForm(ft.AlertDialog):
    pass

class PopupMenu(ft.AlertDialog):
    pass

class EndpointSelectionForm(ft.AlertDialog):
    def __init__(self, *args, **kwargs):
        self.actions = [ft.ListView()]
        for name, endpoint_obj_ref in ep.ENDPOINTS.items():
            self.actions[0].controls.append(ft.ListTile(title=ft.Text(name))) # type: ignore
        super().__init__(*args, title=ft.Text("Endpoint types", text_align=ft.TextAlign.CENTER), actions=self.actions, shape=ft.RoundedRectangleBorder(radius=10), **kwargs)
    
    def handle_select(self):
        pass

class EndpointForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, Title: str, *args, **kwargs):
        self.page = page
        self.actions = [
            ft.Column(controls=[ft.TextField(),
                                ft.TextField(),
                                ft.TextField(),
                                ft.TextField(),
                                ft.Row(
                                    controls=[
                                        ft.TextButton(text="Submit"),
                                        ft.TextButton(text="Close", on_click=lambda _: self.page.close(self)) # type: ignore page reference will not be None
                                    ]
                                )
                                ]),
                        ]
        super().__init__(*args, title=ft.Text(Title, text_align=ft.TextAlign.CENTER, size=28), actions=self.actions, content_padding=15, modal=True,**kwargs)

    def handle_submit(self):
        pass

    def populate_form(self, info):
        pass
