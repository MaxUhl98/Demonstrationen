import cv2
import sys
from random import randint


# Erstellt mehrere Objekte die getrackt werden
# Aus irgendeinem Grund funktioniert der builtin OpenCV Multitracker bei mir nicht, weshalb ich einfach einen eigenen geschrieben habe.
class Multitracker():
    trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

# Funktion zum Erstellen von builtin Object Trackern
    def create_tracker_by_name(self, trackerType):
        # Erstellt ein Tracker Object abhängig vom Namen
        if trackerType == self.trackerTypes[0]:
            tracker = cv2.TrackerBoosting_create()
        elif trackerType == self.trackerTypes[1]:
            tracker = cv2.TrackerMIL_create()
        elif trackerType == self.trackerTypes[2]:
            tracker = cv2.TrackerKCF_create()
        elif trackerType == self.trackerTypes[3]:
            tracker = cv2.TrackerTLD_create()
        elif trackerType == self.trackerTypes[4]:
            tracker = cv2.TrackerMedianFlow_create()
        elif trackerType == self.trackerTypes[5]:
            tracker = cv2.TrackerGOTURN_create()
        elif trackerType == self.trackerTypes[6]:
            tracker = cv2.TrackerMOSSE_create()
        elif trackerType == self.trackerTypes[7]:
            tracker = cv2.TrackerCSRT_create()
        else:
            tracker = None
            print('Incorrect tracker name')
            print('Available trackers are:')
        return tracker

    # Der Multitracker erwartet eine Liste mit Trackernamen, welche in der selben Reihenfolge wie die zu trackenden Objekte angeordnet sind
    def __init__(self, tracker_names: list, bboxes: list, frame):
        self.trackers = []
        self.boxes = bboxes
        # Tracker Initiieren
        for i, track in enumerate(tracker_names):
            elem = self.create_tracker_by_name(track)
            elem.init(frame, bboxes[i])
            self.trackers.append(elem)

    # Funktion zum Bekommen der Koordinaten der Bounding Boxes im Frame (gibt diese als iterable zurück)
    def update(self, frame):
        self.boxes = []
        for i in self.trackers:
            box = i.update(frame)[1]
            self.boxes.append(box)

        return self.boxes

if __name__ == '__main__':
    # Object Tracker festlegen
    trackerType = "CSRT"

    # VideoCapture Object zum erhalten von Webcam Footage erstellen
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # 1. Bild bekommen
    success, frame = cap.read()
    # Abbruch, falls etwas schiefgelaufen ist
    if not success:
        print('Failed to read video')
        sys.exit(1)
    # Listen für spätere Nutzung erstellen
    bboxes = []
    colors = []

    while True:
        # Händisches markieren von zu trackenden Objekten
        #ToDo Momentan arbeite ich noch daran einen yolo Object Detector zu implementieren,
        # damit dieser automatisch alle n Frames alle Objekte die er findet markiert.
        # Dies wird mir die Fähigkeit geben komplett automatisiert Objekte zu erkennen und zu tracken.
        bbox = cv2.selectROI('MultiTracker', frame)
        print('going...')
        print(bbox)
        bboxes.append(bbox)
        colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
        print("q drücken um Selektion zu beenden "
              ""
              "und tracking zu starten")
        print("Irgendeine andere Taste drücken um weitere Objekte für das Tracking zu markieren")
        k = cv2.waitKey(0) & 0xFF
        if (k == 113):  # q is pressed
            break
    # Liste mit Namen der Tracker für die jeweiligen markierten Objekte
    tracker_names = [trackerType for i in range(len(bboxes))]

    # Multitracker Initiieren
    multi_tracker = Multitracker(tracker_names=tracker_names, frame=frame, bboxes=bboxes)

    # Kamerainput bekommen und Verarbeiten
    while 1:
        success, frame = cap.read()
        if not success:
            break

        # Liste von bounding Boxes aus diesem Frame bekommen
        boxes = multi_tracker.update(frame)

        # Bounding Boxes Zeichnen
        for box in boxes:
            p1 = (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame, p1, p2, colors[0], 2, 1)
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break
        # Frame mit Bounding Boxes anzeigen
        cv2.imshow('MultiTracker', frame)
