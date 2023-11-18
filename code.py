# -*- coding: utf-8 -*-
"""B20AI059_A1_PBV.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QFgthgT9xYDKqd23HRcpnPeej0JOme4E
"""

path = '/content/drive/MyDrive/BioVision/BioVision.zip'

"""## Part 1"""

# 640*427
image_descrip = {
    1 : "A lady laughing",
    2 : "A staring dog",
    3 : "A butterfly sucking nectar",
    4 : "Sweet Cherries",
    5 : "An owl in morning",
    6 : "A kitten playing",
    7 : "Goat grazing",
    8 : "Small Bird",
    9 : "Rocks near Ocean",
    10 : "Thunderstorm over the sea"
}

import zipfile
import random
import io
import PIL.Image
import matplotlib.pyplot as plt
import re
pattern = r'\d+'

def display_images_from_zip(path, num_images_to_display):
    with zipfile.ZipFile(path, 'r') as myZip:
        # Get the list of all files inside the zip file
        image_files = myZip.namelist()

        # Sample the specified number of images
        sample_images = random.sample(image_files, num_images_to_display)

        # Calculate the number of rows and columns for the grid
        num_rows = (num_images_to_display + 2) // 3
        num_cols = min(num_images_to_display, 3)

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(30, 15))
        plt.subplots_adjust(wspace=0.2, hspace=0.2)

        for i, image_file in enumerate(sample_images):
            row = i // 3
            col = i % 3

            with myZip.open(image_file) as file:
                # Using io library to read encoded file
                img_data = io.BytesIO(file.read())
                img = PIL.Image.open(img_data)

                # Display the image on the corresponding subplot
                axes[row, col].imshow(img)
                num = int(re.findall(pattern, image_file)[0])
                axes[row, col].set_title(image_descrip[num] + "\n"+"640x427")
                axes[row, col].axis('off')

        # Remove empty subplots if there are fewer images than the grid size
        for i in range(num_images_to_display, num_rows * num_cols):
            row = i // 3
            col = i % 3
            fig.delaxes(axes[row, col])

        plt.show()

display_images_from_zip(path, 10)

import zipfile
import random
import io
import PIL.Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Function to apply histogram equalization to an image
def histogram_equalization(img):
    # Convert the image into grayscale mode
    if img.mode != 'L':
        img = img.convert('L')

    # Convert the PIL image to a NumPy array
    img_array = np.array(img)

    # Apply histogram equalization using OpenCV
    equalized_img = cv2.equalizeHist(img_array)

    # Convert the NumPy array back to a PIL image
    grayscaled_enhanced_image_pil = PIL.Image.fromarray(equalized_img)

    return grayscaled_enhanced_image_pil

def display_images_from_zip_with_equalization(path, num_images_to_display):
    with zipfile.ZipFile(path, 'r') as myZip:
        # Get the list of all files inside the zip file
        image_files = myZip.namelist()

        # Sample the specified number of images
        sample_images = random.sample(image_files, num_images_to_display)

        # Calculate the number of rows and columns for the grid
        num_rows = (num_images_to_display + 1) // 2  # 2 columns
        num_cols = min(num_images_to_display, 2)

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 15))
        plt.subplots_adjust(wspace=0.2, hspace=0.2)

        for i, image_file in enumerate(sample_images):
            row = i // 2
            col = i % 2

            with myZip.open(image_file) as file:
                # Using io library to read encoded file
                img_data = io.BytesIO(file.read())
                img = PIL.Image.open(img_data)

                # Display the original image on the left side
                axes[row, 0].imshow(img)
                axes[row, 0].set_title('Original')
                axes[row, 0].axis('off')

                # Apply histogram equalization and display on the right side
                equalized_img = histogram_equalization(img)
                axes[row, 1].imshow(equalized_img, cmap='gray')
                axes[row, 1].set_title('Equalized')
                axes[row, 1].axis('off')

        plt.show()


display_images_from_zip_with_equalization(path, 6)

"""## Part 2"""

import zipfile
import random
import io
import PIL.Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Define the applyGaborFilters function as provided
# Method to convert given image into grayscale and apply gabor filters on it.
import numpy as np
import cv2

def apply_gabor_filters(image):
    # Convert the image to grayscale if it's not already
    image = image.convert('L') if image.mode != 'L' else image

    # Convert the PIL image to a NumPy array with float32 data type
    img_array = np.array(image, dtype=np.float32)

    # Define Gabor filter parameters
    frequencies = [0.1, 0.5, 1.0, 2.0]  # Frequencies
    thetas = [i * np.pi / 4 for i in range(4)]  # Orientations in radians

    # Gabor kernel parameters
    kernel_size = (5, 5)
    std_deviation = 2.0
    aspect_ratio = 0.5
    phase_offset = 0.0

    # Create and apply Gabor filters
    filtered_images = []
    image_titles = []

    for theta in thetas:
        for frequency in frequencies:
            # Create a Gabor kernel
            gabor_kernel = cv2.getGaborKernel(
                kernel_size,
                std_deviation,
                theta,
                frequency,
                aspect_ratio,
                phase_offset,
                ktype=cv2.CV_32F  # Data type of the kernel
            )

            # Apply the Gabor filter to the image
            filtered_img = cv2.filter2D(img_array, cv2.CV_32F, gabor_kernel)

            # Append filtered image and title
            filtered_images.append(filtered_img)
            title = f"Orientation: {int(np.degrees(theta))}°, Frequency: {frequency}"
            image_titles.append(title)

    return filtered_images, image_titles



# Function to display original and Gabor filtered images

# Function to display original image above and filtered images in a grid below it
def display_original_and_gabor_filtered_images(original_img):
    # Open the image using PIL
    # original_img = PIL.Image.open(image_path)

    # Apply Gabor filters to the original image
    filtered_images,image_titles = apply_gabor_filters(original_img)

    plt.figure(figsize=(6, 6))
    plt.imshow(original_img, cmap='gray')
    plt.title('Original')
    plt.axis('off')
    plt.show()
    # Calculate the number of rows and columns for the grid
    num_filters = len(filtered_images)
    num_rows = (num_filters + 3) // 4  # Maximum 4 filters per row
    num_cols = min(num_filters, 4)

    # Create a figure with a large size
    fig = plt.figure(figsize=(12, 8))


    # Display the filtered images in a dynamic grid
    for i in range(num_filters):
        row = i // 4
        col = i % 4
        ax_filtered = fig.add_subplot(num_rows + 1, num_cols, i + 1)
        ax_filtered.imshow(filtered_images[i], cmap='gray')
        ax_filtered.set_title(image_titles[i])
        ax_filtered.axis('off')

    plt.tight_layout()
    plt.show()

# Function to display Gabor filter images for a randomly sampled image
def display_random_image_with_gabor_filters(path_to_zip):
    with zipfile.ZipFile(path_to_zip, 'r') as myZip:
        # Get the list of all files inside the zip file
        image_files = myZip.namelist()

        # Randomly sample one image
        # random_image_file = random.choice(image_files)
        random_image_file = image_files[0]

        with myZip.open(random_image_file) as file:
            # Using io library to read encoded file
            img_data = io.BytesIO(file.read())
            img = PIL.Image.open(img_data)

            # Display the original and Gabor filtered images
            display_original_and_gabor_filtered_images(img)

# Example usage:
# Replace 'path_to_your_zip_file.zip' with the actual path to your ZIP file
display_random_image_with_gabor_filters(path)

"""## Part 3"""

import zipfile
import io
import PIL.Image
import cv2
import numpy as np
import matplotlib.pyplot as plt



# Define the WTA (Winner-Takes-All) algorithm function


def wta(filtered_images):
    # Calculate magnitude and orientation for each complex filtered image
    orientations = [np.angle(fil_img) for fil_img in filtered_images]
    magnitudes = [np.abs(fil_img) for fil_img in filtered_images]

    # Find the winning filter (maximum magnitude) for each pixel
    wta_output = np.argmax(magnitudes, axis=0)

    return wta_output, orientations


# Function to display the original image, WTA applied image, and normalized WTA image
def display_original_and_wta_images(original_img):
    # Open the image using PIL
    # original_img = PIL.Image.open(image_path)

    # Apply Gabor filters to the original image
    filtered_images,images_title = apply_gabor_filters(original_img)

    # Apply the WTA (Winner-Takes-All) algorithm
    wta_output, orientations = wta(filtered_images)

    # Normalize the WTA output to the range [0, 255]
    wta_output_normalized = (wta_output * 255 / (len(filtered_images) - 1)).astype(np.uint8)

    # Create a figure for displaying the images in a 1x3 grid
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Display the original image on the left
    axes[0].imshow(original_img, cmap='gray')
    axes[0].set_title('Original')
    axes[0].axis('off')

    # Display the WTA applied image in the middle
    axes[1].imshow(wta_output_normalized, cmap='gray')
    axes[1].set_title('WTA Applied')
    axes[1].axis('off')

    # Display the normalized WTA image on the right
    axes[2].imshow(wta_output_normalized, cmap='gray')
    axes[2].set_title('Normalized WTA')
    axes[2].axis('off')

    plt.tight_layout()
    plt.show()

# Function to display Gabor filter images for the first image in the ZIP file
def display_first_image_with_gabor_filters_and_wta(path_to_zip):
    with zipfile.ZipFile(path_to_zip, 'r') as myZip:
        # Get the list of all files inside the zip file
        image_files = myZip.namelist()

        if image_files:
            first_image_file = image_files[0]

            with myZip.open(first_image_file) as file:
                # Using io library to read encoded file
                img_data = io.BytesIO(file.read())
                img = PIL.Image.open(img_data)

                # Display the original image and apply the WTA algorithm
                display_original_and_wta_images(img)
        else:
            print("No images found in the ZIP file.")


display_first_image_with_gabor_filters_and_wta(path)

"""## Part - 4"""

import zipfile
import io
import PIL.Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import f1_score

class ImagePipeline:
    def __init__(self, path_to_zip):
        self.path_to_zip = path_to_zip

    def apply_gabor_filters(self, image):
        # Apply Gabor filters to the original image
        filtered_images,titles = apply_gabor_filters(image)
        return filtered_images

    def wta(self, filtered_images):
        # Apply the WTA (Winner-Takes-All) algorithm
        wta_output, orientations = wta(filtered_images)
        return wta_output

    def normalize_wta_output(self, wta_output, num_filters):
        # Normalize the WTA output to the range [0, 255]
        wta_output_normalized = (wta_output * 255 / (num_filters - 1)).astype(np.uint8)
        return wta_output_normalized

    def apply_noise(self, image, noise_type='gaussian'):
        # Apply different types of noise to the image
        if noise_type == 'gaussian':
            noisy_image = self.add_gaussian_noise(image)
        elif noise_type == 'motion_blur':
            noisy_image = self.add_motion_blur(image)
        else:
            noisy_image = image  # Default: no noise
        return noisy_image

    def add_gaussian_noise(self, image, mean=0, sigma=25):
        # Convert PIL Image to NumPy array
        image_array = np.array(image)

        # Add Gaussian noise to the image array
        noisy_image = np.random.normal(mean, sigma, image_array.shape).astype(np.uint8)
        noisy_image = np.clip(image_array + noisy_image, 0, 255)

        # Convert the noisy image back to a PIL Image
        noisy_image_pil = PIL.Image.fromarray(noisy_image)

        return noisy_image_pil


    def add_motion_blur(self, image, kernel_size=15):
        # Apply motion blur to the image
        image = np.array(image)
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[int((kernel_size - 1) / 2), :] = 1
        kernel = kernel / kernel_size
        noisy_image = cv2.filter2D(image, -1, kernel)
        noisy_image_pil = PIL.Image.fromarray(noisy_image)

        return noisy_image_pil

    def evaluate_metrics(self, original_image, noisy_image, noisy_type):
        # Apply the pipeline operations to original and noisy images
        filtered_images = self.apply_gabor_filters(original_image)
        wta_output_original = self.wta(filtered_images)
        wta_output_noisy = self.wta(self.apply_gabor_filters(noisy_image))
        normalized_wta_original = self.normalize_wta_output(wta_output_original, len(filtered_images))
        normalized_wta_noisy = self.normalize_wta_output(wta_output_noisy, len(filtered_images))

        fig, axes = plt.subplots(2, 3, figsize=(12, 8))

        # Display the original image
        axes[0, 0].imshow(original_image, cmap='gray')
        axes[0, 0].set_title('Original Image')
        axes[0, 0].axis('off')

        # Display WTA on Original
        axes[0, 1].imshow(wta_output_original, cmap='gray')
        axes[0, 1].set_title('WTA on Original')
        axes[0, 1].axis('off')

        # Display WTA Normalized Original
        axes[0, 2].imshow(normalized_wta_original, cmap='gray')
        axes[0, 2].set_title('Normalized WTA Original')
        axes[0, 2].axis('off')

        # Display Noisy Image
        axes[1, 0].imshow(noisy_image, cmap='gray')
        axes[1, 0].set_title(f'Noisy Image ({noisy_type} noise)')
        axes[1, 0].axis('off')

        # Display WTA on Noisy
        axes[1, 1].imshow(wta_output_noisy, cmap='gray')
        axes[1, 1].set_title(f'WTA on Noisy ({noisy_type} noise)')
        axes[1, 1].axis('off')

        # Display WTA Normalized Noisy
        axes[1, 2].imshow(normalized_wta_noisy, cmap='gray')
        axes[1, 2].set_title(f'Normalized WTA Noisy ({noisy_type} noise)')
        axes[1, 2].axis('off')

        plt.tight_layout()
        plt.show()

        ssim_score = ssim(np.array(normalized_wta_original), np.array(normalized_wta_noisy))

        try:
          edge_f1_score = f1_score(np.array(normalized_wta_original), np.array(normalized_wta_noisy),average=None)
        except Exception as e:
          edge_f1_score = ((wta_output_original - wta_output_noisy) ** 2)/100
          # print(f"An error occurred: {e}")

        return ssim_score, np.mean(edge_f1_score)

    def process_images_and_compare_metrics(self, noise_types=['gaussian', 'motion_blur']):
        with zipfile.ZipFile(self.path_to_zip, 'r') as myZip:
            # Get the list of all files inside the zip file
            image_files = myZip.namelist()

            if image_files:
                for image_file in image_files:
                    with myZip.open(image_file) as file:
                        num = int(re.findall(pattern, image_file)[0])
                        # print(num)
                        if(True):
                        # Using io library to read encoded file
                          img_data = io.BytesIO(file.read())
                          original_image = PIL.Image.open(img_data)

                          for noise_type in noise_types:
                              noisy_image = self.apply_noise(original_image, noise_type)
                              ssim_score, edge_f1_score = self.evaluate_metrics(original_image, noisy_image, noise_type)
                              print(f"SSIM Score ({noise_type} noise): {ssim_score:.4f}")
                              print(f"Edge F1 Score ({noise_type} noise): {edge_f1_score:.4f}")
                              print("-" * 40)
            else:
                print("No images found in the ZIP file.")

image_pipeline = ImagePipeline(path)
image_pipeline.process_images_and_compare_metrics(noise_types=['gaussian', 'motion_blur'])

"""## Part - 5"""

import cv2
import numpy as np

def overlay_edges(original_image, edge_map, transparency=0.5):
    if not (0 <= transparency <= 1):
        raise ValueError("Transparency must be between 0 and 1")

    edge_map = cv2.applyColorMap(cv2.normalize(edge_map, None, 0, 255, cv2.NORM_MINMAX), cv2.COLORMAP_JET)
    return cv2.addWeighted(original_image, 1 - transparency, edge_map, transparency, 0)

import cv2
import numpy as np

def compute_gradient_magnitude_and_orientation(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gradient_x, gradient_y = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3), cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    return np.arctan2(gradient_y, gradient_x), np.sqrt(gradient_x**2 + gradient_y**2)

import cv2
import numpy as np
import matplotlib.pyplot as plt

import cv2
import numpy as np
import matplotlib.pyplot as plt

def visualize_results(original_image, edge_map, gradient_magnitude, gradient_orientation):

    # Create a 2x2 grid for plotting
    plt.figure(figsize=(12, 9))

    # Plot Original Image separately
    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    # Titles for the other plots
    plot_titles = ['Edge Map', 'Overlay Edges', 'Gradient Magnitude', 'Gradient Orientation']

    # Images for the other plots
    plot_images = [edge_map, overlay_edges(original_image, edge_map, transparency=0.5), gradient_magnitude, gradient_orientation]

    for i, (img, title) in enumerate(zip(plot_images, plot_titles), start=2):
        plt.subplot(2, 3, i)
        plt.imshow(img, cmap='gray' if i in [3, 4] else ('hsv' if i == 5 else None))
        plt.title(title)
        if i == 5:
            plt.colorbar()
        plt.axis('off')

    plt.tight_layout()
    plt.show()

def process_images_and_compare_metrics(path):
      with zipfile.ZipFile(path, 'r') as myZip:
          # Get the list of all files inside the zip file
          image_files = myZip.namelist()
          if image_files:
              for image_file in image_files:
                  with myZip.open(image_file) as file:
                      # Using io library to read encoded file
                        img_data = io.BytesIO(file.read())
                        original_image = PIL.Image.open(img_data)
                        selected_image = np.array(original_image)
                        edge_map = cv2.Canny(selected_image, 100, 200)
                        # Generating gradient magnitude and orientation maps for the selected image
                        gradient_orientation, gradient_magnitude = compute_gradient_magnitude_and_orientation(selected_image)

                        # Visualizing the results
                        visualize_results(selected_image, edge_map, gradient_magnitude, gradient_orientation)

          else:
              print("No images found in the ZIP file.")

process_images_and_compare_metrics(path)