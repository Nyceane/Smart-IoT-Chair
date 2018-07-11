import WalabotAPI
import time
import sys, os

energy_threshold = 0.8
debug = True
state = False
lastState = False

def run():
    print("Connected to Walabot")
    WalabotAPI.SetProfile(WalabotAPI.PROF_TRACKER)

    # Set scan arena
    WalabotAPI.SetArenaR(15, 40, 10)
    WalabotAPI.SetArenaPhi(-60, 60, 10)
    WalabotAPI.SetArenaTheta(-30, 30, 10)
    print("Arena set")

    # Set image filter
    WalabotAPI.SetDynamicImageFilter(WalabotAPI.FILTER_TYPE_MTI)
    WalabotAPI.SetThreshold(35)

    # Start scan
    WalabotAPI.Start()

    t = time.time()
    while True:
        WalabotAPI.Trigger()
        energy = WalabotAPI.GetImageEnergy() * 1000

        if energy > energy_threshold:
            state = True
        else:
            state = False

        if debug:
            print('Energy: {:<10}Frame Rate: {}'.format(energy, 1/(time.time()-t)))
            t = time.time()


if __name__ == '__main__':
    print("Initialize API")
    WalabotAPI.Init()

    while True:
        WalabotAPI.Initialize()
        # Check if a Walabot is connected
        try:
            WalabotAPI.ConnectAny()
            run()
        except WalabotAPI.WalabotError as err:
            print('Failed to connect to Walabot. error code: {}'.format(str(err.code)))
        except Exception as err:
            print(err)
        finally:
            print("Cleaning API")
            WalabotAPI.Clean()
            time.sleep(2)