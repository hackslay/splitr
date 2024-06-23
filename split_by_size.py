from pydub import AudioSegment
import os

def split_by_size(file_path, target_size_mb, bit_rate_kbps=128):
    """ Split audio file into chunks approximately equal to the specified size in MB. """
    audio = AudioSegment.from_file(file_path)
    # Calculate target duration in milliseconds
    bytes_per_second = (bit_rate_kbps * 1000) / 8
    target_duration_ms = (target_size_mb * 1000 * 1000 * 8) / (bit_rate_kbps * 1000)

    chunks = []
    start_ms = 0
    duration_ms = len(audio)
    while start_ms < duration_ms:
        end_ms = start_ms + target_duration_ms
        if end_ms > duration_ms:
            end_ms = duration_ms
        chunk = audio[start_ms:end_ms]
        chunks.append(chunk)
        start_ms += target_duration_ms

    # Save chunks
    file_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    for i, chunk in enumerate(chunks):
        out_file = os.path.join(file_dir, f"{base_name}_chunk{i}.mp3")
        chunk.export(out_file, format="mp3", bitrate=f"{bit_rate_kbps}k")
