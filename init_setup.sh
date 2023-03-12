echo [$(date)]: "START" 
echo [$(date)]: "creating env with python 3.9 version" 
conda create --name credit_card python=3.9 -y
echo [$(date)]: "activating the environment" 
conda activate credit_card
echo [$(date)]: "installing the dev requirements" 
pip install -r requirements_dev.txt
echo [$(date)]: "END" 