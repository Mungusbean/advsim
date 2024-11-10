import flet as ft
import utils.endpoints.endpoint as ep
import ui_components.components as ui
import ui_components.popup_components as uipopup
import utils.utilfunctions as uf
from LoggerConfig import setup_logger

ICON_ROUTES = {"/": ft.Icon(ft.icons.HOME), 
               "/Chat":ft.Icon(ft.icons.CHAT), 
               "/Editor":ft.Icon(ft.icons.EDIT), 
               "/Endpoints":ft.Icon(ft.icons.CELL_TOWER),
               "/Settings":ft.Icon(ft.icons.SETTINGS)} 

logger = setup_logger(__name__)

def main(page: ft.Page) -> None:
    page.title = "ADVSim" # Sets first page title

    # Set up 


    # Instantiate global UI components
    chat_tab = ui.ChatTab(LLM=None, Chat_title="No Chat Selected", auto_scroll=True) # instantiates the singleton chat interface object 
    chat_tab.auto_scroll = True # Allows the chat to auto scroll to latest message sent, when interacting with the chat UI.
    nav_bar = ui.sideNavBar(reference_Page = page)
    app_bar = ft.AppBar(title=None, bgcolor=ft.colors.SURFACE_VARIANT)

    # Populating the nav bar with routing buttons 
    for route, icon in ICON_ROUTES.items():
        nav_bar.add_NavButton(ui.NavigationButton(page=page, Route=route, Icon=icon, Text=(route[1:] if route[1:] else "Home")))

    # Testing tab adding functionaility
    for i in range(20):
        nav_bar.add_ChatTab(f"Title {i}", f"Description {i}")
    # ================================
    
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
            spacing=26
            )
        )

        match page.route:
            case "/Chat":
                app_bar.title = ft.Text("Chat")
                page.views.append(
                    ft.View(
                        route = "/Chat", 
                        controls= [
                            app_bar,
                            ft.Column(
                                controls=[ft.Container(content=(chat_tab), expand=True, padding=10, border=None),
                                          ui.inputBar(page=page, chat_tab=chat_tab)  # Fixed height at the bottom
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
                        spacing=26
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
                        spacing = 26
                    )
                )

        # print(page.views)
        #logger.debug("Views:", page.views)
        page.views[-1].end_drawer = nav_bar
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
