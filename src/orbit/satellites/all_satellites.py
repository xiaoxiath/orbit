"""Update all_satellites to include Phase 5-6 satellites."""

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

# Import all satellites
basic_system_satellites = [
    system.system_get_info,
    system.system_get_clipboard,
    system.system_set_clipboard,
    system.system_send_notification,
    system.system_take_screenshot,
    system.system_get_volume,
    system.system_set_volume,
    system.system_get_brightness,
    system.system_set_brightness,
]

enhanced_system_satellites = [
    system_enhanced.system_get_detailed_info,
    system_enhanced.system_get_clipboard_history,
    system_enhanced.system_clear_clipboard,
    system_enhanced.system_send_notification_with_sound,
    system_enhanced.system_take_screenshot_selection,
    system_enhanced.system_take_screenshot_window,
    system_enhanced.system_mute_volume,
    system_enhanced.system_unmute_volume,
    system_enhanced.system_volume_up,
    system_enhanced.system_volume_down,
    system_enhanced.system_brightness_up,
    system_enhanced.system_brightness_down,
    system_enhanced.system_sleep,
    system_enhanced.system_reboot,
    system_enhanced.system_shutdown,
]

file_satellites = [
    files.file_list,
    files.file_read,
    files.file_write,
    files.file_delete,
    files.file_move,
    files.file_copy,
    files.file_search,
    files.file_empty_trash,
    files.file_create_directory,
    files.file_get_info,
]

notes_satellites = [
    notes.notes_list,
    notes.notes_get,
    notes.notes_create,
    notes.notes_update,
    notes.notes_delete,
    notes.notes_search,
    notes.notes_list_folders,
]

reminders_satellites = [
    reminders.reminders_list,
    reminders.reminders_create,
    reminders.reminders_complete,
    reminders.reminders_uncomplete,
    reminders.reminders_delete,
    reminders.reminders_list_lists,
]

calendar_satellites = [
    calendar.calendar_list_calendars,
    calendar.calendar_get_events,
    calendar.calendar_create_event,
    calendar.calendar_delete_event,
]

mail_satellites = [
    mail.mail_send,
    mail.mail_list_inbox,
    mail.mail_get,
    mail.mail_delete,
    mail.mail_mark_as_read,
    mail.mail_mark_as_unread,
]

safari_satellites = [
    safari.safari_open,
    safari.safari_get_url,
    safari.safari_get_text,
    safari.safari_list_tabs,
    safari.safari_close_tab,
    safari.safari_search,
    safari.safari_new_tab,
    safari.safari_go_back,
    safari.safari_go_forward,
    safari.safari_refresh,
    safari.safari_zoom_in,
    safari.safari_zoom_out,
]

music_satellites = [
    music.music_play,
    music.music_pause,
    music.music_next,
    music.music_previous,
    music.music_get_current,
    music.music_set_volume,
    music.music_get_volume,
    music.music_play_track,
    music.music_search,
    music.music_get_playlists,
    music.music_shuffle,
]

finder_satellites = [
    finder.finder_open_folder,
    finder.finder_new_folder,
    finder.finder_reveal,
    finder.finder_get_selection,
    finder.finder_empty_trash,
    finder.finder_get_trash_info,
]

contacts_satellites = [
    contacts.contacts_search,
    contacts.contacts_get,
    contacts.contacts_create,
    contacts.contacts_list_all,
]

wifi_satellites = [
    wifi.wifi_connect,
    wifi.wifi_disconnect,
    wifi.wifi_list,
    wifi.wifi_current,
    wifi.wifi_turn_on,
    wifi.wifi_turn_off,
]

app_satellites = [
    apps.app_list,
    apps.app_launch,
    apps.app_quit,
    apps.app_activate,
    apps.app_get_running,
    apps.app_force_quit,
    apps.app_hide,
    apps.app_show,
]

# All satellites combined
all_satellites = (
    basic_system_satellites +
    enhanced_system_satellites +
    file_satellites +
    notes_satellites +
    reminders_satellites +
    calendar_satellites +
    mail_satellites +
    safari_satellites +
    music_satellites +
    finder_satellites +
    contacts_satellites +
    wifi_satellites +
    app_satellites
)

__all__ = ["all_satellites"]
