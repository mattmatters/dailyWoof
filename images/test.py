from face_replace.replacer import ReplaceFace

Replacer = ReplaceFace("./paths/haarcascade_frontalface_alt.xml",
                       "./paths/haarcascade_profileface.xml")

newIm = Replacer.replace_faces("./test_images/thing2.jpg", "./dmx-head.png")
newIm.save('./test_good/new.png')
newIm = Replacer.replace_faces("./test_images/thing3.jpg", "./dmx-head.png")
newIm.save('./test_good/new2.png')
newIm = Replacer.replace_faces("./test_images/thing4.jpg", "./dmx-head.png")
newIm.save('./test_good/new3.png')
newIm = Replacer.replace_faces("./test_images/thing5.jpg", "./dmx-head.png")
newIm.save('./test_good/new4.png')
newIm = Replacer.replace_faces("./test_images/thing6.jpg", "./dmx-head.png")
newIm.save('./test_good/new5.png')
