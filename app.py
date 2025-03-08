import pygame
from pygame.locals import *
import sys
import os

class App:
    def detect_device_type(self):
        try:
            # Check for wireless interface
            wireless_exists = False
            net_path = '/sys/class/net'
            for interface in os.listdir(net_path):
                if os.path.exists(os.path.join(net_path, interface, 'wireless')):
                    wireless_exists = True
                    break
            
            return 'Miyoo Mini Plus' if wireless_exists else 'Miyoo Mini'
        except:
            return 'Unknown Device'

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

    def __init__(self):
        pygame.init()
        self.device_type = self.detect_device_type()
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
        #self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), 'arial.ttf'), 17)
        self.font_size = 32
        self.font = pygame.font.Font(None, self.font_size)
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
        
        self.memo = 'Python is a high-level programming language that has gained immense popularity due to its numerous advantages. Here are some key benefits that make Python attractive to developers and organizations worldwide:\n\n'
        self.memo += '1. Simplicity and Readability:\nPython is known for its simple and concise syntax, which makes it easy to read and understand, even for beginners. This reduces learning time and simplifies code maintenance.\n\n' 
        self.memo += '2. Extensive Libraries and Frameworks:\nPython has a vast standard library and numerous third-party libraries and frameworks, allowing it to address a wide range of tasks from web development (Django, Flask) to data analysis (Pandas, NumPy) and machine learning (TensorFlow, scikit-learn).\n\n' 
        self.memo += '3. Cross-Platform Compatibility: Python is cross-platform, meaning code written in Python can run on various operating systems like Windows, macOS, and Linux without modification.\n\n'
        self.memo += '4. Community and Support:\nPython boasts one of the largest and most active developer communities. This ensures ample resources, support, and regular updates to keep the language current with modern needs.\n\n'
        self.memo += '5. Versatility:\nPython is used in numerous fields, including web development, scientific research, artificial intelligence, and task automation. Its versatility allows developers to use the same language for various tasks, enhancing efficiency.\n\n'
        self.memo += '6. High Development Productivity:\nPython''s high-level syntax and rich library ecosystem accelerate development, reducing time-to-market and increasing development flexibility.\n\n'
        self.memo += '7. Integration with Other Languages:\nPython easily integrates with other languages like C, C++, and Java, serving as a bridge between different software components and maximizing performance.\n\n'
        self.memo += '8. Educational Use:\nDue to its simplicity, Python is often used for educational purposes, making it an excellent first language for learning programming basics.\n\n'
        self.memo += 'Overall, Python offers a powerful set of tools and capabilities, making it an ideal choice for solving diverse programming challenges.'
        
        #self.memo = '1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 '
        
        self.memo_line_offset = 0
        self.memo_lines_max = 0
        self.memo_lines_ouput_max = 13
        
        # Statuses
        self.progressbar_value = 75
        self.item1_turn_status = '< turn on>'
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
                    if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_SPACE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_UP:
                        if self.list_selected_index > 0:
                            self.list_selected_index -= 1
                        else:
                           self.list_selected_index = len(self.main_list) - 1 
                    elif event.key == K_DOWN:
                        if self.list_selected_index < len(self.main_list) - 1:
                            self.list_selected_index += 1
                        else:
                            self.list_selected_index = 0
                    elif event.key == K_LEFT:
                        if self.progressbar_value > 0:
                            self.progressbar_value -= 1
                    elif event.key == K_RIGHT:
                        if self.progressbar_value < 100:
                            self.progressbar_value += 1
                    elif event.key == K_RETURN or event.key == K_LCTRL:  # START or B button
                        self.list_selected_item = self.main_list[self.list_selected_index]
                        # Write CPU clock value when an item is selected
                        if self.write_cpu_clock(self.list_selected_item):
                            self.status_message = 'Clock speed set successfully!'
                            self.status_color = self.green
                            self.status_start_time = pygame.time.get_ticks()
                        else:
                            self.status_message = 'Failed to set clock speed'
                            self.status_color = self.red
                            self.status_start_time = pygame.time.get_ticks()
                    elif event.key == K_e:
                        self.btn1_active = not self.btn1_active
                    elif event.key == K_t:
                        self.btn2_active = not self.btn2_active
                    if self.list_selected_index > self.main_list_output_max - 1:
                        self.list_selected_offset = self.list_selected_index // self.main_list_output_max * self.main_list_output_max
                    else:
                        self.list_selected_offset = 0
                    
                elif self.layout_index == 1:
                    if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_SPACE:
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
            self.draw_button(320, 430, 'Btn 1 (L)', self.btn1_active)
            self.draw_button(430, 430, 'Btn 2 (R)', self.btn2_active)
            self.draw_progressbar(8, 440, 300, 20, self.progressbar_value)
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
        self.draw_text(self.font, self.white, 8, 8, 'left', 'List')
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
            self.draw_text(self.font, item_font_color, x + 2, y + 4, 'left', self.cut_str(line, 70))
            
            if i == 0:
                self.draw_text(self.font, item_font_color, self.app_width - 80, y + 4, 'center', self.item1_turn_status)
            
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
        self.draw_text(self.font, self.white, self.app_width // 2, self.app_height // 2, 'center', 'Good Bye')

if __name__ == "__main__":
    app = App()