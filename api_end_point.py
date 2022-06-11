from flask import Flask, request
from flask_cors import CORS, cross_origin
from run_test import main
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate(
    "firebase/p2pnet-crowdcounting-firebase-adminsdk-fno8v-cb521dbffd.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'p2pnet-crowdcounting.appspot.com'
})

app = Flask(__name__)

def uploadFile(imagePath):

    bucket = storage.bucket()
    image_name = imagePath.split('/')[-1]
    blob = bucket.blob(image_name)
    blob.upload_from_filename(imagePath)
    # to make public access from the URL
    blob.make_public()
    
    imageUrl = 'https://firebasestorage.googleapis.com/v0/b/p2pnet-crowdcounting.appspot.com/o/' + image_name + '?alt=media'
    
    return imageUrl

# CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})
@app.route('/predict', methods=['POST', 'GET'])
@cross_origin()
def predict():
    # jsonData = request.get_json()
    print('api endpoint is running...')
    imageFile = request.files["imageFile"]

    (predict_cnt, imagePath) = main(imageFile)
    imageUrl = uploadFile(imagePath)
    return {
        'head_count': predict_cnt,
        'image_url': imageUrl
    }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
