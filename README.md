# CM_assignment2

---
## Introduction

This toolkit provides functionalities for audio restoration, specifically focusing on the removal of clicks from degraded audio signals. Two main methods are implemented: median filter and Cubic Splines Filter. The toolkit allows users to replace detected clicks in audio signals with either the median value of neighboring samples or a cubic spline interpolation.

---
## Requirements

- Python 3.x
- NumPy
- tqdm
- SciPy
- Matplotlib

---
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Mio-ms/CM_assignment2.git
    ```

2. Install dependencies:

    ```bash
    pip install numpy tqdm scipy matplotlib
    ```

---
## Usage

### 1. Data Preparation

Before using the toolkit, make sure you have the degraded audio file (`degraded.wav`), the clean audio file (`clean.wav`), and a file containing positions of clicks (`detectionfile.npy`). Ensure that the file paths are correctly specified in the `readData` function.

### 2. Running the Toolkit

In the main script (`assignment2.py`), adjust the `path`, `windowLength`, and other parameters as needed. Then, execute the script:

```bash
python assignment2.py
```

---
## Methodology and Results

**Methodology**

### `findMedian(list)`

Calculates the median of a list of numeric values.

### `readData(path)`

Reads degraded and clean audio data along with anomaly positions from the specified path.

### `medianReplace(audioData, position, windowLength)`

Replaces clicks in the audio data with the median value within a specified window.

### `cubicSpline(audioData, position, windowLength)`

Applies cubic spline interpolation to restore clicks in the audio data.

### `MSE(audioData, restoreData, position)`

Calculates the Mean Squared Error (MSE) between the clean and restored audio signals.


**Results**

1. For the median filter, I experimented with different lengths to assess the restoration effectiveness. Specifically, I tested [3, 71], and it was observed that in the figure below, 
* Median filter: When the MSE is minimized, the window length is set to 3.
* Cubic splines filter: When the MSE is minimized, the window length is set to 5.

<img src="mse compare.png" width="700">

2. The figure below depicts a comparison of audio signals, including clicks audio, across various restoration methods and the original audio.

<img src="Comparison of Different Audio Signals.png" width="700">

After listening to the two restored files, I found that there is hardly any difference between them.


---
## Credits

This code was developed for purely academic purposes by Minshuai Jiang as part of the module Computational Methods.

Resources:
- Hwang, H., & Haddad, R. A. (1995). Adaptive median filters: new algorithms and results. IEEE Transactions on image processing, 4(4), 499-502.
- McKinley, S., & Levine, M. (1998). Cubic spline interpolation. College of the Redwoods, 45(1), 1049-1060.