import flet as ft
import pickle as pkl
import utils.endpoints.endpoint as ep
import utils.utilfunctions as ufuncs
from typing import get_origin, get_args, Union
from LoggerConfig import setup_logger

logger = setup_logger(__file__)

class ConfirmationForm(ft.AlertDialog):
    def __init__(self, page:ft.Page, func, *args, title=None, message=None, **kwargs):
        actions =[ft.FilledTonalButton(text="Confirm", on_click=func ), ft.FilledTonalButton(text="Cancel", on_click=lambda _: page.close(self))]
        title = title if title else ft.Text("Confirm choice")
        content = ft.Text(message if message else "Please confirm your choice.")
        super().__init__(title=title,  content=content, actions=actions, *args, **kwargs) # type:ignore
    pass

class EndpointSelectionForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, endpoint_ui, *args, **kwargs):
        self.page: ft.Page = page # reference to the original
        self.endpoint_ui = endpoint_ui # reference to the endpoint ui object in the page depedency injection #TODO: If i wasn't so stupid i would have made a context class to hold all of this.
        self.actions = [ft.ListView(spacing=5)]
        for name in ep.ENDPOINTS.keys():
            self.actions[0].controls.append(ft.ListTile(title=ft.Text(name.capitalize(), text_align=ft.TextAlign.CENTER), bgcolor=ft.colors.SURFACE_VARIANT, on_click=self.handle_select)) # type: ignore
        super().__init__(*args, title=ft.Text("Available Endpoints", text_align=ft.TextAlign.CENTER), actions=self.actions, shape=ft.RoundedRectangleBorder(radius=10), **kwargs)
    
    def handle_select(self, e: ft.ControlEvent):
        key = e.control.title.value.lower() # Gets the name of the endpoint to be used as the key
        endpoint_class = ep.ENDPOINTS[key] # Gets the class ref from key
        params: dict = ufuncs.get_params(endpoint_class) # Gets the params of the class to populate the form
        logger.info(f"class arguments and parameters: {params}") 
        endpoint_form = EndpointForm(page=self.page, endpoint_ui=self.endpoint_ui, Title= "Create " + e.control.title.value + " Endpoint", endpoint_name=key)
        endpoint_form.populate_form(params) # dynamically populates the endpoitn form popup with the required class parameters
        self.page.open(endpoint_form)  # displays the popup form
        self.page.close(self) # explicitly closing the current popup form just incase
        pass

class EndpointForm(ft.AlertDialog):
    """_summary_

    Args:
        ft (_type_): _description_
    """
    def __init__(self, page: ft.Page, endpoint_ui, Title: str, endpoint_name: str, *args, **kwargs):
        self.req_params: dict|None = None
        self.page: ft.Page = page # reference to the original page
        self.endpoint_ui = endpoint_ui # reference to the endpoint ui object in the page
        self.endpoint_name = endpoint_name
        self.actions = [ft.TextButton(text="+ Add", on_click=self.handle_submit), ft.TextButton(text="- Discard", on_click=lambda _: self.page.close(self))]
        self.name_field = ft.TextField(hint_text="Required (filename of endpoint)", bgcolor=ft.colors.SURFACE_VARIANT, border_radius=8, border_color=ft.colors.TRANSPARENT)
        self.content: ft.Column = ft.Column(controls=[ft.Row(controls=[ft.Text("filename", expand=True), self.name_field], width=460)], spacing=5)
        super().__init__(*args, title=ft.Text(Title, text_align=ft.TextAlign.CENTER, size=28), actions=self.actions, content=self.content, modal=True,**kwargs)


    def __validate_fields(self, text_fields) -> bool:
        res = True
        for text_field in text_fields:
            if text_field.controls[1].hint_text == "Required" and not text_field.controls[1].value: # if the text field has the hint required and the text field is not populated 
                text_field.controls[1].hint_style = ft.TextStyle(color=ft.colors.RED_300)
                self.update()
                res = False
        return res

    def populate_form(self, info: dict):
        self.req_params = info
        arg: str
        for arg, value_type in info.items():
            if arg == "args" or arg == "kwargs": continue
            hint_text = "Optional*"
            text_value = value_type[0] 
            if value_type[0]:
                if value_type[0] == "Required":
                    hint_text = value_type[0]
                    text_value = None
                else:
                    hint_text = "Required"
            is_sys_prompt = arg=="system_prompt"
            text_feild = ft.TextField(hint_text=hint_text, 
                                      value=text_value, 
                                      bgcolor=ft.colors.SURFACE_VARIANT, 
                                      border_radius=8, 
                                      border_color=ft.colors.TRANSPARENT, 
                                      multiline=is_sys_prompt, 
                                      max_lines=2 if is_sys_prompt else 1)
            self.content.controls.append(ft.Row(controls=[ft.Text(arg.replace("_"," "), expand=True), text_feild], width=460)) #type: ignore

    def handle_submit(self, event: ft.ControlEvent):
        print(form:=event.control.parent) # gets the obj reference of the alert dialog form that appears
        print(self.req_params)
        text_fields = form.content.controls[1:] # gets the list of textfeilds in the alert dialog
        if not self.__validate_fields(text_fields): return
        name: str = ufuncs.sanitize_string(self.name_field.value, add_filter_characters="_") + "_" + self.endpoint_name # type: ignore validate_fields should prevent name from being None
        try:
            # CLARIFICATION: row.controls[0].value.replace(" ","_") -> the actual name of the class parameter (e.g "API_key")
            # CLARIFICATION: self.__enforce_and_format_types(value=row.controls[1].value -> the value of the parameter cast to the correct values
            if self.req_params is None: return
            params = {(key:=row.controls[0].value.replace(" ","_")) : ufuncs.enforce_and_format_types(value=row.controls[1].value, expected_type=self.req_params[key][1]) for row in text_fields} # Creates a params dictionary from the textfeilds in the form
            # print(params)
            ufuncs.Save_New_Endpoint_data(name=name, endpoint_name=self.endpoint_name, params=params) # saves the arguments/ parameters and the endpoint type into the defined json format
            self.endpoint_ui.add_endpoint_tile(title=ufuncs.sanitize_string(self.name_field.value,add_filter_characters="_"), subtitle=self.endpoint_name) # type: ignore
            self.endpoint_ui.update()
            self.page.close(self) # 
            self.page.open(ft.AlertDialog(content=ft.Row(controls=[ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_300), ft.Text("Successfully saved endpoint!")])))
        except Exception as e:
            logger.warning("Could not save endpoint due to:")
            print(e)
            self.page.open(ft.AlertDialog(content=ft.Row(controls=[ft.Icon(ft.icons.ERROR_OUTLINE_ROUNDED, color=ft.colors.RED_300), ft.Text("Endpoint could not be saved.")])))
            

        
