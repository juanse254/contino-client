import git

class gitHandler:
    def searchGit(rootDir):
        try:
            exists = git.Repo(rootDir).git_dir
            return exists
        except:
            exists = 'not found'
        if exists == 'not found':
            return False
    def fetchData(existentDir): #this function will return a Repo object with all data from the git repo
        repo = git.Repo(existentDir)
        return repo

