import time
import config
import csv
from picamera import PiCamera
from orbit import ISS

print('starting setup!')
startTime = int(time.time())
print('defining functions')
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

def takePhoto(iteration, camera):
    """Take a photo from the PiCamera"""
    print('taking photo')
    point = ISS.coordinates()
    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)
    # Set the EXIF tags specifying the current location
    with open('data.txt', 'a') as file:
        stringToWrite = f"\n image-{iteration}.jpg: {point.latitude} {point.longitude}" 
        file.write(stringToWrite)
        file.close()
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"
    camera.capture(f"{config.base_folder}/image-{iteration}.jpg")

def main():
    """Main loop to run any functions."""
    cam = PiCamera()
    cam.resolution = (1296,972)
    #cam.start_preview()
    iteration = 0
    while int(time.time()) - startTime < config.runTime:
        iteration += 1
        takePhoto(iteration, cam)
        time.sleep(1)

print('starting main function loop')
if __name__ == "__main__":
    main()