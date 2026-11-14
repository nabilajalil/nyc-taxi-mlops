from src.train_compare import candidates
from src.features import make_features


def test_three_candidates_have_same_prediction_interface():
    models = candidates()
    assert set(models) == {"ridge", "random_forest", "hist_gradient_boosting"}
    for pipeline in models.values():
        assert "preprocess" in pipeline.named_steps
        assert "model" in pipeline.named_steps


def test_features_for_candidate_models():
    x = make_features(161, 132, 8, 0)
    assert list(x.columns) == ["PULocationID", "DOLocationID", "pickup_hour", "day_of_week"]
