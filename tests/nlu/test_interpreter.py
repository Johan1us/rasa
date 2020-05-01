import rasa.nlu

import pytest

from rasa.core.interpreter import (
    NaturalLanguageInterpreter,
    RasaNLUHttpInterpreter,
    RasaNLUInterpreter,
    RegexInterpreter,
)
from rasa.model import get_model_subdirectories, get_model
from rasa.nlu import registry, training_data
from rasa.nlu.model import Interpreter
from rasa.utils.endpoints import EndpointConfig
from tests.nlu import utilities

#
# @pytest.mark.parametrize(
#     "pipeline_template", list(registry.registered_pipeline_templates.keys())
# )
# async def test_interpreter_on_pipeline_templates(
#     pipeline_template, component_builder, tmpdir
# ):
#     test_data = "data/examples/rasa/demo-rasa.json"
#
#     config = utilities.base_test_conf(pipeline_template)
#     config["data"] = test_data
#
#     td = training_data.load_data(test_data)
#
#     interpreter = await utilities.interpreter_for(
#         component_builder, "data/examples/rasa/demo-rasa.json", tmpdir.strpath, config
#     )
#
#     texts = ["good bye", "i am looking for an indian spot"]
#
#     for text in texts:
#         result = interpreter.parse(text, time=None)
#         assert result["text"] == text
#         assert not result["intent"]["name"] or result["intent"]["name"] in td.intents
#         assert result["intent"]["confidence"] >= 0
#         # Ensure the model doesn't detect entity types that are not present
#         # Models on our test data set are not stable enough to
#         # require the exact entities to be found
#         for entity in result["entities"]:
#             assert entity["entity"] in td.entities


@pytest.mark.parametrize(
    "metadata",
    [
        {"rasa_version": "0.11.0"},
        {"rasa_version": "0.10.2"},
        {"rasa_version": "0.12.0a1"},
        {"rasa_version": "0.12.2"},
        {"rasa_version": "0.12.3"},
        {"rasa_version": "0.13.3"},
        {"rasa_version": "0.13.4"},
        {"rasa_version": "0.13.5"},
        {"rasa_version": "0.14.0a1"},
        {"rasa_version": "0.14.0"},
        {"rasa_version": "0.14.1"},
        {"rasa_version": "0.14.2"},
        {"rasa_version": "0.14.3"},
        {"rasa_version": "0.14.4"},
        {"rasa_version": "0.15.0a1"},
        {"rasa_version": "1.0.0a1"},
        {"rasa_version": "1.5.0"},
    ],
)
def test_model_is_not_compatible(metadata):
    with pytest.raises(rasa.nlu.model.UnsupportedModelError):
        Interpreter.ensure_model_compatibility(metadata)


@pytest.mark.parametrize("metadata", [{"rasa_version": rasa.__version__}])
def test_model_is_compatible(metadata):
    # should not raise an exception
    assert Interpreter.ensure_model_compatibility(metadata) is None


@pytest.mark.parametrize(
    "parameters",
    [
        {
            "obj": "not-existing",
            "endpoint": EndpointConfig(url="http://localhost:8080/"),
            "type": RasaNLUHttpInterpreter,
        },
        {
            "obj": "trained_nlu_model",
            "endpoint": EndpointConfig(url="http://localhost:8080/"),
            "type": RasaNLUHttpInterpreter,
        },
        {"obj": "trained_nlu_model", "endpoint": None, "type": RasaNLUInterpreter},
        {"obj": "not-existing", "endpoint": None, "type": RegexInterpreter},
    ],
)
def test_create_interpreter(parameters, trained_nlu_model):
    obj = parameters["obj"]
    if obj == "trained_nlu_model":
        _, obj = get_model_subdirectories(get_model(trained_nlu_model))

    interpreter = NaturalLanguageInterpreter.create(parameters["endpoint"] or obj)

    assert isinstance(interpreter, parameters["type"])
