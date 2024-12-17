import flet as ft
import os
import json
import utils.utilfunctions as ufuncs
import ui_components.popup_components as  uipopup
import utils.endpoints.endpoint as ep
from typing import Any, Callable, List, Optional, Sequence
from LoggerConfig import setup_logger

logger = setup_logger(__name__)

class ChatBubble(ft.Card):
    def __init__(self, is_user:bool, id: str | None = None, text: str | None = None, margin: int | float | ft.Margin | None = None, elevation: int | float | None = 0, color: str | None = None, shadow_color: str | None = None, surface_tint_color: str | None = None, shape: ft.OutlinedBorder | None = ft.RoundedRectangleBorder(radius=10), clip_behavior: ft.ClipBehavior | None = None, is_semantic_container: bool | None = None, show_border_on_foreground: bool | None = None, variant: ft.CardVariant | None = None, ref: ft.Ref | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end = None, tooltip: str | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, key: str | None = None, adaptive: bool | None = None):
        if is_user: color = f"{ft.colors.SURFACE_VARIANT},0.8"
        else: color = ft.colors.TRANSPARENT

        if text is None: 
            content = ft.ProgressRing(
                height=24,
                width=24,
                color=ft.colors.GREY_300
            )
        elif "⚠ Something went wrong." in text: # This is really bad as this triggers the color, instead a flag should also be returned in order to prevent this
            content = ft.Container(content = ft.Text("⚠ Something went wrong.", color="red"), padding=24)
        else:
            content: ft.Control = ft.Container(content = ft.Markdown(
                text,
                selectable=True,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, 
                code_theme=ft.MarkdownCodeTheme.ATOM_ONE_DARK_REASONABLE, 
                code_style_sheet=ft.MarkdownStyleSheet(code_text_style=ft.TextStyle(font_family="Courier new"), codeblock_decoration=ft.BoxDecoration(border_radius=10)),
                # code_style=ft.TextStyle(font_family="Courier New"),
                md_style_sheet= ft.MarkdownStyleSheet(a_text_style=ft.TextStyle(font_family="Inter"),)
                # code_style_sheet=ft.MarkdownStyleSheet(code_text_style=ft.TextStyle(font_family="Courier New"))
            ),
            padding=16
            )
        super().__init__(content, margin, elevation, color, shadow_color, surface_tint_color, shape, clip_behavior, is_semantic_container, show_border_on_foreground, variant, ref, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data, key, adaptive)
        self.is_user: bool =  is_user
        self.id: str | None = id

    def __str__(self) -> str: 
        return f"{'User' if self.is_user else 'AI'}"

class ChatTab(ft.ListView):
    """_summary_
    Subclass of a flet ListView object. 
    Holds the conversation between the user and the specified model.
    """
    __Chat_tab_instance = None 

    # To implement a singleton for the chat interface, as only its parameters needs changes
    def __new__(cls, *args, **kwargs):
        if cls.__Chat_tab_instance is None:
            cls.__Chat_tab_instance = super().__new__(cls) 
        return cls.__Chat_tab_instance
        

    def __init__(self, LLM, Chat_title: str, controls: List[ft.Control] | None = None, horizontal: bool | None = None, spacing: int | float | None = 10, item_extent: int | float | None = None, first_item_prototype: bool | None = None, divider_thickness: int | float | None = None, padding: int | float | ft.Padding | None = None, clip_behavior: ft.ClipBehavior | None = None, semantic_child_count: int | None = None, cache_extent: int | float | None = None, auto_scroll: bool | None = None, reverse: bool | None = None, on_scroll_interval: int | float | None = None, on_scroll: Callable[[ft.OnScrollEvent], None] | None = None, ref: ft.Ref | None = None, key: str | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end: Callable[[ft.ControlEvent], None] | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, adaptive: bool | None = None):
        self.Chat_title: str = Chat_title
        self.LLM = LLM
        padding = 10
        auto_scroll = True
        super().__init__(controls, horizontal, spacing, item_extent, first_item_prototype, divider_thickness, padding, clip_behavior, semantic_child_count, cache_extent, auto_scroll, reverse, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, adaptive)

    def __reduce__(self):
        return (self.__class__, (self.LLM, self.Chat_title))

    def add_bubble(self, role: bool, text: str| None) -> None:
        """_summary_

        Args:
            role (bool): True when the message came from the user, False if its by the AI.
            text (str): The message contents. Provided as a string.
        """
        try:
            bubble_alignment = ft.MainAxisAlignment.END if role else ft.MainAxisAlignment.START
            role_name = 'U' if role else 'AI'
            controls = [ChatBubble(
                           is_user = role, 
                           text = text, 
                           id = f"{role_name}_{self.Chat_title}_{len(self.controls)}",
                           width= (1000 if len(text.split()) > 25 else None) if text else None
                           )]
            controls.insert(int(role), 
                                ft.Container(
                                    content=ft.CircleAvatar(content=ft.Text(role_name, color=ft.colors.SURFACE), bgcolor=ft.colors.PURPLE_200 if role else ft.colors.AMBER_200),
                                    alignment=ft.alignment.top_center  # Aligns avatar at the top
                                    ) # type: ignore
                            ) 
            self.controls.append(
                ft.Row(controls= controls, # type: ignore
                        alignment = bubble_alignment,
                        spacing = 10,
                        vertical_alignment= ft.CrossAxisAlignment.START
                    )
                )
        except Exception as e:
            print("Unable to create bubble:", e)

    def pop(self):
        self.controls.pop()

    def clear_bubbles(self):
        self.controls.clear()

    def populate_bubbles_from_chat(self):
        pass

class ChatInputBar(ft.Row):
    """_summary_

    Args:
        ft (_type_): Input bar for manual testing of the model. Allows users to type prompts and test attack modules by sending them to the model.
    """
    def __init__(self, page: ft.Page, alignment: ft.MainAxisAlignment | None = None, vertical_alignment: ft.CrossAxisAlignment | None = None, spacing: int | float | None = None, tight: bool | None = None, wrap: bool | None = None, run_spacing: int | float | None = None, scroll: ft.ScrollMode | None = None, auto_scroll: bool | None = None, on_scroll_interval: int | float | None = None, on_scroll: Callable[[ft.OnScrollEvent], None] | None = None, ref: ft.Ref | None = None, key: str | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end: Callable[[ft.ControlEvent], None] | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, rtl: bool | None = None, adaptive: bool | None = None):
        self.submit_button: ft.IconButton = ft.IconButton(icon= ft.icons.ARROW_UPWARD_ROUNDED,
                                                          icon_color=ft.colors.GREY_400,
                                                          icon_size=36,
                                                          tooltip="Send prompt",
                                                          disabled= True,
                                                          disabled_color=ft.colors.GREY_50,
                                                          on_click= self.send_to_LLM # type:ignore
                                                          )
        self.__hint_text = "Message AI"
        self.new_message: ft.TextField = ft.TextField(hint_text= self.__hint_text,
                                                      border=ft.InputBorder.NONE,
                                                      border_color=ft.colors.TRANSPARENT,
                                                      bgcolor=ft.colors.TRANSPARENT,
                                                      hover_color=ft.colors.TRANSPARENT,
                                                      focused_border_color=ft.colors.TRANSPARENT,
                                                      filled=True,  # Optional: Adds a background color to make it stand out
                                                      autofocus= True,
                                                      autocorrect= False,
                                                      shift_enter= True,
                                                      min_lines= 1,
                                                      max_lines=3,
                                                      expand= True,
                                                      on_change= self.__toggle_submit_button, # type: ignore
                                                      on_submit= self.send_to_LLM # type: ignore
                                                      )
        self.chat_settings_button: ft.IconButton = ft.IconButton(icon=ft.icons.SETTINGS, on_click=lambda _: print("settings buttons clicked!"),icon_color=ft.colors.ON_SURFACE_VARIANT) #TODO: implement the settings tab
        self.page: ft.Page = page 
        self.chat_tab: ChatTab = self.page.session.get("chat_tab") # type: ignore
        controls: list[ft.Control] = [self.chat_settings_button, self.new_message, self.submit_button]
        # self.page: ft.Page = page
        super().__init__(controls, alignment, vertical_alignment, spacing, tight, wrap, run_spacing, scroll, auto_scroll, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, adaptive)

    def __toggle_submit_button(self, e):
        """
        toggles the submit button on if the textfeild input is not blank
        """
        disabled_state = not self.new_message.value or not self.new_message.value.strip()
        self.submit_button.disabled = disabled_state
        self.submit_button.icon_color = ft.colors.SURFACE_TINT if not disabled_state else ft.colors.GREY_200
        self.update()
    
    def __settings_button_on_click(self, e):
        pass

    def send_to_LLM(self, e) -> None: 
        """
        Sends the value of the text feild to the LLM 

        Args:
            e (_type_): event 

        Returns:
            _type_: None
        """
        try:
            if self.chat_tab.LLM is None:
                self.page.open(ft.AlertDialog(icon=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED), title=ft.Text("No Endpoint Detected"), content=ft.Text("please select an endpoint.")))
                self.new_message.value = ""
                self.update()
                return
            # Check if the TextField value is None or empty
            if not self.new_message.value or not self.new_message.value.strip():
                return  # Do nothing if the input is None or empty
            
            prompt = self.new_message.value
            self.new_message.value = ""; self.new_message.update() # clear input from the text feild

            self.submit_button.disabled = True # ensure button and textfeilds are dsiabled while waiting for the message to be sent.
            self.new_message.disabled = True
            self.__toggle_submit_button(None)
            self.update()

            self.chat_tab.add_bubble(role=True,text=prompt) # type: ignore # Adds in and renders the user's prompt bubble
            self.chat_tab.add_bubble(role=False, text=None); self.chat_tab.update() # Add loading bubble while waiting for the API to return the response.

            # response = self.chat_tab.LLM_info.predict(input=prompt)
            # TODO: PLEASE CONFIGURE THIS PROPERLY -> a side pipe should be added before passing the modified user's prompt to the text bubble before adding it. (line 187)
            # TODO: If the above is not implemented, the user will not be able to see how their prompt is mutated and templated from the suffix.
            # TODO: Session ID can remain the chat title.
            response = self.chat_tab.LLM.invoke(
                {"input": prompt},
                config = {"configurable": {"session_id":  self.chat_tab.Chat_title}}

            ) # <- An error would most likely occur here if there are any errors in the payload. 

            self.chat_tab.pop() # Remove the loading bubble.
            self.chat_tab.add_bubble(role=False,text=response); self.chat_tab.update() # Update the chat_tab object with the received response. 

            self.new_message.disabled = False # Re-enable just the textfeild when the page is updated.
            self.new_message.update()
            self.new_message.focus()
        except Exception as e:
            logger.error(f"⚠ Something went wrong.:\n An error occured when trying to send to llm->{e}")

            self.chat_tab.pop() # Remove the loading bubble.
            self.chat_tab.add_bubble(role=False,text=f"{e}"); self.chat_tab.update() # Update the chat_tab object with the received response. 
            self.new_message.disabled = False # unlock the chat input bar just incase
            self.new_message.update()
            self.new_message.focus()

    
class NavigationButton(ft.MenuItemButton):
        def __init__(self, page: ft.Page, Route: str, Icon: ft.Icon=ft.Icon(ft.icons.ABC), Text: str="Button", Text_size: int=16, *args, **kwargs):
            super().__init__(leading = Icon, content=ft.Text(Text, size=Text_size), on_click=lambda _: page.go(Route),*args, **kwargs)
            
class sideNavBar(ft.NavigationDrawer):
    def __init__(
        self,
        page: ft.Page,
        controls: List[ft.Control] | None = None,
        **kwargs
    ):
        self.page: ft.Page = page
        self.Navigations = ft.ListView(
            controls=[
                ft.Row(controls=[ft.Icon( ft.icons.DARK_MODE if self.page.theme_mode is ft.ThemeMode.DARK else ft.icons.LIGHT_MODE, 
                                         size=24,
                                         color=ft.colors.GREEN_400 if self.page.theme_mode is ft.ThemeMode.DARK else None),
                                 ft.CupertinoSwitch(label="Dark mode" if self.page.theme_mode is ft.ThemeMode.DARK else "Light mode", 
                                                    value=self.page.theme_mode is not ft.ThemeMode.DARK, 
                                                    on_change=self.toggle_light_dark, 
                                                    track_color=ft.colors.GREEN_400)], 
                       spacing=5)
            ],
            padding=20,
            spacing = 5
        )

        self.tile_padding = 0.2
        controls = [self.Navigations]
        super().__init__(
            controls=controls,
            **kwargs
        )
    
    def toggle_light_dark(self, e):
            self.page.theme_mode = ft.ThemeMode.DARK if not self.Navigations.controls[0].controls[1].value else ft.ThemeMode.LIGHT # toggles between light and dark
            self.Navigations.controls[0].controls[0] = ft.Icon(ft.icons.DARK_MODE, size=24, color=ft.colors.GREEN_400) if not self.Navigations.controls[0].controls[1].value else ft.Icon(ft.icons.LIGHT_MODE, size=24) # type: ignore // toggles between light and dark icon symbols
            self.Navigations.controls[0].controls[1].label = "Dark mode" if not self.Navigations.controls[0].controls[1].value else "Light Mode" # toggles the text between 
            self.page.update()
    
    def add_NavButton(self, NavButton: NavigationButton) -> bool:
        try:
            self.Navigations.controls.append(NavButton)
            return True
        except Exception as e:

            return False 

class IconListTile(ft.Container):
    def __init__(self, 
                 *args, 
                 Title: str = "Title", 
                 Subtitle: str = "Subtitle", 
                 icons: str = ft.icons.CODE, 
                 Title_size: int = 16, 
                 Subtitle_size: int = 12,
                 Title_color: str| None = None,
                 Subtitle_color: str| None = None,
                 bgcolor: str|None = None,
                 border_radius: int = 8,
                 tooltip: str = "Click to edit",
                 Add_delete_button: bool = True,
                 elevated_hover: bool = True,
                 on_click = None,
                 **kwargs):
        self.Title = Title
        self.Subtitle = Subtitle
        self.Title_size = Title_size
        self.Subtitle_size = Subtitle_size
        self.icon: ft.Icon = ft.Icon(icons)
        self.Title_color = Title_color
        self.Subtitle_color: str = Subtitle_color if Subtitle_color else ft.colors.GREY_400
        self.default_bgcolor = f"{ft.colors.SURFACE_VARIANT},0.3"
        self.elevated_hover = elevated_hover
        if not bgcolor: bgcolor = self.default_bgcolor 
        self.content: ft.Row = ft.Row(controls=[
            ft.Icon(icons),
            ft.Column(controls=[ft.Text(self.Title, color=self.Title_color, size=self.Title_size), ft.Text(self.Subtitle, color=self.Subtitle_color, size=self.Subtitle_size)], spacing=0, expand=True)
        ])
        if Add_delete_button:
            self.delete_button: ft.IconButton = ft.IconButton(icon=ft.icons.DELETE) # delete button's functionality needs to be implmented by case
            self.content.controls.append(self.delete_button)
        super().__init__(*args, animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT), content=self.content, bgcolor=bgcolor, padding=5, on_click=on_click, on_hover=self.__on_hover, border_radius=border_radius, tooltip=tooltip,**kwargs)

    def __on_hover(self, e: ft.ControlEvent):
        e.control.bgcolor = self.default_bgcolor if e.data == "false" else ft.colors.ON_PRIMARY
        if self.elevated_hover:
            if e.data == "true":  # Mouse entered
                self.scale = ft.transform.Scale(1.015)  # Scale up by 1.5%
            else:  # Mouse left
                self.scale = ft.transform.Scale(1.0)  # Reset to original size
            e.control.update()

class EndpointDisplay(ft.Card):
    def __init__(self, page, parent, *args, **kwargs):
        self.__current_endpoint = ft.Text(value="No endpoint selected")
        self.page: ft.Page = page
        self.parentUI: EndpointsUI = parent
        self.none_selected = ft.Text("No endpoint selected", text_align=ft.TextAlign.CENTER, height=300)
        self.content = ft.Container(
                                    content = ft.Column(
                                                controls = [
                                                    ft.Row( controls=[ft.FilledTonalButton(icon=ft.icons.CHECK_CIRCLE, text="Use this Endpoint", on_click=self.__handle_use_endpoint_click), 
                                                                      ft.FilledTonalButton(icon=ft.icons.SAVE_AS_ROUNDED, text="Save Edits", on_click=self.__handle_save_edits_click),
                                                                      ft.FilledTonalButton(icon=ft.icons.ADD_CIRCLE, text="Save New", on_click=self.__handle_save_new_click)
                                                                      ], 
                                                            alignment=ft.MainAxisAlignment.CENTER),
                                                    self.none_selected], 
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.CENTER,),
                                    padding = 10,
                                    expand= True)
        
        super().__init__(*args, content=self.content, expand=True, **kwargs)

    @property
    def display(self):
        return self.content.content.controls[-1] # type: ignore

    def display_endpoint(self, selected_endpoint: str):
        # get selected endpoint's data
        if not (data := ufuncs.load_endpoint_data(name=selected_endpoint)): 
            logger.warning("Could not load endpoint.")
            return
        # self.display = ft.Column()
        self.data = data
        filename = selected_endpoint.split("_")[0]
        data["filename"]: str = filename # type: ignore
        self.params: dict = data["params"] # type: ignore
        endpoint_name: str = data["endpoint_name"] # type: ignore
        width = 480
        new_display = ft.Container(content = ft.Column(spacing=5, height=600))
        self.content.content.controls[-1] = new_display # type: ignore
        endpoint_name_textfield = ft.TextField(hint_text="Required", 
                                                value=endpoint_name, 
                                                bgcolor=ft.colors.SURFACE_VARIANT, 
                                                border_radius=8, 
                                                border_color=ft.colors.TRANSPARENT, 
                                                max_lines=1,
                                                disabled=True)
        filename_textfield = ft.TextField(hint_text="Required", 
                                value=filename, 
                                bgcolor=ft.colors.SURFACE_VARIANT, 
                                border_radius=8, 
                                border_color=ft.colors.TRANSPARENT, 
                                max_lines=1)
        new_display.content.controls.append(ft.Row(controls=[ft.Text("filename", expand=True), filename_textfield], width=width)) # type: ignore
        new_display.content.controls.append(ft.Row(controls=[ft.Text("endpoint name", expand=True), endpoint_name_textfield], width=width)) # type: ignore
        for param, value in self.params.items():
            is_sys_prompt = param=="system_prompt"
            is_APIkey = param=="API_key"
            hint_text = "Optional*"
            text_value = value 
            if value:
                if value == "Required":
                    hint_text = value
                    text_value = None
                else:
                    hint_text = "Required"
            text_feild = ft.TextField(hint_text=hint_text, 
                                      value=text_value, 
                                      bgcolor=ft.colors.SURFACE_VARIANT, 
                                      border_radius=8, 
                                      border_color=ft.colors.TRANSPARENT, 
                                      multiline=is_sys_prompt, 
                                      max_lines=2 if is_sys_prompt else 1,
                                      password=is_APIkey,
                                      can_reveal_password=is_APIkey
                                      )
            new_display.content.controls.append(ft.Row(controls=[ft.Text(param.replace("_"," "), expand=True), text_feild], width=width)) # type: ignore
        self.update()
    
    def __handle_use_endpoint_click(self, e: ft.ControlEvent):
        try:
            if isinstance(self.content.content.controls[-1], ft.Text): #type: ignore // ft.text will be the default flet control showing if there is no endpoint being displayed
                return
            self.page.session.set("selected_endpoint", self.data) # Put the selected endpoint into the session storage
            self.reset_display(text="Endpoint has been set!", text_colour=ft.colors.SURFACE_TINT) # Display a message to indicate successful loading of endpoint into session
        except Exception as error:
            logger.warning(f"An error occured when trying to set endpoint: {error}")
            self.reset_display(text="Could not set endpoint.", text_colour=ft.colors.RED_300) # Display a message to indicate that endpoint has not been set due to an error
        self.page.update()
    
    def __handle_save_edits_click(self, e: ft.ControlEvent):
        if self.data is None: return
        # check if there is an endpoint being currently displayed
        if isinstance(self.display, ft.Text): # Perform a check to see if the display is just Text (indicates that there are no ednpoints selected)
            self.page.open(ft.AlertDialog(content=ft.Row(controls=[ft.Icon(ft.icons.WARNING_AMBER, color=ft.colors.ORANGE_300), ft.Text("No Endpoint Selected!")])))
            return 
        saved_endpoints_path = "../../appdata/saved_endpoints/"
        base_dir = os.path.dirname(__file__)
        old_name = self.data["filename"] 
        old_filename = old_name + "_" + self.data["endpoint_name"]
        old_filepath = os.path.join(base_dir, saved_endpoints_path + old_filename + "/" + old_filename + ".json")

        # self.content.content.controls[-1].content.controls -> refers to the list of row controls which hold the textfeilds. (very messy as I did not create a reference to the display)
        textfields = self.content.content.controls[-1].content.controls # type: ignore // This is the controls of the column object: A list that holds the rows of textfeilds of the display
        logger.info(f"{textfields}")
        logger.info(f"{self.params}")
        new_params = {}

        # endpoint_name = textfields[1].controls[-1].value
        new_name = textfields[0].controls[-1].value
        new_filename = new_name + "_" + self.data["endpoint_name"]
        new_filepath = os.path.join(base_dir, saved_endpoints_path + new_filename + "/" + new_filename + ".json") 

        req_params = ufuncs.get_params(ep.ENDPOINTS[self.data["endpoint_name"]]) # type: ignore // get the required endpoint params for the endepoint type
        for row in textfields[2:]: # start from index 2 as we do not want to iterate through filename and endpoint name.
            param_name: str =  row.controls[0].value 
            textfeild: ft.TextField = row.controls[-1]
            key = param_name.replace(" ","_")
            new_params[key] = ufuncs.enforce_and_format_types(value=textfeild.value, expected_type=req_params[key][1]) # type:ignore
        
        # define the new json to be stored
        new_data = {"endpoint_name": self.data["endpoint_name"], "params": new_params} # type: ignore

        # overwrite the old save and save self.data as the new replaced endpoint definition
        #Overwrite with new data 
        with open(old_filepath, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        logger.debug(f"Successfully edited {self.data['endpoint_name']}") #type: ignore

        old_dirpath = os.path.join(base_dir, saved_endpoints_path + old_filename)
        new_dirpath = os.path.join(base_dir, saved_endpoints_path + new_filename)

        os.rename(old_dirpath, new_dirpath)  # Rename the directory first
        logger.debug(f"Successfully renamed directory '{old_filename}' to '{new_filename}'")

        # Update file paths to reflect the new directory structure
        old_filepath = os.path.join(new_dirpath, old_filename + ".json")
        new_filepath = os.path.join(new_dirpath, new_filename + ".json")

        # Rename the JSON file
        os.rename(old_filepath, new_filepath)
        logger.debug(f"Successfully renamed file '{old_filename}.json' to '{new_filename}.json'")

        # # Rename the json file 
        # os.rename(old_filepath, new_filepath)

        # #rename the directory file
        # os.rename(os.path.join(base_dir, saved_endpoints_path + old_filename), os.path.join(base_dir, saved_endpoints_path + new_filename))
        # logger.debug(f"Scucessfully renamed '{old_filename}' to '{new_filename}'")

        # reload the endpoint data (self.data) to reflect the edits
        if not (data := ufuncs.load_endpoint_data(name=new_filename)): # type: ignore
            logger.warning("Could not load endpoint.")
            return
        
        # update the current selected data 
        self.data = data
        self.data["filename"]: str = new_filename # type: ignore
        
        self.page.open(ft.AlertDialog(content=ft.Row(controls=[ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_300), ft.Text("Endpoint sucessfully edited!")])))
        self.parentUI.populate_endpoint_list()
        self.parentUI.update()

    def __handle_save_new_click(self, e):
        # check if there is an endpoint being currently displayed
        if isinstance(self.display, ft.Text): 
            self.page.open(ft.AlertDialog(content=ft.Row(controls=[ft.Icon(ft.icons.WARNING_AMBER, color=ft.colors.ORANGE_300), ft.Text("No Endpoint Selected!")])))
            return 

        base_dir = os.path.dirname(__file__)
        old_filename = self.data["filename"] # type: ignore

        # self.content.content.controls[-1].content.controls -> refers to the list of row controls which hold the textfeilds. (very messy as I did not create a reference to the display)
        textfields = self.content.content.controls[-1].content.controls # type: ignore // This is the controls of the column object: A list that holds the rows of textfeilds of the display
        logger.info(f"{textfields}")
        logger.info(f"{self.params}")
        new_params = {}

        # endpoint_name = textfields[1].controls[-1].value
        new_filename = textfields[0].controls[-1].value

        # As this should create a new file, we need to make sure the new_filename is not the same as the old filename 
        if new_filename == old_filename:
            self.page.open(ft.AlertDialog(content=ft.Row(controls=[ft.Icon(ft.icons.ERROR_ROUNDED, color=ft.colors.RED_300), ft.Text("New filename cannot be the same as old filename.")])))
            return

        new_filepath = os.path.join(base_dir, "../../appdata/saved_endpoints/" + new_filename + "_" + self.data["endpoint_name"] + ".json") #type: ignore 

        req_params = ufuncs.get_params(ep.ENDPOINTS[self.data["endpoint_name"]]) # type: ignore // get the required endpoint params for the endepoint type
        for row in textfields[2:]: # start from index 2 as we do not want to iterate through filename and endpoint name.
            param_name: str =  row.controls[0].value 
            textfeild: ft.TextField = row.controls[-1]
            key = param_name.replace(" ","_")
            new_params[key] = ufuncs.enforce_and_format_types(value=textfeild.value, expected_type=req_params[key][1]) # type:ignore

        # Create the new endpoint directory
        ufuncs.Save_New_Endpoint_data(name=f"{new_filename}_{self.data['endpoint_name']}", endpoint_name=self.data["endpoint_name"], params=new_params) # type: ignore
        
        # # define the new json to be stored
        # new_data = {"endpoint_name": self.data["endpoint_name"], "params": new_params} # type: ignore

        # # write the new data to a new file.
        # with open(new_filepath, "w", encoding="utf-8") as f:
        #     json.dump(new_data, f, ensure_ascii=False, indent=4)
        # logger.debug(f"Successfully saved new {self.data['endpoint_name']} endppoint to file {new_filename}") #type: ignore

        # reload the endpoint data (self.data) to reflect the edits
        if not (data := ufuncs.load_endpoint_data(name=new_filename + "_" + self.data["endpoint_name"])): # type: ignore
            logger.warning("Could not load endpoint.")
        self.data = data
        self.data["filename"]: str = new_filename # type: ignore
        

        self.page.open(ft.AlertDialog(content=ft.Row(controls=[ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_300), ft.Text("New endpoint sucessfully created!")])))
        self.__handle_use_endpoint_click(None) # type: ignore // Paramter "e" for control event not used in the method. It can be set to None in this case.
        self.parentUI.populate_endpoint_list()
        self.parentUI.update()
    
    def reset_display(self, text: str|None  = None, text_colour: str|None = None):
        self.content.content.controls[-1] = self.__none_selected if not text else ft.Text(text, color=text_colour, text_align=ft.TextAlign.CENTER, height=300) # type: ignore

class EndpointsUI(ft.Column):
    def __init__(self, page: ft.Page, *args, **kwargs):
        self.button_size = 88
        self.button_color = ft.colors.SURFACE_VARIANT
        self.page: ft.Page = page
        self.search_bar = ft.TextField(hint_text="Search available endpoints",
                                       border_color=ft.colors.TRANSPARENT,
                                       fill_color=ft.colors.with_opacity(0.5,ft.colors.SURFACE_VARIANT),
                                       filled=True,
                                       border_radius=12,
                                       expand=True,
                                       on_change=self.__search,
                                       on_submit=self.__search)
        self.endpoint_display_card = EndpointDisplay(page=self.page, parent=self)
        self.endpoints_list = ft.ListView(controls=[],
                                          spacing=5, 
                                          padding=10)
        self.populate_endpoint_list() # Populate all the available endpoints on object instantiation

        self.controls = [
            ft.Row(controls=[
                ft.FloatingActionButton(icon=ft.icons.ADD, 
                                        elevation=0, 
                                        shape=ft.RoundedRectangleBorder(radius=12), 
                                        height=self.button_size, 
                                        width=self.button_size, 
                                        bgcolor=self.button_color,
                                        tooltip="Add an endpoint",
                                        on_click=lambda _: self.page.open(uipopup.EndpointSelectionForm(page=self.page, endpoint_ui=self))), 
                ft.FloatingActionButton(icon=ft.icons.HELP_OUTLINE_ROUNDED, 
                                        elevation=0, 
                                        shape=ft.RoundedRectangleBorder(radius=12), 
                                        height=self.button_size, 
                                        width=self.button_size, 
                                        bgcolor=self.button_color,
                                        tooltip="Help",
                                        on_click=lambda _: print("Wow, the help button has been clicked!")) #TODO: implement the help button to explain what to do 
            ],
            alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                controls = [ft.Column(controls=[self.search_bar, ft.Container(content = self.endpoints_list, expand=True, height=520)], expand=True), self.endpoint_display_card], 
                vertical_alignment=ft.CrossAxisAlignment.START)
        ]

        super().__init__(*args, controls=self.controls, **kwargs)

    def add_endpoint_tile(self, title, subtitle) -> bool:
        try:
            tile = IconListTile(Title=title, Subtitle=subtitle, icons=ft.icons.DATA_OBJECT)
            tile.delete_button.on_click = self.remove_endpoint_tile
            tile.on_click = self.__handle_endpoint_tile_click
            self.endpoints_list.controls.append(tile)
            return True
        except Exception as e:
            logger.warning("Unable to create tile:", e)
            logger.info("Debug Notes:")
            logger.debug(e)
            return False

    def remove_endpoint_tile(self, event: ft.ControlEvent) -> bool:
        try:
            tile: IconListTile = event.control.parent.parent
            # filename = tile.Title + "_" + tile.Subtitle + ".json" # Old implementation of the endpoint management
            dirname = tile.Title + "_" + tile.Subtitle
            base_dir = os.path.dirname(__file__)

            file_path = os.path.join(base_dir, "../../appdata/saved_endpoints/" + dirname)
            if ufuncs.delete_path(file_path): # if the file can be deleted (then go on to remove the tile) else (just leave it, as it should be removed on the next page load)
                self.endpoints_list.controls.remove(tile)
                logger.info("Removed endpoint tile")
                self.page.update() # type: ignore
                return True
            else:
                logger.info("file could not be found")
                return False
        except Exception as e:
            logger.warning("could not remove endpoint tile:", e)
            return False
        
    def populate_endpoint_list(self, filter_word: str = ""):
        saved_endpoints_list = [filename for filename in self.__get_available_endpoints() if filter_word.lower() in filename.split("_")[0].lower()] # Too lazy to actually implement a proper fuzzy search algorithm, for now this will do.
        saved_endpoints_list.sort()
        self.endpoints_list.controls.clear() # Not efficient, but it is reasonable to assume there will not be a huge number of endpoints defined by the user.
        for filename in saved_endpoints_list:
            try:
                saved_name = filename.split(".")[0] # get rid of the file extension
                title, endpoint_name = saved_name.split("_")
                self.add_endpoint_tile(title=title, subtitle=endpoint_name)
            except Exception as e:
                logger.warning("Could not load tile due to incorrect filename:",e)

    def __get_available_endpoints(self) -> list[str]:
        base_dir = os.path.dirname(__file__)
        saved_endpoints_path = os.path.join(base_dir, "../../appdata/saved_endpoints")
        saved_endpoints_list = ufuncs.get_file_names(saved_endpoints_path)
        #print(saved_endpoints_list)
        return saved_endpoints_list
    
    def __handle_endpoint_tile_click(self, event: ft.ControlEvent):
        double_clicked = ufuncs.detect_double_click(page=self.page)
        tile: IconListTile = event.control
        filename = tile.Title + "_" + tile.Subtitle
        self.endpoint_display_card.display_endpoint(filename)
        if double_clicked:
            self.endpoint_display_card._EndpointDisplay__handle_use_endpoint_click(e=None) # type: ignore // just reusing the endpoint display class method to set the endpoint

    def __search(self, event: ft.ControlEvent):
        filter_name = self.search_bar.value
        if not filter_name: filter_name = ""
        self.populate_endpoint_list(filter_name)
        self.update()
    
class ConfigUI(ft.Row):
    def __init__(self, *args, **kwargs):
        self.List = ft.ListView(controls=[
            ft.Text("Mutator", height=300, bgcolor=ft.colors.GREY),
            ft.Text("Template", height=300, bgcolor=ft.colors.GREY),
            ft.Text("Suffix", height=300, bgcolor=ft.colors.GREY),
            ft.Text("Additional", height=300, bgcolor=ft.colors.GREY),
        ])
        self.SidePreview = ft.Container(content=ft.Column(controls=[ft.Text("Side Preview"), ft.Container(bgcolor=ft.colors.GREY, height=300), ft.Icon(ft.icons.ARROW_DOWNWARD), ft.Container(bgcolor=ft.colors.GREY, height=300)]),
                                        bgcolor=ft.colors.AMBER, expand=True, 
                                        alignment=ft.alignment.top_center) #TODO: Temporary placeholder to figure out the layout
        self.controls = [ft.Container(content=self.List, height=600, expand=True), self.SidePreview] #TODO: Tempory placeholder to figure out layout
        super().__init__(*args, controls=self.controls, adaptive=True, vertical_alignment=ft.CrossAxisAlignment.START, **kwargs)

    def insert_attack_module(self, attack_module_name: str) -> bool:
        return True
    
    def remove_attack_module(self, attack_module_name: str) -> bool:
        return True
    
    def populate_config_list(self):
        pass

    def insert_LLM_feature(self, feature_name: str) -> bool:
        return True
    
    def remove_LLM_feature(self, feature_name: str ) -> bool:
        return True
    
    def insert_defence_module(self, defence_module_name: str) -> bool:
        return True
    
    def remove_defence_module(self, defence_module_name: str) -> bool:
        return True
    
    def loadRunnable(self, runnable):
        pass

    def unloadRunnable(self, runnable):
        pass

    def __on_click_save_config(self):
        pass




class testUI(ft.Column):
    def __init__(self, page: ft.Page, *args, **kwargs):
        self.page = page
        controls = []
        super().__init__(*args, controls=controls, **kwargs)
    
    def __load_config(self):
        pass

    def __gather_endpoints(self):
        pass

    def __load_endpoints(self):
        pass

    def __handle_select_dataset(self):
        pass

    def __handle_use_endpoints(self):
        pass
