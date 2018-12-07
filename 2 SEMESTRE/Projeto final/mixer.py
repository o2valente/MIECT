import json

def mix(sheet):
    data = json.loads(sheet)
    music = data["music"]
    bpm = data["bpm"]
    effects = data["effects"]
    samples = data["samples"]
    vol = data["vol"]
    rate = 44100
    beat_duration = (1/bpm) * 60

    for j in range(0, 10):

        for i in range(0, rate*beat_duration):
            amps = []
            for x in range(0, music[j].length):
                amps.append(amp())
