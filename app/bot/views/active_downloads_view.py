"""Views for active downloads."""

from textwrap import dedent

from seedrcc.models import Torrent
from telethon import Button

from app.bot.views import ViewResponse
from app.utils import format_date, format_size, progress_bar
from app.utils.language import Translator


def render_download_status(download: Torrent, translator: Translator) -> ViewResponse:
    """Renders the detailed progress message for a single download."""

    progress = int(float(download.progress))
    title = download.name.strip()
    downloaded_bytes = (progress / 100) * download.size if download.size else 0

    progress_visual = progress_bar(progress, translator)
    downloaded = format_size(downloaded_bytes)
    size = format_size(download.size)
    download_rate = format_size(download.download_rate)
    last_update = format_date(download.last_update)

    message = dedent(f"""
        <b>{translator.get("activeDownloadsBtn")}</b>

        <b>{title if title else ""}</b>
        <b>{translator.get("speedLabel")}</b> {download_rate}/s
        <b>{translator.get("seedersLabel")}</b> {download.seeders}
        <b>{translator.get("leechersLabel")}</b> {download.leechers}
        <b>{translator.get("lastUpdateLabel")}</b> {last_update}

        <b>{translator.get("progressLabel")}</b> {downloaded} / {size} ({float(progress):.1f}%)
        {progress_visual}

        <b>{translator.get("pausedDownloadWarning") if download.stopped else ""}</b>
    """).strip()

    buttons = [[Button.inline(translator.get("cancelBtn"), f"cancel_download_{download.id}".encode())]]

    return ViewResponse(message=message, buttons=buttons)


def render_download_menu(active_downloads, translator: Translator) -> ViewResponse:
    """Render a menu of buttons for multiple active downloads."""
    message = dedent(f"""
        <b>{translator.get("activeDownloadsBtn")}</b>

        {translator.get("selectDownload")}
    """)
    buttons = []
    for download in active_downloads:
        button_text = (
            f"{download.name[:30]}... ({int(float(download.progress))}%)"
            if len(download.name) > 30
            else f"{download.name} ({int(float(download.progress))}%)"
        )
        buttons.append([Button.inline(button_text, f"active_{download.id}".encode())])
    return ViewResponse(message=message.strip(), buttons=buttons)


def render_no_downloads_message(translator: Translator) -> ViewResponse:
    """Render the message when there are no active downloads."""
    return ViewResponse(message=translator.get("noActiveDownloads"))
