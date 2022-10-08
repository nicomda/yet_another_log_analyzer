import sys
sys.path.append('../')
import src.utils as utils

ip_list = ["127.0.0.1", "192.168.1.1", "127.0.0.1", "10.20.10.20", "10.15.1.15"]
epochs = ["1157689312.049","1157703527.004", "1335598251", "1335598304"]
events= 4000000


def test_calculateMostAndLessFrequentIp():
    ip_mostFrequent, ip_lessFrequent=utils.calculateMostAndLessFrequentIp(ip_list)
    assert ip_mostFrequent == ("127.0.0.1",2)
    assert ip_lessFrequent == ("10.15.1.15",1)
    print(ip_list)

def test_calculateOldestTime():
    oldest_time = utils.calculateOldestTime(epochs)
    assert oldest_time == "1157689312.049"


def test_calculateNewestTime():
    newest_time = utils.calculateNewestTime(epochs)
    assert newest_time == "1335598304"


def test_calculateEventsPerSecond():
    events_per_second=utils.calculateEventsPerSecond(epochs,events)
    assert events_per_second == 0.02248340545429928