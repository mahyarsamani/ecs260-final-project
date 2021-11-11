## Instructions to run Mahyar's code
```sh
sudo apt install virtualenv
git clone https://github.com/PyGithub/PyGithub.git
virtualenv -p python3 venv
```
Now append the following line to ```venv/bin/activate```:

```sh
export GITHUB_TOKEN="[your github token]"
```
After do the following:
```sh
source venv/bin/activate
pip install -e PyGithub
python process_issues.py [name of the repo] [output name]
```