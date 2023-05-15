import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# Initialize Firebase app with credentials
cred = credentials.Certificate('../emtest-ea4ab-firebase-adminsdk-khbj8-5011927154.json')
# firebase_admin.initialize_app(credentials=cred, options={'storageBucket': 'emtest-ea4ab.appspot.com'})
firebase_admin.initialize_app(cred, options={'storageBucket': 'gs://emtest-ea4ab.appspot.com'})


def upload_pdf_to_firebase(pdf_file_path, file_name):
    # Get reference to Firebase Storage bucket

    # create a storage client
    bucket = storage.bucket()

    # upload file to Firebase Storage
    blob = bucket.blob(f'destination/{file_name}.pdf')
    blob.upload_from_filename(pdf_file_path)
    print(f'File {filename} uploaded to Firebase Storage.')

upload_pdf_to_firebase('Reports/jenna\'s_Sentimental_evaluation_report.pdf', 'jenna\'s_Sentimental_evaluation_report.pdf')