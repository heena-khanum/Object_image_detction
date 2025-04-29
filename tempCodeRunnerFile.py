import cv2
import face_recognition
import pyttsx3
import webbrowser
import speech_recognition as sr
import sys

# Function to load and encode image
def load_and_encode_image(image_path):
    img = face_recognition.load_image_file(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locs = face_recognition.face_locations(img)
    if len(face_locs) > 0:
        face_loc = face_locs[0]
        encode = face_recognition.face_encodings(img, [face_loc])[0]
        return img, encode
    else:
        print(f"No faces found in image: {image_path}")
        return img, None

# Function to capture voice input
def get_voice_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

# Function to recognize person in webcam frame and handle LinkedIn prompt
def recognize_person(frame, known_encodings, names, engine, last_detected):
    face_locs = face_recognition.face_locations(frame)
    print(f"Detected {len(face_locs)} faces in the frame.")
    detected_name = "Unknown"
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

                # Display details in console for the first time detection
                if name != last_detected[0]:
                    last_detected[0] = name  # Update last detected name
                    details = {
                        "Muskan": {
                            "Name": "MUSKAN SHAMA",
                            "Designation": "ASSISTANT PROFESSOR",
                            "Department": "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",
                            "LinkedIn": "https://www.linkedin.com/in/muskan-shama-152561291/"
                        },
                        "Alfiya": {
                            "Name": "ALFIYA JAVEED",
                            "Designation": "ASSISTANT PROFESSOR",
                            "Department": "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",
                            "LinkedIn": "https://www.linkedin.com/in/alfiya-javeed-b4082b224/"
                        },
                        "Girish": {
                            "Name": "Dr. Girish L",
                            "Designation": "H O D & Associate Professor",
                            "Department": "Artificial Intelligence & Data Science",
                            "LinkedIn": "https://www.linkedin.com/in/dr-girish-l-87859a23a/"
                        },
                        "Kotramma": {
                            "Name": "KOTRAMMA MATHADA",
                            "Designation": "Assistant Professor",
                            "Department": "Artificial Intelligence and Data Science",
                            "LinkedIn": "https://www.linkedin.com/in/kotramma-mathada-4b296b9b"
                        },
                        "Shruthi": {
                            "Name": "SHRUTHI S",
                            "Designation": "Assistant Professor",
                            "Department": "Artificial Intelligence & Data Science",
                            "LinkedIn": None
                        },
                        "Anand": {
                            "Name": "S KRISHNA ANAND",
                            "Designation": "PROFESSOR",
                            "Department": "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",
                            "LinkedIn": "https://www.linkedin.com/in/s-krishna-anand-1a924717/"
                        },
                        "Rekha": {
                            "Name": "Dr. REKHA H",
                            "Designation": "Professor & H O D",
                            "Department": "Information Science and Engineering",
                            "LinkedIn": None
                        },
                        "Basavesh": {
                            "Name": "Dr.Basavesha D",
                            "Designation": "Associate Professor & H O D",
                            "Department": "Computer Science and Technology",
                            "LinkedIn": None
                        },
                        "Princi": {
                            "Name": "Dr m vishwanath",
                            "Designation": "Principal of SIET",
                            "Department" : "Mechanical Engineering",
                            "LinkedIn": None,
                            "Message": "Our principal's message: At SIET, we believe in embracing challenges as opportunities for growth and success. Our institution fosters a culture of dedication and resilience, empowering students to overcome life’s obstacles and pursue their dreams with confidence and grace. We invite all students and faculty to join us in this transformative journey of exploration and enlightenment."
                        },
                    }

                    if name in details:
                        detail = details[name]
                        print(f"\nNAME: {detail['Name']}")
                        print(f"Designation: {detail.get('Designation', 'Not available')}")
                        print(f"Department: {detail.get('Department', 'Not available')}")
                        if detail['LinkedIn']:
                            print(f"LinkedIn: {detail['LinkedIn']}")
                        else:
                            print("LinkedIn: Not available")
                        if 'Message' in detail:
                            print(f"\nMessage from Principal:")
                            print(detail['Message'])

                        # Speak out the details
                        engine.say(f"Name: {detail['Name']}. Designation: {detail.get('Designation', 'Not available')}. Department: {detail.get('Department', 'Not available')}.")
                        if 'Message' in detail:
                            engine.say(detail['Message'])
                        engine.runAndWait()

                        # Ask if user wants to visit LinkedIn profile
                        if detail['LinkedIn']:
                            engine.say(f"Would you like to visit {detail['Name']}'s LinkedIn profile?")
                            engine.runAndWait()
                            voice_response = get_voice_input("Would you like to visit the LinkedIn profile? (yes/no): ")
                            if voice_response is not None:
                                response = voice_response.strip().lower()
                                print(f"User response: {response}")
                                if "yes" in response:
                                    webbrowser.open(detail['LinkedIn'])
                            else:
                                engine.say("It appears the detected person may not have a LinkedIn profile.")
                                engine.runAndWait()

            for (top, right, bottom, left) in face_locs:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                detected_name = name
    return frame

# Load and encode images for each person
def load_encode_all():
    images = {
        "Muskan": "C:\\project\\imagesbasic\\muskan.png",
        "Alfiya": "C:\\project\\imagesbasic\\alfiya.png",
        "Girish": "C:\\project\\imagesbasic\\girish.png",
        "Kotramma": "C:\\project\\imagesbasic\\kotramma2.png",
        "Shruthi": "C:\\project\\imagesbasic\\shruthi test.jpg",
        "Anand": "C:\\project\\imagesbasic\\anand.png",
        "Rekha": "C:\\project\\imagesbasic\\rekha.png",
        "Basavesh": "C:\\project\\imagesbasic\\basaveshsir.jpeg",
        "Princi": "C:\\project\\imagesbasic\\princi.png",
    }
    known_encodings = []
    names = []
    for name, image_path in images.items():
        _, encode = load_and_encode_image(image_path)
        if encode is not None:
            known_encodings.append(encode)
            names.append(name)
    return known_encodings, names

# Main function to perform face recognition
def main():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    known_encodings, names = load_encode_all()
    print(f"Loaded encodings for: {names}")

    cap = cv2.VideoCapture(0)  # 0 for default webcam
    last_detected = [None]  # Variable to store last detected name

    while True:
        # Prompt user for detection permission before each detection cycle
        engine.say("Do you want to detect? Please say 'detect' or 'start detection' to begin.")
        engine.runAndWait()

        # Get voice response
        voice_response = get_voice_input("Say 'detect' or 'start detection' to begin or 'quit' to exit: ")
        
        if voice_response:
            voice_response = voice_response.lower()

            # Check for detection start
            if 'detect' in voice_response or 'start detection' in voice_response:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                frame = recognize_person(frame, known_encodings, names, engine, last_detected)
                cv2.imshow('Webcam Face Recognition', frame)

                # Prompt before exit
                engine.say("Want to dive into more detections? I’m your vision buddy!")
                engine.runAndWait()
                break  # Exit the loop after speaking

            elif 'quit' in voice_response:
                break
            else:
                print("Invalid command. Please say 'detect', 'start detection', or 'quit'.")

        else:
            # Fallback to text input if voice response is not recognized
            text_response = input("Type 'detect' to start detection or 'quit' to exit: ").strip().lower()

            # Check for detection start
            if 'detect' in text_response or 'start detection' in text_response:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                frame = recognize_person(frame, known_encodings, names, engine, last_detected)
                cv2.imshow('Webcam Face Recognition', frame)

                # Prompt before exit
                engine.say("Want more? Just give me a shout!")
                engine.runAndWait()
                break  # Exit the loop after speaking

            elif 'quit' in text_response:
                break
            else:
                print("Invalid command. Please type 'detect', 'start detection', or 'quit'.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    engine.say("Want more? Just give me a shout!")
    engine.runAndWait()
    sys.exit()  # Terminate the script

if __name__ == "__main__":
    main()
