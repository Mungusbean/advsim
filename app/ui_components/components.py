import flet as ft
import utils.endpoints.endpoint as ep
from typing import Any, Callable, List, Optional, Sequence
from langchain.llms.base import LLM
# from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from utils.endpoints.endpoint import Save_New_Endpoint

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
        elif text == "⚠ Something went wrong.":
            content = ft.Container(content = ft.Text("⚠ Something went wrong.", color="red"), padding=24)
        else:
            content: ft.Control = ft.Container(content = ft.Markdown(
                text,
                selectable=True,
                # extension_set="gitHubWeb", # type: ignore
                extension_set=ft.MarkdownExtensionSet.COMMON_MARK, # type: ignore
                # code_theme="atom-one-dark", # type: ignore
                code_theme=ft.MarkdownCodeTheme.ATOM_ONE_DARK_REASONABLE, # type: ignore
                code_style=ft.TextStyle(font_family="Courier New"),
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
                                    content=ft.CircleAvatar(content=ft.Text(role_name), bgcolor=ft.colors.PURPLE_200 if role else ft.colors.AMBER_200),
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

    def delete_bubble(self, index):
        pass

    def clear_chat(self):
        pass


class inputBar(ft.Row):
    """_summary_

    Args:
        ft (_type_): Input bar for manual testing of the model. Allows users to type prompts and test attack modules by sending them to the model.
    """
    def __init__(self, page: ft.Page, chat_tab: ChatTab, alignment: ft.MainAxisAlignment | None = None, vertical_alignment: ft.CrossAxisAlignment | None = None, spacing: int | float | None = None, tight: bool | None = None, wrap: bool | None = None, run_spacing: int | float | None = None, scroll: ft.ScrollMode | None = None, auto_scroll: bool | None = None, on_scroll_interval: int | float | None = None, on_scroll: Callable[[ft.OnScrollEvent], None] | None = None, ref: ft.Ref | None = None, key: str | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end: Callable[[ft.ControlEvent], None] | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, rtl: bool | None = None, adaptive: bool | None = None):
        self.submit_button: ft.IconButton = ft.IconButton(icon= ft.icons.ARROW_CIRCLE_UP_ROUNDED,
                                                          icon_color=ft.colors.GREY_400,
                                                          icon_size=50,
                                                          tooltip="Send prompt",
                                                          disabled= True,
                                                          disabled_color=ft.colors.GREY_50,
                                                          on_click= self.send_to_LLM # type:ignore
                                                          )
        self.__hint_text = "Message AI"
        self.new_message: ft.TextField = ft.TextField(hint_text= self.__hint_text,
                                                      border_color=ft.colors.TRANSPARENT,
                                                      border_radius= 25,  # Set rounded corners
                                                      filled=True,  # Optional: Adds a background color to make it stand out
                                                      autofocus= True,
                                                      autocorrect= False,
                                                      shift_enter= True,
                                                      min_lines= 1,
                                                      max_lines=3,
                                                      expand= True,
                                                      on_change= self._toggle_submit_button, # type: ignore
                                                      on_submit= self.send_to_LLM # type: ignore
                                                      )
        self.chat_tab: ChatTab = chat_tab
        controls: List[ft.Control] = [self.new_message, self.submit_button]
        # self.page: ft.Page = page
        super().__init__(controls, alignment, vertical_alignment, spacing, tight, wrap, run_spacing, scroll, auto_scroll, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, adaptive)

    def _toggle_submit_button(self, e):
        """
        toggles the submit button on if the textfeild input is not blank
        """
        self.submit_button.disabled = not self.new_message.value or not self.new_message.value.strip()
        self.update()


    def send_to_LLM(self, e) -> None:
        """
        Sends the value of the text feild to the LLM 

        Args:
            e (_type_): event 

        Returns:
            _type_: None
        """
        if self.chat_tab.LLM is None:
            return
        # Check if the TextField value is None or empty
        if not self.new_message.value or not self.new_message.value.strip():
            return  # Do nothing if the input is None or empty
        
        prompt = self.new_message.value
        self.new_message.value = ""; self.new_message.update() # clear input from the text feild

        self.submit_button.disabled = True # ensure button and textfeilds are dsiabled while waiting for the message to be sent.
        self.new_message.disabled = True
        self.update()

        self.chat_tab.add_bubble(role=True,text=prompt) # type: ignore # Adds in and renders the user's prompt bubble
        self.chat_tab.add_bubble(role=False, text=None); self.chat_tab.update() # Add loading bubble while waiting for the API to return the response.

        # response = self.chat_tab.LLM_info.predict(input=prompt)
        response = self.chat_tab.LLM.invoke(
            {"input": prompt},
            config = {"configurable": {"session_id":  self.chat_tab.Chat_title}}

        )
        self.chat_tab.pop() # Remove the loading bubble.

        self.chat_tab.add_bubble(role=False,text=response); self.chat_tab.update() # Update the chat_tab object with the received response. 

        self.new_message.disabled = False # Re-able just the textfeild when the page is updated.
        self.new_message.update()
        
    
class NavigationButton(ft.MenuItemButton):
        def __init__(self, page: ft.Page, Route: str, Icon: ft.Icon=ft.Icon(ft.icons.ABC), Text: str="Button", Text_size: int=16, *args, **kwargs):
            super().__init__(leading = Icon, content=ft.Text(Text, size=Text_size), on_click=lambda _: page.go(Route),*args, **kwargs)
            

class sideNavBar(ft.NavigationDrawer):
    def __init__(
        self,
        reference_Page: ft.Page,
        controls: List[ft.Control] | None = None,
        **kwargs
    ):
        self.reference_Page = reference_Page
        self.Navigations = ft.ListView(
            controls=[
                ft.Row(controls=[ft.Icon(ft.icons.LIGHT_MODE, size=24),ft.CupertinoSwitch(label="Light mode", value=True, on_change=self.toggle_light_dark, track_color=ft.colors.GREEN_400)], spacing=5)
            ],
            padding=20,
            spacing = 5
        )
        self.tabs = ft.ListView()

        self.tile_padding = 0.2
        controls = [self.Navigations, self.tabs]
        super().__init__(
            controls=controls,
            **kwargs
        )
    
    def toggle_light_dark(self, e):
            self.reference_Page.theme_mode = ft.ThemeMode.DARK if not self.Navigations.controls[0].controls[1].value else ft.ThemeMode.LIGHT # toggles between light and dark
            self.Navigations.controls[0].controls[0] = ft.Icon(ft.icons.DARK_MODE, size=24, color=ft.colors.GREEN_400) if not self.Navigations.controls[0].controls[1].value else ft.Icon(ft.icons.LIGHT_MODE, size=24) # type: ignore toggles between light and dark icon symbols
            self.Navigations.controls[0].controls[1].label = "Dark mode" if not self.Navigations.controls[0].controls[1].value else "Light Mode"
            self.reference_Page.update()

    def delete_ChatTab(self, event: ft.ControlEvent) -> bool:
        """Removes an elements from the NavBar class's navigations list

        Args:
            event (ft.ControlEvent): for internal use as a lambda function in flet objects.

        Returns:
            bool: Returns True when the tab is sucessfully deleted else returns false
        """
        try:
            self.tabs.controls.remove(event.control.parent.parent) # removing the selected tab from the navigation drawer
            print("Sucessfully deleted tab")
            self.tabs.update()
            return True
        except Exception as e:
            print(f"Could not delete tab due to: {e}")
            return False

    def add_ChatTab(self, title: str, description: str) -> bool:
        """Adds a new tab to the navigation drawer for access later. Tabs are used to hold specific model setups.
        Returns True if sucessfully added tab else returns False

        Args:
            title (str): title for the tab to be added.
            description (str): short ddesceription for tab to be added.
        """
        try:
            delete_button = ft.IconButton(icon=ft.icons.DELETE,
                                          on_click= self.delete_ChatTab) # type: ignore (I'm doing some bad stuff with flet objects rn)
            tile=ft.ExpansionTile(title= ft.Text(title),
                                        affinity= ft.TileAffinity.PLATFORM,
                                        controls= [ft.Row(controls=[
                                            ft.Text(description),
                                            delete_button
                                        ])]
                                        )

            self.tabs.controls.append(tile) # appending the tile to nav controls (no need to update page as the entire navigation drawer is event based and not added directly to a page)
            return True
        except Exception as e:
            # should probably use loggers
            print(f"Ran into error when attempting to add tab: {e}")
            return False
    
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
                 on_click = None,
                 **kwargs):
        self.default_bgcolor = f"{ft.colors.SURFACE_VARIANT},0.3"
        if not bgcolor: bgcolor = self.default_bgcolor 
        self.icon = ft.Icon(icons)
        self.Subtitle_color = Subtitle_color if Subtitle_color else ft.colors.GREY_400
        self.content = ft.Row(controls=[
            ft.Icon(icons),
            ft.Column(controls=[ft.Text(Title, color=Title_color, size=Title_size), ft.Text(Subtitle, color=self.Subtitle_color, size=Subtitle_size)], spacing=0, expand=True),
            ft.IconButton(icon=ft.icons.DELETE)
        ])
        super().__init__(*args, content=self.content, bgcolor=bgcolor, padding=5, on_click=on_click, on_hover=self.__on_hover, border_radius=border_radius, tooltip=tooltip,**kwargs)

    def __on_hover(self, e):
        e.control.bgcolor = self.default_bgcolor if e.data == "false" else ft.colors.ON_PRIMARY
        e.control.update()
        pass


    pass

class EndpointsUI(ft.Column):
    def __init__(self, page: ft.Page, *args, **kwargs):
        self.button_size = 88
        self.button_color = ft.colors.SURFACE_VARIANT
        self.controls = [
            ft.Row(controls=[
                ft.FloatingActionButton(icon=ft.icons.ADD, 
                                        elevation=0, 
                                        shape=ft.RoundedRectangleBorder(radius=12), 
                                        height=self.button_size, 
                                        width=self.button_size, 
                                        bgcolor=self.button_color,
                                        tooltip="Add an endpoint",
                                        on_click=lambda _: print("Wow, the add endpoint button has been clicked!")),
                ft.FloatingActionButton(icon=ft.icons.HELP_OUTLINE_ROUNDED, 
                                        elevation=0, 
                                        shape=ft.RoundedRectangleBorder(radius=12), 
                                        height=self.button_size, 
                                        width=self.button_size, 
                                        bgcolor=self.button_color,
                                        tooltip="Help",
                                        on_click=lambda _: print("Wow, the help button has been clicked!"))
            ],
            alignment=ft.MainAxisAlignment.CENTER),
            ft.Column(
                controls=[
                ft.TextField(hint_text="Search available endpoints",
                             border_color=ft.colors.TRANSPARENT,
                             fill_color=ft.colors.with_opacity(0.5,ft.colors.SURFACE_VARIANT),
                             filled=True,
                             border_radius=12,
                             expand=True),
                ft.Container(
                content = ft.ListView(controls=[IconListTile(on_click=lambda _: print("icon tile 1 clicked")), IconListTile(on_click=lambda _: print("icon tile 2 clicked"))],
                            spacing=5, 
                            padding=10))],
                width=800),
        ]
        super().__init__(*args,controls=self.controls, **kwargs)

    def add_endpoint_tile(self) -> bool:
        return True

    def remove_endpoint_tile(self) -> bool:
        return True

    def search(self, name: str) -> list:
        return list()
    
    def on_click_endpoint_tile(self):
        pass

class EditorUI(ft.Row):
    def __init__(self, *args, **kwargs):
        self.controls = []
        super().__init__(*args, controls=self.controls, **kwargs)

    def insert_attack_module(self, attack_module_name: str) -> bool:
        return True

    def remove_attack_module(self, attack_module_name: str) -> bool:
        return True
    
    def insert_LLM_feature(self, feature_name: str) -> bool:
        return True 
    
    def remove_LLM_feature(self, feature_name: str ) -> bool:
        return True
    
    def insert_defence_module(self, defence_module_name: str) -> bool:
        return True
    
    def remove_defence_module(self, defence_module_name: str) -> bool:
        return True
    