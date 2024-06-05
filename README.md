

# Essay Grader

1. 確定自己的路徑在 essay-grader/ 下

2. 確定自己有client_secret_desktop.json檔案，並放在essay-grader/private下

3. 確定自己有把 `.env` 檔案放在 essay-grader/private 下 (或是改用export OPENAI_API_KEY=sk-proj-xxx)

```
OPENAI_API_KEY=sk-proj-
```

4. 安裝所需套件： `poetry install`

5. 執行程式： `poetry run start`


## 沒有Poetry的安裝方式

1. 安裝所需套件

```bash
python -m venv venv
source venv/bin/activate
export OPENAI_API_KEY=sk-proj-xxx
pip install -r requirements.txt
```

2. 執行程式

```bash
python -m essay_judge.interface
```
