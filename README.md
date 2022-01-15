# QSIQC: Predict diffusion MRI quality ratings

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/richford/qsiqc/main/app.py)

This repository hosts a web app and docker image to calculate predicted quality
control (QC) ratings for preprocessed diffusion MRI data.

## Input

The QC model expects an input CSV file containing automated QC metrics from
[QSIPrep](https://qsiprep.readthedocs.io/en/latest/). The CSV must contain at
least the following columns:

- subject_id
- raw_dimension_x
- raw_dimension_y
- raw_dimension_z
- raw_voxel_size_x
- raw_voxel_size_y
- raw_voxel_size_z
- raw_max_b
- raw_neighbor_corr
- raw_num_bad_slices
- raw_num_directions
- raw_coherence_index
- raw_incoherence_index
- t1_dimension_x
- t1_dimension_y
- t1_dimension_z
- t1_voxel_size_x
- t1_voxel_size_y
- t1_voxel_size_z
- t1_max_b
- t1_neighbor_corr
- t1_num_bad_slices
- t1_num_directions
- t1_coherence_index
- t1_incoherence_index
- mean_fd
- max_fd
- max_rotation
- max_translation
- max_rel_rotation
- max_rel_translation
- t1_dice_distance

## Directions

We provide two methods to produce QC ratings:

### Web-based QC prediction on Streamlit

Use our [Streamlit App](https://share.streamlit.io/richford/qsiqc/main/app.py)
to upload your CSV file and view and download the generated QC scores.

### Docker-based QC prediction

You may then execute the QSIQC docker container from any directory

```bash
docker run --rm -v "$PWD":/home ghcr.io/richford/qsiqc example_dwiqc.csv
```

where you should replace `example_dwiqc.csv` with the name of your input CSV file. This will use the default tag `latest`. To use a different tag, append the tag name to the image name, e.g. `ghcr.io/richford/qsiqc:v0.1`
