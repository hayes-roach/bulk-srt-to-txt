import os
import re
import argparse
from pathlib import Path

def parse_srt_file(file_path):
    """
    Parse an SRT file and extract only the text content, removing timestamps and sequence numbers.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    # Split content into blocks (separated by double newlines)
    blocks = content.strip().split('\n\n')
    
    text_lines = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        
        # Skip empty blocks
        if not lines or not lines[0].strip():
            continue
            
        # Each SRT block has:
        # Line 1: Sequence number
        # Line 2: Timestamp
        # Line 3+: Subtitle text
        
        if len(lines) >= 3:
            # Skip sequence number (line 0) and timestamp (line 1)
            # Extract text content (line 2 onwards)
            subtitle_text = '\n'.join(lines[2:])
            
            # Remove HTML tags if present
            subtitle_text = re.sub(r'<[^>]+>', '', subtitle_text)
            
            # Clean up extra whitespace
            subtitle_text = ' '.join(subtitle_text.split())
            
            if subtitle_text.strip():
                text_lines.append(subtitle_text.strip())
    
    return text_lines

def convert_srt_to_txt(input_folder, output_file):
    """
    Convert all SRT files in a folder to a single TXT file.
    """
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return False
    
    if not input_path.is_dir():
        print(f"Error: '{input_folder}' is not a directory.")
        return False
    
    # Find all SRT files in the folder
    srt_files = list(input_path.glob('*.srt'))
    
    if not srt_files:
        print(f"No SRT files found in '{input_folder}'.")
        return False
    
    print(f"Found {len(srt_files)} SRT file(s):")
    for srt_file in sorted(srt_files):
        print(f"  - {srt_file.name}")
    
    all_text = []
    
    # Process each SRT file
    for srt_file in sorted(srt_files):
        print(f"Processing: {srt_file.name}")
        
        try:
            text_lines = parse_srt_file(srt_file)
            
            if text_lines:
                # Add a header with the filename
                all_text.append(f"\n=== {srt_file.name} ===\n")
                all_text.extend(text_lines)
                all_text.append("")  # Add empty line between files
                
            print(f"  Extracted {len(text_lines)} text segments")
            
        except Exception as e:
            print(f"  Error processing {srt_file.name}: {e}")
            continue
    
    if not all_text:
        print("No text content extracted from any SRT files.")
        return False
    
    # Write to output file
    try:
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))
        
        print(f"\nSuccessfully created: {output_file}")
        print(f"Total lines written: {len([line for line in all_text if line.strip()])}")
        return True
        
    except Exception as e:
        print(f"Error writing to output file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert multiple SRT files to a single TXT file, removing timestamps.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python srt_to_txt.py /path/to/srt/files output.txt
  python srt_to_txt.py ./subtitles combined_transcription.txt
  python srt_to_txt.py . all_transcripts.txt
        """
    )
    
    parser.add_argument('input_folder', 
                       help='Path to folder containing SRT files')
    parser.add_argument('output_file', 
                       help='Path for the output TXT file')
    parser.add_argument('--no-headers', 
                       action='store_true',
                       help='Do not add filename headers between files')
    
    args = parser.parse_args()
    
    # Convert SRT files to TXT
    success = convert_srt_to_txt(args.input_folder, args.output_file)
    
    if success:
        print("\nConversion completed successfully!")
    else:
        print("\nConversion failed.")
        exit(1)

if __name__ == "__main__":
    main()