import polling
import pickle
import requests
import git
import json
from gitHandler import gitHandler

HOST = 'http://127.0.0.1:8000/'
repo = None
index = None
#TODO:Este servicio deberia ser una clase.
def pollGit(Repo):
    global index
    index = Repo.commit().committed_date
    global repo
    repo = Repo
    polling.poll(
        lambda: gitHandler.fetchData(Repo.working_dir).commit().committed_date != index,
        step=10,
        poll_forever=True,
        check_success=is_correct_response,
    )

def is_correct_response(error):
    if error == True:
        global repo
        remote_url = repo.remotes.origin.url
        pivot_commit = checkDelta(remote_url)

        #mandar solo el delta
        delta = []
        commitsToSend = commitListtoArray(list(repo.iter_commits(pivot_commit + '..HEAD')))
        commitsToSend.reverse()
        for commit in commitsToSend:
            #patch = repo.git.show()
            patch = repo.git.format_patch('-1', '--stdout', commit) #TODO: revisar si esto es correcto, hay que usar diff para el merge info.
            parent_commit_id = repo.commit(commit).parents[0].hexsha
            current_branch = repo.active_branch.name
            parent_branch = repo.git.branch(['--contains', parent_commit_id]).replace("* ", "")#TODO: usar objeto git y no consola P.D: esto funciona?
            email = repo.commit(commit).author.email
            username = repo.commit(commit).author.name
            commit_id = repo.commit(commit).hexsha
            message = repo.commit(commit).message
            offset = repo.commit(commit).author_tz_offset
            time = repo.commit(commit).authored_date
            tempCommit = json.dumps({
                'patch':str(patch),
                'remote_url': str(remote_url),
                'parent_commit_id': str(parent_commit_id),
                'commit_id': str(commit_id),
                'current_branch': str(current_branch),
                'parent_branch': str(parent_branch),
                'email': str(email),
                'username': str(username),
                'message': str(message),
                'time': str(time),
                'offset': str(offset)
            })
            delta.append(tempCommit)

        global index
        index = repo.commit().committed_date
        print('mando el commmit o diff al server')
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        req = requests.post(HOST, data=json.dumps(delta), headers = headers)


def checkDelta(remote_url):
    try:
        completeList= list(repo.iter_commits(repo.active_branch))
        idList = commitListtoArray(completeList)
        jsonList = json.dumps({'commits' : idList, 'url' : remote_url})
        req = requests.post(HOST + 'commitCheck/', data=jsonList)
        print(req.content)
        return json.loads(req.text)['pivot_commit']
    except BaseException as e:
        print("Couldnt get delta")
        print(e)

def commitListtoArray(list):
    idList = []
    for commit in list:
        idList.append(commit.hexsha)
    return idList

        #aqu hay llamar otra vez a la funcion original, cambiando el repo anterior por el nuevo para sacar nuevos cambios. o sea llamar a gitHandler con el Repo actual o devolver algo al main para que salga del loop y pueda volver a llamar.
