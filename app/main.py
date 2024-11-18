import flet as ft
import utils.endpoints.endpoint as ep
import ui_components.components as ui
import ui_components.popup_components as uipopup
import utils.utilfunctions as ufuncs
from LoggerConfig import setup_logger
from utils.LLM.CustomLLM import RequestsLLM

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda

# Setup
ICON_ROUTES = {"/": ft.Icon(ft.icons.HOME), 
               "/Chat":ft.Icon(ft.icons.CHAT), 
               "/Editor":ft.Icon(ft.icons.EDIT), 
               "/Endpoints":ft.Icon(ft.icons.CELL_TOWER),
               "/Configuration":ft.Icon(ft.icons.BUILD_CIRCLE_ROUNDED),
               "/Settings":ft.Icon(ft.icons.SETTINGS)} 

logger = setup_logger(__name__) # Creates the logger for the main flet application
ufuncs.create_masterkey() # Attempts to create a masterkey

def main(page: ft.Page) -> None:
    page.title = "ADVSim" # Sets first page title

    # Instantiate global components and add them to the page session, the global variables can be acessed by passing a the page reference to any of the releveant functions or objects
    session_settings: dict = dict() # loads the settings saved by the user
    selected_endpoint: dict = {}
    last_time_click: list
    chat_tab: ui.ChatTab
    app_bar: ft.AppBar
    nav_bar: ui.sideNavBar

    page.session.set("session_settings",  session_settings)
    page.session.set("selected_endpoint", selected_endpoint)
    page.session.set("last_time_click", last_time_click:= [0]) # time keeper for detecting double clicks, a list is used as a global mutable object to be changed
    page.session.set("chat_tab", chat_tab:= ui.ChatTab(LLM=None, Chat_title="No Chat Selected", auto_scroll=True)) # instantiates the global singleton chat interface object 
    chat_tab.auto_scroll = True # Allows the chat to auto scroll to latest message sent, when interacting with the chat UI.
    page.session.set("nav_bar", nav_bar:= ui.sideNavBar(page = page)) # global nav_bar
    page.session.set("app_bar", app_bar:= ft.AppBar(title=None, bgcolor=ft.colors.SURFACE_VARIANT)) # global appbar
    chat_tab.auto_scroll = True

    # Populating the nav bar with routing buttons 
    for route, icon in ICON_ROUTES.items():
        nav_bar.add_NavButton(ui.NavigationButton(page=page, Route=route, Icon=icon, Text=(route[1:] if route[1:] else "Home")))
    
    # print("objects initialised")
    logger.info("objects initialised")

    # Note to self: please, PLEASE find a better way to do this, this is horrible
    def route_change(e: ft.RouteChangeEvent) -> None:
        page.views.clear()
        app_bar.title = ft.Text("Home")
        page.views.append(
            ft.View(
            route ="/", # Sets this as the base route 
            controls = [
                app_bar,
                ft.Text(value="Home", size=30),
            ],
            vertical_alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            spacing=26,
            scroll=ft.ScrollMode.ALWAYS
            )
        )

        match page.route:
            case "/Chat":
                if page.session.get("selected_endpoint"):
                    app_bar.title = ft.Text("Chat")
                    endpoint_details: dict = page.session.get("selected_endpoint") # type: ignore
                    params = endpoint_details["params"]

                    # # for debugging
                    # for key, val in params.items():
                    #     print(f"{key} : {val} -> type: ({type(val)})")

                    llm = RequestsLLM().create_endpoint(endpoint_type=endpoint_details["endpoint_name"], params=params)
                    prompt = ChatPromptTemplate.from_messages(
                        [
                            MessagesPlaceholder(variable_name="history"),
                            ("human", "{input}"),
                        ]
                    )

                    # New memory implementation
                    store = {}
                    def get_session_history(session_id: str) -> BaseChatMessageHistory:
                        if session_id not in store:
                            store[session_id] = ChatMessageHistory()
                        return store[session_id]


                    runnable = prompt | llm 

                    LLM_conversation = RunnableWithMessageHistory(
                        runnable=runnable, # type: ignore
                        get_session_history=get_session_history,
                        input_messages_key="input",
                        history_messages_key="history"
                    )                
                    chat_tab.LLM = LLM_conversation
                page.views.append(
                    ft.View(
                        route = "/Chat", 
                        controls= [
                            app_bar,
                            ft.Column(
                                controls=[ft.Container(content=(chat_tab), expand=True, padding=10, border=None),
                                          ft.Container(content = ui.inputBar(page=page), border_radius=24, bgcolor=ft.colors.SURFACE_VARIANT, padding=0, alignment=ft.alignment.center)  # Fixed height at the bottom
                                ],
                                expand=True)  # The column expands to take up the entire page height
                        ]
                    )
                )
                
            case "/Editor":
                app_bar.title = ft.Text("Editor")
                page.views.append(
                    ft.View(
                        route= "/Editor",
                        controls = [
                            app_bar,
                            ft.Text("Editor", size=30)
                        ],
                        vertical_alignment= ft.MainAxisAlignment.CENTER,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        spacing=26,
                        scroll=ft.ScrollMode.ALWAYS
                    )
                )
            
            case "/Endpoints":
                app_bar.title = ft.Text("Endpoints")
                page.views.append(
                    ft.View(
                        route= "/Endpoints",
                        controls = [
                            app_bar,
                            ft.Text("Endpoints", size=30),
                            ui.EndpointsUI(page=page)
                        ],
                        vertical_alignment= ft.MainAxisAlignment.CENTER,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        spacing = 26,
                        scroll=ft.ScrollMode.ALWAYS
                    )
                )
            
            case "/Settings":
                app_bar.title = ft.Text("Settings")
                page.views.append(
                    ft.View(
                        route= "/Settings",
                        controls = [
                            app_bar,
                            ft.Text("Settings", size=30),
                        ],
                        vertical_alignment= ft.MainAxisAlignment.CENTER,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        spacing = 26,
                        scroll=ft.ScrollMode.ALWAYS
                    )
                )

            case "/Configuration":
                app_bar.title = ft.Text("Configuration")
                page.views.append(
                    ft.View(
                        route= "/Configuration",
                        controls = [
                            app_bar,
                            ft.Text("Configuration", size=30),
                        ],
                        vertical_alignment= ft.MainAxisAlignment.CENTER,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        spacing = 26,
                        scroll=ft.ScrollMode.ALWAYS
                    )
                )

        # print(page.views)
        #logger.debug("Views:", page.views)
        new_nav_bar = ui.sideNavBar(page=page)
        page.views[-1].end_drawer = new_nav_bar
        for route, icon in ICON_ROUTES.items():
            new_nav_bar.add_NavButton(ui.NavigationButton(page=page, Route=route, Icon=icon, Text=(route[1:] if route[1:] else "Home")))
        page.update()

    def view_pop(e: ft.ViewPopEvent) -> None:
        page.views.pop()
        top_view: ft.View = page.views[-1]
        page.go(top_view.route) # type: ignore

    # print("setting routing functions...")
    logger.info("setting routing functions...")
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    # print("navigated to home route")
    logger.info("navigated to home route")



ft.app(target=main)
