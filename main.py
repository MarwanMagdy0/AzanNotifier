from utiles import *

# TODO: colors

class TimestampOperations:
    @staticmethod
    def get_current_date_string():
        today = datetime.now()
        return "{}-{}-{}".format(today.day, today.month, today.year)
    
    @staticmethod
    def delta_time2hoursMinuitsSeconds(delta_time):
        hours, remainder = divmod(delta_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return int(hours), int(minutes), int(seconds)

    @staticmethod
    def timestamp2hoursMinuit(timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%I:%M %p")

class TrayThread(QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
    
    def on_left_click(self):
        """
        this method show the screen of the program
        """
        self.ui.show()
        self.ui.activateWindow()
    
    def on_right_click(self):
        """
        this method closes the entire program
        """
        self.ui.close()

    def run(self):
        image = Image.open(PATH + "logo.png")

        # Create a menu item with the left-click event handler
        menu = (pystray.MenuItem("show", self.on_left_click, default = True),
                pystray.MenuItem("exit", self.on_right_click))

        # Create the tray icon with the menu
        icon = pystray.Icon("tray_icon", image, "Tray Icon", menu)

        # Run the tray icon
        icon.run()


class UI(QDialog):
    milad_label      : QLabel
    hijri_label      : QLabel
    next_pray_label  : QLabel
    fajr_label       : QLabel
    sunrise_label    : QLabel
    duhr_label       : QLabel
    asr_label        : QLabel
    maghrib_label    : QLabel
    isha_label       : QLabel
    firstthird_label : QLabel
    midnight_label   : QLabel
    lastthird_label  : QLabel
    imsak_label      : QLabel
    def __init__(self):
        super().__init__()
        loadUi(PATH + "load.ui", self)
        self.prev_pray = None
        self.update_day_data()
        self.start_tray_thread()
        self.init_timer()
    
    def init_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_next_pray_label)
        self.timer.start()
    
    def start_tray_thread(self):
        self.tray_thread = TrayThread(self)
        self.tray_thread.start()

    def update_day_data(self):
        self.fixed_date = datetime.now() # this date is fixed every day to just compare with the now time, if diffrence in day update it again
        with open(PATH + "year_data.json", "r") as file:
            year_data = json.load(file)
            self.day_data = year_data[str(self.fixed_date.month)][str(self.fixed_date.day)]
        print(self.day_data["praying_times"])
        self.update_labels()
        self.update_next_pray_label()
    
    def update_labels(self):
        praying_times = self.day_data["praying_times"]
        hijri_date    = self.day_data["hijri_date"]
        self.milad_label     .setText(TimestampOperations.get_current_date_string())
        self.hijri_label     .setText(hijri_date)
        self.fajr_label      .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Fajr"]))
        self.sunrise_label   .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Sunrise"]))
        self.duhr_label      .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Dhuhr"]))
        self.asr_label       .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Asr"])) 
        self.maghrib_label   .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Maghrib"])) 
        self.isha_label      .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Isha"])) 
        self.firstthird_label.setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Firstthird"])) 
        self.midnight_label  .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Midnight"])) 
        self.lastthird_label .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Lastthird"])) 
        self.imsak_label     .setText(TimestampOperations.timestamp2hoursMinuit(praying_times["Imsak"]))


    def update_next_pray_label(self):
        if datetime.now().date() != self.fixed_date.date():
            self.update_day_data()
            
        for pray_name, pray_time in self.day_data["praying_times"].items():
            if time.time() < pray_time:
                delta_time = pray_time - time.time()
                hours, minuits, seconds = TimestampOperations.delta_time2hoursMinuitsSeconds(delta_time)
                if hours==0 and minuits <= NOTIFY_BEFORE and self.prev_pray != pray_name:
                    notify(f"remaining {NOTIFY_BEFORE} Min until {pray_name} starts")
                    self.prev_pray = pray_name
                remaining_time_string = f"{hours}:{minuits}:{seconds}"
                next_pray_text = "{} until {} starts".format(remaining_time_string, pray_name)
                self.next_pray_label.setText(next_pray_text)
                break
    

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        if event.spontaneous():
            self.hide()
            event.ignore()
        else:
            event.accept()
    




if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    # print(ui.delta_time2hoursMinuitsSeconds(60*61 + ))
    app.exec_()