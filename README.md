# Github repo watcher
## License
MIT License.
## Status
A working skeleton missing actual API calls.
## Usage
### Sensitive settings
Edit `.secrets.yaml` in the project root folder.
```yaml
default:
  github:
    user: GITHUB_USER
    token: GITHUB_TOKEN
```
Alternatively, you can set shell variables `GITHUBWATCHER_GITHUB__USER` and `GITHUBWATCHER_GITHUB__TOKEN` before running the script.
### Installing
In a directory one level above the project:
```shell
python -m venv .
. bin/activate
cd github-watcher
pip install -r requirements.txt
```
### Docker
```shell
docker build -t YOUR_NAME/github-watcher --network host  .
```
### Upgrading requirements
```
pip-compile --upgrade
```
### Running tests
```shell
./tests.sh
```
### Running
```shell
GITHUBWATCHER_GITHUB__REPO='repo_of_interest' ./main.py
```
