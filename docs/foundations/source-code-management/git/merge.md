 

## Commit and Status

| Command | Explanation & Link |
|---------|---------------------|
| `git commit -a` | Stages files automatically |
| `git log -p` | Produces patch text |
| `git show` | Shows various objects |
| `git diff` | Is similar to the Linux `diff` command, and can show the differences in various commits |
| `git diff --staged` | An alias to --cached, this will show all staged files compared to the named commit |
| `git add -p` | Allows a user to interactively review patches to add to the current commit |
| `git mv` | Similar to the Linux `mv` command, this moves a file |
| `git rm` | Similar to the Linux `rm` command, this deletes, or removes a file |

## Branching and Merging

| Command | Explanation & Link |
|---------|--------------------|
| `git branch` | Used to manage branches |
| `git branch <name>` | Creates the branch |
| `git branch -d <name>` | Deletes the branch |
| `git branch -D <name>` | Forcibly deletes the branch |
| `git checkout <branch>` | Switches to a branch |
| `git checkout -b <branch>` | Creates a new branch and switches to it |
| `git merge <branch>` | Merge joins branches together |
| `git merge --abort` | If there are merge conflicts (meaning files are incompatible), --abort can be used to abort the merge action |
| `git log --graph --oneline` | This shows a summarized view of the commit history for a repo |

## Remote Repositories

| Command | Explanation & Links |
|---------|---------------------|
|`git remote` | Lists remote repos|
|`git remote -v` | List remote repos verbosely|
| `git remote show <name>` | Describes a single remote repo |
| `git remote update` | Fetches the most up-to-date objects|
| `git fetch` | Downloads specific objects|
| `git branch -r` | Lists remote branches; can be combined with other branch arguments to manage remote branches|
