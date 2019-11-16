from dependency_injector import containers, providers
from NasaCollageGUI.Logger import Logger
from NasaCollageGUI.pyqt.MainWindow import MainWindow


class ComponentsContainer(containers.DeclarativeContainer):
    """Application ComponentContainer"""

    config = providers.Configuration('config')
    logger = providers.Singleton(Logger, name='example')

    request_handler = providers.Singleton()

    main_window = providers.Singleton(MainWindow())


