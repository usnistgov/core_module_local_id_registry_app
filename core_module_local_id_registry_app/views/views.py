""" Local Id Registry Module
"""
import json
from re import match
from urllib.parse import urljoin

from django.urls import reverse

from core_curate_app.components.curate_data_structure import (
    api as curate_data_structure_api,
)
from core_main_app.utils.requests_utils.requests_utils import send_get_request
from core_main_registry_app.components.data.api import generate_unique_local_id
from core_module_local_id_registry_app import settings
from core_parser_app.tools.modules.views.builtin.input_module import AbstractInputModule
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)


class LocalIdRegistryModule(AbstractInputModule):
    def __init__(self):
        """Initialize module"""
        self.error_data = None

        if "core_linked_records_app" in settings.INSTALLED_APPS:
            from core_linked_records_app import settings as linked_records_settings

            placeholder = "A PID will be generated for this resource"
            styles = ["core_module_local_id_registry_app/css/module_local_id.css"]
            scripts = ["core_module_local_id_registry_app/js/module_local_id.js"]
            disabled = False

            # Retrieve PID settings
            self.pid_settings = {
                "xpath": linked_records_settings.PID_XPATH,
                "format": linked_records_settings.PID_FORMAT,
                "systems": list(linked_records_settings.ID_PROVIDER_SYSTEMS.keys()),
                "prefixes": linked_records_settings.ID_PROVIDER_PREFIXES,
            }
        else:
            placeholder = None
            styles = list()
            scripts = list()
            disabled = True

            self.pid_settings = None

        AbstractInputModule.__init__(
            self,
            styles=styles,
            scripts=scripts,
            disabled=disabled,
            placeholder=placeholder,
        )

    @staticmethod
    def _get_curate_datastructure_from_module_id(module_id, user):
        module_element = data_structure_element_api.get_by_id(module_id)
        data_structure_element = data_structure_element_api.get_root_element(
            module_element
        )
        return curate_data_structure_api.get_by_data_structure_element_root_id(
            data_structure_element, user
        )

    def _init_prefix_and_record(self, data, curate_data_structure_id, user):
        # If data is not empty and linked records installed, get record name and
        # prefix.
        record_host_pid_url = None
        settings_host_pid_url = None

        try:
            data_split = data.split("/")

            record_host_pid_url = "/".join(data_split[:-2])
            self.default_value = data_split[-1]
            self.default_prefix = data_split[-2]

            settings_host_pid_url = urljoin(
                settings.SERVER_URI,
                reverse(
                    "core_linked_records_app_rest_provider_record_view",
                    kwargs={
                        "provider": self.pid_settings["systems"][0],
                        "record": "",
                    },
                ),
            )[:-1]

            assert record_host_pid_url == settings_host_pid_url
            assert self.default_prefix in self.pid_settings["prefixes"]

            # Check the record name match the expected format.
            record_format_match = match(
                r"^(%s|)$" % self.pid_settings["format"], self.default_value
            )

            assert record_format_match is not None

            # Check that the URL is not already assigned.
            record_response = send_get_request("%s?format=json" % data)

            # Retrieve curate datastructure associated with the current form. Used
            # to check if the data being edited is the same as the one with the
            # assigned PID.
            curate_data_structure_object = curate_data_structure_api.get_by_id(
                curate_data_structure_id, user
            )

            assert record_response.status_code == 404 or (
                curate_data_structure_object["data"] is not None
                and json.loads(record_response.text)["id"]
                == str(curate_data_structure_object["data"]["id"])
            )
        except IndexError:
            self.default_prefix = None
            self.default_value = None

            self.error_data = data
        except AssertionError:
            if record_host_pid_url != settings_host_pid_url:
                self.default_prefix = None
                self.default_value = None

            self.error_data = data

    def _retrieve_data(self, request):
        """Retrieve module's data

        Args:
            request:

        Returns:

        """
        self.has_errors = None
        self.default_value = None
        self.default_prefix = None
        data = None
        module_id = None

        if request.method == "GET":
            data = request.GET.get("data", None)
            module_id = request.GET.get("module_id")

            # No data available and linked records not installed, a local ID needs to be
            # generated automatically.
            if not data and "core_linked_records_app" not in settings.INSTALLED_APPS:
                data = generate_unique_local_id(settings.LOCAL_ID_LENGTH)

            self.default_value = data
        elif request.method == "POST":  # Update the existing `data` field.
            data = request.POST.get("data", None)
            module_id = request.POST.get("module_id")

        # Additional checks if linked_records is installed.
        if data and "core_linked_records_app" in settings.INSTALLED_APPS:
            curate_data_structure = self._get_curate_datastructure_from_module_id(
                str(module_id), request.user
            )
            self._init_prefix_and_record(data, curate_data_structure.pk, request.user)

        return data

    def _render_data(self, request):
        """Return module's data rendering

        Args:
            request:

        Returns:

        """
        if "core_linked_records_app" not in settings.INSTALLED_APPS:
            return ""

        if not self.default_value and not self.error_data:
            context = {
                "icon": "fa-info-circle",
                "type": "info",
                "message": "Enter the permanent link to this data. Record "
                "name should match %s" % self.pid_settings["format"],
            }
        elif self.error_data:
            context = {
                "icon": "fa-times-circle",
                "type": "danger",
                "message": "Invalid local ID provided (%s). Select a valid prefix and record name."
                % self.error_data,
            }
        else:
            context = {
                "icon": "fa-check-circle",
                "type": "success",
                "message": "Record valid and available for registration!",
            }

        return self.render_template(
            "core_module_local_id_registry_app/pid_display_box.html", context
        )

    def _render_module(self, request):
        """Create HTML representation of the module

        Args:
            request:

        Returns:

        """
        # Create the default input module
        module_template = super(LocalIdRegistryModule, self)._render_module(request)

        if "core_linked_records_app" in settings.INSTALLED_APPS:
            pid_default_url = urljoin(
                settings.SERVER_URI,
                reverse(
                    "core_linked_records_app_rest_provider_record_view",
                    kwargs={"provider": "local", "record": ""},
                ),
            )

            context = {
                "pid_host_url": pid_default_url
                if pid_default_url.rsplit("/", 1)[-1] != ""
                else pid_default_url.rsplit("/", 1)[0],
                "pid_prefixes": self.pid_settings["prefixes"],
                "default_prefix": self.default_prefix,
                "default_input_module": module_template,
            }

            module_template = AbstractInputModule.render_template(
                "core_module_local_id_registry_app/pid_edit_input.html", context=context
            )

        return module_template
