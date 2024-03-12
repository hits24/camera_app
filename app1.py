from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webcam Capture</title>
    <script type="text/javascript" src="https://unpkg.com/webcam-easy/dist/webcam-easy.min.js"></script>
    <style>
        #webcam {
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <video id="webcam" autoplay playsinline width="640" height="480"></video>
    <canvas id="canvas" class="d-none"></canvas>
    <button id="snap">Capture</button>
    <button id="save">Save</button>
    <script>
        const webcamElement = document.getElementById('webcam');
        const canvasElement = document.getElementById('canvas');
        const snapButton = document.getElementById('snap');
        const saveButton = document.getElementById('save');
        const webcam = new Webcam(webcamElement, 'user', canvasElement);

        window.addEventListener('load', () => {
            webcam.start()
                .then(result => {
                    console.log("webcam started");
                })
                .catch(err => {
                    console.log(err);
                });
        });

        snapButton.addEventListener('click', () => {
            webcam.snap();
        });

        saveButton.addEventListener('click', () => {
            const imageSrc = webcam.snap();
            fetch('/save-image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({image: imageSrc}),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    </script>
</body>
</html>
'''

@app.route('/start_cam')
def start_cam():
    return render_template_string(index_html)

if __name__ == '__main__':
    app.run(debug=True)