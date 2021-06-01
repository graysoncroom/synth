#!/bin/python3
import matplotlib.pyplot as plt
import math, wave, struct

sample_rate = 44100.0 # hertz (this is CD quality; increase for higher quality, decrease for lower)
duration = 3.0 # seconds
frequency = 440.0 # hertz

# 1000 * duration    = duration in milliseconds
# 1000 * sample_rate = sample_rate in millihertz
# and duration * sample_rate = number of total samples (b/c time * (1/time) = amount)
# note: we truncate it to an integer with int(...)
number_of_samples = int((duration*1000) * (sample_rate / 1000.0))

def main():
    x_sample = [ 2*math.pi*(1/frequency)*t for t in range(number_of_samples) ]
    y_sample = [ math.sin(x) for x in x_sample ]

    #plt.plot(x_sample, y_sample)
    #plt.xlabel('Time (t)')
    #plt.ylabel('y-axis')
    #plt.show()

    with wave.open('sound.wav', 'wb') as f:
        f.setnchannels(1) # mono
        f.setsampwidth(2) # size of each number we give it
        f.setframerate(sample_rate)
        for y in y_sample:
            # y from y_sample is the result of some y = sin(...)
            # notice that there is no amplitude
            # therefore y must be between -1 and 1 by properties of sine waves
            # since sample width = number of bytes each frame gets to store value
            # then sample width = 2 => we get 16 bits to store value
            # A singed 16-bit number has the range -32,768 to 32,767
            # (assuming 2s complement representation, which obv we are using as it is standard to do so)
            # to ensure we are in acceptable range do the following: frame data = (y * 32,767)
            # this doesn't make the "most" of the range we have with a 16-bit 2s comp number,
            # but it's good enough for our purposes
            # in general, assuming the machine uses bytes of 8 bits, for a sample size n:
            # frame data = y * 2^(n*8 - 1)
            f.writeframesraw(struct.pack('h', int(y*32767)))

if __name__ == '__main__':
    main()
