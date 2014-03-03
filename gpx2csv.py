#usage:
#python3 gpx2csv.py outputDirectory
#remember to escape spaces in file paths with \

#load required modules
import sys
import os
import xml.etree.ElementTree as ET
import csv

#get the full path of the source, parent directory of source, list of files in source, and remove .DS_Store file from list
directory = os.path.abspath(sys.argv[1])
directoryParent = os.path.split(directory)[0]
csvDir = os.path.join(directoryParent,'csv')
fileNames = os.listdir(directory)
if '.DS_Store' in fileNames:
	fileNames.remove('.DS_Store')
filePaths = [os.path.join(directory,fn) for fn in fileNames]

#check if csv folder exists in same parent directory as source, if not make it
if not os.path.exists(csvDir):
    os.makedirs(csvDir)

#parse gpx files for desired data
for x in range(0, len(fileNames)):
	tree = ET.parse(filePaths[x])
	root = tree.getroot()
	time = tree.findall('.//{http://www.topografix.com/GPX/1/1}time')
	trackPoints = tree.findall('.//{http://www.topografix.com/GPX/1/1}trkpt')
	elevation = tree.findall('.//{http://www.topografix.com/GPX/1/1}ele')
	hr = tree.findall('.//{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr')

#write csv file for each gpx with heading and data sorted by column
	targetPath = os.path.join(csvDir,fileNames[x])
	with open(targetPath + '.csv', 'wb') as csvfile:
		datawriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for x in range(0, 4):
			datawriter.writerow([])
		datawriter.writerow(['Time', 'blank', 'blank', 'blank', 'blank', 'blank', 'Hrate', 'blank', 'Altitude (m)', 'blank', 'blank', 'Latitude', 'Longitude', 'blank', 'blank', 'blank', 'blank', 'blank'])
		for x in range(0, len(trackPoints)):
			datawriter.writerow([time[x].text, '0', '0', '0', '0', '0',  hr[x].text, '0', elevation[x].text,  '0', '0', trackPoints[x].attrib['lat'], trackPoints[x].attrib['lon'], '0', '0', '0', '0', '0'])
