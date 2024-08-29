import flet as ft
import requests


def main(page: ft.Page):
    # Define state variables
    name = ft.TextField(label="Your name", width=200)
    greeting = ft.Text()

    # Event handler function
    def on_button_click(e):
        greeting.value = f"Hello, {name.value}!"
        page.update()

    # Create UI layout
    page.title = "Simple Flet App"
    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=[name]),
                ft.ElevatedButton("Greet Me", on_click=on_button_click),
                greeting,
            ]
        )
    )

    page.update()

ft.app(target=main)