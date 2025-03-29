from textual.app import App, ComposeResult
from textual.widgets import Button, Label


class MyApp(App):
    CSS_PATH = "app.css"

    def compose(self) -> ComposeResult:
        self.close_button = Button("Close", id="close")
        yield Label("This is a Textual App TUI", id="label")
        yield self.close_button

    def on_mount(self) -> None:
        self.screen.styles.background = "green"
        self.close_button.styles.background = "purple"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)


if __name__ == "__main__":
    app = MyApp()
    app.run()
