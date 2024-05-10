"""
This module implements a Flask server for emotion detection.
"""

from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector, emotion_predictor

app = Flask(__name__)

HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500

@app.route("/emotionDetector")
def sent_detector():
    """
    Analyzes the emotion in the provided text and returns the formatted response.
    """
    text_to_detect = request.args.get('textToAnalyze')

    if not text_to_detect:
        return jsonify({'error': 'Invalid text! Please try again!'}), HTTP_BAD_REQUEST

    response = emotion_detector(text_to_detect)
    formated_response = emotion_predictor(response)

    if formated_response['dominant_emotion'] is None:
        return jsonify({'error': 'Invalid text! Please try again.'}), HTTP_INTERNAL_SERVER_ERROR

    output = f"For the given statement, the system response is \
        'anger': {formated_response['anger']}, \
        'disgust': {formated_response['disgust']}, \
        'fear': {formated_response['fear']}, \
        'joy': {formated_response['joy']} \
        and 'sadness': {formated_response['sadness']}. \
        The dominant emotion is {formated_response['dominant_emotion']}."

    return output

@app.route("/")
def render_index_page():
    """
    Renders the index.html page.
    """
    return render_template('index.html')

@app.errorhandler(HTTP_INTERNAL_SERVER_ERROR)
def internal_server_error():
    """
    Handles internal server errors and returns a JSON response.
    """
    return jsonify({'error': 'Internal Server Error'}), HTTP_INTERNAL_SERVER_ERROR

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
