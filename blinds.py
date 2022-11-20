import time
import sys
import RPi.GPIO as GPIO

NUM_ATTEMPTS = 12
# TRANSMIT_PIN = 12

KNOWN_CODES = {
    "up0": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlSlSlSlSlSlLsSlSlSlL",
    "dn0": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlSlSlSlSlLsLsSlSlLsL",
    "st0": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlSlSlSlLsSlLsSlLsSlL",

    "up1": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlSlLsSlSlSlLsSlSlSlL",
    "dn1": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlSlLsSlSlLsLsSlSlLsL",
    "st1": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlSlLsSlLsSlLsSlLsSlL",

    "up2": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlLsSlSlSlSlLsSlSlSlL",
    "dn2": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlLsSlSlSlLsLsSlSlLsL",
    "st2": "SlLsLsSlLsSlSlSlSlSlLsSlLsSlSlLsLsLsLsLsLsLsSlLsSlSlSlSlSlSlLsSlSlLsSlLsSlLsSlL"
}

TIMINGS = {
    'attempts_gap': 0.008,   # time to wait between attempts
    'first_on': 4.733/1000.0,     # initial extended signal time
    'first_gap': 1.490/1000.0,   # gap between initial signal to next digit
    'long': 0.65015/1000.0,     # long signal time (i.e. digit 1)
    'short': 0.290282/1000.0,    # time between long signal to the next digit # 0.001
    'sleep': 8.340/1000.0
}


def transmit(codes, transmit_pin):
    '''
    Transmits all codes received, assuming: 
    - each code starts with an extended init signal (`first_on` and `first_gap`)
    - long on  + short gap = 1
    - short on + long gap  = 0
    '''
    transmitted = []
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(transmit_pin, GPIO.OUT)
    for code_name in codes:
        code = KNOWN_CODES[code_name]
        GPIO.output(transmit_pin, 0)
        transmitted.append(code)
        time.sleep(TIMINGS['sleep'])
        for t in range(NUM_ATTEMPTS):
            print('#' + str(t) + ' attempt for "' + code + '"')
            GPIO.output(transmit_pin, 1)
            time.sleep(TIMINGS['first_on'])
            GPIO.output(transmit_pin, 0)
            time.sleep(TIMINGS['first_gap'])
            for i in code:
                if i == 's':
                    GPIO.output(transmit_pin, 0)
                    time.sleep(TIMINGS['short'])
                    # print(TIMINGS['short'])
                elif i == 'l':
                    GPIO.output(transmit_pin, 0)
                    time.sleep(TIMINGS['long'])
                    # print(TIMINGS['long'])
                elif i == 'S':
                    GPIO.output(transmit_pin, 1)
                    time.sleep(TIMINGS['short'])
                    # print(TIMINGS['short'])
                elif i == 'L':
                    GPIO.output(transmit_pin, 1)
                    time.sleep(TIMINGS['long'])
                    # print(TIMINGS['long'])
                else:
                    continue
            GPIO.output(transmit_pin, 0)
            time.sleep(TIMINGS['sleep'])
    GPIO.cleanup()
    return transmitted


if __name__ == '__main__':
    # Receive codes to run as cmd args: `python transmitter.py example`
    codes_to_send = sys.argv[1:]
    if codes_to_send:
        transmit(codes_to_send)