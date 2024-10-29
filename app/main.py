import flet as ft
import ui_components.components as ui



def main(page: ft.Page) -> None:
    page.title = "Home" # Sets first page title

    # Instantiate global UI components
    chat_tab = ui.ChatTab(LLM=None, Chat_title="No Chat Selected", auto_scroll=True) # instantiates the singleton chat interface object for manual testing 
    chat_tab.auto_scroll = True
    nav_bar = ui.sideNavBar(reference_Page = page)

    # Testing tab adding functionaility
    for i in range(20):
        nav_bar.add_ChatTab(f"Title {i}", f"Description {i}")

    app_bar = ft.AppBar(title=None)
    print("objects initialised")

    def route_change(e: ft.RouteChangeEvent) -> None:
        page.views.clear()
        app_bar.title = ft.Text("Home")
        page.views.append(
            ft.View(
            route ="/", # Sets this as the base route 
            controls = [
                app_bar,
                ft.Text(value="Home", size=30),
                ft.ElevatedButton(text='Chat', on_click=lambda _: page.go('/ManualChatUI'))
            ],
            vertical_alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            spacing = 26
            )
        )

        match page.route:
            case "/ManualChatUI":
                app_bar.title = ft.Text("Chat")
                page.views.append(
                    ft.View(
                        route = "/ManualChatUI", 
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
                        spacing = 26
                    )
                )
            
            case "/Endpoints":
                app_bar.title = ft.Text("Endpoints")
                page.views.append(
                    ft.View(
                        route= "/Endpoints",
                        controls = [
                            app_bar,
                            ft.Text("Endpoints", size=30)
                        ],
                        vertical_alignment= ft.MainAxisAlignment.CENTER,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        spacing = 26
                    )
                )

        print(page.views)
        page.views[-1].end_drawer = nav_bar
        page.update()

    def view_pop(e: ft.ViewPopEvent) -> None:
        page.views.pop()
        top_view: ft.View = page.views[-1]
        page.go(top_view.route) # type: ignore

    print("setting routing functions...")
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    print("navigated to home route")



ft.app(target=main)
