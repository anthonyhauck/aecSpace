# aecSpace
Python classes useful for creating and editing volumes indicating building spaces.

These classes and this example were developed using the Anaconda development
environment, relevant due to the need for the pythonOCC toolkit, a Python
wrapper around the open source openCascade geometry kernel. The conda package
manager makes it easy to install pythonOCC.

To install Anaconda, visit https://www.anaconda.com/download/

To install pythonOCC, open the Anaconda prompt (not the OS command prompt!)
that you should find installed as a separate aplication from Anaconda 
Navigator, and paste in this line from http://www.pythonocc.org/download/

conda install -c conda-forge -c dlr-sc -c pythonocc -c oce pythonocc-core==0.18.1

After this you theoretically have everything you need to run this example.
Make sure your IDE can find the folder where you've stored these *.py files and run aecSpaceTowerExample.py
All the code outside of the tower example file has been encapsulated as discrete objects.

The immdiate issue I see with this methodology is speed -- the sympy library handling geometric
transformations might be a bit slow. I'll be profiling to track down the most constly operations.

Please leave questions and comments.

Anthony Hauck | Black Arts Consulting

anthony |at| blackarts.co
