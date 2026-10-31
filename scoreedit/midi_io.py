"""Minimal Standard MIDI File import/export for the piano-roll editor."""

from __future__ import annotations

from pathlib import Path


TICKS_PER_QUARTER = 480
TICKS_PER_CELL = TICKS_PER_QUARTER // 4


def _read_variable_length(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    while True:
        if offset >= len(data):
            raise ValueError("Unexpected end of MIDI data.")
        byte = data[offset]
        offset += 1
        value = (value << 7) | (byte & 0x7F)
        if byte < 0x80:
            return value, offset


def _write_variable_length(value: int) -> bytes:
    if value < 0:
        raise ValueError("MIDI delta times cannot be negative.")
    encoded = [value & 0x7F]
    value >>= 7
    while value:
        encoded.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(encoded)


def _track_events(track: bytes):
    offset = 0
    tick = 0
    running_status = None
    while offset < len(track):
        delta, offset = _read_variable_length(track, offset)
        tick += delta
        if offset >= len(track):
            break
        status = track[offset]
        if status & 0x80:
            offset += 1
            if status < 0xF0:
                running_status = status
        elif running_status is not None:
            status = running_status
        else:
            raise ValueError("MIDI track contains an invalid running status.")

        if status == 0xFF:
            if offset >= len(track):
                raise ValueError("Incomplete MIDI meta event.")
            meta_type = track[offset]
            length, offset = _read_variable_length(track, offset + 1)
            payload = track[offset : offset + length]
            if len(payload) != length:
                raise ValueError("Incomplete MIDI meta event data.")
            offset += length
            if meta_type == 0x2F:
                break
        elif status in (0xF0, 0xF7):
            length, offset = _read_variable_length(track, offset)
            offset += length
        else:
            event_type = status & 0xF0
            data_length = 1 if event_type in (0xC0, 0xD0) else 2
            payload = track[offset : offset + data_length]
            if len(payload) != data_length:
                raise ValueError("Incomplete MIDI channel event.")
            offset += data_length
            yield tick, status, payload


def _parse_tracks(content: bytes) -> list[bytes]:
    if len(content) < 14 or content[:4] != b"MThd":
        raise ValueError("Not a Standard MIDI File.")
    header_length = int.from_bytes(content[4:8], "big")
    if header_length < 6 or 8 + header_length > len(content):
        raise ValueError("Invalid MIDI header.")
    format_type = int.from_bytes(content[8:10], "big")
    track_count = int.from_bytes(content[10:12], "big")
    division = int.from_bytes(content[12:14], "big")
    if format_type not in (0, 1) or division & 0x8000:
        raise ValueError("Only metrical Standard MIDI Files (formats 0 and 1) are supported.")
    if division == 0:
        raise ValueError("MIDI ticks per quarter note cannot be zero.")

    tracks = []
    offset = 8 + header_length
    for _ in range(track_count):
        if content[offset : offset + 4] != b"MTrk" or offset + 8 > len(content):
            raise ValueError("Invalid MIDI track header.")
        length = int.from_bytes(content[offset + 4 : offset + 8], "big")
        offset += 8
        track = content[offset : offset + length]
        if len(track) != length:
            raise ValueError("MIDI track is truncated.")
        tracks.append(track)
        offset += length
    return tracks


def import_midi(path: str | Path, columns: int, rows: int) -> list[tuple[int, int, int]]:
    """Return piano-roll notes as ``(column, row, duration_in_cells)``."""
    content = Path(path).read_bytes()
    tracks = _parse_tracks(content)
    ticks_per_quarter = int.from_bytes(content[12:14], "big")
    ticks_per_cell = max(1, ticks_per_quarter // 4)
    active: dict[tuple[int, int], list[int]] = {}
    notes = []

    for track in tracks:
        for tick, status, payload in _track_events(track):
            command = status & 0xF0
            channel = status & 0x0F
            if command not in (0x80, 0x90):
                continue
            pitch, velocity = payload
            is_on = command == 0x90 and velocity > 0
            key = (channel, pitch)
            if is_on:
                active.setdefault(key, []).append(tick)
                continue

            starts = active.get(key)
            if not starts:
                continue
            start_tick = starts.pop(0)
            if not starts:
                active.pop(key, None)
            column = round(start_tick / ticks_per_cell)
            duration = max(1, round((tick - start_tick) / ticks_per_cell))
            row = rows - 1 - (pitch - 48)
            if 0 <= column < columns and 0 <= row < rows:
                notes.append((column, row, duration))
    return sorted(notes)


def export_midi(
    path: str | Path,
    notes: list[tuple[int, int, int]],
    rows: int,
    tempo_bpm: int = 120,
    velocity: int = 96,
) -> None:
    """Write piano-roll notes as a format-0 Standard MIDI File."""
    if not 20 <= tempo_bpm <= 300:
        raise ValueError("MIDI tempo must be between 20 and 300 BPM.")
    if not 1 <= velocity <= 127:
        raise ValueError("MIDI note velocity must be between 1 and 127.")
    events = []
    for column, row, duration in notes:
        pitch = 48 + rows - 1 - row
        if not 0 <= pitch <= 127:
            raise ValueError(f"MIDI pitch out of range: {pitch}")
        if column < 0 or duration <= 0:
            raise ValueError("MIDI note positions and durations must be positive.")
        start = column * TICKS_PER_CELL
        end = start + duration * TICKS_PER_CELL
        events.append((start, 1, bytes((0x90, pitch, velocity))))
        events.append((end, 0, bytes((0x80, pitch, 0))))
    events.sort(key=lambda event: (event[0], event[1]))

    track = bytearray()
    microseconds_per_quarter = 60_000_000 // tempo_bpm
    track.extend(b"\x00\xff\x51\x03" + microseconds_per_quarter.to_bytes(3, "big"))
    previous_tick = 0
    for tick, _, event in events:
        track.extend(_write_variable_length(tick - previous_tick))
        track.extend(event)
        previous_tick = tick
    track.extend(b"\x00\xff\x2f\x00")

    header = (
        b"MThd"
        + (6).to_bytes(4, "big")
        + (0).to_bytes(2, "big")
        + (1).to_bytes(2, "big")
        + TICKS_PER_QUARTER.to_bytes(2, "big")
    )
    track_chunk = b"MTrk" + len(track).to_bytes(4, "big") + track
    Path(path).write_bytes(header + track_chunk)
