import cv2
import numpy as np
import mss
import os

class TextureDetector:
    def __init__(self):
        self.screen_capture = mss.mss()
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'soil.jpg') # CASE SENSITIVE
        self.template = cv2.imread(template_path)
        
        if self.template is None:
            raise FileNotFoundError("Template image not found")
            
        self.template_color = np.mean(self.template, axis=(0,1))

    def run(self):
        while True:
            # Capture screen and convert to BGR
            screen = np.array(self.screen_capture.grab({'left': 0, 'top': 0, 'width': 1920, 'height': 1080}))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

            # Calculate color difference
            diff = np.abs(screen - self.template_color)
            mask = (np.mean(diff, axis=2) < 18).astype(np.uint8) * 255

            # Create a visualization image
            vis_image = screen.copy()
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find largest contour
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Create a black image same size as screen
                mask_vis = np.zeros_like(screen)
                
                # Only show mask pixels within the rectangle
                roi_mask = mask[y:y+h, x:x+w]
                mask_vis[y:y+h, x:x+w][roi_mask == 255] = [0, 255, 0]  # Green color for mask pixels
                
                # Blend the mask visualization with the original image
                alpha = 0.5
                vis_image = cv2.addWeighted(vis_image, 1, mask_vis, alpha, 0)
                
                # Draw rectangle and center point
                cv2.rectangle(vis_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center_x, center_y = x + w//2, y + h//2
                cv2.circle(vis_image, (center_x, center_y), 5, (0, 0, 255), -1)
                print(f"Center: ({center_x}, {center_y})")

            # Show both the mask and the original image with overlay
            cv2.imshow('Detection', vis_image)
            cv2.imshow('Mask', mask)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

TextureDetector().run()
