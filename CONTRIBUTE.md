If not explicitly discussed or arranged with the `code evangelist`, no one should directly edit this repository in any way. To make contributions, use the procedure described in `How to contribute`.

___

# Contributing:

## Keep in mind:

#### Commits:

When adding files to the staging-area, make sure that the files you add are necessary. Try not to clutter up the repo with files produces by the OS -- i.e _.DS_store_ on mac -- or any config file produces by text-formatting tools or IDE's (VSCode and pycharm). Directories produced by the python-interpreter should also not be added to the repo, mainly  _\_\_pychache\_\__. _(Take a look at [.gitignore](https://git-scm.com/docs/gitignore))_

Commit often, and try to use informative commit-messages. Don't try to describe the changes you have made in the code, but rather try and describe how the code changes the program.

#### Code-Style:
Adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/) or [Googles Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md). Be sure to comment your code thoroughly.

#### Pull Requests:
Before making a pull request, make sure that the original repository hasn't been changed. If it has, you must pull the repo, make sure everything works, then create the pull request.

The easiest way to do this is to add a remote to the original repository. A remote is basically just an alias for the repo-url (so that you don't have to type out the whole thing everytime). It's recommended to configure two remotes - One to your own repository called `origin`, and one to the original repository called `upstream`. 

```bash
>>> git remote add upstream https://github.com/rats-studio/digital_impersonator.git
>>> git remote add origin https://github.com/<you-git-account>/digital_impersonator.git
```

Now you can update your own repo simple as: 

```bash
>>> git pull upstream master
```

## How to contribute:

1. Fork the repository to your own github-account. 
2. Clone your repository into a directory on your local machine
4. Create a new branch - This will be where you commit your changes. _N.B: You should not change the code on the master branch_
5. Push your branch to your own repository
6. Create a pull request with your branch and the master branch of the original repo
7. Cross fingers and wait
