from twython import Twython
from time import sleep
from datetime import datetime
from picamera import PiCamera
from gpiozero import LED
from gpiozero import Button
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

#The numbers in brackets, below, refer to the GPIO pin to which the LEDs and button are connected
def main():
    button = Button(5)

    red=LED(2)
    amber=LED(17)
    green=LED(11)

    button.wait_for_press()

    red.on()
    amber.on()
    green.on()

    with PiCamera() as camera:  
        timestamp = datetime.now().isoformat()
        photo_path = '/home/pi/push-button-photo/photos/%s.jpg' % timestamp
        camera.start_preview()
        sleep(1)
        red.off()
        amber.on()
        green.on()
        sleep(1)
        red.off()
        amber.off()
        green.on()
        sleep(1)
        red.off()
        amber.off()
        green.off()
        camera.capture(photo_path)
        camera.stop_preview()

    message = "I have been taking photos with code..."
    with open(photo_path, 'rb') as photo:
        twitter.update_status_with_media(status=message, media=photo)
    print("Tweeted: %s" % message)

if __name__ == '__main__':
    main()
