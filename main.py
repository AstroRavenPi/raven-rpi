import time
from sense_hat import SenseHat
import config
from picamera import PiCamera
from orbit import ISS

startTime = int(time.time())

#Setup Camera and SenseHAT
camera = PiCamera()
camera.resolution = (1296,972)
camera.start_preview()

#SenseHAT not used, but makes it easy to tell if code runs.
sense = SenseHat()
sense.set_pixels(config.image)

def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def takePhoto(iteration):
    """Take a photo from the PiCamera"""
    point = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"
    camera.capture(f"{config.base_folder}/image-{iteration}.jpg")

def main():
    """Main loop to run any functions."""
    iteration = 0
    while int(time.time()) - startTime < config.runTime:
        iteration += 1
        takePhoto(iteration)
        time.sleep(1)

if __name__ == "__main__":
    main()