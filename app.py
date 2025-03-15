import pygame
from pygame.locals import *
import sys
import os

class App:
    def detect_device_type(self):
        try:
            # Try to read the device model file
            with open('/tmp/deviceModel', 'r') as f:
                device_id = f.read().strip()
                if device_id == '354':
                    return 'Miyoo Mini Plus'
                elif device_id == '283':
                    return 'Miyoo Mini'
        except:
            pass  # Fall through to user selection if file doesn't exist or can't be read
        
        return 'Unknown'  # Temporary value until we can show the selection screen

    def show_device_selection(self):
        # Clear screen
        pygame.draw.rect(self.screen, self.menu_item_color, (0, 0, self.app_width, self.app_height))
        self.draw_text(self.font, self.white, self.app_width // 2, 8, 'center', 'Select Your Device')
        
        # Device options
        devices = ['Miyoo Mini', 'Miyoo Mini Plus']
        selected_index = 0
        
        while True:
            # Clear screen with background color
            pygame.draw.rect(self.screen, self.menu_item_color, (0, 0, self.app_width, self.app_height))
            self.draw_text(self.font, self.white, self.app_width // 2, 8, 'center', 'Select Your Device')
            
            # Draw device options
            for i, device in enumerate(devices):
                if i == selected_index:
                    item_background_color = self.white
                    item_font_color = self.black
                else:
                    item_background_color = self.menu_item_color
                    item_font_color = self.white
                
                # Draw item background
                x = 8
                y = self.font_size * (i + 1) + 8
                width = self.app_width - 16
                height = self.font_size
                pygame.draw.rect(self.screen, item_background_color, (x, y, width, height - 1), 0)
                
                # Draw item text
                self.draw_text(self.font, item_font_color, x + 2, y + 4, 'left', device)
            
            # Draw controls help text
            self.draw_text(self.font, self.gray, self.app_width // 2, self.app_height - 40, 'center', 'A/B: Select   Up/Down: Navigate')
            
            pygame.display.flip()

            # Handle input
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        selected_index = (selected_index - 1) % len(devices)
                    elif event.key == K_DOWN:
                        selected_index = (selected_index + 1) % len(devices)
                    elif event.key in [K_RETURN, K_LCTRL, K_SPACE]:  # A or B button
                        return devices[selected_index]
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.time.wait(10)  # Small delay to prevent high CPU usage

    def draw_text(self, font, color, x, y, align='left', text=''):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if align == 'center':
            text_rect.midtop = (x, y)
        elif align == 'right':
            text_rect.topright = (x, y)
        else:  # left
            text_rect.topleft = (x, y)
        self.screen.blit(text_obj, text_rect)
        
    def draw_button(self, x, y, text, active):
        width = 100
        height = 40
        if active == True:
            color = self.button_color
        else:
            color = self.button_color_active
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        self.draw_text(self.font, self.white, x + width // 2, y + height // 2 - self.font.get_height() // 2, 'center', text)

    def draw_progressbar(self, x, y, width, height, percent):
        pygame.draw.rect(self.screen, self.progressbar_color, (x, y, width, height))
        pygame.draw.rect(self.screen, self.progressbar_bar_color, (x, y, int(width * (percent / 100.0)), height))
        
    def draw_scrollbox(self, x, y, width, percent):
        height = self.app_height - y - 30
        scrollbox_width = 4
        scrollbox_height = height // (self.memo_lines_max / self.memo_lines_ouput_max)
        scrollbox_y = y + (height - scrollbox_height) * (percent / 100.0)
        # background scrollbox
        pygame.draw.rect(self.screen, self.scrollbox_background_color, (x, y, scrollbox_width, height), 0)
        # active scroll
        if percent != -1:
            pygame.draw.rect(self.screen, self.white, (x, scrollbox_y, scrollbox_width, scrollbox_height), 0)

    def read_cpu_clock(self):
        try:
            retroarch_path = '/mnt/SDCARD/RetroArch'
            clock_file = os.path.join(retroarch_path, 'cpuclock.txt')
            if os.path.exists(clock_file):
                with open(clock_file, 'r') as f:
                    return f.read().strip()
            return '1200'  # Default value when file doesn't exist
        except:
            return '1200'  # Default value on any error

    def __init__(self):
        pygame.init()
        self.app_width = 640
        self.app_height = 480
        self.screen = pygame.display.set_mode((self.app_width, self.app_height))
        pygame.display.set_caption('App')
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((7, 18, 22))
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.gray = pygame.Color(128, 128, 128)
        self.green = pygame.Color(0, 255, 0)
        self.red = pygame.Color(255, 0, 0)
        self.menu_item_color = pygame.Color(58, 69, 73)
        self.memo_background_color = pygame.Color(28, 35, 40)
        self.scrollbox_background_color = pygame.Color(60, 70, 72)
        self.button_color = pygame.Color(41, 50, 59)
        self.button_color_active = pygame.Color(59, 71, 84)
        self.progressbar_color = pygame.Color(50, 54, 65)
        self.progressbar_bar_color = pygame.Color(160, 169, 176)
        self.font_size = 32
        self.font = pygame.font.Font(None, self.font_size)

        # First try to detect device type from file
        self.device_type = self.detect_device_type()
        # If unknown, show selection screen
        if self.device_type == 'Unknown':
            self.device_type = self.show_device_selection()

        self.fps_controller = pygame.time.Clock()
        self.layout_index = 0
        self.goodbye_start_time = 0
        self.status_message = ''
        self.status_color = self.white
        self.status_start_time = 0
        
        # Generate list based on device type
        if self.device_type == 'Miyoo Mini Plus':
            self.main_list = [str(x) for x in range(1200, 1900, 100)]
        else:  # Miyoo Mini or Unknown Device
            self.main_list = [str(x) for x in range(1200, 1700, 100)]
            
        self.main_list_output_max = 12
        self.list_selected_index = 0    
        self.list_selected_offset = 0  
        self.list_selected_item = ''
        
        # Read current CPU clock
        self.current_clock = self.read_cpu_clock()
         
        # Statuses
        self.progressbar_value = 75
        self.btn1_active = False
        self.btn2_active = False

        self.main_loop()

    def main_loop(self):
        while True:
            self.handle_events()
            self.update_screen()
            self.fps_controller.tick(30) #fps limiter

    def write_cpu_clock(self, clock_value):
        try:
            # Get RetroArch directory path
            retroarch_path = '/mnt/SDCARD/RetroArch'
            # Check if directory exists
            if not os.path.exists(retroarch_path):
                return False
            # Write the file
            with open(os.path.join(retroarch_path, 'cpuclock.txt'), 'w') as f:
                f.write(clock_value)
            return True
        except:
            return False

    def update_nds_settings(self, clock_value):
        try:
            settings_path = '/mnt/SDCARD/Emu/NDS/resources/settings.json'
            if os.path.exists(settings_path):
                import json
                # Read current settings
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                # Update maxcpu value
                settings['maxcpu'] = int(clock_value)
                # Write updated settings
                with open(settings_path, 'w') as f:
                    json.dump(settings, f, indent=4)
                return True
        except:
            return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LSHIFT:  # X button
                    self.layout_index = 2  # Switch to goodbye screen
                    self.goodbye_start_time = pygame.time.get_ticks()
                elif self.layout_index == 0:
                    if event.key == K_UP:
                        if self.list_selected_index > 0:
                            self.list_selected_index -= 1
                        else:
                           self.list_selected_index = len(self.main_list) - 1 
                    elif event.key == K_DOWN:
                        if self.list_selected_index < len(self.main_list) - 1:
                            self.list_selected_index += 1
                        else:
                            self.list_selected_index = 0
                    elif event.key == K_RETURN or event.key == K_LCTRL or event.key == K_SPACE:  # START or B or A button
                        self.list_selected_item = self.main_list[self.list_selected_index]
                        success = True
                        settings_updated = False
                        
                        # Write CPU clock value when an item is selected
                        if not self.write_cpu_clock(self.list_selected_item):
                            success = False
                        
                        # Update settings if needed
                        if success:
                            settings_updated = self.update_nds_settings(self.list_selected_item)
                            self.current_clock = self.list_selected_item  # Update current clock value
                            
                        # Set appropriate status message
                        if success:
                            if settings_updated:
                                self.status_message = 'Settings updated successfully!'
                            else:
                                self.status_message = 'Clock speed updated!'
                            self.status_color = self.green
                        else:
                            self.status_message = 'Failed to update settings'
                            self.status_color = self.red
                        self.status_start_time = pygame.time.get_ticks()
                        
                    if self.list_selected_index > self.main_list_output_max - 1:
                        self.list_selected_offset = self.list_selected_index // self.main_list_output_max * self.main_list_output_max
                    else:
                        self.list_selected_offset = 0
                    
                elif self.layout_index == 1:
                    if event.key == K_ESCAPE or event.key == K_BACKSPACE:
                        self.layout_index = 0
                    elif event.key == K_UP:
                        if self.memo_line_offset > 0:
                            self.memo_line_offset -= 1
                    elif event.key == K_DOWN:
                        if self.memo_line_offset < self.memo_lines_max - self.memo_lines_ouput_max:
                            self.memo_line_offset += 1
                    
    def update_screen(self):
        self.screen.fill((0, 0, 0))
        if self.layout_index == 0:
            self.draw_layout_list()
        elif self.layout_index == 1:
            self.draw_layout_memo()
        elif self.layout_index == 2:
            self.draw_goodbye()
            # Check if 2 seconds have passed
            if pygame.time.get_ticks() - self.goodbye_start_time >= 2000:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        
    def draw_layout_list(self):
        self.draw_text(self.font, self.white, 8, 8, 'left', 'CPU Clock Speeds')
        self.draw_text(self.font, self.gray, self.app_width - 8, 8, 'right', self.device_type)
        
        # Draw status message if within time window (2 seconds)
        if self.status_message and pygame.time.get_ticks() - self.status_start_time < 2000:
            self.draw_text(self.font, self.status_color, self.app_width // 2, self.app_height - 100, 'center', self.status_message)
        
        for i, line in enumerate(self.main_list):
            if i < self.list_selected_offset:
                continue
            if i - self.list_selected_offset >= self.main_list_output_max:
                continue
            if i == self.list_selected_index:
                item_background_color = self.white
                item_font_color = self.black
            else:
                item_background_color = self.menu_item_color
                item_font_color = self.white
            
            # Items
            x = 8
            y = self.font_size * (i - self.list_selected_offset + 1) + 8
            width = self.app_width - 16
            height = self.font_size
            pygame.draw.rect(self.screen, item_background_color, (x, y, width, height - 1), 0)
            
            # Draw the line text
            text = self.cut_str(line, 70)
            self.draw_text(self.font, item_font_color, x + 2, y + 4, 'left', text)
            
            # Draw "Current Clock Speed" if this is the current clock
            if self.current_clock and line == self.current_clock:
                self.draw_text(self.font, item_font_color, x + width - 4, y + 4, 'right', "Current Clock Speed")
        
        # Draw button controls at the bottom
        self.draw_text(self.font, self.gray, self.app_width // 2, self.app_height - 40, 'center', 'A/B: Select   X: Exit')
        
    def draw_layout_memo(self):
        self.draw_text(self.font, self.white, 8, 8, 'left', 'Display: ' + self.list_selected_item)
        self.draw_text(self.font, self.gray, self.app_width - 8, 8, 'right', self.device_type)
        lines = self.add_line_breaks(self.memo, 46).split('\n')
        self.memo_lines_max = len(lines)
        
        # Scroll
        if self.memo_lines_max > self.memo_lines_ouput_max:
            scroll_percent = self.memo_line_offset * 100 // (self.memo_lines_max - self.memo_lines_ouput_max)
        else:
            scroll_percent = -1
        self.draw_scrollbox(self.app_width - 8, 30, 6, scroll_percent)
        
        self.draw_text(self.font, self.gray, 620, 455, 'right', str(self.memo_line_offset * 100 // (self.memo_lines_max - self.memo_lines_ouput_max)) + '%')
        pygame.draw.rect(self.screen, self.memo_background_color, (9, 30, self.app_width - 24, self.app_height - 60), 0)
        
        # Output lines of text
        for i, line in enumerate(lines):
            if i < self.memo_line_offset:
                continue
            if i - self.memo_line_offset >= self.memo_lines_ouput_max:
                continue
            self.draw_text(self.font, self.white, 18, self.font_size * (i - self.memo_line_offset) + 40, 'left', line)
        
    def cut_str(self, string, n):
        if len(string) > n:
            return string[:n-3] + '...'
        else:
            return string
            
    def add_line_breaks(self, text, n):
        result = ''
        count = 0

        for char in text:
            result += char
            count += 1

            if char == '\n':
                count = 0
                continue

            if count == n:
                count = 0
                text_len = len(result)
                added = False

                for i in range(1, n + 1):
                    if text_len - i < 0:
                        break
                    if result[text_len - i] == ' ':
                        result = result[:text_len - i] + '\n' + result[text_len - i + 1:]
                        added = True
                        break

                if not added:
                    result += '\n'
            
        return result

    def draw_goodbye(self):
        # Center the "Good Bye" text on screen
        self.draw_text(self.font, self.white, self.app_width // 2, self.app_height // 2, 'center', 'Good Bye! Exiting App...')

if __name__ == "__main__":
    app = App()