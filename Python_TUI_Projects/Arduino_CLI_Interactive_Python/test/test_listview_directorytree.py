from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, ListItem, ListView, Footer, Label
from textual.containers import Container
from pathlib import Path


class Listview_Directorytree(App):
    CSS_PATH = "css/listview_directorytree.css"

    def compose(self) -> ComposeResult:
        with Container(id="container_test"):
            yield DirectoryTree("./", id="directory_tree")
            yield ListView(id="list_view")

        yield Footer()

    def on_directory_tree_directory_selected(
        self, event: DirectoryTree.DirectorySelected
    ) -> None:
        selected_path = event.path
        list_view = self.query_one("#list_view", ListView)
        list_view.clear()

        try:
            for item in Path(selected_path).iterdir():
                list_view.append(ListItem(Label(str(item.name))))

        except PermissionError:
            list_view.append(ListItem(Label("Permission Denied")))


if __name__ == "__main__":
    app = Listview_Directorytree()
    app.run()
