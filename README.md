# Emergent taxonomy generator

![alt text](https://github.com/UNDP-Accelerator-Labs/Raving-AI-Panama/blob/main/flask_app/static/img/preview.png)

## Steps

### Creating a database and generating synthetic content

If you do have access to data, you can skip this section and move straight to the next one.

#### 1- Create the database
The first step is to create a database (DB). By default, this application will look for a `PostgreSQL` DB named `raving_ai_panama`. You can chose any other name, but be sure to either:
- update the default `db` argument value in the `connect` function in `db/connect.py`; or
- pass your `db` name as an argument in the call to `connect(db={your_db_name})` in the `init()` function in `db/init_db.py`

At this point, you do not need to create any tables inside the DB. These will automatically be created later on. However, if you really want to initiate the DB now, e.g., to see the full schema, you can run `db/init_db.py`.

#### 2- Generate the data
Now that the database is created, the next step is to generate the data.

Note that the generator relies on `ollama` and, by default, `llama3.1:8B`. You can configure this by either:
- changing the default `model` keyword argument value in the `generate_response` function in `generate_data/generate.py`; or
- passing any model you like in the `generate_data/__main__py` call to the `generate_response` function.

Importantly, be sure to use an `ollama` compatible model. You can browse models on the official [Ollama website](https://ollama.com/search).

Once you are happy with the model selection, simply run `python3 generate_data/ {n}`, passing the `n: int` argument to set the number of data points you would like to generate.

### Generating keywords

Note that to run `KeyBERT`, you need `numpy<2`. You may need to force this using the following command:
```
pip install --force-reinstall -v "numpy<2"
```

`LLM/embed.py` requires an ollama compatible embedding model. By default it uses `nomic-embed-text`.