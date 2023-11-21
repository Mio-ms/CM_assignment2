import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt


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
    position = np.load(path + "/detectionfile.npy")
    return audioData, position


def replace(audioData, position, windowLength):
    if windowLength % 2 == 0:
        print("Please input a odd value.")
        return None
    else:
        for i in range(len(position)):
            padding = (windowLength - 1) / 2
            processData = audioData[(position[i] - int(padding)): (position[i] + int(padding))]
            medianData = findMedian(processData)
            print(position[i], medianData)
            audioData[position[i]] = medianData
        return audioData


if __name__ == '__main__':
    path = "/home/jiangmi/tcd/computationalMethod/CM_assignment2"
    audioData, position = readData(path)
    windowLength = 5
    modifyData = replace(audioData, position, windowLength)
    plt.plot(modifyData)
