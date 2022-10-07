from collections import Counter
from datetime import datetime

def calculateMostAndLessFrequentIp(ips: list) -> list:
    '''Use collections to get the most and less frequent ip'''
    # Assumption: More than 1 IP could match any of the filters, but we'll consider first and last element of Counter(Dict subclass) to simplify
    occurences = Counter(ips)
    return occurences.most_common()[0], occurences.most_common()[-1]


def calculateOldestTime(epochs: list) -> str:
    epochs.sort()
    return epochs[0]


def calculateNewestTime(epochs: list) -> str:
    epochs.sort()
    return epochs[-1]


def calculateEventsPerSecond(epochs: list, events: int) -> float:
    epochs.sort()
    oldest_date = datetime.fromtimestamp(float(epochs[0]))
    newest_date = datetime.fromtimestamp(float(epochs[-1]))
    time_difference_in_seconds = (newest_date-oldest_date).total_seconds()
    return float(events)/time_difference_in_seconds
