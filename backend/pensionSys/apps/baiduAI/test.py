from faceDetection import get_face
from faceCompare import compare_face
from bodyCoordinate import get_body_coordinate
from bodyAttributes import get_body_attributes
img = 'C:/Users/56936/Pictures/Camera Roll/WIN_20190612_20_26_40_Pro.jpg'

print(get_face(img))

img1 = 'C:/Users/56936/Pictures/Camera Roll/WIN_20190612_20_26_40_Pro.jpg'
img2 = 'C:/Users/56936/Pictures/Camera Roll/WIN_20190612_20_27_22_Pro.jpg'

print(compare_face(img1,img2))

img = 'C:/Users/56936/Desktop/1.jpg'

print(get_body_coordinate(img))
print(get_body_attributes(img))