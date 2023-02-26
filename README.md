# lynx-scene-host
- [lynx-scene-host](#lynx-scene-host)
  - [python-common managment](#python-common-managment)


## python-common managment

Execution of python code inside `execution-engine` requires some knowledge of structures used in *lynx* project
which are included in [lynx-python-common](https://github.com/group-project-gut/lynx-python-common). This project imports them by using `git subtree mechanism`.

In order to pull commits from the repository use following commandline

```bash
git subtree pull --prefix src/deps https://github.com/group-project-gut/lynx-python-common.git master --squash
```

The next step is to install `lynx-python-common` python package to your env:

```bash
cd src/deps
pip install -e .
```
