import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def detect_esca_spots(image):
    # Convert the image to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for the color of esca spots
    lower_red_brown1 = np.array([0, 50, 50])  # Lower bound for red/brown spots
    upper_red_brown1 = np.array([10, 255, 255])  # Upper bound for red/brown spots

    lower_red_brown2 = np.array([160, 50, 50])  # Another lower bound for red/brown spots
    upper_red_brown2 = np.array([180, 255, 255])  # Another upper bound for red/brown spots

    lower_light_brown = np.array([10, 30, 30])  # Lower bound for light brown spots
    upper_light_brown = np.array([20, 255, 200])  # Upper bound for light brown spots

    # Create masks for the esca spots
    mask1 = cv2.inRange(hsv, lower_red_brown1, upper_red_brown1)
    mask2 = cv2.inRange(hsv, lower_red_brown2, upper_red_brown2)
    mask3 = cv2.inRange(hsv, lower_light_brown, upper_light_brown)

    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.bitwise_or(mask, mask3)

    # Optionally refine the mask (e.g., removing small noise, filling holes)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask

def process_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Processing images in directory: {input_dir}")

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, filename)
            print(f"Processing image: {image_path}")

            image = cv2.imread(image_path)
            if image is None:
                print(f"Error reading image: {image_path}")
                continue

            mask = detect_esca_spots(image)

            # Exclude the background using a different color range or other methods
            # Assuming the leaf is green and the background is not
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])

            leaf_mask = cv2.inRange(hsv, lower_green, upper_green)
            mask = cv2.bitwise_and(mask, mask, mask=cv2.bitwise_not(leaf_mask))

            # Construct the output filename
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_mask.jpg"
            output_path = os.path.join(output_dir, output_filename)

            # Save the mask
            if np.count_nonzero(mask) > 0:  # Check if the mask is not empty
                cv2.imwrite(output_path, mask)
                print(f"Saved mask to: {output_path}")

                # # Display the original image and the mask for debugging
                # plt.figure(figsize=(10, 5))
                # plt.subplot(1, 2, 1)
                # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                # plt.title('Original Image')
                # plt.axis('off')

                # plt.subplot(1, 2, 2)
                # plt.imshow(mask, cmap='gray')
                # plt.title('Esca Mask')
                # plt.axis('off')

                # plt.show()
            else:
                print(f"No esca spots detected in image: {image_path}")

input_directory = '/Users/michaelrodden/Desktop/ESCA_images/grapeleaf_images/test/esca'
output_directory = '/Users/michaelrodden/Desktop/ESCA_images/grapeleaf_images/ground_truth'
process_images(input_directory, output_directory)
