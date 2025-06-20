import cv2
import numpy as np
import random

def create_cad_base(width=800, height=600):
    """Create a blank CAD-style canvas with grid background"""
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Add grid background
    for i in range(0, width, 20):
        cv2.line(img, (i, 0), (i, height), (220, 220, 220), 1)
    for j in range(0, height, 20):
        cv2.line(img, (0, j), (width, j), (220, 220, 220), 1)
    
    # Add title block
    cv2.rectangle(img, (width-200, height-50), (width-10, height-10), (200, 200, 255), -1)
    cv2.putText(img, "ENG-001", (width-180, height-25), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    return img

def add_cad_features(img):
    """Add complex CAD features to image"""
    # Main components
    cv2.rectangle(img, (100, 100), (300, 300), (0, 0, 0), 2)
    cv2.circle(img, (500, 200), 80, (0, 0, 0), 2)
    
    # Internal features
    cv2.rectangle(img, (120, 120), (180, 180), (0, 0, 255), 2)  # Red component
    cv2.circle(img, (500, 200), 30, (0, 0, 0), 2)  # Inner circle
    
    # Mechanical elements
    cv2.line(img, (300, 200), (420, 200), (0, 0, 0), 3)  # Connecting shaft
    cv2.ellipse(img, (420, 200), (40, 20), 30, 0, 360, (0, 0, 0), 2)  # Flange
    
    # Dimension lines
    cv2.line(img, (100, 320), (300, 320), (0, 150, 0), 1)  # Horizontal dim
    cv2.line(img, (100, 310), (100, 330), (0, 150, 0), 1)
    cv2.line(img, (300, 310), (300, 330), (0, 150, 0), 1)
    cv2.putText(img, "200.00", (180, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0), 1)
    
    return img

def modify_cad_features(img):
    """Apply diverse modifications to CAD image"""
    # Change dimensions
    cv2.rectangle(img, (100, 100), (320, 300), (0, 0, 0), 2)  # Wider rectangle
    
    # Add new feature
    cv2.circle(img, (600, 400), 50, (0, 0, 255), 2)  # New red circle
    
    # Modify existing feature
    cv2.ellipse(img, (420, 200), (50, 30), 30, 0, 360, (255, 0, 0), 2)  # Blue modified flange
    
    # Remove feature (by covering with background)
    cv2.rectangle(img, (115, 115), (185, 185), (255, 255, 255), -1)
    
    # Change dimension value
    cv2.rectangle(img, (180, 335), (240, 355), (255, 255, 255), -1)
    cv2.putText(img, "220.00", (180, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0), 1)
    
    # Add cross-section indicator
    cv2.line(img, (500, 280), (550, 330), (0, 100, 255), 2)
    cv2.line(img, (550, 280), (500, 330), (0, 100, 255), 2)
    
    return img

def generate_cad_pair(output_prefix="cad_drawing"):
    """Generate original and modified CAD image pair"""
    # Create base images
    original = create_cad_base()
    modified = original.copy()
    
    # Add features
    original = add_cad_features(original)
    modified = add_cad_features(modified)
    
    # Apply modifications only to modified image
    modified = modify_cad_features(modified)
    
    # Save images
    cv2.imwrite(f"{output_prefix}_original.png", original)
    cv2.imwrite(f"{output_prefix}_modified.png", modified)
    print(f"Generated: {output_prefix}_original.png and {output_prefix}_modified.png")
    return original, modified

if __name__ == "__main__":
    # Generate 3 different complexity levels
    for i in range(1, 4):
        generate_cad_pair(f"complex_cad_{i}")
