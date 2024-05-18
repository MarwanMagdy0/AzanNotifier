from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QDesktopWidget
from PyQt5.QtCore import QTimer, QThread, Qt, QPoint
from plyer import notification
from datetime import datetime
from PyQt5.uic import loadUi
from PIL import Image
import traceback
import pystray
import logging
import json
import time
import sys
import os

PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
NOTIFY_BEFORE = 15 # this is the time that program notifies you before the pray in minuits

def notify(message):
    notification.notify(
        title="Azan Notifier",
        message=message,
        app_name='Azan Notifier',
        timeout=1
    )


class Logger:
    @staticmethod
    def logIntoFile(file_name):
        # Create the root logger and set its level to DEBUG
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # Create a file handler and set its level to INFO
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Create a console handler and set its level to INFO
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Set custom exception hook to handle uncaught exceptions
        sys.excepthook = Logger.handle_exception

    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        # Log unhandled exceptions with traceback
        logging.error(f'Unhandled exception: {exc_type.__name__}: {exc_value}')
        logging.error("".join(traceback.format_tb(exc_traceback)))

Logger.logIntoFile(PATH + "logg.log")