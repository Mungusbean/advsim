from typing import Any, Callable, List, Optional
import flet as ft
from langchain.llms.base import LLM
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory

class ChatBubble(ft.Card):
    def __init__(self, is_user:bool, id: str | None = None, text: str | None = None, margin: int | float | ft.Margin | None = None, elevation: int | float | None = None, color: str | None = None, shadow_color: str | None = None, surface_tint_color: str | None = None, shape: ft.OutlinedBorder | None = ft.RoundedRectangleBorder(radius=20), clip_behavior: ft.ClipBehavior | None = None, is_semantic_container: bool | None = None, show_border_on_foreground: bool | None = None, variant: ft.CardVariant | None = None, ref: ft.Ref | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end = None, tooltip: str | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, key: str | None = None, adaptive: bool | None = None):
        if is_user: color = "gray"
        else: color = "white"

        if text is None: 
            content = ft.ProgressRing(
                height=24,
                width=24,
                color=ft.colors.GREY_300
            )
        else:
            content: ft.Control = ft.Container(content = ft.Markdown(
                text,
                selectable=True,
                extension_set="gitHubWeb", # type: ignore
                code_theme="atom-one-dark",
                code_style=ft.TextStyle(font_family="Courier New")
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
    def __init__(self, LLM_info, Chat_title: str, controls: List[ft.Control] | None = None, horizontal: bool | None = None, spacing: int | float | None = 10, item_extent: int | float | None = None, first_item_prototype: bool | None = None, divider_thickness: int | float | None = None, padding: int | float | ft.Padding | None = None, clip_behavior: ft.ClipBehavior | None = None, semantic_child_count: int | None = None, cache_extent: int | float | None = None, auto_scroll: bool | None = None, reverse: bool | None = None, on_scroll_interval: int | float | None = None, on_scroll: Callable[[ft.OnScrollEvent], None] | None = None, ref: ft.Ref | None = None, key: str | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end: Callable[[ft.ControlEvent], None] | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, adaptive: bool | None = None):
        self.Chat_title: str = Chat_title
        self.LLM_info = LLM_info
        padding = 10
        auto_scroll = True
        super().__init__(controls, horizontal, spacing, item_extent, first_item_prototype, divider_thickness, padding, clip_behavior, semantic_child_count, cache_extent, auto_scroll, reverse, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, adaptive)

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


class inputBar(ft.Row):
    """_summary_

    Args:
        ft (_type_): Input bar for manual testing of the model. Allows users to type prompts and test attack modules by sending them to the model.
    """
    def __init__(self, chat_tab: ChatTab, alignment: ft.MainAxisAlignment | None = None, vertical_alignment: ft.CrossAxisAlignment | None = None, spacing: int | float | None = None, tight: bool | None = None, wrap: bool | None = None, run_spacing: int | float | None = None, scroll: ft.ScrollMode | None = None, auto_scroll: bool | None = None, on_scroll_interval: int | float | None = None, on_scroll: Callable[[ft.OnScrollEvent], None] | None = None, ref: ft.Ref | None = None, key: str | None = None, width: int | float | None = None, height: int | float | None = None, left: int | float | None = None, top: int | float | None = None, right: int | float | None = None, bottom: int | float | None = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: dict[str, int | float] | int | float | None = None, opacity: int | float | None = None, rotate: int | float | ft.Rotate | None = None, scale: int | float | ft.Scale | None = None, offset: ft.Offset | tuple[float | int, float | int] | None = None, aspect_ratio: int | float | None = None, animate_opacity: bool | int | ft.Animation | None = None, animate_size: bool | int | ft.Animation | None = None, animate_position: bool | int | ft.Animation | None = None, animate_rotation: bool | int | ft.Animation | None = None, animate_scale: bool | int | ft.Animation | None = None, animate_offset: bool | int | ft.Animation | None = None, on_animation_end: Callable[[ft.ControlEvent], None] | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, rtl: bool | None = None, adaptive: bool | None = None):
        self.submit_button: ft.IconButton = ft.IconButton(icon= ft.icons.ARROW_CIRCLE_UP_ROUNDED,
                                                          icon_color=ft.colors.GREY_400,
                                                          icon_size=50,
                                                          tooltip="Send prompt",
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
                                                      on_submit= self.send_to_LLM # type: ignore
                                                      )
        self.chat_tab = chat_tab
        controls: List[ft.Control] = [self.new_message, self.submit_button]
        super().__init__(controls, alignment, vertical_alignment, spacing, tight, wrap, run_spacing, scroll, auto_scroll, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, adaptive)

    def send_to_LLM(self, e):
        prompt = self.new_message.value
        self.new_message.value = ""; self.new_message.update() # clear input from the text feild


        self.chat_tab.add_bubble(role=True,text=prompt) # type: ignore # Add in the user's prompt bubble
        self.chat_tab.add_bubble(role=False, text=None); self.chat_tab.update() # Add loading bubble while waiting for the API to return the response.
        
        # Disable the text feild until a response is received from the LLM API

        response = self.chat_tab.LLM_info.predict(input=prompt)
        self.chat_tab.pop() # Remove the loading bubble.

        self.chat_tab.add_bubble(role=False,text=response); self.chat_tab.update() # Update the chat_tab object with the received response. 





class sideNavBar(ft.NavigationDrawer):
    def __init__(self, controls: List[ft.Control] | None = None, open: bool = False, selected_index: int | None = None, bgcolor: str | None = None, elevation: int | float | None = None, indicator_color: str | None = None, indicator_shape: ft.OutlinedBorder | None = None, shadow_color: str | None = None, surface_tint_color: str | None = None, tile_padding: int | float | ft.Padding | None = None, position: ft.NavigationDrawerPosition | None = None, on_change: Callable[[ft.ControlEvent], None] | None = None, on_dismiss: Callable[[ft.ControlEvent], None] | None = None, ref: ft.Ref | None = None, disabled: bool | None = None, visible: bool | None = None, data: Any = None):
        self.Navigations = ft.ListView(
            controls=[
                ft.Text("Placeholder1"),
                ft.Text("Placeholder2"),
                ft.Text("Placeholder3"),
                ft.Text("Placeholder4")
            ]
        )
        controls = [self.Navigations]
        super().__init__(controls, open, selected_index, bgcolor, elevation, indicator_color, indicator_shape, shadow_color, surface_tint_color, tile_padding, position, on_change, on_dismiss, ref, disabled, visible, data)
    
    def delete_ChatTab(self, event):
        event.control.parent.controls.remove(event.control)
        #add callbacdk to update page?



    # Method to help add a dismissable chat to the navbar
    # Onclick, loads the selected chat and system into the chat.
    def add_ChatTab(self, title: str, description: str):
        if len(self.controls) < 1: return # type: ignore
        exp = ft.ExpansionPanel(
            header= ft.ListTile(title=ft.Text(title))
        )
        exp.content = ft.ListTile(subtitle=ft.Text(description),
                                  trailing=ft.IconButton(ft.icons.DELETE, on_click=print("To be implemented"), data=exp)

        )
        self.controls.append(ft.Dismissible( # type: ignore
            content= exp,
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            secondary_background=ft.Container(content=ft.Text("delete"),
                                              bgcolor=ft.colors.RED_300),
            dismiss_thresholds={
                ft.DismissDirection.END_TO_START: 0.2
            }
        ))
    
    pass