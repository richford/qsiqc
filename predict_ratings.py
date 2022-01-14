#!/opt/conda/bin/python

import click
import os
import os.path as op
import pandas as pd

from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier


def get_voting_classifier():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    xgb_model_dir = op.join(dir_path, "saved_models")
    models = {}
    xgb_model_files = sorted(
        [fname for fname in os.listdir(xgb_model_dir) if fname.endswith(".json")]
    )

    for fname in xgb_model_files:
        xgb = XGBClassifier()
        xgb.load_model(op.join(xgb_model_dir, fname))
        cv_idx = int(fname.split(".json")[0][-1])
        models[cv_idx] = xgb

    weights = {
        0: 0.9439393939393939,
        1: 0.9237373737373737,
        2: 0.8603174603174604,
        3: 0.8818181818181818,
        4: 0.907070707070707,
        5: 0.9312169312169312,
    }

    estimators = {f"cv{i}": models[i] for i in weights.keys()}
    voter = VotingClassifier(
        estimators=estimators, weights=list(weights.values()), voting="soft"
    )
    voter.estimators_ = list(estimators.values())
    voter.le_ = LabelEncoder().fit([0, 1])
    voter.classes_ = voter.le_.classes_

    return voter


def predict_ratings(input_df):
    expected_columns = [
        "raw_dimension_x",
        "raw_dimension_y",
        "raw_dimension_z",
        "raw_voxel_size_x",
        "raw_voxel_size_y",
        "raw_voxel_size_z",
        "raw_max_b",
        "raw_neighbor_corr",
        "raw_num_bad_slices",
        "raw_num_directions",
        "raw_coherence_index",
        "raw_incoherence_index",
        "t1_dimension_x",
        "t1_dimension_y",
        "t1_dimension_z",
        "t1_voxel_size_x",
        "t1_voxel_size_y",
        "t1_voxel_size_z",
        "t1_max_b",
        "t1_neighbor_corr",
        "t1_num_bad_slices",
        "t1_num_directions",
        "t1_coherence_index",
        "t1_incoherence_index",
        "mean_fd",
        "max_fd",
        "max_rotation",
        "max_translation",
        "max_rel_rotation",
        "max_rel_translation",
        "t1_dice_distance",
    ]

    try:
        df_qc = input_df[expected_columns]
    except KeyError:
        raise ValueError(
            "Columns in input file do not match expected columns."
            f"Expected: {expected_columns}, "
            f"but got: {df_qc.columns.tolist()}"
        )

    voter = get_voting_classifier()
    ratings = voter.predict_proba(df_qc)[:, 1]
    df_ratings = pd.DataFrame(index=df_qc.index)
    df_ratings["rating"] = ratings
    return df_ratings


@click.command()
@click.option("--output_csv", default="output.csv")
@click.argument("input_csv", type=click.Path(exists=True, dir_okay=False))
def main(output_csv, input_csv):
    input_df = pd.read_csv(input_csv, index_col="subject_id")

    df_ratings = predict_ratings(input_df)
    df_ratings.to_csv(op.join(op.dirname(input_csv), output_csv))


if __name__ == "__main__":
    main()