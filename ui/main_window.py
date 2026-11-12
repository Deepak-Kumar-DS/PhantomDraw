import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QStackedWidget,
    QSizePolicy,
    QGridLayout
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class PhantomMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PhantomDraw AI")
        self.resize(1400, 850)
        self.setMinimumSize(1050, 650)

        self.setStyleSheet("""
            QMainWindow {
                background: #0b0d14;
            }

            QWidget {
                color: #f1f5f9;
                font-family: Segoe UI;
            }

            QFrame#Sidebar {
                background: #111522;
                border-right: 1px solid #252b3b;
            }

            QLabel#Logo {
                font-size: 25px;
                font-weight: bold;
                color: #8b9cff;
            }

            QLabel#Subtitle {
                color: #8993aa;
                font-size: 11px;
            }

            QPushButton#NavButton {
                background: transparent;
                color: #aab3c8;
                text-align: left;
                padding: 13px 15px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
            }

            QPushButton#NavButton:hover {
                background: #202941;
                color: white;
            }

            QPushButton#NavButton:checked {
                background: #29365b;
                color: #a5b4fc;
                font-weight: bold;
            }

            QFrame#Topbar {
                background: #111522;
                border-bottom: 1px solid #252b3b;
            }

            QLabel#PageTitle {
                font-size: 23px;
                font-weight: bold;
            }

            QLabel#Muted {
                color: #929db3;
                font-size: 12px;
            }

            QFrame#Card {
                background: #151b2b;
                border: 1px solid #29334b;
                border-radius: 14px;
            }

            QPushButton#PrimaryButton {
                background: #6677f5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 18px;
                font-weight: bold;
            }

            QPushButton#PrimaryButton:hover {
                background: #7888ff;
            }

            QPushButton#SecondaryButton {
                background: #222b40;
                color: #dce3f5;
                border: 1px solid #35415d;
                border-radius: 8px;
                padding: 10px 15px;
            }

            QPushButton#SecondaryButton:hover {
                background: #303c58;
            }
        """)

        self.pages = {}
        self.nav_buttons = {}

        self.build_interface()

    # ---------------------------------
    # MAIN INTERFACE
    # ---------------------------------

    def build_interface(self):

        central = QWidget()
        main_layout = QHBoxLayout(central)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setCentralWidget(central)

        # Sidebar
        sidebar = self.create_sidebar()

        # Main content
        content_area = QWidget()

        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Topbar
        topbar = self.create_topbar()

        # Pages
        self.stack = QStackedWidget()

        self.create_pages()

        content_layout.addWidget(topbar)
        content_layout.addWidget(self.stack)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)

        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        self.show_page("Dashboard")

    # ---------------------------------
    # SIDEBAR
    # ---------------------------------

    def create_sidebar(self):

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(245)

        layout = QVBoxLayout(sidebar)

        layout.setContentsMargins(15, 25, 15, 20)
        layout.setSpacing(8)

        logo = QLabel("✦ PhantomDraw")
        logo.setObjectName("Logo")

        subtitle = QLabel("AI CREATIVE WORKSPACE")
        subtitle.setObjectName("Subtitle")

        layout.addWidget(logo)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        navigation = [
            ("⌂", "Dashboard"),
            ("✎", "Drawing Studio"),
            ("◉", "Air Drawing"),
            ("✧", "AI Studio"),
            ("▤", "Whiteboard"),
            ("▣", "Animation Studio"),
            ("◇", "3D Studio"),
            ("▱", "My Projects"),
            ("⚙", "Settings")
        ]

        for icon, name in navigation:

            button = QPushButton(f"{icon}   {name}")

            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, page=name:
                self.show_page(page)
            )

            self.nav_buttons[name] = button

            layout.addWidget(button)

        layout.addStretch()

        version = QLabel("PhantomDraw AI  •  v1.0.0")
        version.setObjectName("Subtitle")

        layout.addWidget(version)

        return sidebar

    # ---------------------------------
    # TOPBAR
    # ---------------------------------

    def create_topbar(self):

        topbar = QFrame()
        topbar.setObjectName("Topbar")
        topbar.setFixedHeight(70)

        layout = QHBoxLayout(topbar)

        layout.setContentsMargins(25, 10, 25, 10)

        self.current_page_label = QLabel("Dashboard")
        self.current_page_label.setObjectName("PageTitle")

        workspace = QLabel("● Workspace Ready")
        workspace.setObjectName("Muted")

        layout.addWidget(self.current_page_label)
        layout.addStretch()
        layout.addWidget(workspace)

        return topbar

    # ---------------------------------
    # CREATE ALL PAGES
    # ---------------------------------

    def create_pages(self):

        page_names = [
            "Dashboard",
            "Drawing Studio",
            "Air Drawing",
            "AI Studio",
            "Whiteboard",
            "Animation Studio",
            "3D Studio",
            "My Projects",
            "Settings"
        ]

        for name in page_names:

            if name == "Dashboard":
                page = self.create_dashboard()

            else:
                page = self.create_module_page(name)

            self.pages[name] = page
            self.stack.addWidget(page)

    # ---------------------------------
    # DASHBOARD
    # ---------------------------------

    def create_dashboard(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 25)
        layout.setSpacing(20)

        welcome = QLabel("Welcome to PhantomDraw AI")
        welcome.setFont(QFont("Segoe UI", 25, QFont.Bold))

        description = QLabel(
            "Your creative workspace. Draw, design and create."
        )
        description.setObjectName("Muted")

        layout.addWidget(welcome)
        layout.addWidget(description)

        layout.addSpacing(15)

        # Main banner
        banner = QFrame()
        banner.setObjectName("Card")

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(25, 25, 25, 25)

        banner_title = QLabel("Create Without Limits")
        banner_title.setFont(QFont("Segoe UI", 21, QFont.Bold))

        banner_text = QLabel(
            "Bring your ideas to life with intelligent drawing tools, "
            "hand tracking and creative workflows."
        )

        banner_text.setObjectName("Muted")
        banner_text.setWordWrap(True)

        start_button = QPushButton("Open Drawing Studio")

        start_button.setObjectName("PrimaryButton")
        start_button.setCursor(Qt.PointingHandCursor)

        start_button.clicked.connect(
            lambda: self.show_page("Drawing Studio")
        )

        banner_layout.addWidget(banner_title)
        banner_layout.addWidget(banner_text)
        banner_layout.addSpacing(10)
        banner_layout.addWidget(start_button, alignment=Qt.AlignLeft)

        layout.addWidget(banner)

        section_title = QLabel("Creative Workspace")
        section_title.setFont(QFont("Segoe UI", 17, QFont.Bold))

        layout.addWidget(section_title)

        # Feature cards
        grid = QGridLayout()
        grid.setSpacing(15)

        cards = [
            ("✎", "Drawing Studio", "Create digital artwork."),
            ("◉", "Air Drawing", "Draw using hand gestures."),
            ("✧", "AI Studio", "Explore intelligent tools."),
            ("▤", "Whiteboard", "Create and present ideas."),
            ("▣", "Animation Studio", "Create frame animations."),
            ("◇", "3D Studio", "Explore 3D creativity.")
        ]

        for index, (icon, title, description) in enumerate(cards):

            card = self.create_feature_card(
                icon,
                title,
                description
            )

            row = index // 3
            column = index % 3

            grid.addWidget(card, row, column)

        layout.addLayout(grid)

        layout.addStretch()

        footer = QLabel(
            "Developed by Deepak Kumar Sharma"
        )

        footer.setObjectName("Muted")
        footer.setAlignment(Qt.AlignCenter)

        layout.addWidget(footer)

        return page

    # ---------------------------------
    # FEATURE CARD
    # ---------------------------------

    def create_feature_card(self, icon, title, description):

        card = QFrame()
        card.setObjectName("Card")
        card.setMinimumHeight(150)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(
            "font-size: 27px; color: #9baaff;"
        )

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Bold))

        description_label = QLabel(description)
        description_label.setObjectName("Muted")
        description_label.setWordWrap(True)

        button = QPushButton("Open →")
        button.setObjectName("SecondaryButton")
        button.setCursor(Qt.PointingHandCursor)

        button.clicked.connect(
            lambda checked=False, page=title:
            self.show_page(page)
        )

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(button, alignment=Qt.AlignLeft)

        return card

    # ---------------------------------
    # OTHER MODULE PAGES
    # ---------------------------------

    def create_module_page(self, name):

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(15)

        title = QLabel(name)
        title.setFont(QFont("Segoe UI", 25, QFont.Bold))

        description = QLabel(
            f"{name} workspace"
        )

        description.setObjectName("Muted")

        panel = QFrame()
        panel.setObjectName("Card")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(25, 25, 25, 25)

        message = QLabel(
            f"{name} module is ready for development."
        )

        message.setFont(QFont("Segoe UI", 15))
        message.setWordWrap(True)

        panel_layout.addWidget(message)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(15)
        layout.addWidget(panel)

        layout.addStretch()

        return page

    # ---------------------------------
    # PAGE NAVIGATION
    # ---------------------------------

    def show_page(self, page_name):

        if page_name not in self.pages:
            return

        self.stack.setCurrentWidget(
            self.pages[page_name]
        )

        self.current_page_label.setText(page_name)

        for name, button in self.nav_buttons.items():

            button.setChecked(name == page_name)


# ---------------------------------
# APPLICATION ENTRY
# ---------------------------------

def run_application():

    app = QApplication(sys.argv)

    app.setApplicationName("PhantomDraw AI")

    window = PhantomMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_application()