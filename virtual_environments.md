# Virtual Environments

When you start a new python project, you want to first create a virtual environment in your python project folder. When you activate the virtual environment, any packages you install are only installed within the virtual environment, and not on your whole system.

In the command line, navigate to your python project folder.

`python3 -m venv env`
This creates the virtual environment

`source env/bin/activate`
This activates it

Now pip install your desired packages, but since I've included them all in a requirements.txt file, simply run this to install all the ones the project needs.
`pip install -r requirements.txt`

`deactivate`
This deactivate the virtual environment

