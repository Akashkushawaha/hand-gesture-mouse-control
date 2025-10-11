import cv2

class CameraHandler:
    def __init__(self, camera_id=0, width=640, height=480):
        # initiallizing camera
        self.cam = cv2.VideoCapture(0)

    def read_frames (self):
        # on running contineously displays camera feed until pressed 'q'
        if not self.cam.isOpened():
            print("error in opening camera")
        else:
            loop_switch =True
            while loop_switch:
                frame_capture_sucess,frame =  self.cam.read()
                if not frame_capture_sucess:
                    print("issue in camera_utils capturing video frame")
                    loop_switch =False
                cv2.imshow('Video Feed', frame)                 
                if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' to quit
                   self.release_camera()
                   break
    def release_camera(self,key_press_time=0):
        self.cam.release()
        cv2.waitKey(key_press_time)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    cam = CameraHandler()
    cam.read_frames()