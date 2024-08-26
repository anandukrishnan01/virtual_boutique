from datetime import datetime
import os
from pathlib import Path
import cv2
import sys
import webbrowser


sys.path.insert(1, str(Path(__file__).resolve().parent.parent.parent/'virtual_butique/cmate'))
from cmate.cmate_main import CMate


def blend_images(profile_img, source_img, profile_dir, source_dir, dest_dir):
    print('Blending')
    ensure_directory_exists(dest_dir)
    
    # Ensure profile directory exists
    ensure_directory_exists(profile_dir)
    print("profilecmate",profile_img)
    print("sourcecmate",source_img)
    "apply cloth to profile image and save to result"
    # verify file exists
    if not (Path(profile_dir)/profile_img).exists():
        raise FileNotFoundError("Profile Image not found.")
        
    if not (Path(source_dir)/source_img).exists():
        raise FileNotFoundError("Source Image not found.")
    # apply cmate
    cloth_blender = CMate(str(Path(source_dir)/source_img),
                          str(Path(profile_dir)/profile_img))
    print("blend",source_img)
    print("blend ",profile_img)
    final_img, errors = cloth_blender.apply_cloth()
    filename = "result-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
    dest_path = Path(dest_dir) / filename
    print("final img cmate.py",final_img)
    print("final file cmate.py",filename)
    print("Destination path:", dest_path) 
    # cv2.imwrite(str(Path(dest_dir)/filename), final_img)
    # webbrowser.open(dest_path.as_uri())
    # Save the final image
    if cv2.imwrite(str(dest_path), final_img):
        print('Image saved successfully')
    else:
        print('Failed to save image')
        raise Exception('Failed to save image')

    # Return the relative path for the saved image
    return str(dest_path.relative_to('media')), errors

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)