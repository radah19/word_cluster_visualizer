@REM Set up Virtual Environment
py -m pip install virtualenv
py -m venv venv

@REM Activate Virtual Environment
call .\venv\Scripts\activate

@REM Install dependencies for server
py -m pip install -r requirements.txt

@REM Create Necessary Directories
mkdir cluster_visualizations