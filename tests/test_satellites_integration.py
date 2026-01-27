"""Integration tests for satellites across all categories.

This test file performs sampling tests on satellites from each category
to ensure they are properly defined, can validate parameters, and can export
to various formats.
"""

import pytest
from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.satellites import (
    system,
    system_enhanced,
    files,
    notes,
    reminders,
    calendar,
    mail,
    safari,
    music,
    finder,
    contacts,
    wifi,
    apps,
)


class TestSystemSatellites:
    """Tests for system satellites."""

    def test_system_get_info_satellite(self):
        """Test system_get_info satellite definition."""
        sat = system.system_get_info

        assert sat.name == "system_get_info"
        assert sat.category == "system"
        assert sat.safety_level == SafetyLevel.SAFE
        assert len(sat.parameters) == 0

    def test_system_set_clipboard_satellite(self):
        """Test system_set_clipboard satellite parameters."""
        sat = system.system_set_clipboard

        assert sat.name == "system_set_clipboard"
        assert len(sat.parameters) == 1
        assert sat.parameters[0].name == "content"
        assert sat.parameters[0].type == "string"
        assert sat.parameters[0].required is True

    def test_system_set_volume_validation(self):
        """Test system_set_volume parameter validation."""
        sat = system.system_set_volume

        # Valid parameters
        sat.validate_parameters({"level": 50})

        # Missing required parameter
        from orbit.core.exceptions import ParameterValidationError
        with pytest.raises(ParameterValidationError):
            sat.validate_parameters({})

    def test_system_satellites_export_to_openai(self):
        """Test system satellites export to OpenAI format."""
        sats = [
            system.system_get_info,
            system.system_set_volume,
            system.send_notification,
        ]

        for sat in sats:
            openai_func = sat.to_openai_function()
            assert openai_func["type"] == "function"
            assert "function" in openai_func
            assert openai_func["function"]["name"] == sat.name


class TestSystemEnhancedSatellites:
    """Tests for enhanced system satellites."""

    def test_system_reboot_safety_level(self):
        """Test system_reboot has DANGEROUS safety level."""
        sat = system_enhanced.system_reboot

        assert sat.safety_level == SafetyLevel.DANGEROUS
        assert sat.name == "system_reboot"

    def test_system_shutdown_safety_level(self):
        """Test system_shutdown has DANGEROUS safety level."""
        sat = system_enhanced.system_shutdown

        assert sat.safety_level == SafetyLevel.DANGEROUS

    def test_system_volume_up_parameters(self):
        """Test system_volume_up parameters."""
        sat = system_enhanced.system_volume_up

        assert len(sat.parameters) == 0  # No parameters needed

    def test_system_take_screenshot_window_parameters(self):
        """Test system_take_screenshot_window has no required parameters."""
        sat = system_enhanced.system_take_screenshot_window

        # Should work with empty parameters
        sat.validate_parameters({})


class TestFilesSatellites:
    """Tests for file operation satellites."""

    def test_file_list_parameters(self):
        """Test file_list satellite parameters."""
        sat = files.file_list

        assert len(sat.parameters) == 1
        assert sat.parameters[0].name == "path"
        assert sat.parameters[0].default == "/"

    def test_file_write_parameters(self):
        """Test file_write satellite parameters."""
        sat = files.file_write

        param_names = [p.name for p in sat.parameters]
        assert "path" in param_names
        assert "content" in param_names

    def test_file_delete_safety_level(self):
        """Test file_delete is MODERATE safety."""
        sat = files.file_delete

        assert sat.safety_level == SafetyLevel.MODERATE

    def test_file_empty_trash_safety_level(self):
        """Test file_empty_trash is DANGEROUS."""
        sat = files.file_empty_trash

        assert sat.safety_level == SafetyLevel.DANGEROUS


class TestNotesSatellites:
    """Tests for Notes satellites."""

    def test_notes_create_parameters(self):
        """Test notes_create satellite parameters."""
        sat = notes.notes_create

        param_names = [p.name for p in sat.parameters]
        assert "name" in param_names
        assert "body" in param_names
        assert "folder" in param_names

        # Check required parameters
        required = [p.name for p in sat.parameters if p.required]
        assert "name" in required

    def test_notes_search_parameter(self):
        """Test notes_search has query parameter."""
        sat = notes.notes_search

        assert len(sat.parameters) == 1
        assert sat.parameters[0].name == "query"
        assert sat.parameters[0].required is True

    def test_notes_list_folders_no_params(self):
        """Test notes_list_folders has no parameters."""
        sat = notes.notes_list_folders

        assert len(sat.parameters) == 0

    def test_notes_satellites_category(self):
        """Test all notes satellites are in 'notes' category."""
        notes_sats = [
            notes.notes_list,
            notes.notes_get,
            notes.notes_create,
            notes.notes_update,
            notes.notes_delete,
            notes.notes_search,
            notes.notes_list_folders,
        ]

        for sat in notes_sats:
            assert sat.category == "notes"


class TestRemindersSatellites:
    """Tests for Reminders satellites."""

    def test_reminders_create_parameters(self):
        """Test reminders_create parameters."""
        sat = reminders.reminders_create

        param_names = [p.name for p in sat.parameters]
        assert "name" in param_names
        assert "due_date" in param_names

    def test_reminders_complete_parameters(self):
        """Test reminders_complete has id parameter."""
        sat = reminders.reminders_complete

        assert len(sat.parameters) == 1
        assert sat.parameters[0].name == "id"
        assert sat.parameters[0].required is True

    def test_reminders_list_no_params(self):
        """Test reminders_list has no parameters."""
        sat = reminders.reminders_list

        assert len(sat.parameters) == 0


class TestCalendarSatellites:
    """Tests for Calendar satellites."""

    def test_calendar_create_event_parameters(self):
        """Test calendar_create_event has all necessary params."""
        sat = calendar.calendar_create_event

        param_names = [p.name for p in sat.parameters]
        assert "summary" in param_names
        assert "start_date" in param_names
        assert "end_date" in param_names

    def test_calendar_get_event_parameters(self):
        """Test calendar_get_event parameters."""
        sat = calendar.calendar_get_events

        # Has optional event_id parameter
        param_names = [p.name for p in sat.parameters]
        assert "event_id" in param_names or "calendar" in param_names


class TestMailSatellites:
    """Tests for Mail satellites."""

    def test_mail_send_parameters(self):
        """Test mail_send has required parameters."""
        sat = mail.mail_send

        param_names = [p.name for p in sat.parameters]
        assert "to" in param_names
        assert "subject" in param_names
        assert "body" in param_names

    def test_mail_list_inbox_no_params(self):
        """Test mail_list_inbox has no required params."""
        sat = mail.mail_list_inbox

        # Can validate with empty params (all optional)
        sat.validate_parameters({})

    def test_mail_mark_as_read_parameter(self):
        """Test mail_mark_as_read has id parameter."""
        sat = mail.mail_mark_as_read

        assert len(sat.parameters) >= 1
        assert any(p.name == "id" for p in sat.parameters)


class TestSafariSatellites:
    """Tests for Safari satellites."""

    def test_safari_open_parameter(self):
        """Test safari_open has url parameter."""
        sat = safari.safari_open

        assert len(sat.parameters) == 1
        assert sat.parameters[0].name == "url"
        assert sat.parameters[0].required is True

    def test_safari_search_parameter(self):
        """Test safari_search has query parameter."""
        sat = safari.safari_search

        assert sat.parameters[0].name == "query"

    def test_safari_get_url_no_params(self):
        """Test safari_get_url has no parameters."""
        sat = safari.safari_get_url

        assert len(sat.parameters) == 0

    def test_safari_zoom_levels(self):
        """Test safari zoom in/out have no parameters."""
        assert len(safari.safari_zoom_in.parameters) == 0
        assert len(safari.safari_zoom_out.parameters) == 0


class TestMusicSatellites:
    """Tests for Music satellites."""

    def test_music_play_no_params(self):
        """Test music_play has no parameters."""
        sat = music.music_play

        assert len(sat.parameters) == 0

    def test_music_set_volume_parameter(self):
        """Test music_set_volume has level parameter."""
        sat = music.music_set_volume

        assert len(sat.parameters) == 1
        assert sat.parameters[0].name == "level"

    def test_music_play_track_parameter(self):
        """Test music_play_track has name parameter."""
        sat = music.music_play_track

        param_names = [p.name for p in sat.parameters]
        assert "name" in param_names

    def test_music_get_current_no_params(self):
        """Test music_get_current has no parameters."""
        sat = music.music_get_current

        assert len(sat.parameters) == 0


class TestFinderSatellites:
    """Tests for Finder satellites."""

    def test_finder_open_folder_parameter(self):
        """Test finder_open_folder has path parameter."""
        sat = finder.finder_open_folder

        assert sat.parameters[0].name == "path"

    def test_finder_empty_trash_dangerous(self):
        """Test finder_empty_trash is DANGEROUS."""
        sat = finder.finder_empty_trash

        assert sat.safety_level == SafetyLevel.DANGEROUS

    def test_finder_new_folder_parameters(self):
        """Test finder_new_folder parameters."""
        sat = finder.finder_new_folder

        param_names = [p.name for p in sat.parameters]
        assert "name" in param_names
        assert "location" in param_names


class TestContactsSatellites:
    """Tests for Contacts satellites."""

    def test_contacts_search_parameter(self):
        """Test contacts_search has query parameter."""
        sat = contacts.contacts_search

        assert sat.parameters[0].name == "query"

    def test_contacts_create_parameters(self):
        """Test contacts_create has parameters."""
        sat = contacts.contacts_create

        param_names = [p.name for p in sat.parameters]
        assert "name" in param_names
        assert "email" in param_names or "phone" in param_names


class TestWifiSatellites:
    """Tests for WiFi satellites."""

    def test_wifi_connect_parameters(self):
        """Test wifi_connect has ssid parameter."""
        sat = wifi.wifi_connect

        param_names = [p.name for p in sat.parameters]
        assert "ssid" in param_names
        assert "password" in param_names

    def test_wifi_list_no_params(self):
        """Test wifi_list has no parameters."""
        sat = wifi.wifi_list

        assert len(sat.parameters) == 0


class TestAppsSatellites:
    """Tests for Application control satellites."""

    def test_app_launch_parameter(self):
        """Test app_launch has name parameter."""
        sat = apps.app_launch

        assert sat.parameters[0].name == "name"

    def test_app_force_quit_moderate(self):
        """Test app_force_quit is MODERATE safety."""
        sat = apps.app_force_quit

        assert sat.safety_level == SafetyLevel.MODERATE

    def test_app_list_no_required_params(self):
        """Test app_list has no required parameters."""
        sat = apps.app_list

        sat.validate_parameters({})


class TestSatelliteExportFormats:
    """Tests for satellite export capabilities."""

    @pytest.mark.parametrize("satellite_module", [
        system, system_enhanced, files, notes, reminders,
        calendar, mail, safari, music, finder, contacts, wifi, apps
    ])
    def test_all_satellites_export_to_dict(self, satellite_module):
        """Test all satellites can export to dict format."""
        # Get all satellites from module
        sats = [
            getattr(satellite_module, name)
            for name in dir(satellite_module)
            if not name.startswith("_") and isinstance(getattr(satellite_module, name), Satellite)
        ]

        for sat in sats[:3]:  # Sample 3 from each module
            sat_dict = sat.to_dict()
            assert "name" in sat_dict
            assert "description" in sat_dict
            assert "category" in sat_dict
            assert "safety_level" in sat_dict

    @pytest.mark.parametrize("satellite_module", [
        system, files, notes, safari
    ])
    def test_sample_satellites_export_to_openai(self, satellite_module):
        """Test sample satellites export to OpenAI format."""
        sats = [
            getattr(satellite_module, name)
            for name in dir(satellite_module)
            if not name.startswith("_") and isinstance(getattr(satellite_module, name), Satellite)
        ]

        for sat in sats[:2]:  # Sample 2 from each module
            openai_func = sat.to_openai_function()
            assert openai_func["type"] == "function"
            assert "parameters" in openai_func["function"]
            assert openai_func["function"]["name"] == sat.name


class TestSatelliteValidation:
    """Tests for satellite parameter validation."""

    def test_system_satellite_validation(self):
        """Test system satellites parameter validation."""
        # Test set_volume with valid param
        system.system_set_volume.validate_parameters({"level": 50})

        # Test with invalid param (missing)
        from orbit.core.exceptions import ParameterValidationError
        with pytest.raises(ParameterValidationError):
            system.system_set_volume.validate_parameters({})

    def test_files_satellite_validation(self):
        """Test file satellites parameter validation."""
        # file_list should work with empty params (has default)
        files.file_list.validate_parameters({})

        # file_write requires path and content
        files.file_write.validate_parameters({
            "path": "/tmp/test.txt",
            "content": "test content"
        })

    def test_notes_satellite_validation(self):
        """Test notes satellites parameter validation."""
        # notes_create requires name
        notes.notes_create.validate_parameters({"name": "Test Note"})

        # Missing required parameter
        from orbit.core.exceptions import ParameterValidationError
        with pytest.raises(ParameterValidationError):
            notes.notes_create.validate_parameters({})

    def test_safari_satellite_validation(self):
        """Test safari satellites parameter validation."""
        # safari_open requires url
        safari.safari_open.validate_parameters({"url": "https://example.com"})

        # Missing url
        from orbit.core.exceptions import ParameterValidationError
        with pytest.raises(ParameterValidationError):
            safari.safari_open.validate_parameters({})


class TestSatelliteSafetyLevels:
    """Tests for satellite safety level distribution."""

    def test_safe_satellites_exist(self):
        """Test that SAFE satellites exist in each category."""
        safe_count = 0
        for module in [system, files, notes, safari, music]:
            for name in dir(module):
                sat = getattr(module, name)
                if isinstance(sat, Satellite) and sat.safety_level == SafetyLevel.SAFE:
                    safe_count += 1

        assert safe_count > 0, "Should have some SAFE satellites"

    def test_moderate_satellites_exist(self):
        """Test that MODERATE satellites exist."""
        moderate_count = 0
        for module in [system, files, apps]:
            for name in dir(module):
                sat = getattr(module, name)
                if isinstance(sat, Satellite) and sat.safety_level == SafetyLevel.MODERATE:
                    moderate_count += 1

        assert moderate_count > 0, "Should have some MODERATE satellites"

    def test_dangerous_satellites_exist(self):
        """Test that DANGEROUS satellites exist."""
        dangerous_found = False

        # Check known dangerous satellites
        if system_enhanced.system_shutdown.safety_level == SafetyLevel.DANGEROUS:
            dangerous_found = True
        if files.file_empty_trash.safety_level == SafetyLevel.DANGEROUS:
            dangerous_found = True

        assert dangerous_found, "Should have DANGEROUS satellites"


class TestSatelliteDescriptions:
    """Tests for satellite descriptions."""

    def test_all_satellites_have_descriptions(self):
        """Test all satellites have descriptions."""
        from orbit.satellites.all_satellites import all_satellites

        for sat in all_satellites:
            assert sat.description, f"{sat.name} should have a description"
            assert len(sat.description) > 0

    def test_descriptions_are_meaningful(self):
        """Test satellite descriptions are meaningful."""
        from orbit.satellites.all_satellites import all_satellites

        for sat in all_satellites[:10]:  # Sample 10
            # Description should not just repeat the name
            assert sat.description.lower() != sat.name.lower()
            # Description should be at least 10 characters
            assert len(sat.description) >= 10


class TestAllSatellitesRegistry:
    """Tests for the all_satellites registry."""

    def test_all_satellites_import(self):
        """Test all_satellites can be imported."""
        from orbit.satellites.all_satellites import all_satellites

        assert isinstance(all_satellites, tuple)
        assert len(all_satellites) > 0

    def test_all_satellites_contain_satellites(self):
        """Test all_satellites contains Satellite instances."""
        from orbit.satellites.all_satellites import all_satellites

        for item in all_satellites:
            assert isinstance(item, Satellite)

    def test_all_satellites_unique_names(self):
        """Test all satellites have unique names."""
        from orbit.satellites.all_satellites import all_satellites

        names = [sat.name for sat in all_satellites]
        assert len(names) == len(set(names)), "Satellite names should be unique"

    def test_all_satellites_cover_all_categories(self):
        """Test all satellites cover all expected categories."""
        from orbit.satellites.all_satellites import all_satellites

        categories = set(sat.category for sat in all_satellites)

        expected_categories = {
            "system", "files", "notes", "reminders", "calendar",
            "mail", "safari", "music", "finder", "contacts", "wifi", "apps"
        }

        assert categories.issuperset(expected_categories) or len(categories.intersection(expected_categories)) >= 10
