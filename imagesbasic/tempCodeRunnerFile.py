
import cv2
import face_recognition

# Function to load and encode image
def load_and_encode_image(image_path):
    img = face_recognition.load_image_file(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locs = face_recognition.face_locations(img)
    if len(face_locs) > 0:
        face_loc = face_locs[0]
        encode = face_recognition.face_encodings(img, [face_loc])[0]
        cv2.rectangle(img, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (255, 0, 255), 2)
        return img, encode
    else:
        print(f"No faces found in image: {image_path}")
        return img, None

# Function to compare face encodings
def compare_faces(known_encode, test_encode):
    return face_recognition.compare_faces([known_encode], test_encode)

# Function to recognize person in webcam frame
def recognize_person(frame, known_encodings, names):
    face_locs = face_recognition.face_locations(frame)
    print(f"Detected {len(face_locs)} faces in the frame.")
    if face_locs:
        encodings = face_recognition.face_encodings(frame, face_locs)
        for encode, face_loc in zip(encodings, face_locs):
            matches = face_recognition.compare_faces(known_encodings, encode)
            print(f"Match results: {matches}")
            name = "Unknown"
            if True in matches:
                matched_idx = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matched_idx:
                    name = names[i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
            top, right, bottom, left = face_loc
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return frame

# Load and encode images for each person
def load_encode_all():
    # Load and encode images for each person
    imgmusk, encodeMusk = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\muskan.png')
    imgalf, encodeAlf = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\alfiya.png')
    imggiri, encodeGiri = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\girish.png')
    imgkot, encodeKot = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\kotramma2.png')
    imgshru, encodeShru = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\shruthi test.jpg')
    imganan, encodeAnan = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\anand.png')
    imgbas, encodeBas = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\basavesh.png')
    imgrek, encodeRek = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\rekha.png')
    imgprinci, encodePrinci = load_and_encode_image('C:\\Users\\heena\\OneDrive\\Documents\\facerecognition\\.vs\\imagesbasic\\princi.png')

    known_encodings = []
    names = ['Muskan', 'Alfiya', 'Girish', 'Kotramma', 'Shruthi', 'Anand', 'Basavesh', 'Rekha', 'Princi']
    
    encodings = [encodeMusk, encodeAlf, encodeGiri, encodeKot, encodeShru, encodeAnan, encodeBas, encodeRek, encodePrinci]
    for name, encoding in zip(names, encodings):
        if encoding is not None:
            known_encodings.append(encoding)
        else:
            print(f"Encoding for {name} not found.")

    return known_encodings, names

# Main function to perform face recognition
def main():
    # Load and encode all images
    known_encodings, names = load_encode_all()
    print(f"Loaded encodings for: {names}")

    # Open webcam
    cap = cv2.VideoCapture(0)  # 0 for default webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip frame horizontally for mirror view

        # Recognize each person in the frame
        frame = recognize_person(frame, known_encodings, names)

        cv2.imshow('Webcam Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Entry point of the program
if __name__ == "__main__":
    main()