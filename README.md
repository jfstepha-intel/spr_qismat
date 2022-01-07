1/7/22 - Had to re-migrate again because it was screwed up the first time.

Migrated from gitlab to github https://github.com/jfstepha-intel/spr_qismat.git

# Sapphire Rapids QISMAT

## How to create a repository like this:

- Setup and run pyQismat and PyCharm as per instructions in that repo.
- Get access to gitlab.devtools.intel.com
- Create a new repository
- PyCharm: VCS -> Chechout From Version Control -> GIT -> Enter URL and directory path
- Create the submodule:
  - In bash window: (Windows Start->GIT bash)
    ```
    cd your/project/directory
    git clone ssh://git@gitlab.devtools.intel.com:29418/jfstepha/pyQismat.git pyQISMAT
    git submodule init
    git submodule update
    ```
- PyCharm ->  settings -> Project -> project structure -> right click on pyQismat in the center pane, and select "sources"

