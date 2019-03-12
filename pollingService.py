import polling
from gitHandler import *

def pollGit(Repo):
    polling.poll(
        lambda: gitHandler.fetchData(Repo.working_dir) != Repo, #TODO:esto verifica si hay algun cambio no necesariamente un commit, esto hay q agregar y testear. Hay q ver si es mejor ver el index o comparar el commit.
        step=300,
        poll_forever=True,
        check_success=is_correct_response,
    )

def is_correct_response():
    print('mando el commmit o diff al server')
    #aqui hay llamar otra vez a la funcion original, cambiando el repo anterior por el nuevo para sacar nuevos cambios. o sea llamar a gitHandler con el Repo actual.