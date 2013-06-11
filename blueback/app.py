import blueback.config
from blueback.job import Job

def run():
    configs = blueback.config.get_config()

    for config in configs:
        job = Job(config)
        job.run()


if __name__ == "__main__":
    run()
