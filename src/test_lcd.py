from lcd_display import LCD_display
import constants as cst

lcd = LCD_display(cst.LCD_BUS)
lcd.set_cursor(1)
lcd.display_char(65)

while True:
    pass
