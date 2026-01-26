
import pyautogui
import time
import math

class MouseController:

    def __init__(self,screen_width=None, screen_height=None):
        if screen_width is None or screen_height is None:
            screen_width, screen_height = pyautogui.size()
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Initialize pyautogui settings
        # mouse failsafe allows moving mouse to corner to stop program
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01
        # smoothing prevents head jitter of cursor
        self.smooth_x = 0 
        self.smooth_y = 0
        self.smooth_factor = 0.5

        # prevengt accidental clicks
        self.last_click_time = 0
        self.click_delay = 0.3  # seconds

        # dragging state
        self.is_dragging = False
        print(f"MouseController initialized with screen size: {self.screen_width}x{self.screen_height}")

    def map_coordinates(self,x,y,frame_width, frame_height, padding=10, flip=True):
        # Args:
        #     x, y: Hand coordinates in camera frame
        #     frame_width, frame_height: Camera frame dimensions (640x480)
        #     padding: Pixels to ignore from frame edges (creates dead zone)
        #     flip: Flip X coordinate for natural mirror control
            
        # Returns:
        #     screen_x, screen_y: Mapped screen coordinates

        # apply padding (create dead zone)
        #as near edge  hand tracking becomes difficult
        effictive_frame_width = frame_width - 2 * padding
        effictive_frame_height = frame_height - 2 * padding

        adjusted__x = min(max(x - padding, 0), effictive_frame_width)
        adjusted__y = min(max(y - padding, 0), effictive_frame_height)
         # STEP 4: Flip X coordinate for mirror effect (optional but natural)
        # Without flip: Move hand right → cursor moves right
        # With flip: Move hand right → cursor moves left (like a mirror)
        if flip:
            adjusted__x = effictive_frame_width - adjusted__x
        # Mapping to screen coordinates
        mapped_x = (adjusted__x / effictive_frame_width) * self.screen_width
        mapped_y = (adjusted__y / effictive_frame_height) * self.screen_height

        # Apply smoothing for stable movement
        self.smooth_x = (self.smooth_x * self.smooth_factor + mapped_x) + (mapped_x * (1 - self.smooth_factor))
        self.smooth_y = (self.smooth_y * self.smooth_factor + mapped_y) + (mapped_y * (1 - self.smooth_factor))
        return int(self.smooth_x), int(self.smooth_y)
    
    def move_cursor(self, x, y):
        """
        Move mouse cursor to position
        
        What this does:
        - Moves cursor to specified screen coordinates
        - Has error handling in case something goes wrong
        
        Args:
            x, y: Screen coordinates (not camera coordinates!)
        """
        try:
            pyautogui.moveTo(x, y)
        except Exception as e:
            print(f"Error moving cursor: {e}")

    def can_click(self):
        # Prevent accidental rapid clicks
        current_time = time.time()
        if current_time - self.last_click_time >= self.click_delay:
            self.last_click_time = current_time
            return True
        return False

    def left_click(self):
        """Perform left mouse click if allowed by click delay"""
        if self.can_click():
            try:
                pyautogui.click(button='left')
                self.last_click_time = time.time()
                return True
            except Exception as e:
                print(f"Error performing left click: {e}")
        return False
    
    def right_click(self):
        """Perform right mouse click if allowed by click delay"""
        if self.can_click():
            try:
                pyautogui.click(button='right')
                self.last_click_time = time.time()
                return True
            except Exception as e:
                print(f"Error performing right click: {e}")
        return False
    
    def double_click(self):
        """Perform double mouse click if allowed by click delay"""
        if self.can_click():
            try:
                pyautogui.doubleClick()
                self.last_click_time = time.time()
                return True
            except Exception as e:
                print(f"Error performing double click: {e}")
        return False
    
    def start_drag(self):
        """Start mouse drag operation"""
        if not self.is_dragging:
            try:
                pyautogui.mouseDown()
                self.is_dragging = True
            except Exception as e:
                print(f"Error starting drag: {e}")
    def drag_end(self):
        """End mouse drag operation"""
        if self.is_dragging:
            try:
                pyautogui.mouseUp()
                self.is_dragging = False
            except Exception as e:
                print(f"Error ending drag: {e}")

    def scroll(self, clicks):
        """Scroll mouse wheel
        
        Args:
            clicks: Number of scroll clicks (positive=up, negative=down)
        """
        try:
            pyautogui.scroll(clicks)
        except Exception as e:
            print(f"Error scrolling: {e}")
    
    def set_smoothing(self, smoothing_factor):
        """Set smoothing factor for cursor movement
        
        Args:
            factor: Smoothing factor (0 to 1), higher = smoother
        """
        if 0 <= smoothing_factor <= 1:
            self.smooth_factor = smoothing_factor
        else:
            print("Smoothing factor must be between 0 and 1")

    def set_click_delay(self, delay):
        """
        Set minimum time between clicks
        
        Args:
            delay: Delay in seconds (minimum 0.1)
        """
        self.click_delay = max(0.1, delay)
        print(f"Click delay set to: {self.click_delay}s")


if __name__ == "__main__":
# ═══════════════════════════════════════════════════════════════
# TEST CODE
# ═══════════════════════════════════════════════════════════════

    print("\n" + "="*60)
    print("       MOUSE CONTROLLER TEST")
    print("="*60)
    print("\n📋 This will test mouse movement and clicks")
    print("   WARNING: Your cursor will move automatically!")
    print("   Move mouse to TOP-LEFT corner to emergency stop")
    print("\n   Starting in 3 seconds...\n")
    print("="*60 + "\n")
    
    try:
        # Give user time to read
        time.sleep(3)
        
        # Initialize controller
        print("🎯 Initializing mouse controller...")
        mouse = MouseController()
        
        print("\n✅ Mouse controller ready!")
        print("\n" + "-"*60)
        print("TEST 1: Coordinate Mapping")
        print("-"*60 + "\n")
        
        # Test coordinate mapping
        frame_width, frame_height = 640, 480
        
        test_positions = [
            (320, 240, "Center"),
            (100, 100, "Top-left"),
            (540, 100, "Top-right"),
            (100, 380, "Bottom-left"),
            (540, 380, "Bottom-right"),
        ]
        
        print("Testing coordinate conversion:")
        for cam_x, cam_y, position in test_positions:
            screen_x, screen_y = mouse.map_coordinates(
                cam_x, cam_y,
                frame_width, frame_height,
                padding=50
            )
            print(f"  {position:15} Camera({cam_x:3},{cam_y:3}) → Screen({screen_x:4},{screen_y:4})")
        
        print("\n" + "-"*60)
        print("TEST 2: Cursor Movement")
        print("-"*60 + "\n")
        
        # Get current position
        current_x, current_y = pyautogui.position()
        print(f"Current cursor position: ({current_x}, {current_y})")
        
        print("\nMoving cursor in square pattern in 2 seconds...")
        time.sleep(2)
        
        # Calculate square positions
        center_x = mouse.screen_width // 2
        center_y = mouse.screen_height // 2
        offset = 150
        
        square_positions = [
            (center_x - offset, center_y - offset, "Top-left"),
            (center_x + offset, center_y - offset, "Top-right"),
            (center_x + offset, center_y + offset, "Bottom-right"),
            (center_x - offset, center_y + offset, "Bottom-left"),
            (center_x, center_y, "Center"),
        ]
        
        for x, y, pos in square_positions:
            print(f"  Moving to {pos}...")
            mouse.move_cursor(x, y)
            time.sleep(0.8)
        
        print("\n✅ Movement test complete!")
        
        print("\n" + "-"*60)
        print("TEST 3: Mouse Clicks")
        print("-"*60 + "\n")
        
        print("Left click in 2 seconds...")
        time.sleep(2)
        
        if mouse.left_click():
            print("  ✅ Left click performed!")
        
        time.sleep(1)
        print("\nRight click in 2 seconds...")
        time.sleep(2)
        
        if mouse.right_click():
            print("  ✅ Right click performed!")
        
        print("\n" + "-"*60)
        print("TEST 4: Click Debouncing")
        print("-"*60 + "\n")
        
        print("Testing debouncing (trying to click 5 times rapidly):")
        for i in range(5):
            result = mouse.left_click()
            status = "✅ Clicked" if result else "⏸️  Blocked (too soon)"
            print(f"  Attempt {i+1}: {status}")
            time.sleep(0.1)  # Try every 0.1 seconds
        
        print("\n" + "="*60)
        print("       ALL TESTS COMPLETED!")
        print("="*60)
        print("\n✅ Mouse controller is working correctly!")
        print("\n" + "="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user (Ctrl+C)")
    except pyautogui.FailSafeException:
        print("\n\n⚠️  FAILSAFE triggered! (Mouse moved to corner)")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n✅ Test completed!\n")  
