from pydub import AudioSegment
from pydub.silence import split_on_silence

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
    combined.append(current_chunk)  # Add the last chunk
    return combined

# Load the lecture file
lecture = AudioSegment.from_file("input.mp3")

# Input the start time for processing (format: hh:mm:ss)
start_time = input("Enter start time (hh:mm:ss): ")
start_time_ms = get_milliseconds(start_time)

# Slice the audio from the specified start time
lecture_from_start = lecture[start_time_ms:]

# Split on silence, adjust silence_thresh and silence duration as needed
chunks = split_on_silence(
    lecture_from_start,
    min_silence_len=500,  # in ms
    silence_thresh=-40   # in dB
)

# Minimum length for each chunk (15 minutes)
min_length_ms = 15 * 60 * 1000

# Combine chunks to meet the minimum length requirement
combined_chunks = combine_chunks(chunks, min_length_ms)

# Save each chunk
for i, chunk in enumerate(combined_chunks):
    out_file = f"chunk{i}.mp3"
    chunk.export(out_file, format="mp3")
