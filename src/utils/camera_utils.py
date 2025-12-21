import cv2

class CameraHandler:
    def __init__(self, camera_id=0, width=640, height=480):
        # initiallizing camera
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if not self.cam.isOpened():
            print("Error: Could not open camera")
            raise Exception("Camera initialization failed")
        else:
            print(f"Camera initialized: {width}x{height}")

    def read_frame(self):
        # on running contineously displays camera feed until pressed 'q'
        if not self.cam.isOpened():
            print("error in opening camera")
        else:
            frame_capture_sucess,frame =  self.cam.read()
            if not frame_capture_sucess:
                print("issue in camera_utils capturing video frame")
                return False,None
            return True,frame

    def display_frame(self,frame,window_name="video feed"):
        cv2.imshow(window_name,frame)
        
    def release_camera(self,key_press_time=0):
        self.cam.release()
        cv2.waitKey(key_press_time)
        cv2.destroyAllWindows()
    def get_frame_dimensions(self):
      if not self.cam.isOpened():
        print("Error: Could not open video stream.")
        exit()
      frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
      frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))  
      return frame_width,frame_height



if __name__ == "__main__":
    cam = CameraHandler()
    while True:
        frames =cam.read_frames()
        cam.display_frame(frames)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release_camera()
            break