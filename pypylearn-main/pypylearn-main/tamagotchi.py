import pygame, random, sys, os, platform
from pygame.locals import *

if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

# ============================================================
# SECTION 1: ANIMATION DATA
# These are the visual representations of the Tamagotchi
# Each tuple contains 32 numbers representing 32 rows of pixels
# ============================================================

#Animations
IDLE_EGG = ((0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x7e000,0x87000,0x103800,0x300c00,0x700400,0x418200,0x418200,0x400200,0x700600,0x3c0c00,0x1e0800,0x3ffc00,0x0),(0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x7e000,0x87000,0x103800,0x300c00,0x700400,0x400200,0x418200,0x418200,0x700600,0x3c0c00,0xffff00,0x0))
IDLE_BABY = ((0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x78000,0xb4000,0x1fe000), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x78000,0xcc000,0x84000,0xb4000,0x84000,0x78000,0x0))
IDLE_MATURE = ((0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0xfc00,0x10200,0x24900,0x20100,0x23100,0x20100,0x20100,0x10200,0xfc00,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0xfc00,0x10200,0x28500,0x23100,0x23100,0x20100,0x10200,0xfc00,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0))
SLEEP_BABY = ((0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x78000,0xfc000,0x1fe000), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x1fe000,0x3ff000))
SLEEP_MATURE = ((0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x3fc00,0x40200,0x80100), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x1f800,0x20400,0x40200,0x40200))
OVERLAY_ZZZ = ((0x0,0x0,0x0,0x0,0xf800000,0x4000000,0x2000000,0x1000000,0xf800000,0x0,0x0,0x3c00000,0x1000000,0x800000,0x3c00000,0x0,0x700000,0x200000,0x700000,0x0,0x80000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0xf800000,0x4000000,0x2000000,0x1000000,0xf800000,0x0,0x0,0x3c00000,0x1000000,0x800000,0x3c00000,0x0,0x700000,0x200000,0x700000,0x0,0x80000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0))
OVERLAY_EAT = ((0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x4000000,0x2000000,0x7700000,0xff00000,0xfd00000,0xff00000,0x7f00000,0x7e00000,0x3c00000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x4000000,0x2000000,0x7700000,0xfe00000,0xfc00000,0xfe00000,0x7f00000,0x7e00000,0x3c00000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x4000000,0x2000000,0x7400000,0xf800000,0xf800000,0xf800000,0x7c00000,0x7e00000,0x3c00000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x4000000,0x2000000,0x7000000,0xf000000,0xe000000,0xe000000,0x7000000,0x7800000,0x3c00000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x4000000,0x2000000,0x1000000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0))
OVERLAY_STINK = ((0x0,0x0,0x0,0x0,0x10000000,0x8000008,0x10000004,0xa000028,0x11000044,0xa000028,0x1000044,0x12000020,0x21000040,0x10000000,0x20000000,0x10000000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0x10000000,0x8000008,0x10000004,0xa000028,0x11000044,0xa000028,0x1000044,0x12000020,0x21000040,0x10000000,0x20000000,0x10000000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0))
OVERLAY_DEAD = ((0x0,0x0,0xfc00000,0x1fe00000,0x1b600000,0x1fe00000,0xfc00000,0xfc00000,0x5400000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x7e00000,0xff00000,0xdb00000,0xff00000,0x7e00000,0x7e00000,0x2a00000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0))
OVERLAY_EXCLAIM = ((0x0,0x20,0x70,0x70,0x70,0x70,0x70,0x70,0x70,0x20,0x0,0x20,0x70,0x20,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0), (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0))
OVERLAY_CLEAN = ((0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2,0x2),)

# ============================================================
# SECTION 2: UI COMPONENTS
# These are the icons and displays shown on screen
# ============================================================

#Components
SELECTOR = (0x7800000f,0x60000003,0x40000001,0x40000001,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x40000001,0x40000001,0x60000003,0x7800000f)
FEED = (0x0,0x0,0x0,0x0,0x0,0x7805a0,0x7c05a0,0x7c05a0,0x7c05a0,0x7c05a0,0x7c05a0,0x7c05a0,0x7c07e0,0x7c07e0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x7803c0,0x300180,0x0,0x0,0x0)
FLUSH = (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x2000000,0x5000000,0x5000000,0x4800000,0x4800000,0x4400000,0x4400000,0x4400000,0x2200000,0x2200000,0x1200000,0xffff00,0x1200280,0x11ffd00,0x1000080,0x1000080,0x1000080,0x1000080,0x1000080,0x1000080,0x1000040,0xffff80,0x0,0x0,0x0)
HEALTH = (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x3ffffc0,0xc000030,0x10912488,0x10912488,0x10492908,0x8000010,0x8000010,0x8000410,0x4000820,0x4001020,0x4002020,0x201c040,0x201c040,0x1ffff80,0x0,0x0,0x0)
ZZZ = (0x0,0x0,0x0,0x0,0xf800000,0x4000000,0x2000000,0x1000000,0xf800000,0x0,0x0,0x3c00000,0x1000000,0x800000,0x3c00000,0x0,0x700000,0x200000,0x700000,0x0,0x80000,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0)
DISPLAY_HUNGER = (0x0,0x0,0x3bcc94a4,0x4852b4a4,0x39c2d4bc,0x485a94a4,0x4bdc9324,0x0,0x0,0x0,0x0,0x1ffffff8,0x20000004,0x20000004,0x20000004,0x20000004,0x20000004,0x1ffffff8,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0)
DISPLAY_ENERGY = (0x0,0x0,0x498ef4bc,0x4a521584,0x704e368c,0x43521484,0x3b92f4bc,0x0,0x0,0x0,0x0,0x1ffffff8,0x20000004,0x20000004,0x20000004,0x20000004,0x20000004,0x1ffffff8,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0)
DISPLAY_WASTE = (0x0,0x0,0x7df38e44,0x4405144,0x1c439f44,0x4441154,0x7c439128,0x0,0x0,0x0,0x0,0x1ffffff8,0x20000004,0x20000004,0x20000004,0x20000004,0x20000004,0x1ffffff8,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0)
DISPLAY_AGE = (0x0,0x0,0x7ce38,0x5144,0x1c17c,0x5944,0x7de44,0x0,0x0,0x0,0x0,0x1ffffff8,0x20000004,0x20000004,0x20000004,0x20000004,0x20000004,0x1ffffff8,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0)
DISPLAY_BACK = (0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x498c710,0x2a52918,0x185e77c,0x2a52918,0x4992710,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0)

# ============================================================
# SECTION 3: GAME CONSTANTS
# These control the game rules and thresholds
# ============================================================

# Age milestones - when Tamagotchi evolves or dies
AGE_HATCH = 128                      # Age when egg hatches into baby
AGE_MATURE = 796                     # Age when baby becomes mature
AGE_RESET_THRESHOLD = 1000           # NEW: Age when Tamagotchi resets (adjustable: 100, 1000, 5000, etc.)
AGE_DEATHFROMNATURALCAUSES =1000    # Maximum age before death

# Hunger levels - how hungry the Tamagotchi is
HUNGER_CANEAT = 32                   # Minimum hunger to allow eating
HUNGER_NEEDSTOEAT = 128             # Hunger level that shows warning
HUNGER_SICKFROMNOTEATING = 256      # Hunger causes sickness
HUNGER_DEADFROMNOTEATING = 512      # Hunger causes death

# Energy levels - how tired the Tamagotchi is
ENERGY_CANSLEEP = 150               # Maximum energy to allow sleeping
ENERGY_TIRED = 64                   # Energy level that shows warning
ENERGY_PASSOUT = 8                  # Energy level that forces sleep (auto-passout)

# Waste levels - how dirty the Tamagotchi is
WASTE_EXPUNGE = 256                 # Waste level that affects happiness
WASTE_AUTO_CLEAN = 400              # NEW: Waste level where Tamagotchi auto-cleans itself

# NEW: Energy gains from activities
ENERGY_FROM_FOOD = 20               # Energy gained when eating
ENERGY_FROM_SLEEP = 8               # Energy gained per cycle while sleeping

# Colors for the display
BG_COLOR = (160, 178, 129)          # Greenish background (like original Tamagotchi)
PIXEL_COLOR = (10, 12, 6)           # Dark color for pixels
NONPIXEL_COLOR = (156, 170, 125)    # Slightly different background
TRANSPARENT_COLOR = (0, 0, 0, 0)    # Transparent for overlays
BTN_BORDER_COLOR = (128, 12, 24)    # Button border (dark red)
BTN_CENTER_COLOR = (200, 33, 44)    # Button center (bright red)
ERROR_COLOR = (200, 50, 50)         # Red for error messages
SUCCESS_COLOR = (50, 150, 50)       # Green for success messages

# Game timing
FPS = 30                            # Frames per second
SECOND = 1000                       # Milliseconds in a second
SCREEN_WIDTH = 500                  # Screen width in pixels
SCREEN_HEIGHT = 520                 # Screen height in pixels

# ============================================================
# SECTION 4: HELPER FUNCTIONS
# These functions help with rendering and calculations
# ============================================================

def bitor(current_frame, overlay_frame):
    """
    Combines two animation frames using bitwise OR
    This is used to overlay effects (like ZZZ or food) on the pet
    
    Example: Pet animation + ZZZ overlay = Pet sleeping with ZZZ
    """
    l = []
    for i in range(32):
        b = current_frame[i] | overlay_frame[i]  # Bitwise OR combines the pixels
        l.append(b)
    return tuple(l)

def get_bits(number, num_bits):
    """
    Converts a number into individual bits (0 or 1)
    This is how we turn the animation data into pixels on screen
    
    Example: Number 7 (binary: 111) becomes [1, 1, 1]
    """
    return [(number >> bit) & 1 for bit in range(num_bits - 1, -1, -1)]

def render_display(image_data, fg_color, bg_color, off=0, percv=0):
    """
    Draws the main display area showing the Tamagotchi
    
    Parameters:
    - image_data: The animation frame to draw
    - fg_color: Color for "on" pixels (foreground)
    - bg_color: Color for "off" pixels (background)
    - off: Offset for animation movement
    - percv: Percentage bar for stats (0-27)
    """
    for y in range(32):  # 32 rows
        bits = get_bits(image_data[y], 32+off)
        bits.reverse()
        for x in range(off, 32+off):  # 32 columns
            color = bg_color
            if x in range(len(bits)):
                # Draw pixel if bit is 1, or if drawing percentage bar
                if bits[x] or percv > 0 and y > 11 and x > 2 and y < 17 and x < 3 + percv:
                    color = fg_color
            pygame.draw.rect(screen, color, ((x-off)*10+32, y*10+64, 8, 8))

def render_component(surface, image_data, fg_color, bg_color=(255, 255, 255)):
    """
    Draws UI components like buttons and icons
    Similar to render_display but for smaller elements
    """
    pixels = pygame.PixelArray(surface)
    for y in range(surface.get_height()):
        bits = get_bits(image_data[y], surface.get_width())
        for x, bit in enumerate(bits):
            if (bit):
                pixels[x][y] = fg_color
            else:
                pixels[x][y] = bg_color
    del pixels

# ============================================================
# SECTION 5: GAME LOGIC FUNCTIONS
# These control the Tamagotchi's behavior
# ============================================================

def do_random_event(pet):
    """
    Random events that happen occasionally to add unpredictability
    Makes the game more interesting and less predictable
    """
    num = random.randint(0, 31)  # Random number 0-31
    if num == 12:
        pet['hunger'] += 1      # Sometimes gets hungrier faster
    elif num == 16:
        pet['energy'] -= 1      # Sometimes gets tired faster
    elif num == 18:
        pet['energy'] += 1      # Sometimes gains energy
    elif num == 20:
        pet['waste'] += 1       # Sometimes makes more waste
    elif num == 7:
        pet['happiness'] += 1   # Sometimes gets happier
    elif num == 4:
        pet['happiness'] -= 1   # Sometimes gets sadder

def do_cycle(pet):
    """
    Main game cycle - runs every second
    Updates all stats and checks for auto-clean
    
    Returns: "AUTO_CLEAN" if Tamagotchi cleans itself, None otherwise
    """
    do_random_event(pet)  # First do a random event
    
    # Regular stat changes every second
    pet['hunger'] += 1    # Gets hungrier
    pet['waste'] += 1     # Makes more waste
    pet['energy'] -= 1    # Gets more tired
    pet['age'] += 2       # Gets older
    
    # NEW FEATURE: Auto-clean when waste gets too high
    # Tamagotchi cleans up after itself!
    if pet['waste'] >= WASTE_AUTO_CLEAN:
        pet['waste'] = 0
        return "AUTO_CLEAN"
    
    # Waste affects happiness
    if pet['waste'] >= WASTE_EXPUNGE:
        pet['happiness'] -= 1
    
    return None

def get_offset():
    """
    Creates a small random movement for the Tamagotchi
    Makes it look like it's bouncing or moving slightly
    """
    return random.randint(-3, 2)

def get_next_frame(animation_frames, current_frame):
    """
    Cycles through animation frames
    Creates the illusion of movement by switching between frames
    """
    return (current_frame + 1) % len(animation_frames)

def trigger_death(stage):
    """
    Handles death animation
    Shows sleeping position with skull overlay
    """
    if stage == 1:
        current_anim = SLEEP_BABY
    elif stage == 2:
        current_anim = SLEEP_MATURE
    overlay_anim = OVERLAY_DEAD
    return current_anim, overlay_anim, True, True

def trigger_sleep(stage):
    """
    Handles sleep animation
    Shows sleeping position with ZZZ overlay
    """
    if stage == 1:
        current_anim = SLEEP_BABY
    elif stage == 2:
        current_anim = SLEEP_MATURE
    overlay_anim = OVERLAY_ZZZ
    return current_anim, overlay_anim, True, True

def reset_tamagotchi():
    """
    NEW FUNCTION: Resets Tamagotchi to beginning
    Called when age reaches threshold
    Returns a new pet dictionary with starting stats
    """
    return {
        'hunger': 0,
        'energy': 256,
        'waste': 0,
        'age': 0,
        'happiness': 0
    }

# ============================================================
# SECTION 6: UI FUNCTIONS
# These handle menus, buttons, and displays
# ============================================================

def update_page(startpageid):
    """
    Changes the stats page display
    0=Hunger, 1=Age, 2=Waste, 3=Energy, 4=Back
    """
    if startpageid == 0:
        stats_page = DISPLAY_HUNGER
    elif startpageid == 1:
        stats_page = DISPLAY_AGE
    elif startpageid == 2:
        stats_page = DISPLAY_WASTE
    elif startpageid == 3:
        stats_page = DISPLAY_ENERGY
    elif startpageid == 4:
        stats_page = DISPLAY_BACK
    return stats_page

def get_button_at_pixel(x, y):
    """
    Determines which button was clicked based on mouse position
    Returns: 0 (left button), 1 (middle button), 2 (right button), or None
    """
    if y > 420 and y < 484:  # Check if click is in button area
        button = 0
        for i in range(0, 288, 96):  # Check each of the 3 buttons
            if x > 64 + i and x < 128 + i:
                return button
            else:
                button += 1
    return None

def render_buttons(left, top):
    """
    Draws the three circular buttons at the bottom
    """
    for i in range(0, 288, 96):  # 3 buttons, 96 pixels apart
        pygame.draw.ellipse(screen, BTN_BORDER_COLOR, (left + i, top, 64, 64))
        pygame.draw.ellipse(screen, BTN_CENTER_COLOR, (left + i + 4, top + 4, 56, 56))
        pygame.draw.ellipse(screen, PIXEL_COLOR, (left + i, top, 64, 64), 1)

def show_message(message, color, duration):
    """
    NEW FUNCTION: Creates a message to display on screen
    Returns a dictionary with message info
    
    Parameters:
    - message: Text to display
    - color: Color of the message
    - duration: How many frames to show the message
    """
    return {'text': message, 'color': color, 'timer': duration}

# ============================================================
# SECTION 7: MAIN GAME FUNCTION
# This is where everything comes together
# ============================================================

def main():
    global screen, clock
    
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Tamagotchi')
    
    # Create fonts for text
    font = pygame.font.SysFont('Arial', 14)
    message_font = pygame.font.SysFont('Arial', 18, bold=True)
    
    # Create selector image (the cursor that shows which button is selected)
    selector_img = pygame.Surface((32, 32)).convert_alpha()
    render_component(selector_img, SELECTOR, PIXEL_COLOR, TRANSPARENT_COLOR)
    
    # Set up timer to trigger game updates every second
    pygame.time.set_timer(USEREVENT + 1, SECOND)

    # ============================================================
    # GAME STATE VARIABLES
    # ============================================================
    
    # Tamagotchi stats - the core data of your pet
    pet = {
        'hunger': 0,      # 0 = full, higher = hungrier
        'energy': 256,    # 256 = max energy, 0 = exhausted
        'waste': 0,       # 0 = clean, higher = dirtier
        'age': 0,         # Starts at 0, increases every cycle
        'happiness': 0    # Can go positive or negative
    }
    
    # Counters - keep track of positions and frames
    off = 0           # Offset for animation movement
    selid = 0         # Which button is selected (0-3)
    startpageid = 0          # Which stats page is showing (0-4)
    stage = 0         # Evolution stage (0=egg, 1=baby, 2=mature)
    frame = 0         # Current animation frame
    ol_frame = 0      # Current overlay frame
    
    # Flags - track the current state of the game
    stats = False         # Is stats screen showing?
    has_overlay = False   # Is there an overlay (ZZZ, food, etc.)?
    cleaning = False      # Is cleaning animation playing?
    eating = False        # Is eating animation playing?
    sleeping = False      # Is Tamagotchi sleeping?
    dead = False          # Is Tamagotchi dead?
    update_game = False   # Should we update game logic this frame?
    
    # NEW: Message system for displaying feedback to player
    message = None        # Current message to display
    message_timer = 0     # How long to show message
    
    # NEW: Reset counter for tracking resets
    reset_count = 0       # Number of times Tamagotchi has been reset
    
    # Animation states
    current_anim = IDLE_EGG      # Current main animation
    overlay_anim = OVERLAY_ZZZ    # Current overlay animation
    stats_page = DISPLAY_HUNGER   # Current stats page

    # ============================================================
    # MAIN GAME LOOP
    # This runs continuously until you close the game
    # ============================================================
    
    while True:
        screen.fill(BG_COLOR)  # Clear screen with background color
        mousex = 0
        mousey = 0

        # ============================================================
        # EVENT HANDLING
        # Check for user input (clicks, closing window)
        # ============================================================
        
        for event in pygame.event.get():
            if event.type == QUIT:
                # User closed the window
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                # User clicked mouse - save position
                mousex, mousey = event.pos
            elif event.type == USEREVENT + 1:
                # Timer event - happens every second (or faster during cleaning)
                if cleaning:
                    # Speed up timer during cleaning animation
                    pygame.time.set_timer(USEREVENT + 1, int(SECOND / 10))
                update_game = True  # Flag to update game logic

        # ============================================================
        # BUTTON LOGIC
        # Determine which button was clicked and what to do
        # ============================================================
        
        button = get_button_at_pixel(mousex, mousey)
        
        if button == 0:  # LEFT BUTTON - Navigate left
            if stats:
                # In stats screen - previous page
                startpageid -= 1
                if startpageid <= -1:
                    startpageid = 4
                stats_page = update_page(startpageid)
            else:
                # In main screen - previous action
                selid -= 1
                if selid <= -1:
                    selid = 3
                    
        elif button == 1:  # MIDDLE BUTTON - Execute action
            if stage > 0 or selid == 2:  # Can only act if hatched (except stats)
                
                if selid == 0:  # FEED ACTION
                    # Check if Tamagotchi is hungry enough to eat
                    if pet['hunger'] >= HUNGER_CANEAT:
                        eating = True
                        overlay_anim = OVERLAY_EAT
                        ol_frame = 0
                        has_overlay = True
                        message = show_message("I'm eating! Yummy!", SUCCESS_COLOR, 60)
                        message_timer = 60
                    else:
                        # Not hungry - show error
                        message = show_message("I'm not hungry! :(", ERROR_COLOR, 60)
                        message_timer = 60
                        
                elif selid == 1:  # CLEAN ACTION
                    # Check if there's enough waste to clean
                    if pet['waste'] >= 50:
                        cleaning = True
                        overlay_anim = OVERLAY_CLEAN
                        ol_frame = 0
                        has_overlay = True
                        message = show_message("Cleaning up...", SUCCESS_COLOR, 60)
                        message_timer = 60
                    else:
                        # Already clean - show error
                        message = show_message("I'm already clean!", ERROR_COLOR, 60)
                        message_timer = 60
                        
                elif selid == 2:  # STATS ACTION
                    # Toggle stats display
                    stats = not stats
                    
                elif selid == 3:  # SLEEP ACTION
                    # Check if Tamagotchi has low enough energy to sleep
                    if pet['energy'] <= ENERGY_CANSLEEP:
                        current_anim, overlay_anim, sleeping, has_overlay = trigger_sleep(stage)
                        message = show_message("Zzz...", SUCCESS_COLOR, 60)
                        message_timer = 60
                    else:
                        # Too energetic to sleep - show error
                        message = show_message("I'm not tired yet!", ERROR_COLOR, 60)
                        message_timer = 60
                        
        elif button == 2:  # RIGHT BUTTON - Navigate right
            if stats:
                # In stats screen - next page
                startpageid += 1
                startpageid %= 5
                stats_page = update_page(startpageid)
            else:
                # In main screen - next action
                selid += 1
                selid %= 4

        # ============================================================
        # GAME LOGIC UPDATE
        # This runs every second (when update_game is True)
        # ============================================================
        
        if update_game:
            
            # --------------------------------------------------------
            # AGE AND EVOLUTION SYSTEM
            # --------------------------------------------------------
            
            # Check for hatching (egg -> baby)
            if stage == 0 and pet['age'] > AGE_HATCH:
                stage += 1
                current_anim = IDLE_BABY
                has_overlay = False
                message = show_message("*hatched* I'm a baby!", SUCCESS_COLOR, 90)
                message_timer = 90
            
            # Check for maturity (baby -> mature)
            if stage == 1 and pet['age'] > AGE_MATURE:
                stage += 1
                current_anim = IDLE_MATURE
                message = show_message("I just became an adult! :D", SUCCESS_COLOR, 90)
                message_timer = 90
            
            # --------------------------------------------------------
            # NEW FEATURE: AGE RESET SYSTEM
            # When Tamagotchi reaches age threshold, reset to beginning
            # --------------------------------------------------------
            
            if pet['age'] >= AGE_RESET_THRESHOLD and not dead:
                # Reset the Tamagotchi!
                reset_count += 1
                pet = reset_tamagotchi()
                stage = 0
                current_anim = IDLE_EGG
                has_overlay = False
                sleeping = False
                eating = False
                cleaning = False
                
                # Show reset message
                message = show_message(f"Restarting... {reset_count + 1}", SUCCESS_COLOR, 120)
                message_timer = 120
            
            # --------------------------------------------------------
            # EATING ANIMATION
            # --------------------------------------------------------
            
            if eating and ol_frame == len(overlay_anim) - 1:
                # Eating animation finished
                eating = False
                has_overlay = False
                ol_frame = 0
                pet['hunger'] = 0  # Reset hunger to 0 (full)
                
                # NEW: Eating also restores energy!
                pet['energy'] += ENERGY_FROM_FOOD
                if pet['energy'] > 256:
                    pet['energy'] = 256  # Cap at maximum
            
            # --------------------------------------------------------
            # SLEEPING SYSTEM
            # --------------------------------------------------------
            
            if sleeping:
                # NEW: Sleeping restores energy
                pet['energy'] += ENERGY_FROM_SLEEP
                
                # Wake up when fully rested
                if pet['energy'] >= 256:
                    sleeping = False
                    has_overlay = False
                    
                    # Return to appropriate animation for current stage
                    if stage == 0:
                        current_anim = IDLE_EGG
                    elif stage == 1:
                        current_anim = IDLE_BABY
                    elif stage == 2:
                        current_anim = IDLE_MATURE
                    
                    message = show_message("Waking up, feeling fresh :D", SUCCESS_COLOR, 60)
                    message_timer = 60
            
            # --------------------------------------------------------
            # CLEANING ANIMATION
            # --------------------------------------------------------
            
            if cleaning:
                off -= 1  # Scroll animation
                if off == -33:
                    # Cleaning animation finished
                    off = 0
                    cleaning = False
                    has_overlay = False
                    pet['waste'] = 0  # Reset waste to 0 (clean)
                    pygame.time.set_timer(USEREVENT + 1, SECOND)  # Reset timer speed
            else:
                # --------------------------------------------------------
                # NORMAL GAME UPDATES (when not animating)
                # --------------------------------------------------------
                
                if not dead:
                    # Animate the pet
                    frame = get_next_frame(current_anim, frame)
                    off = get_offset()
                
                if not sleeping and not dead:
                    # Run the game cycle (aging, hunger, etc.)
                    cycle_result = do_cycle(pet)
                    
                    # NEW: Check if auto-clean happened
                    if cycle_result == "AUTO_CLEAN":
                        message = show_message("I'm cleaning myself..", SUCCESS_COLOR, 60)
                        message_timer = 60
                    
                    # --------------------------------------------------------
                    # NEW FEATURE: AUTO-PASSOUT FROM LOW ENERGY
                    # If energy drops too low, force sleep
                    # --------------------------------------------------------
                    
                    if pet['energy'] < ENERGY_PASSOUT:
                        if stage > 0:
                            pet['happiness'] -= 64  # Lose happiness from passing out
                        current_anim, overlay_anim, sleeping, has_overlay = trigger_sleep(stage)
                        message = show_message("I'm too tired! Passing out...", ERROR_COLOR, 90)
                        message_timer = 90
                
                # --------------------------------------------------------
                # OVERLAY SYSTEM (warnings and effects)
                # --------------------------------------------------------
                
                if not sleeping and not cleaning and not eating and not dead:
                    # Show appropriate overlay based on conditions
                    if pet['waste'] >= WASTE_EXPUNGE:
                        # Too dirty - show stink clouds
                        overlay_anim = OVERLAY_STINK
                        has_overlay = True
                    elif pet['energy'] <= ENERGY_TIRED or pet['hunger'] >= HUNGER_NEEDSTOEAT \
                        or pet['waste'] >= WASTE_EXPUNGE - WASTE_EXPUNGE // 3:
                        # Needs attention - show exclamation mark
                        overlay_anim = OVERLAY_EXCLAIM
                        has_overlay = True
                    else:
                        # All good - no overlay needed
                        has_overlay = False
                
                # --------------------------------------------------------
                # DEATH SYSTEM
                # --------------------------------------------------------
                
                if not dead:
                    # Check death conditions
                    if pet['hunger'] >= HUNGER_DEADFROMNOTEATING or \
                       pet['age'] >= AGE_DEATHFROMNATURALCAUSES:
                        # Tamagotchi died!
                        off = 3
                        current_anim, overlay_anim, dead, has_overlay = trigger_death(stage)
                        message = show_message("I'm dead. RIP.", ERROR_COLOR, 180)
                        message_timer = 180
            
            # Animate overlay if present
            if has_overlay:
                ol_frame = get_next_frame(overlay_anim, ol_frame)
            
            update_game = False  # Reset update flag

        # ============================================================
        # RENDERING SECTION
        # Draw everything on screen
        # ============================================================
        
        # --------------------------------------------------------
        # Draw action icons at top
        # --------------------------------------------------------
        
        zipped = zip([FEED, FLUSH, HEALTH, ZZZ], [i for i in range(64, 320, 64)])
        z = list(zipped)
        for i in range(len(z)):
            img = pygame.Surface((32, 32))
            render_component(img, z[i][0], PIXEL_COLOR, NONPIXEL_COLOR)
            screen.blit(pygame.transform.flip(img, True, False), (z[i][1], 16))

        # --------------------------------------------------------
        # Draw selector (shows which action is selected)
        # --------------------------------------------------------
        
        screen.blit(pygame.transform.flip(selector_img, True, False), (64+(selid*64), 16))

        # --------------------------------------------------------
        # Draw main display (Tamagotchi or stats)
        # --------------------------------------------------------
        
        if stats:
            # STATS MODE: Show stat bars
            if startpageid == 0:
                percv = pet['hunger'] * 27 // HUNGER_NEEDSTOEAT
            elif startpageid == 1:
                percv = pet['age'] * 27 // AGE_RESET_THRESHOLD  # NEW: Uses reset threshold
            elif startpageid == 2:
                percv = (pet['waste'] % WASTE_EXPUNGE) * 27 // WASTE_EXPUNGE
            elif startpageid == 3:
                percv = pet['energy'] * 27 // 256
            elif startpageid == 4:
                percv = 0
            
            if percv > 27:
                percv = 27
            
            render_display(stats_page, PIXEL_COLOR, NONPIXEL_COLOR, 0, percv)
        else:
            # NORMAL MODE: Show Tamagotchi
            if has_overlay:
                # Combine pet animation with overlay (like ZZZ or food)
                animation = bitor(current_anim[frame], overlay_anim[ol_frame])
            else:
                animation = current_anim[frame]
            
            render_display(animation, PIXEL_COLOR, NONPIXEL_COLOR, off)

        # --------------------------------------------------------
        # Draw debug information (shows all stats)
        # --------------------------------------------------------
        
        surf = font.render('DEBUG --', True, PIXEL_COLOR)
        screen.blit(surf, (360, 60))
        
        debug = (('AGE: %s', 'HUNGER: %s', 'ENERGY: %s', 'WASTE: %d', 'HAPPINESS: %s'), \
                ('age', 'hunger', 'energy', 'waste', 'happiness'))
        
        for pos, y in enumerate(i for i in range(70, 120, 10)):
            surf = font.render(debug[0][pos] % pet[debug[1][pos]], True, PIXEL_COLOR)
            screen.blit(surf, (360, y))
        
        # NEW: Show reset count
        reset_surf = font.render(f'RESETS: {reset_count}', True, PIXEL_COLOR)
        screen.blit(reset_surf, (360, 130))
        
        # NEW: Show age until reset
        age_until_reset = AGE_RESET_THRESHOLD - pet['age']
        if age_until_reset > 0 and not dead:
            reset_info = font.render(f'Reset in: {age_until_reset}', True, PIXEL_COLOR)
            screen.blit(reset_info, (360, 140))

        # --------------------------------------------------------
        # NEW: Draw message system
        # --------------------------------------------------------
        
        if message and message_timer > 0:
            # Draw semi-transparent background for message
            msg_surf = message_font.render(message['text'], True, message['color'])
            msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, 380))
            
            # Background box
            padding = 10
            bg_rect = pygame.Rect(msg_rect.left - padding, msg_rect.top - padding,
                                 msg_rect.width + padding * 2, msg_rect.height + padding * 2)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect)
            pygame.draw.rect(screen, PIXEL_COLOR, bg_rect, 2)
            
            # Message text
            screen.blit(msg_surf, msg_rect)
            
            # Countdown timer
            message_timer -= 1
            if message_timer <= 0:
                message = None

        # --------------------------------------------------------
        # Draw buttons at bottom
        # --------------------------------------------------------
        
        render_buttons(64, 420)

        # --------------------------------------------------------
        # Update display and maintain frame rate
        # --------------------------------------------------------
        
        pygame.display.update()
        clock.tick(FPS)

# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == '__main__':
    main()