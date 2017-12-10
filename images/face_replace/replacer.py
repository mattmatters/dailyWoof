"""Uses haar cascade classifier to find all faces and their general orientation"""
import os.path
import numpy
import cv2
from PIL import Image
from face_replace.face_types import FACE_TYPES
from face_replace.face import Face

class ReplaceFace:
    """Basically a wrapper around opencv"""

    def __init__(self, frontalFacePath, profileFacePath):
        if (os.path.isfile(frontalFacePath) == False
                and os.path.isfile(profileFacePath) == False):
            raise ValueError('haarCascade: the files specified do not exist.')

        self._frontalFacePath = frontalFacePath
        self._profileFacePath = profileFacePath

        self._frontalCascade = cv2.CascadeClassifier(frontalFacePath)
        self._profileCascade = cv2.CascadeClassifier(profileFacePath)

    ##
    # Find a face (frontal or profile) in the input image.
    # To find the right profile the input image is vertically flipped,
    # this is done because the training file for profile faces was
    # trained only on left profile.
    # @param inputImg the image where the cascade will be called
    # @param frontalScaleFactor=1.1
    # @param rotatedFrontalScaleFactor=1.1
    # @param leftScaleFactor=1.1
    # @param rightScaleFactor=1.1
    # @param minSizeX=30
    # @param minSizeX=30
    # @param rotationAngleCCW (positive) angle for rotated face detector
    # @param rotationAngleCW (negative) angle for rotated face detector
    #
    # Return code: 1=Frontal, 2=FrontRotLeft, 3=FronRotRight,
    #              4=ProfileLeft, 5=ProfileRight.
    def find_faces(self,
                   inputImg,
                   frontalScaleFactor=1.1,
                   rotatedFrontalScaleFactor=1.1,
                   leftScaleFactor=1.1,
                   rightScaleFactor=1.1,
                   minSizeX=30,
                   minSizeY=30,
                   rotationAngleCCW=30,
                   rotationAngleCW=-30):

        rows, cols = numpy.shape(inputImg)

        faces = []
        # Front
        front_faces = self._findFrontalFace(inputImg, frontalScaleFactor,
                                            minSizeX, minSizeY)

        faces += [Face(FACE_TYPES['FRONT'], x) for x in front_faces]

        # Rotated left
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotationAngleCCW,
                                    1)  #30 degrees ccw rotation
        inputImgRot = cv2.warpAffine(inputImg, M, (cols, rows))
        front_left = self._findFrontalFace(
            inputImgRot, rotatedFrontalScaleFactor, minSizeX, minSizeY)
        faces += [Face(FACE_TYPES['FRONT_LEFT'], x) for x in front_left]

        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotationAngleCW,
                                    1)  #30 degrees ccw rotation
        inputImgRot = cv2.warpAffine(inputImg, M, (cols, rows))
        front_right = self._findFrontalFace(
            inputImgRot, rotatedFrontalScaleFactor, minSizeX, minSizeY)
        faces += [Face(FACE_TYPES['FRONT_RIGHT'], x) for x in front_right]

        left = self._findProfileFace(inputImg, leftScaleFactor, minSizeX,
                                     minSizeY)
        faces += [Face(FACE_TYPES['LEFT'], x) for x in left]

        # flipped_inputImg = cv2.flip(inputImg, 1)
        # right = self._findProfileFace(flipped_inputImg, rightScaleFactor,
        #                               minSizeX, minSizeY)

        # Some weird logic for flipping faces
        # if (self.is_face_present == True):
        #             self.face_type = 5
        #             f_w, f_h = flipped_inputImg.shape[::
        #                                               -1]  #finding the max dimensions
        #             self.face_x = f_w - (
        #                 self.face_x + self.face_w
        #             )  #reshape the x to unfold the mirroring
        #             return (self.face_x, self.face_y, self.face_w, self.face_h)

        return faces

    def replace_faces(self, input_img_path, replace_img_path):
        img = cv2.imread(input_img_path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #Declaring the two classifiers
        # Looking for faces with cascade
        # The classifier moves over the ROI
        # starting from a minimum dimension and augmentig
        # slightly based on the scale factor parameter.
        # The scale factor for the frontal face is 1.10 (10%)
        # Scale factor: 1.15=15%,1.25=25% ...ecc
        # Higher scale factors means faster classification
        # but lower accuracy.
        faces = self.find_faces(
            gray_img,
            frontalScaleFactor=1.2,
            rotatedFrontalScaleFactor=1.1,
            leftScaleFactor=1.15,
            rightScaleFactor=1.15,
            minSizeX=80,
            minSizeY=80,
            rotationAngleCCW=30,
            rotationAngleCW=-30)

        if not len(faces):
            return Image.open(input_img_path).convert("RGBA")

        target_img = Image.open(input_img_path)
        target_img = target_img.convert("RGBA")
        replace_img = Image.open(replace_img_path)

        for face in faces:
            scaled_img = replace_img.resize((face.width, face.height))
            alpha_layer = Image.new("RGBA", target_img.size)
            alpha_layer.paste(scaled_img, (face.coord_x1, face.coord_y1), scaled_img)
            target_img = Image.alpha_composite(target_img, alpha_layer)

        return target_img

    def _findFrontalFace(self,
                         inputImg,
                         scaleFactor=1.1,
                         minSizeX=30,
                         minSizeY=30,
                         minNeighbors=4):

        #Cascade: frontal faces
        faces = self._frontalCascade.detectMultiScale(
            inputImg,
            scaleFactor=scaleFactor,
            minNeighbors=minNeighbors,
            minSize=(minSizeX, minSizeY),
            flags=cv2.cv2.CASCADE_SCALE_IMAGE)

        return faces

    def _findProfileFace(self,
                         inputImg,
                         scaleFactor=1.1,
                         minSizeX=30,
                         minSizeY=30,
                         minNeighbors=4):

        #Cascade: left profile
        faces = self._profileCascade.detectMultiScale(
            inputImg,
            scaleFactor=scaleFactor,
            minNeighbors=minNeighbors,
            minSize=(minSizeX, minSizeY),
            flags=cv2.cv2.CASCADE_SCALE_IMAGE)

        return faces
