If not explicitly discussed or arranged with the `code evangelist`, no one should directly edit this repository in any way. To make contributions, use the procedure described in `How to contribute`.

___

# Contributing:

## Keep in mind:

### Commits:

When adding files to the staging-area, make sure that the files you add are necessary. Try not to clutter up the repo with files produces by the OS -- i.e _.DS_store_ on mac -- or any config file produces by text-formatting tools or IDE's (VSCode and pycharm). Directories produced by the python-interpreter should also not be added to the repo, mainly  _\_\_pychache\_\__. _(Take a look at [.gitignore](https://git-scm.com/docs/gitignore))_

Commit often, and try to use informative commit-messages. Don't try to describe the changes you have made in the code, but rather try and describe how the code changes the program.

### Code-Style:
Adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/) or [Googles Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md). Be sure to comment your code thoroughly.

## How to contribute:

1. Fork the repository to your own github-account. 
2. Clone your repository into a directory on your local machine
3. Add a remote to the original repository called _upstream_
4. Add a remote to your own repository called _origin_
5. pull the master-branch from the upstream remote _(this should be done anytime there's been any changes to the original repo)_
5. Create a new branch - This will be where you commit your changes. _N.B: You should not change the code on the master branch_
6. Push you branch to your _origin_ remote
7. Create a pull request with your branch and the master branch of the original repo
8. Cross fingers and wait
