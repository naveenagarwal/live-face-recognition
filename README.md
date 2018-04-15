# Live Face Recognition

Steps to train the model.

* Create a directory with the person's name in the directory 'training_data'
* Click few of the person's pictures using your webcam with different expressions and put that in the directory created in step 1.
* Run the command 'python training.py'
* To check if model is sufficently trainined or not 
    * Run - 'python live_face_recognition.py' # it should open your image and should greet you.
* Press 'ctrl + c' to terminate the program.

# Note - This program is created and tested on osx version 10.12.4 and uses the cv2 and face_recognition modules.