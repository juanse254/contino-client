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
    def fetchData(self, existentDir):
        repo = git.Repo(existentDir)

