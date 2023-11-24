import numpy as np
from tqdm import tqdm
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy import interpolate


def findMedian(list):
    """Calculate the median of a list of numeric values.

    Args:
        list (list): A list of numeric values.

    Returns:
        list: The median of the input list. If the list has an odd
        number of elements, the middle element is returned. If the list has an
        even number of elements, the average of the two middle elements is returned.
    """
    listLength = len(list)
    list.sort()
    if listLength % 2 == 0:
        middlePosition = listLength // 2
        median = (list[middlePosition] + list[middlePosition - 1]) / 2
    else:
        middlePosition = listLength // 2
        median = list[middlePosition]
    return median


def readData(path):
    samplerate, audioData = wav.read(path + "/degraded.wav")
    samplerate, audioClean = wav.read(path + "/clean.wav")
    position = np.load(path + "/detectionfile.npy")
    return samplerate, audioData, audioClean, position


def medianReplace(audioData, position, windowLength):
    if windowLength % 2 == 0:
        print("Please input a odd value.")
        return None
    else:
        audioCopy = np.copy(audioData)
        for i in tqdm(range(len(position))):
            padding = (windowLength - 1) / 2
            processData = audioCopy[(position[i] - int(padding)): (position[i] + int(padding) + 1)]
            medianData = findMedian(processData)
            audioCopy[position[i]] = medianData
        print("Done")
        return audioCopy


def MSE(audioData, restoreData, position):
    return np.square(audioData[position] / 32768 - restoreData[position] / 32768).mean()
# def cubicSpline(audioData, position, windowLength):


if __name__ == '__main__':
    path = "/home/jiangmi/tcd/computationalMethod/CM_assignment2"
    samplerate, audioData, audioClean, position = readData(path)
    windowLength = 5
    audioClean = audioClean / 2
    restoreData = medianReplace(audioData, position, windowLength)
    mse = MSE(audioClean, restoreData, position)
    print(mse)
    plt.plot(restoreData)
