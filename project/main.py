from datetime import datetime

from loguru import logger

if __name__ == "__main__":
    from project.pipeline import Pipeline
    from project.scripts.generate_datas import generate_datas

    logger.info("Generating datas for 2024-01-01 to 2024-01-10")
    generate_datas()

    logger.info("Running pipeline for 2024-01-01")
    Pipeline(datetime(2024, 1, 1)).run()
