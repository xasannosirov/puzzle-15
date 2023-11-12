from ui import QApplication, sys, Game

app = QApplication(sys.argv)
game = Game(4)
sys.exit(app.exec_())
