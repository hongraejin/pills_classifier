import cv2
import os
import glob
import sys
files = glob.glob(os.path.join("D:\\pills_classifier\\src\\UI\\picture\\",'*.png'))
file = files[6]

src =cv2.imread(file)
dst = src.copy()
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# cv2.HoughCircle(검출 이미지, 검출 방법, 해상도 비율, 최소 거리, 캐니 엣지 임계값, 중심임계값,최소 반지름, 최대반지름)
# 검출 방법은 2단계 허프 변환방법 그레디언트 사용
# 해상도 비율은 원의 중심을 검출하는 데 사용되는 누산 평면의 해상도를  의미
# 인수를 1로 지정할 경우 입력한 이미지와 동일한 해상도를 가짐. 
# 인수를 2로 지정하면 누산 평면의 해상도가 절반으로 줄어 입력 이미지의 크기와 반비례함 
# 최소 거리 : 일차적으로 검출된 원과 원 사이의 최소 거리
# 케니 엣지 임계값은 허프 변홚에서 자체적으로 케니엣지를 적용하게 되고 이때 사용되는 상위 임계값을 의미
# 하위 임곗값은 자동으로 할당. 상위 임곗값의 절반에 해당하는 값을 사용
# 중심 임계값은 그레디언트 방법에 적용된 중심 히스토그램(누산 평면)에 대한 임곗값. 이 값보다 낮을 경우 더 많은 원이 검출됨
# 최소 반지름과 최대 반지름은 검출될 원의 반지름 범위. 0을 입력할 경우 반지름에 대한 제한 조건을 두지 않음
# 최소 반지름과 최대 반지름에 0을 입력할 경우 반지름을 고려하지 않고 검출하며, 최대 반지름에 음수를 입력할 경우 검출된 원의 중심만 반환
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,15, param1=250, param2=10, minRadius=5, maxRadius=50)
print(circles)
print(circles.shape)
for i in circles[0]:
    cv2.circle(dst, (i[0],i[1]),(i[2]),(255,255,255),1)

cv2.imshow('src',src)
cv2.imshow('dst',dst)
cv2.waitKey()
cv2.destroyAllWindows()