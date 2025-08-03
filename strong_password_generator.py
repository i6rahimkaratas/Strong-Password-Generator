import pygame
import random
import string
import os
from datetime import datetime

pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 200)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
GRAY = (189, 195, 199)
DARK_GRAY = (52, 73, 94)


WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Güçlü Şifre Üreticisi")


font_large = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 24)

class PasswordGenerator:
    def __init__(self):
        self.input_text = ""
        self.generated_password = ""
        self.message = ""
        self.message_color = BLACK
        self.stage = "input"  
        
    def generate_strong_password(self, length):
        """Güçlü şifre üret"""
        if length < 4:
            return None
            
        
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
        
        
        random.shuffle(password)
        return ''.join(password)
    
    def save_password_to_file(self, password):
        """Şifreyi dosyaya kaydet"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sifre_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Üretilen Şifre: {password}\n")
                f.write(f"Uzunluk: {len(password)} karakter\n")
                f.write(f"Oluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                f.write("\nGüvenlik Notları:\n")
                f.write("- Bu şifreyi güvenli bir yerde saklayın\n")
                f.write("- Şifreyi kimseyle paylaşmayın\n")
                f.write("- Düzenli olarak şifrenizi değiştirin\n")
            
            return filename
        except Exception as e:
            return None
    
    def handle_input(self, event):
        """Klavye girişlerini işle"""
        if event.type == pygame.KEYDOWN:
            if self.stage == "input":
                if event.key == pygame.K_RETURN:
                    
                    if self.input_text.isdigit() and int(self.input_text) > 0:
                        length = int(self.input_text)
                        if length > 100:
                            self.message = "Maksimum uzunluk 100 karakter olabilir!"
                            self.message_color = RED
                        else:
                            password = self.generate_strong_password(length)
                            if password:
                                self.generated_password = password
                                self.stage = "generated"
                                self.message = f"{length} karakterlik güçlü şifre üretildi!"
                                self.message_color = GREEN
                            else:
                                self.message = "Minimum 4 karakter uzunluğunda şifre gerekli!"
                                self.message_color = RED
                    else:
                        self.message = "Lütfen geçerli bir sayı girin!"
                        self.message_color = RED
                        
                elif event.key == pygame.K_BACKSPACE:
                    
                    self.input_text = self.input_text[:-1]
                    self.message = ""
                    
                else:
                    
                    if event.unicode.isdigit() and len(self.input_text) < 3:
                        self.input_text += event.unicode
                        self.message = ""
                        
            elif self.stage == "generated":
                if event.key == pygame.K_s:
                    
                    filename = self.save_password_to_file(self.generated_password)
                    if filename:
                        self.stage = "saved"
                        self.message = f"Şifre '{filename}' dosyasına kaydedildi!"
                        self.message_color = GREEN
                    else:
                        self.message = "Dosya kaydedilemedi!"
                        self.message_color = RED
                        
                elif event.key == pygame.K_r:
                    
                    self.reset()
                    
            elif self.stage == "saved":
                if event.key == pygame.K_r:
                    
                    self.reset()
    
    def reset(self):
        
        self.input_text = ""
        self.generated_password = ""
        self.message = ""
        self.stage = "input"
    
    def draw(self, screen):
        
        screen.fill(WHITE)
        
        
        title = font_large.render("Güçlü Şifre Üreticisi", True, DARK_GRAY)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        if self.stage == "input":
            
            prompt = font_medium.render("Şifre uzunluğunu girin (4-100):", True, BLACK)
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 120))
            
            
            input_box = pygame.Rect(WIDTH//2 - 100, 160, 200, 40)
            pygame.draw.rect(screen, WHITE, input_box)
            pygame.draw.rect(screen, BLUE, input_box, 2)
            
            
            text_surface = font_medium.render(self.input_text, True, BLACK)
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
            
            
            if pygame.time.get_ticks() % 1000 < 500:  
                cursor_x = input_box.x + 10 + text_surface.get_width()
                pygame.draw.line(screen, BLACK, (cursor_x, input_box.y + 8), (cursor_x, input_box.y + 32), 2)
            
            
            instruction = font_small.render("Enter tuşuna basın", True, GRAY)
            screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, 220))
            
        elif self.stage == "generated":
            
            success_text = font_medium.render("Şifre başarıyla üretildi!", True, GREEN)
            screen.blit(success_text, (WIDTH//2 - success_text.get_width()//2, 120))
            
            
            password_box = pygame.Rect(50, 160, WIDTH-100, 60)
            pygame.draw.rect(screen, GRAY, password_box)
            pygame.draw.rect(screen, DARK_GRAY, password_box, 2)
            
            
            password_text = self.generated_password
            if len(password_text) > 40:
                
                line1 = password_text[:40]
                line2 = password_text[40:]
                
                text1 = font_small.render(line1, True, BLACK)
                text2 = font_small.render(line2, True, BLACK)
                screen.blit(text1, (password_box.x + 10, password_box.y + 10))
                screen.blit(text2, (password_box.x + 10, password_box.y + 35))
            else:
                text = font_medium.render(password_text, True, BLACK)
                screen.blit(text, (password_box.x + 10, password_box.y + 15))
            
            
            save_text = font_small.render("S - Dosyaya Kaydet", True, BLUE)
            restart_text = font_small.render("R - Yeniden Başla", True, BLUE)
            screen.blit(save_text, (WIDTH//2 - 100, 260))
            screen.blit(restart_text, (WIDTH//2 - 100, 285))
            
        elif self.stage == "saved":
            
            success_text = font_medium.render("Şifre dosyaya kaydedildi!", True, GREEN)
            screen.blit(success_text, (WIDTH//2 - success_text.get_width()//2, 150))
            
            
            restart_text = font_small.render("R - Yeni Şifre Üret", True, BLUE)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 200))
        
        
        if self.message:
            message_surface = font_small.render(self.message, True, self.message_color)
            screen.blit(message_surface, (WIDTH//2 - message_surface.get_width()//2, HEIGHT - 60))

def main():
    clock = pygame.time.Clock()
    generator = PasswordGenerator()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                generator.handle_input(event)
        
        
        generator.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()