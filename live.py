from src.capture   import Capture
from src.display   import Display
from src.transform import Transform
from src.label     import Label
from src.detect    import Detect
from src.encode    import Encode


detect = Detect()
encode = Encode()
label = Label()
trans = Transform()

refs, ref_map = encode.images()

with Display() as display, Capture() as capture:
    while display.key() != 'q':
        image = capture.frame()
        label.set_image(image)
        small = trans.scale_image(image)
        locs, encs = detect.all(small)
        for i in range(len(encs)):
            lbl = False
            enc = encs[i]
            loc = locs[i]
            cmps = detect.compare(refs, enc)
            for j in range(len(cmps)):
                if cmps[j]:
                    lbl = ref_map[j]
            if lbl:
                loc = trans.scale_location(loc)
                label.set_location(loc).outline().header(lbl)
        image = label.get_image()
        display.show(image)
                
