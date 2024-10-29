from typing import Any, Callable, List, Optional
import flet as ft
from langchain.llms.base import LLM
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory

class ChatBubble(ft.Card):
    def __init__(self, is_user:bool, id: str | None = None, text: str | None = None, margin: int | float | ft.Margin | None = None, elevation: int | float | None = None, color: str | None = None, shadow_color: str | None = None, surface_tint_color: str | None = None, shape: ft.OutlinedBorder | None = ft.RoundedRectangleBorder(radius=10), clip_behavior: ft.ClipBehavior | None = None, is_semantic_container: bool | None = None, show_border_on_foreground: bool | None = None, variant: ft.CardVariant | None = None, ref: ft.Ref | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end = None, tooltip: str | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, key: str | None = None, adaptive: bool | None = None):
        if is_user: color = "gray"
        else: color = "white"

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
            padding=24
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

    # To implement a singleton for the chat interface, as only its parameters needs to be changes for 
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
            controls.insert(int(role),ft.CircleAvatar(content = ft.Text(role_name),
                                                      bgcolor = ft.colors.PURPLE_200 if role else ft.colors.AMBER_200)) # type: ignore
            self.controls.append(
                ft.Row(controls= controls, # type: ignore
                        alignment = bubble_alignment,
                        spacing = 10
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
        self.new_message: ft.TextField = ft.TextField(hint_text= "Message AI",
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
        
    

class sideNavBar(ft.NavigationDrawer):
    def __init__(
        self,
        reference_Page,
        controls: List[ft.Control] | None = None,
        **kwargs
    ):
        self.reference_Page = reference_Page
        self.Navigations = ft.ListView(
            controls=[
                ft.ElevatedButton(text='Home', on_click=lambda _: self.reference_Page.go('/Home')),
                ft.ElevatedButton(text='Chat', on_click=lambda _: self.reference_Page.go('/ManualChatUI')),
                ft.ElevatedButton(text='Editor', on_click=lambda _: self.reference_Page.go('/Editor')),
                ft.ElevatedButton(text='Endpoints', on_click=lambda _: self.reference_Page.go('/Endpoints'))
            ],
            padding=20
        )
        self.tabs = ft.ListView()

        self.tile_padding = 0.2
        controls = [self.Navigations, self.tabs]
        super().__init__(
            controls=controls,
            **kwargs
        )

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
        
class OptionsGrid(ft.GridView):
    def __init__(self, controls: List[ft.Control] | None = None, horizontal: bool | None = None, runs_count: int | None = None, max_extent: int | None = None, spacing: int | float | None = None, run_spacing: int | float | None = None, child_aspect_ratio: int | float | None = None, padding: int | float | ft.Padding | None = None, clip_behavior: ft.ClipBehavior | None = None, semantic_child_count: int | None = None, cache_extent: int | float | None = None, ref: ft.Ref | None = None, key: str | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end: Callable[[ft.ControlEvent], None] | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, auto_scroll: bool | None = None, reverse: bool | None = None, on_scroll_interval: int | float | None = None, on_scroll: Callable[[ft.OnScrollEvent], None] | None = None, adaptive: bool | None = None):
        if controls is None:
            controls = [
                
            ]
        super().__init__(controls, horizontal, runs_count, max_extent, spacing, run_spacing, child_aspect_ratio, padding, clip_behavior, semantic_child_count, cache_extent, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, auto_scroll, reverse, on_scroll_interval, on_scroll, adaptive)
    


class TopMenuBar(ft.MenuBar):
    def __init__(self, controls: List[ft.Control]|None = None, clip_behavior: ft.ClipBehavior | None = None, style: ft.MenuStyle | None = None, ref: ft.Ref | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None):
        if controls is None:
            controls = [ft.MenuItemButton(),
                        ft.MenuItemButton(),
                        ]
        super().__init__(controls, clip_behavior, style, ref, expand, expand_loose, col, opacity, visible, disabled, data)


    # Sub Menu Handlers 
    def handle_submenu_open(self):
        pass

    def handle_submenu_close(self):
        pass

    def handle_submenu_hover(self):
        pass

    def handle_submenu_click(self):
        pass

    # Menu buttons Handlers
    def handle_menubutton_hover(self):
        pass

    def handle_menubutton_click(self, e, route): 
        pass

    pass
