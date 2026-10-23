from zen_api_utils.streaming.acquisition import ExperimentAcquisition


def test_acquisition_from_plan_extracts_dimensions_and_wells() -> None:
    plan = {
        "source": {"path": "example.czexp"},
        "acquisition_blocks": [
            {
                "dimensions": {"T": 2, "C": 3, "Z": 4, "S": 5, "M": 6, "ZSpacing": 1.5},
                "channels": [{"name": "DAPI", "pixel_type": "GRAY16"}],
                "positions": [{"well_id": "A01"}, {"well_id": "B02"}, {"well_id": "A01"}],
                "split_scenes_in_separate_files": True,
            }
        ],
    }

    result = ExperimentAcquisition.from_plan(plan)

    assert result.experiment_name == "example"
    assert result.dimensions.channels == 3
    assert result.dimensions.tiles == 6
    assert result.well_ids == ("A01", "B02")
    assert result.well_count == 2
