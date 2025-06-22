# bulk-srt-to-txt
Convert multiple subtitle files (.srt) from a directory to a single consolidated text file.

## Usage

```bash
python srt_to_txt.py input_directory output.txt
```

## Requirements

- Python 3.6+
- No external dependencies

## Installation

```bash
git clone https://github.com/hayes-roach/bulk-srt-to-txt.git
cd srt-to-txt
```

## Examples

Process all SRT files in current directory:
```bash
python srt_to_txt.py . transcript.txt
```

Process files from specific folder:
```bash
python srt_to_txt.py ./subtitles combined.txt
```

## What it does

- Removes timestamps and sequence numbers
- Strips HTML tags from subtitle text
- Handles UTF-8 and Latin-1 encodings
- Combines multiple files with filename separators
- Processes all `.srt` files in the specified directory

## Options

```
--no-headers    Skip filename headers in output
--help         Show usage information
```

## Output format

```
=== file1.srt ===

First subtitle text here.
Second subtitle text here.

=== file2.srt ===

More subtitle content.
```

## Notes

The script expects standard SRT format:
```
1
00:00:01,000 --> 00:00:04,000
Subtitle text here

2
00:00:05,000 --> 00:00:08,000
More text
```

Handles common subtitle formatting issues and encoding problems automatically.

## License

MIT
