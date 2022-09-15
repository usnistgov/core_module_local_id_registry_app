""" Test units
"""

import json
from unittest.case import TestCase
from unittest.mock import patch, Mock

from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_module_local_id_registry_app.views.views import LocalIdRegistryModule
from tests import test_settings
from tests.views.LocalIdRegistryModule.fixtures import (
    MockPID,
    MockResponse,
    mock_return_fn_args_as_dict,
    MockProvider,
    MockData,
    MockDataStructureApi,
)


class TestLocalIdRegistryModuleInitDefault(TestCase):
    """Test Local Id Registry Module Init Default"""

    def test_error_data_is_none(self):
        """test_error_data_is_none"""

        local_id_module = LocalIdRegistryModule()
        self.assertIsNone(local_id_module.error_data)

    @patch(
        "core_parser_app.tools.modules.views.builtin.input_module."
        "AbstractInputModule.__init__"
    )
    def test_abstract_input_module_init_called(self, mock_abstract_input_module_init):
        """test_abstract_input_module_init_called"""

        LocalIdRegistryModule()
        mock_abstract_input_module_init.assert_called()


class TestLocalIdRegistryModuleInitWithPID(TestCase):
    """Test Local Id Registry Module Init With PID"""

    def setUp(self) -> None:
        if "core_linked_records_app" not in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.append("core_linked_records_app")

        self.module = LocalIdRegistryModule()

    def test_placeholder_is_initialized(self):
        """test_placeholder_is_initialized"""

        self.assertIsNotNone(self.module.placeholder)

    def test_styles_is_initialized(self):
        """test_styles_is_initialized"""

        self.assertEqual(len(self.module.styles), 1)

    def test_scripts_is_initialized(self):
        """test_scripts_is_initialized"""

        self.assertEqual(len(self.module.scripts), 2)

    def test_disabled_is_initialized(self):
        """test_disabled_is_initialized"""

        self.assertFalse(self.module.disabled)

    def test_pid_settings_is_initialized(self):
        """test_pid_settings_is_initialized"""

        self.assertEqual(
            self.module.pid_settings,
            {
                "xpath": test_settings.PID_XPATH,
                "format": test_settings.PID_FORMAT,
                "system": test_settings.ID_PROVIDER_SYSTEM_NAME,
                "prefixes": test_settings.ID_PROVIDER_PREFIXES,
            },
        )


class TestLocalIdRegistryModuleInitWithoutPID(TestCase):
    """Test Local Id Registry Module Init Without PID"""

    def setUp(self) -> None:
        while "core_linked_records_app" in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.remove("core_linked_records_app")

        self.module = LocalIdRegistryModule()

    def test_placeholder_is_initialized(self):
        """test_placeholder_is_initialized"""

        self.assertIsNone(self.module.placeholder)

    def test_styles_is_initialized(self):
        """test_styles_is_initialized"""

        self.assertEqual(len(self.module.styles), 0)

    def test_scripts_is_initialized(self):
        """test_scripts_is_initialized"""

        self.assertEqual(len(self.module.scripts), 1)

    def test_disabled_is_initialized(self):
        """test_disabled_is_initialized"""

        self.assertTrue(self.module.disabled)

    def test_pid_settings_is_initialized(self):
        """test_pid_settings_is_initialized"""

        self.assertIsNone(self.module.pid_settings)


class TestLocalIdRegistryModuleInitPrefixAndRecord(TestCase):
    """Test Local Id Registry Module Init Prefix And Record"""

    @classmethod
    def setUpClass(cls) -> None:
        if "core_linked_records_app" not in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.append("core_linked_records_app")

    def setUp(self) -> None:
        patch_provider_manager = patch(
            "core_linked_records_app.utils.providers.ProviderManager.get",
            return_value=MockProvider(),
        )
        patch_provider_manager.start()
        self.addCleanup(patch_provider_manager.stop)

        self.module = LocalIdRegistryModule()

    @staticmethod
    def set_default_test_data(as_string=False):
        """set_default_test_data"""

        mock_data = MockPID() if not as_string else str(MockPID())
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        return [mock_data, mock_curate_data_structure_id, mock_user]

    def test_incorrect_host_url_sets_prefix_to_none(self):
        """test_incorrect_host_url_sets_prefix_to_none"""

        mock_data = "mock_incorrect_url"
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )

        self.assertIsNone(self.module.default_prefix)

    def test_incorrect_host_url_sets_value_to_none(self):
        """test_incorrect_host_url_sets_value_to_none"""

        mock_data = "mock_incorrect_url"
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )

        self.assertIsNone(self.module.default_value)

    def test_incorrect_host_url_sets_error_data(self):
        """test_incorrect_host_url_sets_error_data"""

        mock_data = "mock_incorrect_url"
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )

        self.assertEqual(self.module.error_data, mock_data)

    @patch("core_module_local_id_registry_app.views.views.curate_data_structure_api")
    def test_correct_url_sets_correct_prefix(self, mock_curate_data_structure_api):
        """test_correct_url_sets_correct_prefix"""

        mock_curate_data_structure_api.return_value = None
        mock_data = MockPID()
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            str(mock_data), mock_curate_data_structure_id, mock_user
        )

        self.assertEqual(self.module.default_prefix, mock_data.prefix)

    @patch("core_module_local_id_registry_app.views.views.curate_data_structure_api")
    def test_correct_url_sets_correct_value(self, mock_curate_data_structure_api):
        """test_correct_url_sets_correct_value"""

        mock_curate_data_structure_api.return_value = None
        mock_data = MockPID()
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            str(mock_data), mock_curate_data_structure_id, mock_user
        )
        self.assertEqual(self.module.default_value, mock_data.value)

    def test_settings_host_url_uses_default_system(self):
        """test_settings_host_url_uses_default_system"""

        mock_data = str(MockPID(provider="mock_not_default_provider"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertEqual(self.module.error_data, mock_data)

    def test_settings_host_url_does_not_end_with_slash(self):
        """test_settings_host_url_does_not_end_with_slash"""

        mock_data = str(MockPID())
        mock_data = "%s/" % mock_data if mock_data[-1] != "/" else mock_data

        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertEqual(self.module.error_data, mock_data)

    def test_settings_host_url_not_equals_to_record_host_url_sets_prefix_to_none(self):
        """test_settings_host_url_not_equals_to_record_host_url_sets_prefix_to_none"""

        mock_data = str(MockPID(provider="mock_not_default_provider"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertIsNone(self.module.default_prefix)

    def test_settings_host_url_not_equals_to_record_host_url_sets_value_to_none(self):
        """test_settings_host_url_not_equals_to_record_host_url_sets_value_to_none"""

        mock_data = str(MockPID(provider="mock_not_default_provider"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertIsNone(self.module.default_value)

    def test_settings_host_url_not_equals_to_record_host_url_sets_error_data(self):
        """test_settings_host_url_not_equals_to_record_host_url_sets_error_data"""

        mock_data = str(MockPID(provider="mock_not_default_provider"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertIsNotNone(self.module.error_data)

    def test_invalid_prefix_keeps_prefix(self):
        """test_invalid_prefix_keeps_prefix"""

        mock_data = str(MockPID(prefix="invalid_prefix"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertIsNotNone(self.module.default_prefix)

    def test_invalid_prefix_keeps_value(self):
        """test_invalid_prefix_keeps_value"""

        mock_data = str(MockPID(prefix="invalid_prefix"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertIsNotNone(self.module.default_value)

    def test_invalid_prefix_sets_error_data(self):
        """test_invalid_prefix_sets_error_data"""

        mock_data = str(MockPID(prefix="invalid_prefix"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertEqual(self.module.error_data, mock_data)

    def test_invalid_format_keeps_prefix(self):
        """test_invalid_format_keeps_prefix"""

        mock_data = str(MockPID(value="$invalid_value"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertIsNotNone(self.module.default_prefix)

    def test_invalid_format_keeps_value(self):
        """test_invalid_format_keeps_value"""

        mock_data = str(MockPID(value="$invalid_value"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertIsNotNone(self.module.default_value)

    def test_invalid_format_sets_error_data(self):
        """test_invalid_format_sets_error_data"""

        mock_data = str(MockPID(value="$invalid_value"))
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            mock_data, mock_curate_data_structure_id, mock_user
        )
        self.assertEqual(self.module.error_data, mock_data)

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_module_local_id_registry_app.views.views.curate_data_structure_api")
    def test_unexisting_record_keeps_prefix(
        self, mock_curate_data_structure_api, mock_send_get_request
    ):
        """test_unexisting_record_keeps_prefix"""

        mock_curate_data_structure_api.return_value = None
        mock_send_get_request.return_value = MockResponse(text="", status_code=404)

        self.module._init_prefix_and_record(*self.set_default_test_data(as_string=True))
        self.assertIsNotNone(self.module.default_prefix)

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_module_local_id_registry_app.views.views.curate_data_structure_api")
    def test_unexisting_record_keeps_value(
        self, mock_curate_data_structure_api, mock_send_get_request
    ):
        """test_unexisting_record_keeps_value"""

        mock_curate_data_structure_api.return_value = None
        mock_send_get_request.return_value = MockResponse(text="", status_code=404)

        self.module._init_prefix_and_record(*self.set_default_test_data(as_string=True))
        self.assertIsNotNone(self.module.default_value)

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_module_local_id_registry_app.views.views.curate_data_structure_api")
    def test_unexisting_record_sets_error_data_to_none(
        self, mock_curate_data_structure_api, mock_send_get_request
    ):
        """test_unexisting_record_sets_error_data_to_none"""

        mock_curate_data_structure_api.return_value = None
        mock_send_get_request.return_value = MockResponse(text="", status_code=404)

        self.module._init_prefix_and_record(*self.set_default_test_data(as_string=True))
        self.assertIsNone(self.module.error_data)

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    @patch("core_linked_records_app.utils.dict.get_value_from_dot_notation")
    def test_editing_existing_record_keeps_prefix(
        self,
        mock_get_value_from_dot_notation,
        mock_curate_data_structure_api_get_by_id,
        mock_send_get_request,
    ):
        """test_editing_existing_record_keeps_prefix"""

        mock_data = MockData()
        mock_send_get_request.return_value = MockResponse(
            text=json.dumps(mock_data.to_json()), status_code=200
        )
        mock_curate_data_structure_api_get_by_id.return_value = MockDataStructureApi(
            data=mock_data
        )
        mock_get_value_from_dot_notation.return_value = str(MockPID())

        self.module._init_prefix_and_record(*self.set_default_test_data(as_string=True))

        self.assertEqual(
            self.module.default_prefix, self.set_default_test_data()[0].prefix
        )

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    @patch("core_linked_records_app.utils.dict.get_value_from_dot_notation")
    def test_editing_existing_record_keeps_value(
        self,
        mock_get_value_from_dot_notation,
        mock_curate_data_structure_api_get_by_id,
        mock_send_get_request,
    ):
        """test_editing_existing_record_keeps_value"""

        mock_data = MockData()
        mock_send_get_request.return_value = MockResponse(
            text=json.dumps(mock_data.to_json()), status_code=200
        )
        mock_curate_data_structure_api_get_by_id.return_value = MockDataStructureApi(
            data=mock_data
        )
        mock_get_value_from_dot_notation.return_value = str(MockPID())

        self.module._init_prefix_and_record(*self.set_default_test_data(as_string=True))

        self.assertEqual(
            self.module.default_value, self.set_default_test_data()[0].value
        )

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    @patch("core_linked_records_app.utils.dict.get_value_from_dot_notation")
    def test_editing_existing_record_sets_error_data_to_none(
        self,
        mock_get_value_from_dot_notation,
        mock_curate_data_structure_api_get_by_id,
        mock_send_get_request,
    ):
        """test_editing_existing_record_sets_error_data_to_none"""

        mock_data = {"id": "mock_id", "dict_content": {}}
        mock_send_get_request.return_value = MockResponse(
            text=json.dumps(mock_data), status_code=200
        )
        mock_curate_data_structure_api_get_by_id.return_value = {"data": mock_data}
        mock_get_value_from_dot_notation.return_value = str(MockPID())

        self.module._init_prefix_and_record(*self.set_default_test_data(as_string=True))

        self.assertIsNone(self.module.error_data)

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    @patch("core_linked_records_app.utils.dict.get_value_from_dot_notation")
    def test_duplicate_pid_keeps_prefix(
        self,
        mock_get_value_from_dot_notation,
        mock_curate_data_structure_api_get_by_id,
        mock_send_get_request,
    ):
        """test_duplicate_pid_keeps_prefix"""

        mock_data_1 = MockData(pk=1)
        mock_data_2 = MockData(pk=2)
        mock_send_get_request.return_value = MockResponse(
            text=json.dumps(mock_data_1.to_json()), status_code=200
        )
        mock_curate_data_structure_api_get_by_id.return_value = MockDataStructureApi(
            data=mock_data_2
        )
        mock_get_value_from_dot_notation.return_value = str(
            MockPID(prefix="mock_prefix_2", value="mock_record_2")
        )

        mock_data = MockPID()
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            str(mock_data), mock_curate_data_structure_id, mock_user
        )

        self.assertEqual(self.module.default_prefix, mock_data.prefix)

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    @patch("core_linked_records_app.utils.dict.get_value_from_dot_notation")
    def test_duplicate_pid_keeps_value(
        self,
        mock_get_value_from_dot_notation,
        mock_curate_data_structure_api_get_by_id,
        mock_send_get_request,
    ):
        """test_duplicate_pid_keeps_value"""

        mock_data_1 = MockData(pk=1)
        mock_data_2 = MockData(pk=2)
        mock_send_get_request.return_value = MockResponse(
            text=json.dumps(mock_data_1.to_json()), status_code=200
        )
        mock_curate_data_structure_api_get_by_id.return_value = MockDataStructureApi(
            data=mock_data_2
        )
        mock_get_value_from_dot_notation.return_value = str(
            MockPID(prefix="mock_prefix_2", value="mock_record_2")
        )

        mock_data = MockPID()
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            str(mock_data), mock_curate_data_structure_id, mock_user
        )

        self.assertEqual(self.module.default_value, mock_data.value)

    @patch("core_module_local_id_registry_app.views.views.send_get_request")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    @patch("core_linked_records_app.utils.dict.get_value_from_dot_notation")
    def test_duplicate_pid_sets_error_data(
        self,
        mock_get_value_from_dot_notation,
        mock_curate_data_structure_api_get_by_id,
        mock_send_get_request,
    ):
        """test_duplicate_pid_sets_error_data"""

        mock_data_1 = MockData(pk=1)
        mock_data_2 = MockData(pk=2)
        mock_send_get_request.return_value = MockResponse(
            text=json.dumps(mock_data_1.to_json()), status_code=200
        )
        mock_curate_data_structure_api_get_by_id.return_value = MockDataStructureApi(
            data=mock_data_2
        )
        mock_get_value_from_dot_notation.return_value = str(
            MockPID(prefix="mock_prefix_2", value="mock_record_2")
        )

        mock_data = MockPID()
        mock_curate_data_structure_id = 1
        mock_user = create_mock_user("1")

        self.module._init_prefix_and_record(
            str(mock_data), mock_curate_data_structure_id, mock_user
        )

        self.assertEqual(self.module.error_data, str(mock_data))


class TestLocalIdRegistryModuleGetRetrieveDataWithPID(TestCase):
    """Test Local Id Registry Module Get Retrieve Data With PID"""

    def setUp(self) -> None:
        if "core_linked_records_app" not in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.append("core_linked_records_app")

        patch_provider_manager = patch(
            "core_linked_records_app.utils.providers.ProviderManager.get",
            return_value=MockProvider(),
        )
        patch_provider_manager.start()
        self.addCleanup(patch_provider_manager.stop)

        self.module = LocalIdRegistryModule()

        self.request = Mock()
        self.request.method = "GET"
        self.request.GET = dict()
        self.request.build_absolute_uri = lambda char: ""

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    def test_data_set_to_default_if_not_in_request(
        self, mock_get_curate_datastructure_from_module_id
    ):
        """test_data_set_to_default_if_not_in_request"""

        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        result = self.module._retrieve_data(self.request)

        self.assertEqual(result, "")

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_data_is_set_to_request_param(
        self, mock_init_prefix_and_record, mock_get_curate_datastructure_from_module_id
    ):
        """test_data_is_set_to_request_param"""

        mock_request_data = "mock_data"
        mock_init_prefix_and_record.return_value = mock_request_data
        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        self.request.GET["data"] = mock_request_data

        result = self.module._retrieve_data(self.request)

        self.assertEqual(result, mock_request_data)

    @patch("core_module_local_id_registry_app.views.views.generate_unique_local_id")
    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    def test_generate_unique_local_id_not_called(
        self,
        mock_get_curate_datastructure_from_module_id,
        mock_generate_unique_local_id,
    ):
        """test_generate_unique_local_id_not_called"""

        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        self.module._retrieve_data(self.request)

        self.assertFalse(mock_generate_unique_local_id.called)

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_value_is_set_to_data(
        self, mock_init_prefix_and_record, mock_get_curate_datastructure_from_module_id
    ):
        """test_value_is_set_to_data"""

        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        mock_request_data = "mock_data"
        self.request.GET["data"] = mock_request_data
        self.module._retrieve_data(self.request)

        self.assertEqual(self.module.default_value, mock_request_data)

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_init_prefix_and_record_called_if_data_is(
        self, mock_init_prefix_and_record, mock_get_curate_datastructure_from_module_id
    ):
        """test_init_prefix_and_record_called_if_data_is"""

        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        mock_request_data = "mock_data"
        self.request.GET["data"] = mock_request_data
        self.module._retrieve_data(self.request)

        self.assertTrue(mock_init_prefix_and_record.called)

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_init_prefix_and_record_called_if_data_is_none(
        self, mock_init_prefix_and_record, mock_get_curate_datastructure_from_module_id
    ):
        """test_init_prefix_and_record_called_if_data_is_none"""

        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        self.module._retrieve_data(self.request)

        self.assertTrue(mock_init_prefix_and_record.called)


class TestLocalIdRegistryModuleGetRetrieveDataWithoutPID(TestCase):
    """Test Local Id Registry Module Get Retrieve Data Without PID"""

    def setUp(self) -> None:
        while "core_linked_records_app" in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.remove("core_linked_records_app")

        self.module = LocalIdRegistryModule()

        self.request = Mock()
        self.request.method = "GET"
        self.request.GET = dict()

    @patch("core_module_local_id_registry_app.views.views.generate_unique_local_id")
    def test_data_is_set_if_not_in_request(self, mock_generate_unique_local_id):
        """test_data_is_set_if_not_in_request"""

        mock_generated_data = "mock_generated_data"
        mock_generate_unique_local_id.return_value = mock_generated_data
        result = self.module._retrieve_data(self.request)

        self.assertEqual(result, mock_generated_data)

    def test_data_is_set_to_request_param(self):
        """test_data_is_set_to_request_param"""

        mock_request_data = "mock_data"
        self.request.GET["data"] = mock_request_data

        result = self.module._retrieve_data(self.request)

        self.assertEqual(result, mock_request_data)

    @patch("core_module_local_id_registry_app.views.views.generate_unique_local_id")
    def test_generate_unique_local_id_called(self, mock_generate_unique_local_id):
        """test_generate_unique_local_id_called"""

        self.module._retrieve_data(self.request)

        self.assertTrue(mock_generate_unique_local_id.called)

    def test_value_is_set_to_data(self):
        """test_value_is_set_to_data"""

        mock_request_data = "mock_data"
        self.request.GET["data"] = mock_request_data

        self.module._retrieve_data(self.request)

        self.assertEqual(self.module.default_value, mock_request_data)

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_init_prefix_and_record_not_called_if_data_is_set(
        self, mock_init_prefix_and_record
    ):
        """test_init_prefix_and_record_not_called_if_data_is_set"""

        mock_request_data = "mock_data"
        self.request.GET["data"] = mock_request_data

        self.module._retrieve_data(self.request)

        self.assertFalse(mock_init_prefix_and_record.called)


class TestLocalIdRegistryModulePostRetrieveDataWithPID(TestCase):
    """Test Local Id Registry Module Post Retrieve Data With PID"""

    def setUp(self) -> None:
        if "core_linked_records_app" not in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.append("core_linked_records_app")

        patch_provider_manager = patch(
            "core_linked_records_app.utils.providers.ProviderManager.get",
            return_value=MockProvider(),
        )
        patch_provider_manager.start()
        self.addCleanup(patch_provider_manager.stop)

        self.module = LocalIdRegistryModule()

        self.request = Mock()
        self.request.method = "POST"
        self.request.POST = {"module_id": 1}
        self.request.build_absolute_uri = lambda char: ""

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    def test_data_set_to_default_if_not_in_request(
        self, mock_get_curate_datastructure_from_module_id
    ):
        """test_data_set_to_default_if_not_in_request"""

        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        result = self.module._retrieve_data(self.request)

        self.assertEqual(result, "")

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_data_is_set_to_request_param(
        self, mock_init_prefix_and_record, mock_get_curate_datastructure_from_module_id
    ):
        """test_data_is_set_to_request_param"""

        mock_data = "mock_data"
        mock_init_prefix_and_record.return_value = mock_data
        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        self.request.POST["data"] = mock_data
        result = self.module._retrieve_data(self.request)

        self.assertEqual(result, mock_data)

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_init_prefix_and_record_called_if_data_is_set(
        self, mock_init_prefix_and_record, mock_get_curate_datastructure_from_module_id
    ):
        """test_init_prefix_and_record_called_if_data_is_set"""

        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        mock_data = "mock_data"
        self.request.POST["data"] = mock_data
        self.module._retrieve_data(self.request)

        self.assertTrue(mock_init_prefix_and_record.called)

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_get_curate_datastructure_from_module_id"
    )
    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_init_prefix_and_record_called_if_data_none(
        self, mock_init_prefix_and_record, mock_get_curate_datastructure_from_module_id
    ):
        """test_init_prefix_and_record_called_if_data_none"""

        mock_get_curate_datastructure_from_module_id.return_value = Mock(
            spec=CurateDataStructure
        )
        self.module._retrieve_data(self.request)

        self.assertTrue(mock_init_prefix_and_record.called)


class TestLocalIdRegistryModulePostRetrieveDataWithoutPID(TestCase):
    """Test Local Id Registry Module Post Retrieve Data Without PID"""

    def setUp(self) -> None:
        while "core_linked_records_app" in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.remove("core_linked_records_app")

        self.module = LocalIdRegistryModule()

        self.request = Mock()
        self.request.method = "POST"
        self.request.POST = dict()

    def test_data_none_if_not_in_request(self):
        """test_data_none_if_not_in_request"""

        result = self.module._retrieve_data(self.request)

        self.assertIsNone(result)

    def test_data_is_set_to_request_param(self):
        """test_data_is_set_to_request_param"""

        mock_data = "mock_data"
        self.request.POST["data"] = mock_data
        result = self.module._retrieve_data(self.request)

        self.assertEqual(result, mock_data)

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_init_prefix_and_record_not_called_if_data_is_set(
        self, mock_init_prefix_and_record
    ):
        """test_init_prefix_and_record_not_called_if_data_is_set"""

        mock_data = "mock_data"
        self.request.POST["data"] = mock_data
        self.module._retrieve_data(self.request)
        self.module._retrieve_data(self.request)

        self.assertFalse(mock_init_prefix_and_record.called)

    @patch(
        "core_module_local_id_registry_app.views.views.LocalIdRegistryModule."
        "_init_prefix_and_record"
    )
    def test_init_prefix_and_record_not_called(self, mock_init_prefix_and_record):
        """test_init_prefix_and_record_not_called"""

        self.module._retrieve_data(self.request)

        self.assertFalse(mock_init_prefix_and_record.called)


class TestLocalIdRegistryModuleRenderDataWithPID(TestCase):
    """Test Local Id Registry Module Render Data With PID"""

    def setUp(self) -> None:
        if "core_linked_records_app" not in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.append("core_linked_records_app")

        patch_render_template = patch(
            "core_module_local_id_registry_app.views.views."
            "LocalIdRegistryModule.render_template",
            side_effect=mock_return_fn_args_as_dict,
        )
        patch_render_template.start()
        self.addCleanup(patch_render_template.stop)

        self.module = LocalIdRegistryModule()
        self.request = Mock()

    def test_no_value_and_no_error_return_info_box(self):
        """test_no_value_and_no_error_return_info_box"""

        self.module.default_value = None
        self.module.error_data = None

        result = self.module._render_data(self.request)

        self.assertEqual(result["arg1"]["type"], "info")

    def test_error_return_danger_box(self):
        """test_error_return_danger_box"""

        self.module.error_data = "mock_data"

        result = self.module._render_data(self.request)

        self.assertEqual(result["arg1"]["type"], "danger")

    def test_no_error_return_success_box(self):
        """test_no_error_return_success_box"""

        self.module.default_value = "mock_data"
        self.module.error_data = None

        result = self.module._render_data(self.request)

        self.assertEqual(result["arg1"]["type"], "success")


class TestLocalIdRegistryModuleRenderDataWithoutPID(TestCase):
    """Test Local Id Registry Module Render Data Without PID"""

    def setUp(self) -> None:
        while "core_linked_records_app" in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.remove("core_linked_records_app")

        self.module = LocalIdRegistryModule()
        self.request = Mock()

    def test_returns_empty_string(self):
        """test_returns_empty_string"""

        result = self.module._render_data(self.request)

        self.assertEqual(result, "")


class TestLocalIdRegistryModuleRenderModuleWithPID(TestCase):
    """Test Local Id Registry Module Render Module With PID"""

    @classmethod
    def setUpClass(cls) -> None:
        if "core_linked_records_app" not in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.append("core_linked_records_app")

    def setUp(self) -> None:
        self.mock_abstract_render_module = "mock_abstract_render_module"
        patch_render_module = patch(
            "core_module_local_id_registry_app.views.views."
            "AbstractInputModule._render_module",
            return_value=self.mock_abstract_render_module,
        )
        patch_render_module.start()
        self.addCleanup(patch_render_module.stop)

        patch_render_template = patch(
            "core_module_local_id_registry_app.views.views."
            "AbstractInputModule.render_template",
            side_effect=mock_return_fn_args_as_dict,
        )
        patch_render_template.start()
        self.addCleanup(patch_render_template.stop)

        patch_provider_manager = patch(
            "core_linked_records_app.utils.providers.ProviderManager.get",
            return_value=MockProvider(),
        )
        patch_provider_manager.start()
        self.addCleanup(patch_provider_manager.stop)

        self.module = LocalIdRegistryModule()
        self.module.default_prefix = "mock_default_prefix"
        self.request = Mock()

    def test_context_pid_host_does_not_contains_final_slash(self):
        """test_context_pid_host_does_not_contains_final_slash"""

        result = self.module._render_module(self.request)

        self.assertNotEqual(result["context"]["pid_host_url"][-1], "/")

    def test_context_contains_input_module(self):
        """test_context_contains_input_module"""

        result = self.module._render_module(self.request)

        self.assertEqual(
            result["context"]["default_input_module"], self.mock_abstract_render_module
        )


class TestLocalIdRegistryModuleRenderModuleWithoutPID(TestCase):
    """Test Local Id Registry Module Render Module Without PID"""

    def setUp(self) -> None:
        while "core_linked_records_app" in test_settings.INSTALLED_APPS:
            test_settings.INSTALLED_APPS.remove("core_linked_records_app")

        self.module = LocalIdRegistryModule()
        self.request = Mock()

    @patch(
        "core_module_local_id_registry_app.views.views."
        "AbstractInputModule._render_module"
    )
    def test_returns_input_module(self, mock_render_module):
        """test_returns_input_module"""

        mock_module = "mock_module"
        mock_render_module.return_value = mock_module
        result = self.module._render_module(self.request)

        self.assertEqual(mock_module, result)
