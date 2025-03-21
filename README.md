A program meant to visualize word clusters generated that relate old English words, depending on spelling and definition of the word. The dataset only includes words from medieval documents that are 10 or more characters.

### Setup
Simply run these commands, or run `setupConfig.bat`/`setupConfig.bash`
```
>>> py -m pip install virtualenv
>>> py -m venv venv
>>> .\venv\Scripts\activate
>>> py -m pip install -r requirements.txt
```
This will set up the Python virtual environment with the required dependencies.
### Use
The program comes with generated datasets already, and this program really only looks at the data to generate data visualizations with.

On a terminal, activate the python virtual environment & run `src/main.py`, which should prompt you with instructions on what to do thereafter.
```
>>> .\venv\Scripts\activate
>>> (venv) λ py ./src/cluster_visualizer.py
```
