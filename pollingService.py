import polling
import pickle
import requests
import git
from gitHandler import gitHandler

HOST = 'http://127.0.0.1:8000/'
PORT = 8000
repo = None
index = None

def pollGit(Repo):
    global index
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
        remote_url = repo.git.remote('get-url', 'origin')
        patch = repo.git.show()
        parent_commit_id = repo.git.rev_parse('HEAD~1')
        current_branch = repo.active_branch.name
        parent_branch = repo.git.branch(['--contains', parent_commit_id])
        username = repo.commit().author.email
        global index
        index = repo.commit().committed_date
        print('mando el commmit o diff al server')
        req = requests.post(HOST,data={'patch':patch,
                                       'remote_url': remote_url,
                                       'parent_commit_id': parent_commit_id,
                                       'current_branch': current_branch,
                                       'parent_branch': parent_branch,
                                       'username': username}) # Aqui solo mando el repo que es el padre pero puedo mandar repo.git.diff() que es el patch o lo que sea realmente.
        print(req.text)

        #aqui hay llamar otra vez a la funcion original, cambiando el repo anterior por el nuevo para sacar nuevos cambios. o sea llamar a gitHandler con el Repo actual o devolver algo al main para que salga del loop y pueda volver a llamar.