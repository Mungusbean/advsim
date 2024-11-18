import flet as ft
import utils.endpoints.endpoint as ep
import utils.utilfunctions as ufuncs
from LoggerConfig import setup_logger

logger = setup_logger(__file__)

class GeneralPopUp(ft.AlertDialog):
    pass

class ConfirmationForm(ft.AlertDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(title=ft.Text("Confirm choice"), *args, **kwargs)
    pass

class PopupMenu(ft.AlertDialog):
    pass

class EndpointSelectionForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, endpoint_ui, *args, **kwargs):
        self.page: ft.Page = page # reference to the original
        self.endpoint_ui = endpoint_ui # reference to the endpoint ui object in the page depedency injection #TODO: If i wasn't so stupid i would have made a context class to hold all of this.
        self.actions = [ft.ListView(spacing=5)]
        for name in ep.ENDPOINTS.keys():
            self.actions[0].controls.append(ft.ListTile(title=ft.Text(name.capitalize(), text_align=ft.TextAlign.CENTER), bgcolor=ft.colors.SURFACE_VARIANT, on_click=self.handle_select)) # type: ignore
        super().__init__(*args, title=ft.Text("Endpoint types", text_align=ft.TextAlign.CENTER), actions=self.actions, shape=ft.RoundedRectangleBorder(radius=10), **kwargs)
    
    def handle_select(self, e: ft.ControlEvent):
        key = e.control.title.value.lower() # Gets the name of the endpoint to be used as the key
        endpoint_class = ep.ENDPOINTS[key] # Gets the class ref from key
        params: dict = ufuncs.get_params(endpoint_class) # Gets the params of the class to populate the form
        # print(info) # Change this to a logger
        endpoint_form = EndpointForm(page=self.page, endpoint_ui=self.endpoint_ui, Title= "Create " + e.control.title.value + " Endpoint", endpoint_name=key)
        endpoint_form.populate_form(params)
        self.page.open(endpoint_form) 
        self.page.close(self)
        pass

class EndpointForm(ft.AlertDialog):
    """_summary_

    Args:
        ft (_type_): _description_
    """
    def __init__(self, page: ft.Page, endpoint_ui, Title: str, endpoint_name: str, *args, **kwargs):
        self.page: ft.Page = page # reference to the original page
        self.endpoint_ui = endpoint_ui # reference to the endpoint ui object in the page
        self.endpoint_name = endpoint_name
        self.actions = [ft.TextButton(text="+ Add", on_click=self.handle_submit), ft.TextButton(text="- Discard", on_click=lambda _: self.page.close(self))]
        self.name_field = ft.TextField(hint_text="Required (filename of endpoint)", bgcolor=ft.colors.SURFACE_VARIANT, border_radius=8, border_color=ft.colors.TRANSPARENT)
        self.content = ft.Column(controls=[ft.Row(controls=[ft.Text("filename", expand=True), self.name_field], width=460)], spacing=5)
        super().__init__(*args, title=ft.Text(Title, text_align=ft.TextAlign.CENTER, size=28), actions=self.actions, content=self.content, modal=True,**kwargs)

    def validate_fields(self, text_fields) -> bool:
        for row in text_fields:
            if row.controls[1].hint_text == "Required" and not row.controls[1].value:
                return False
        return True

    def handle_submit(self, event: ft.ControlEvent):
        print(form:=event.control.parent) # gets the obj reference of the alert dialog form that appears
        text_fields = form.content.controls[1:] # gets the list of textfeilds in the alert dialog
        if not self.validate_fields(text_fields): return
        name: str = self.name_field.value + "_" + self.endpoint_name # type: ignore validate_fields should prevent name from being None
        try:
            params = {row.controls[0].value.replace(" ","_") : row.controls[1].value for row in text_fields}
            print(params)
            ufuncs.Save_New_Endpoint_data(name=name, endpoint_name=self.endpoint_name, params=params)
            self.endpoint_ui.add_endpoint_tile(title=self.name_field.value, subtitle=self.endpoint_name)
            self.endpoint_ui.update()
            self.page.close(self)
            self.page.open(ft.AlertDialog(content=ft.Row(controls=[ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_300), ft.Text("Successfully saved endpoint!")])))
        except Exception as e:
            logger.warning("Could not save endpoint due to:")
            print(e)
            pass

    def populate_form(self, info: dict):
        param: str
        for param, value in info.items():
            if param == "args" or param == "kwargs": continue
            hint_text = "Optional*"
            text_value = value 
            if value:
                if value == "Required":
                    hint_text = value
                    text_value = None
                else:
                    hint_text = "Required"
            is_sys_prompt = param=="system_prompt"
            text_feild = ft.TextField(hint_text=hint_text, 
                                      value=text_value, 
                                      bgcolor=ft.colors.SURFACE_VARIANT, 
                                      border_radius=8, 
                                      border_color=ft.colors.TRANSPARENT, 
                                      multiline=is_sys_prompt, 
                                      max_lines=2 if is_sys_prompt else 1)
            self.content.controls.append(ft.Row(controls=[ft.Text(param.replace("_"," "), expand=True), text_feild], width=460)) #type: ignore
        
