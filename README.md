# CPU Overclock for Onion OS

A Python application for Miyoo Mini and Miyoo Mini Plus devices running Onion OS that allows users to control CPU clock speeds. The application provides a simple interface to adjust clock speeds and automatically updates relevant system settings.

## Features

- Easy-to-use interface for selecting CPU clock speeds
- Automatic detection of device type (Miyoo Mini vs Miyoo Mini Plus)
- Different clock speed ranges based on device capabilities
- Saves clock speed settings to RetroArch & NDS configuration
- Visual indication of current clock speed


## Installation

1. Download all files from this GitHub Repository to your computer.
2. Insert the SD card of your device into your computer.
3. Navigate to "App" folder on the SD card of your device.
4. Create a folder called "CpuOverclock". (Must be named exactly this or else the icon for the application wont be displayed correctly).
5. Copy all files inside the CpuOverclock folder.
6. Place SD card back into your device and start the device.
7. The "CPU Overclock" app will now be in the App section of Onion OS.
   

## Usage

- Use UP/DOWN to navigate through available clock speeds
- Press A or B to select and apply a clock speed
- Press X to exit the application
- Current clock speed is highlighted in the list
- Status messages confirm successful updates

## Requirements
- Miyoo Mini or Miyoo Mini Plus device running Onion OS

## File Structure
- `app.py` - Main application file
- Settings are saved in RetroArch and NDS emulator configurations

## Notes

- Default clock speed is 1200MHz if no previous setting exists
- Clock speed ranges:
  - Miyoo Mini: 1200MHz - 1600MHz
  - Miyoo Mini Plus: 1200MHz - 1800MHz

## License

MIT License 
