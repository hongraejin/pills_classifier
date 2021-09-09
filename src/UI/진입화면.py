import time
import os
import datetime
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2



class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.figure = plt.Figure()
        self.cpt = cv2.VideoCapture(0)
        self.current_frame = None
        self.fps = 24
        self.initUI()

    def initUI(self):

        self.setWindowTitle('약 나누미')
        self.setGeometry(100,100,1024,768)

        self.startBtn = QPushButton('촬영시작', self)
        self.startBtn.move(100,100)
        self.startBtn.setFixedSize(QSize(100,50))
        self.startBtn.clicked.connect(self.start)

        self.pictureBtn = QPushButton('사진찍기', self)
        self.pictureBtn.move(100,200)
        self.pictureBtn.setFixedSize(QSize(100,50))
        self.pictureBtn.clicked.connect(self.save_figure)

        self.classifyBtn = QPushButton('분류하기', self)
        self.classifyBtn.move(100,300)
        self.classifyBtn.setFixedSize(QSize(100,50))
        self.classifyBtn.clicked.connect(self.classify)

        self.endBtn = QPushButton("촬영종료", self)
        self.endBtn.move(100,400)
        self.endBtn.setFixedSize(QSize(100,50))
        self.endBtn.clicked.connect(self.stop)

        self.canvas = FigureCanvas(self.figure)
        self.canvas.move(300,300)
        self.canvas.draw()

        self.frame = QLabel(self)
        self.frame.resize(640,480)
        self.frame.setScaledContents(True)
        self.frame.move(300,100)

        _, self.img_o = self.cpt.read()

        self.show()

    def classify(self):

        print("분류하기 진입")
        if not self.current_frame_for_save.any():
            print("현재 저장된 이미지가 없습니다.")
            return

        # cv2.imshow('input',self.current_frame_for_save)
        dst = self.current_frame_for_save.copy()
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

        # cv2.HoughCircles(이미지 배열, HOUGH_GRADIENT 상수, 이미지 해상도, 원의 최소거리,
        # param1 : Edge 검출 threshold, param2 : 작으면 원이 아닌 것도 검출, 크면 원에 가까운 것 검출
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15, param1=150, param2=30, minRadius=5, maxRadius=50)

        # 에러 제어 코드
        if circles is None:
            print("검출된 원이 없습니다.")
            return

        if not circles.any():
            print("원형 이미지가 없습니다.")
            return

        for i in circles[0]:
            cv2.circle(dst, (i[0], i[1]), (i[2]), (255, 255, 255), 1)

        cv2.imshow('dst',dst)
        cv2.waitKey()
        cv2.destroyAllWindows()



    def start(self):
        print("start 진입")
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 / self.fps)

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))
        self.timer.stop()

    def save_figure(self):
        if self.current_frame is None:
            return

        now_string = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

        try:
            os.mkdir('picture')
        except Exception as e:
            print(e)

        try:
            cv2.imwrite("picture\\"+now_string+".png", self.current_frame_for_save)
        except Exception as e:
            print('촬영에 실패하였습니다.')
            print(e)


    def nextFrameSlot(self):
        _, cam = self.cpt.read()

        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
        self.current_frame = cam.copy()
        frame_for_save = cv2.cvtColor(cam, cv2.COLOR_RGB2BGR)
        self.current_frame_for_save = frame_for_save.copy()

        img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = MyWidget()
    sys.exit(app.exec_())