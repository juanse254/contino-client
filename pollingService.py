import polling
import pickle
import requests
from gitHandler import gitHandler

HOST = 'http://127.0.0.1:8000/'
PORT = 8000
repo = None

def pollGit(Repo):
    index = Repo.commit().committed_date
    global repo
    repo = Repo
    polling.poll(
        lambda: gitHandler.fetchData(Repo.working_dir).commit().committed_date != index, #TODO:esto verifica si hay algun commit local nuevo en comparacion al anterior(el llamado por la func).
        step=10,
        poll_forever=True,
        check_success=is_correct_response,
    )

def is_correct_response(error):
    if error == True:
        global repo
        print('mando el commmit o diff al server')
        req = requests.post(HOST,data=pickle.dumps(repo)) # Aqui solo mando el repo que es el padre pero puedo mandar repo.git.diff() que es el patch o lo que sea realmente.
        print(req.text)

        #aqui hay llamar otra vez a la funcion original, cambiando el repo anterior por el nuevo para sacar nuevos cambios. o sea llamar a gitHandler con el Repo actual o devolver algo al main para que salga del loop y pueda volver a llamar.