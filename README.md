A program meant to visualize word clusters generated that relate old English words, depending on spelling and definition of the word. The dataset only includes words from medieval documents that are 10 or more characters.
<img width="590" height="498" alt="image" src="https://github.com/user-attachments/assets/a3443f1c-f61a-4eb3-b7c4-ef155b5c3a9d" />
![unnamed](https://github.com/user-attachments/assets/67b170f2-c27e-4576-ad08-6a59bd73b2d5)
<img width="609" height="569" alt="image" src="https://github.com/user-attachments/assets/78c12e16-7e53-4ac4-bcc9-3a83831e3324" />



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
