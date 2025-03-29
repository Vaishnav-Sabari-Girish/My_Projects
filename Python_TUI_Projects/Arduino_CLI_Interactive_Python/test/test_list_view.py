from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, ListItem, ListView


class ListViewApp(App):
    CSS_PATH = "css/list_view.css"

    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(Label("One")), ListItem(Label("Two")), ListItem(Label("Three"))
        )

        yield Footer()


if __name__ == "__main__":
    app = ListViewApp()
    app.run()
