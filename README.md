# CPU Overclock for Onion OS

A Python application for Miyoo Mini and Miyoo Mini Plus devices running Onion OS that allows users to control CPU clock speeds. The application provides a simple interface to adjust clock speeds and automatically updates relevant system settings.

## Features

- Easy-to-use interface for selecting CPU clock speeds
- Automatic detection of device type (Miyoo Mini vs Miyoo Mini Plus)
- Different clock speed ranges based on device capabilities
- Saves clock speed settings to RetroArch configuration
- Updates NDS emulator settings automatically
- Visual indication of current clock speed
- Smooth exit with goodbye message

## Installation

1. Copy the application files to your Miyoo Mini device
2. Ensure Python and Pygame are installed on your device
3. Place the app in an accessible location on your device

## Usage

- Use UP/DOWN to navigate through available clock speeds
- Press A or B to select and apply a clock speed
- Press X to exit the application
- Current clock speed is highlighted in the list
- Status messages confirm successful updates

## Requirements

- Python 3.x
- Pygame
- Onion OS
- Miyoo Mini or Miyoo Mini Plus device

## File Structure

- `app.py` - Main application file
- `cpuclock.txt` - Stores the current CPU clock speed
- Settings are saved in RetroArch and NDS emulator configurations

## Notes

- Default clock speed is 1200MHz if no previous setting exists
- Clock speed ranges:
  - Miyoo Mini: 1200MHz - 1600MHz
  - Miyoo Mini Plus: 1200MHz - 1800MHz

## License

MIT License 