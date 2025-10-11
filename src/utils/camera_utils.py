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
            frame_capture_sucess,frame =  self.cam.read()
            if not frame_capture_sucess:
                print("issue in camera_utils capturing video frame")
                return None          
            if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' to quit
                self.release_camera()
                return "quit"
            return frame

    def display_frame(self,frame,window_name="video feed"):
        cv2.imshow(window_name,frame)
        
    def release_camera(self,key_press_time=0):
        self.cam.release()
        cv2.waitKey(key_press_time)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    cam = CameraHandler()
    cam.read_frames()