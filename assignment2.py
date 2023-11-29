import time
import numpy as np
import unittest
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.io.wavfile import write
from scipy.interpolate import CubicSpline
from tqdm import tqdm


def findMedian(list):
    """Calculate the median of a list of numeric values.

    Args:
        list (list): A list of numeric values.

    Returns:
        list: The median of the input list. If the list has an odd
        number of elements, the middle element is returned. If the list has an
        even number of elements, the average of the two middle elements is returned.
    """
    listCopy = np.copy(list)
    listLength = len(list)
    listCopy.sort()
    if listLength % 2 == 0:
        middlePosition = listLength // 2
        median = (listCopy[middlePosition] + listCopy[middlePosition - 1]) / 2
    else:
        middlePosition = listLength // 2
        median = listCopy[middlePosition]
    return median


def readData(path):
    """Reads degraded and clean audio data along with clicks positions from the specified path.

    Args:
        path (str): The path to the directory containing audio files and detection file.

    Returns:
        tuple: A tuple containing the following elements:
            - samplerate (int): The sampling rate of the audio data.
            - audioData (numpy.ndarray): The degraded audio data.
            - audioClean (numpy.ndarray): The clean audio data.
            - position (numpy.ndarray): An array of clicks positions.
    """
    samplerate, audioData = wav.read(path + "/degraded.wav")
    samplerate, audioClean = wav.read(path + "/clean.wav")
    position = np.load(path + "/detectionfile.npy")
    return samplerate, audioData, audioClean, position


def medianReplace(audioData, position, windowLength):
    """Replaces clicks in the audio data with the median value within a specified window.

    Args:
        audioData (numpy.ndarray): The input audio data.
        position (numpy.ndarray): An array of clicks positions.
        windowLength (int): The length of the window used for median replacement. It should be an odd value.

    Returns:
        numpy.ndarray or None: If windowLength is odd, returns a new array with clicks replaced by the median value within the window.
        If windowLength is even, prints a message and returns None.
    """
    if windowLength % 2 == 0:
        print("Please input a odd value.")
        return None
    else:
        audioCopy = np.copy(audioData)
        start_time = time.time()  # Record start time
        for i in tqdm(range(len(position))):
            padding = (windowLength - 1) / 2
            processData = audioCopy[(
                position[i] - int(padding)): (position[i] + int(padding) + 1)]
            medianData = findMedian(processData)
            audioCopy[position[i]] = medianData
        end_time = time.time()  # Record end time
        runtime = end_time - start_time
        print(f"Median Filter Runtime: {runtime} seconds")
        print("Done")
        return audioCopy


def MSE(audioData, restoreData, position):
    """Calculates the Mean Squared Error (MSE) between the clean and restored audio signals.

    Args:
        audioData (numpy.ndarray): The clean audio data.
        restoreData (numpy.ndarray): The restored audio data.
        position (numpy.ndarray): An array of positions corresponding to clicks.

    Returns:
        float: The calculated Mean Squared Error (MSE) between the clean and restored audio signals.
            The values in audioData and restoreData should be normalized to the range [-1, 1].
            If no restore data is provided, a message is printed, and None is returned.
    """
    try:
        mse = np.square(audioData[position] / 32768 -
                        restoreData[position] / 32768).mean()
        return mse
    except:
        print('No restore data are input.')


def cubicSpline(audioData, position, windowLength):
    """Applies cubic spline interpolation to restore clicks in the audio data.

    Args:
        audioData (numpy.ndarray): The input audio data.
        position (numpy.ndarray): An array of clicks positions.
        windowLength (int): The length of the window used for cubic spline interpolation. It should be an odd value.

    Returns:
        numpy.ndarray or None: If windowLength is odd, returns a new array with clicks restored using cubic spline interpolation.
        If windowLength is even, prints a message and returns None.
    """
    if windowLength % 2 == 0:
        print("Please input a odd value.")
        return None
    else:
        audioCopy = np.copy(audioData)
        start_time = time.time()  # Record start time
        for i in range(len(position)):
            padding = (windowLength - 1) / 2
            index = [(position[i] - int(padding)),
                     (position[i] + int(padding))]
            x = np.linspace(index[0], index[1], windowLength)
            cubicSplineX = np.delete(x, int(padding))
            cubicSplineY = np.delete(
                audioCopy[index[0]: index[1] + 1], int(padding))
            cs = CubicSpline(cubicSplineX, cubicSplineY)
            xInterp = np.linspace(index[0], index[1], 101)
            yInterp = cs(xInterp)
            audioCopy[position[i]] = yInterp[55]
        end_time = time.time()  # Record end time
        runtime = end_time - start_time
        print(f"Cubic Spline Runtime: {runtime} seconds")
        return audioCopy


def plotAudioSignals(audioData, medianRestoreData, cubicRestoreData, audioClean):
    """Plots four audio signals in a 2x2 subplot arrangement.

    Args:
        audioData (numpy.ndarray): The original audio data.
        medianRestoreData (numpy.ndarray): The audio data after median restoration.
        cubicRestoreData (numpy.ndarray): The audio data after cubic spline restoration.
        audioClean (numpy.ndarray): The original clean audio data.
    """
    # Plot audioData
    plt.subplot(2, 2, 1)
    plt.plot(audioData)
    plt.title('Original Audio Data')
    # Plot medianRestoreData
    plt.subplot(2, 2, 2)
    plt.plot(medianRestoreData)
    plt.title('Median Restored Data')
    # Plot cubicRestoreData
    plt.subplot(2, 2, 3)
    plt.plot(cubicRestoreData)
    plt.title('Cubic Spline Restored Data')
    # Plot audioClean
    plt.subplot(2, 2, 4)
    plt.plot(audioClean)
    plt.title('Original Clean Audio')
    # Adjust layout for better visualization
    plt.tight_layout()
    # Show the plots
    plt.show()


def plotMseComparison(windowsList, medianMseList, cubicMseList):
    """
    Plots the Mean Squared Error (MSE) comparison between two lists.

    Parameters:
    - windowsList: List of window lengths.
    - medianMseList: List of MSE values for the median method.
    - cubicMseList: List of MSE values for the cubic method.
    """
    # Plot MSE for median method
    plt.plot(windowsList, medianMseList, label='medianMse', color='blue')
    # Plot MSE for cubic method
    plt.plot(windowsList, cubicMseList, label='cubicMse', color='red')
    # Add legend
    plt.legend()
    # Add title and axis labels
    plt.title('MedianMSE and CubicMSE Comparison')
    plt.xlabel('Window Length')
    plt.ylabel('MSE')
    # Add grid
    plt.grid()
    # Display the plot
    plt.show()


def saveAsWav(audio_data, sample_rate, file_name):
    """
    Save a NumPy array as a WAV file.

    Parameters:
    - audio_data (numpy.ndarray): The input audio data.
    - sample_rate (int): The sample rate of the audio data.
    - file_name (str): The desired file name for the WAV file.
    """
    # Save the audio data as a WAV file
    write(file_name, sample_rate, audio_data)
    print(f"Saved as {file_name}")


class TestAudioSignalRestoration(unittest.TestCase):
    def setUp(self):
        self.path = "/home/jiangmi/tcd/computationalMethod/CM_assignment2"
        self.samplerate, self.audioData, self.audioClean, self.position = readData(
            self.path)

    def test_findMedian(self):
        test_list = [1, 3, 5, 2, 4]
        self.assertEqual(findMedian(test_list), 3)


if __name__ == '__main__':
    path = "/home/jiangmi/tcd/computationalMethod/CM_assignment2"
    samplerate, audioData, audioClean, position = readData(path)
    print(audioClean)
    audioClean = audioClean / 2
    medianMseList = []
    cubicMseList = []
    windowsList = []
    for i in range(3, 71, 2):
        windowLength = i
        medianRestoreData = medianReplace(audioData, position, windowLength)
        cubicRestoreData = cubicSpline(audioData, position, windowLength)
        medianMse = MSE(audioClean, medianRestoreData, position)
        cubicMse = MSE(audioClean, cubicRestoreData, position)
        medianMseList.append(medianMse)
        cubicMseList.append(cubicMse)
        windowsList.append(i)
        print(medianMse, cubicMse)
    plotMseComparison(windowsList, medianMseList, cubicMseList)
    medianRestoreData = medianReplace(audioData, position, 3)
    cubicRestoreData = cubicSpline(audioData, position, 5)
    plotAudioSignals(audioData, medianRestoreData,
                     cubicRestoreData, audioClean)
    # saveAsWav(medianRestoreData, samplerate, 'output_medianFilter.wav')
    # saveAsWav(cubicRestoreData, samplerate, 'output_cubicSplines.wav')
    unittest.main()
