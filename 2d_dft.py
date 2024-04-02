# -*- coding: utf-8 -*-
"""2D_DFT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ALefglxPNrqU74pEpk9guH7a208lnGxx
"""

from google.colab import drive

drive.mount('/content/drive')

File = '/content/drive/MyDrive/Assignmnent/Knee.pgm'

import numpy as np
from scipy import fftpack
from PIL import Image  # Assuming you have Pillow (PIL Fork) installed

import numpy as np
from scipy import fftpack
from PIL import Image  # Assuming you have Pillow (PIL Fork) installed
  # Read the image
img = Image.open(File).convert('L')  # Convert to grayscale
f = np.asarray(img)
def dft_ideal_lowpass(f, D0, P, Q):
  """
  Calculates the DFT of an image and applies an ideal low-pass filter.

  Args:
      f: The input image as a 2D NumPy array.
      D0: The cutoff frequency for the ideal low-pass filter.
      P: The padded width (2M-1).
      Q: The padded height (2N-1).

  Returns:
      g: The filtered image (smoothed version of f).
      H: The ideal low-pass filter in the frequency domain.
  """



  # Zero-pad the original image
  f_pad = np.zeros((P, Q))
  M, N = f.shape
  f_pad[:M, :N] = f

  # Center the low frequency by multiplying by (-1)^(x+y)
  f_pad_centered = f_pad * (-1)**(np.arange(P)[:, np.newaxis] + np.arange(Q))

  # Calculate the 2D DFT (fast Fourier transform)
  F_uv = fftpack.fft2(f_pad_centered)

  # Define the ideal low-pass filter in the frequency domain
  u, v = np.meshgrid(np.arange(Q), np.arange(P))
  D_uv = np.sqrt((u - P//2)**2 + (v - Q//2)**2)  # Distance from center
  H_uv = np.zeros_like(F_uv)
  H_uv[D_uv <= D0] = 1  # Apply cutoff frequency

  # Apply the filter in the frequency domain
  G_uv = F_uv * H_uv

  # Perform the inverse 2D DFT (fast inverse Fourier transform)
  g = fftpack.ifft2(G_uv).real  # Take the real part

  return g, H_uv

# Example usage
P = 2 * f.shape[0] - 1
Q = 2 * f.shape[1] - 1
D01 = 0.2 * np.sqrt(P**2 + Q**2)  # Example cutoff frequency 1 (low)
D02 = 0.8 * np.sqrt(P**2 + Q**2)  # Example cutoff frequency 2 (high)

g1, H1 = dft_ideal_lowpass(f.copy(), D01, P, Q)
g2, H2 = dft_ideal_lowpass(f.copy(), D02, P, Q)

# Display or save the filtered images and filters (g1, g2, H1, H2)
# You can use libraries like matplotlib or OpenCV for visualization
# This example uses Pillow (PIL Fork) to save the filtered images
g1_img = Image.fromarray(g1.astype(np.uint8))  # Convert back to uint8 for image display
g2_img = Image.fromarray(g2.astype(np.uint8))
g1_img.save("filtered_low.jpg")
g2_img.save("filtered_high.jpg")