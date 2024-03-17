# Workerflow Executor Worker

This component runs on worker nodes to execute tasks that are handed through workflow executor's task manager.

Tasks are run using celery. Results are posted back using a separate rabbitmq queue.


# Running

In development the `.env` file at project root is used. In production set the env variable `WE_WORKER_ENV_FILE` to point to the env file. The `WE_WORKER_ENV_FILE` env variable takes precedence over the .env file in project root folder.
