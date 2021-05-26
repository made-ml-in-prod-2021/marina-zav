import click

from ml_project.data import read_data
from ml_project.models.model_fit_predict import deserialize_model, predict_model
from ml_project.utils import init_logger

logger = init_logger("logger")


def predict(model, input_df, output_data_path):
    predicts = predict_model(model, input_df)
    input_df["predict"] = predicts
    input_df.to_csv(output_data_path, index=False)
    logger.info(f"predicts saved to {output_data_path}")


def predict_pipeline(model_path: str, input_data_path: str, output_data_path: str):
    logger.info(
        f"start predict pipeline. model_path {model_path}, input_data_path {input_data_path}, "
        f"output_data_path {output_data_path}"
    )
    model = deserialize_model(model_path)

    input_data = read_data(input_data_path)

    predict(model, input_data, output_data_path)

    logger.info("end predict pipeline.")


@click.command(name="predict_pipeline")
@click.argument("model_path")
@click.argument("input_data_path")
@click.argument("output_data_path")
def predict_pipeline_command(
    model_path: str, input_data_path: str, output_data_path: str
):
    predict_pipeline(model_path, input_data_path, output_data_path)


if __name__ == "__main__":
    predict_pipeline_command()
