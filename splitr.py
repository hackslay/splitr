from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def get_milliseconds(hms_time):
    """ Convert time in 'hh:mm:ss' format to milliseconds """
    h, m, s = map(int, hms_time.split(':'))
    return ((h * 3600) + (m * 60) + s) * 1000

def combine_chunks(chunks, min_length_ms):
    """ Combine smaller chunks into chunks of at least the minimum length """
    combined = []
    current_chunk = chunks[0]
    for chunk in chunks[1:]:
        if len(current_chunk) < min_length_ms:
            current_chunk += chunk
        else:
            combined.append(current_chunk)
            current_chunk = chunk
    if len(current_chunk) >= min_length_ms:  # Make sure the last chunk meets the minimum length
        combined.append(current_chunk)
    return combined

def split_audio(file_path, start_time):
    """ Split audio file based on silence """
    lecture = AudioSegment.from_file(file_path)
    start_time_ms = get_milliseconds(start_time)
    lecture_from_start = lecture[start_time_ms:]

    chunks = split_on_silence(
        lecture_from_start,
        min_silence_len=500,  # in ms
        silence_thresh=-40   # in dB
    )

    min_length_ms = 15 * 60 * 1000
    combined_chunks = combine_chunks(chunks, min_length_ms)

     # Determine the directory of the input file
    file_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    for i, chunk in enumerate(combined_chunks):
        out_file = os.path.join(file_dir, f"{base_name}{i}.mp3")
        chunk.export(out_file, format="mp3")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python splitr.py <file_path> <start_time>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    start_time = sys.argv[2]
    split_audio(file_path, start_time)
