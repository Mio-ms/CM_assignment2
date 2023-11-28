import numpy as np
from tqdm import tqdm
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import CubicSpline


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
            processData = audioCopy[(
                position[i] - int(padding)): (position[i] + int(padding) + 1)]
            medianData = findMedian(processData)
            audioCopy[position[i]] = medianData
        print("Done")
        return audioCopy


def MSE(audioData, restoreData, position):
    try:
        mse = np.square(audioData[position] / 32768 - restoreData[position] / 32768).mean()
        return mse
    except:
        print('No restore data are input.')


def cubicSpline(audioData, position, windowLength):
    if windowLength % 2 == 0:
        print("Please input a odd value.")
        return None
    else:
        audioCopy = np.copy(audioData)
        for i in range(len(position)):
            padding = (windowLength - 1) / 2
            index = [(position[i] - int(padding)), (position[i] + int(padding))]
            x = np.linspace(index[0], index[1], windowLength)
            cubicSplineX = np.delete(x, int(padding))
            cubicSplineY = np.delete(
                audioCopy[index[0]: index[1] + 1], int(padding))
            cs = CubicSpline(cubicSplineX, cubicSplineY)
            xInterp = np.linspace(index[0], index[1], 51)
            yInterp = cs(xInterp)
            audioCopy[position[i]] = yInterp[25]
        return audioCopy


if __name__ == '__main__':
    path = "/home/jiangmi/tcd/computationalMethod/CM_assignment2"
    samplerate, audioData, audioClean, position = readData(path)
    windowLength = 5
    audioClean = audioClean / 2
    medianRestoreData = medianReplace(audioData, position, windowLength)
    cubicRestoreData = cubicSpline(audioData, position, windowLength)
    medianMse = MSE(audioClean, medianRestoreData, position)
    cubicMse = MSE(audioClean, cubicRestoreData, position)
    print(medianMse, cubicMse)
