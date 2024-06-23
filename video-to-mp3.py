import subprocess
import sys
import os

def convert_video_to_mp3(input_file, output_file=None, bitrate="96k"):
    """
    Convert a video file to an MP3 file using ffmpeg with a specified bitrate.
    
    :param input_file: The path to the input video file.
    :param output_file: The path to the output MP3 file. If None, use the base name of the input file.
    :param bitrate: The bitrate for the output MP3 file (default is 96k).
    """
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}.mp3"
    
    try:
        # Call ffmpeg to convert the video to mp3
        subprocess.run([
            "ffmpeg", 
            "-i", input_file, 
            "-vn",  # No video
            "-ab", bitrate,  # Audio bitrate
            output_file
        ], check=True)
        print(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python video-to-mp3.py <input_video_file> [output_mp3_file]")
        sys.exit(1)
    
    input_video_file = sys.argv[1]
    output_mp3_file = sys.argv[2] if len(sys.argv) == 3 else None
    
    # Ensure output directory exists if output file is specified
    if output_mp3_file:
        output_dir = os.path.dirname(output_mp3_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    convert_video_to_mp3(input_video_file, output_mp3_file)
