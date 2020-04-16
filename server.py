import os
import face_recognition
import cv2

from flask import Flask, request, abort, jsonify, send_from_directory

UPLOAD_DIRECTORY = "/opt/altere_bruder/backend/files/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)


@api.route('/hello')
def hello_world():
    print('HELLO WORLD!')
    return "Hello World!"


@api.route("/files")
def list_files():
    print('HELLO FILE LS')
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/files/<path:path>")
def get_file(path):
    print('HELLO FILE DL')
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    print('HELLO FILE UL')
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201


@api.route("/apply", methods=["GET"])
def post_apply():
    input_movie = cv2.VideoCapture(os.path.join(UPLOAD_DIRECTORY, "video.mp4"))
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create an output movie file (make sure resolution/frame rate matches input video!)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_movie = cv2.VideoWriter(os.path.join(UPLOAD_DIRECTORY, "output.api"), fourcc, 29.97, (640, 360))

    # Load some sample pictures and learn how to recognize them.
    image = face_recognition.load_image_file(os.path.join(UPLOAD_DIRECTORY, "face.jpg"))
    img_face_encoding = face_recognition.face_encodings(image)[0]


    known_faces = [
        img_face_encoding
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0

    while True:
        # Grab a single frame of video
        ret, frame = input_movie.read()
        frame_number += 1

        # Quit when the input video file ends
        if not ret:
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

            # If you had more than 2 faces, you could make this logic a lot prettier
            # but I kept it simple for the demo
            name = None
            if match[0]:
                name = "Lin-Manuel Miranda"
            elif match[1]:
                name = "Alex Lacamoire"

            face_names.append(name)

        # Label the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
                continue

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Write the resulting image to the output video file
        print("Writing frame {} / {}".format(frame_number, length))
        output_movie.write(frame)

    # All done!
    input_movie.release()
    cv2.destroyAllWindows()
    return "", 201


print('HELLO ENTRY')
api.run(debug=False, port=8080)
