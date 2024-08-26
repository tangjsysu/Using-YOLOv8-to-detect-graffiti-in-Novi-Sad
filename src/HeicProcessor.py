import simplekml
import exifread
import os
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

img_path = "../data/Graffiti and streetart"
HEICpath = "../data/Graffiti and streetart"

# Convert the coordinates from degrees, minutes, seconds to decimal
def decimal_coords(coords, ref):
    decimal_degrees = float(coords[0]) + float(coords[1]) / 60 + float(coords[2]) / 3600
    if ref == 'S' or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees

# Get the coordinates and the time of the image
def get_heicGeoCoords(heicPath):
    image = Image.open(heicPath)
    image.verify()

    exif = image.getexif().get_ifd(0x8825)
    geo_tagging_info = {}
    if not exif:
        raise ValueError("No EXIF metadata found")
    else:
        gps_keys = ['GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
                    'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp', 'GPSSatellites', 'GPSStatus', 'GPSMeasureMode',
                    'GPSDOP', 'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack', 'GPSImgDirectionRef',
                    'GPSImgDirection', 'GPSMapDatum', 'GPSDestLatitudeRef', 'GPSDestLatitude', 'GPSDestLongitudeRef',
                    'GPSDestLongitude', 'GPSDestBearingRef', 'GPSDestBearing', 'GPSDestDistanceRef', 'GPSDestDistance',
                    'GPSProcessingMethod', 'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential']

        for k, v in exif.items():
            try:
                geo_tagging_info[gps_keys[k]] = v
            except IndexError:
                pass
        coords = (decimal_coords(geo_tagging_info['GPSLatitude'], geo_tagging_info['GPSLatitudeRef']),
                  decimal_coords(geo_tagging_info['GPSLongitude'], geo_tagging_info['GPSLongitudeRef']))
        return coords

# Get the time of the image
def get_heicTime(heicPath):
    pic_data = exifread.process_file(open(heicPath, 'rb'))
    time = pic_data['Image DateTime']
    time_stamp = str(time)[2:4] + str(time)[5:7] + str(time)[8:10] + str(time)[11:13] + str(time)[14:16] + str(time)[
                                                                                                           17:19]
    return time_stamp


if __name__ == '__main__':

    imgs = os.listdir("../data/Graffiti and streetart")

    dateDatas = []
    date2Details = {}
    for imgName in imgs:
        if imgName[-4:] == 'HEIC':
            try:
                img_path = HEICpath + '/' + imgName

                thisTime = get_heicTime(img_path)
                thisCoords = get_heicGeoCoords(img_path)

                dateDatas.append(int(thisTime))
                date2Details[thisTime] = [thisCoords, imgName]
                print("Done=>" + imgName)
            except ValueError:
                print("No EXIF metadata found=>" + imgName)
    dateDatas.sort()
    print(dateDatas)

    kml = simplekml.Kml()
    lin = kml.newlinestring(name="trip")
    lin.extrude = 1
    lin.altitudemode = simplekml.AltitudeMode.clamptoground
    lin.style.linestyle.width = 5
    lin.style.linestyle.color = simplekml.Color.blue

    for date in dateDatas:
        coords = date2Details[str(date)][0]
        pnt = kml.newpoint(description='test', coords=[(coords[1], coords[0])])
        description = '<![CDATA[<img style="max-width:500px;" src="file:///D:/anaconda/envs/NLP/gisproject/data/Graffiti and streetart/' + \
                      date2Details[str(date)][1][:-5] + '.HEIC">]]>'
        pnt.description = description
        lin.coords.addcoordinates([(coords[1], coords[0])])
    kml.save("test.kml")


