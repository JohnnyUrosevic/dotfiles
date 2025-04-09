#########################################
########## Importing Libreries ##########
#########################################

import re
from libqtile import backend, bar, layout, widget, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

import os
import subprocess

from colors import gruv_mat
from colors import gruvbox

fullscreen_mode = False
fullscreen_window = None

#########################################
#############    hooks     ##############
#########################################


########## Auto Start Programs ##########
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/autostart/autostart.sh")
    subprocess.Popen([home])


@hook.subscribe.group_window_add
def switchtogroup(group, window):
    name = group.info()['name']
    if name != 'scratchpad':
        go_to_group(qtile.groups_map[name])(qtile)


def enter_fullscreen(qtile, window, group):
    global fullscreen_mode
    global fullscreen_window

    fullscreen_mode = True
    fullscreen_window = (window, group)

    qtile.windows_map[window].togroup('fullscreen', switch_group=False)
    qtile.focus_screen(0)
    qtile.groups_map['fullscreen'].toscreen()

    qtile.config.update(follow_mouse_focus=False)


def exit_fullscreen(qtile):
    global fullscreen_mode
    global fullscreen_window

    fullscreen_mode = False

    window, home = fullscreen_window

    if window in [info['id'] for info in qtile.windows()]:
        qtile.windows_map[window].togroup(home)

    fullscreen_window = None
    qtile.config.update(follow_mouse_focus=True)


def fullscreen_window_exists(qtile):
    for info in qtile.windows():
        if info['fullscreen']:
            return True, info['id'], info['group']

    return False, None, None


@hook.subscribe.float_change
def checkforfullscreen():
    global fullscreen_mode
    # not ('firefox' in qtile.current_window.get_wm_class())
    res, window, group = fullscreen_window_exists(qtile)
    if res:
        enter_fullscreen(qtile, window, group)
    else:
        exit_fullscreen(qtile)


@hook.subscribe.client_killed
def client_killed(window):
    checkforfullscreen()


@hook.subscribe.client_new
def new_client(window):
    checkforfullscreen()


#########################################
######### Shortcut Variables ############
#########################################
#### Button Variables ####
mod = "mod4"
alt = "mod1"

########## Powerline from extras ########

arrow_powerlineRight = {"decorations": [PowerLineDecoration(path="arrow_right", size=11)]}
arrow_powerlineLeft = {"decorations": [PowerLineDecoration(path="arrow_left", size=11)]}
rounded_powerlineRight = {"decorations": [PowerLineDecoration(path="rounded_right", size=11)]}
rounded_powerlineLeft = {"decorations": [PowerLineDecoration(path="rouded_left", size=11)]}
slash_powerlineRight = {"decorations": [PowerLineDecoration(path="forward_slash", size=11)]}
slash_powerlineLeft = {"decorations": [PowerLineDecoration(path="back_slash", size=11)]}
######## Applicaton Variables ###########
terminal = 'kitty'
app_launcher = 'zsh -c "rofi -show drun -disable-history -show-icons"'
# make cmd launcher respect alisas
cmd_launcher = 'rofi -run-list-command \". ~/.alias\" -run-command \"/usr/bin/zsh -i -c \'{cmd}\'\" -show run -disable-history'
win_launcher = 'zsh -c "rofi -show window -show-icons"'
calc_launcher = 'rofi -show calc -modi calc -no-show-match -no-sort'
clipcat_launcher = 'clipcat-menu'
browser = "firefox"
file_manager = "nemo"
screenshot = "flameshot full"
screenshot_gui = "flameshot gui"
lock = "betterlockscreen -l dimblur"

#########################################
############# key Bindings ##############
#########################################


def move_to_next_screen(qtile, direction=1):
    current_group = qtile.current_screen.group
    other_index = (qtile.screens.index(qtile.current_screen) + direction) % len(qtile.screens)
    other = qtile.screens[other_index].group
    qtile.current_window.togroup(other.name)
    # because of our hook we have to explicity switch back to old group
    current_group.toscreen()


keys = [
    ######### Switch between windows #########
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "period", lazy.next_screen(), desc="Move focus between monitors"),
    ######### Toggling Between Active Groups #########
    Key([mod], "Tab", lazy.screen.next_group(skip_empty=True), desc="Toggle next active group"),
    Key([alt], "Tab", lazy.screen.prev_group(skip_empty=True), desc="Toggle previous active group"),
    ######### Moving windows #########
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod], "comma", lazy.function(move_to_next_screen)),
    Key([mod, "shift"], "comma", lazy.function(move_to_next_screen, -1)),
    ######### Resizing windows #########
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    ######### Actions ##########
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    ######### Toggle Layout #########
    Key([alt], "Return", lazy.window.toggle_fullscreen(), desc="Toggle Full Screen"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle Floating layout"),
    Key([mod, "shift"], "o", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    ######### Rofi #########
    Key([mod], "space", lazy.spawn(app_launcher), desc="Launch Rofi drun"),
    Key([alt], "space", lazy.spawn(cmd_launcher), desc="Launch Rofi run"),
    Key([alt], "w", lazy.spawn(win_launcher), desc="Launch Rofi Windows"),
    Key([mod], "c", lazy.spawn(calc_launcher), desc="Launch Rofi Qalc"),
    ######### Clipcat #########
    Key([alt], "c", lazy.spawn(clipcat_launcher), desc="Launch Rofi clipcat"),
    ######### Power and Lockscreen #########
    Key([mod, "shift"], "e", lazy.spawn(os.path.expanduser("~/.config/qtile/scripts/power.sh")), desc="Rofi Power Menu"),
    Key([mod, "shift"], "x", lazy.spawn(lock), desc="Betterlockscreen"),
    ######### Application Shortcuts #########
    Key([mod], "w", lazy.spawn(browser), desc="Launch Browser"),
    Key([mod], "n", lazy.spawn(file_manager), desc="Launch File Manager"),
    ######### Screenshots #########
    Key([mod], "Print", lazy.spawn(screenshot), desc="Screenshot"),
    Key([], "Print", lazy.spawn(screenshot_gui), desc="Screenshot"),
    ######### Media keys #########
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master toggle"), desc="Mute"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next track"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous track"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Pause/Unpause"),
]

#########################################
############# Groups/Workspaces #########
#########################################


class PinnedGroup(Group):

    def __init__(self, *args, pinned_screen, **kwargs):
        self.pinned_screen = pinned_screen
        super().__init__(*args, screen_affinity=pinned_screen, **kwargs)


groups = [
    Group("1", label="󰈹", matches=[Match(wm_class="firefox")], layout="max"),
    Group("2", label="", matches=[Match(wm_class=re.compile("(Code)|(kitty)"))], layout="columns"),
    PinnedGroup("3", label="󰭹", matches=[Match(wm_class="discord")], layout="columns", pinned_screen=1),
    PinnedGroup("4", label="󰋙", matches=[Match(wm_class="Slippi Launcher")], layout="max", pinned_screen=0),
    PinnedGroup("5", label="󰓓", matches=[Match(wm_class=re.compile(r"steam.*|league.*"))], layout="columns", pinned_screen=0),
    Group("6", label="", matches=[Match(wm_class="obsidian")], layout="max"),
    Group("7", label="", matches=[Match(wm_class="nemo")], layout="columns"),
    PinnedGroup("8", label="󰚀", matches=[Match(wm_class=re.compile(r"qBittorrent|via.*"))], layout="columns", pinned_screen=0),
]


def go_to_group(g: Group):

    def callback(qtile):
        if len(qtile.screens) == 1 or (not fullscreen_mode and not g.screen_affinity):
            qtile.groups_map[g.name].toscreen()
            return

        if fullscreen_mode and g.name != 'fullscreen':
            qtile.focus_screen(1)
            qtile.groups_map[g.name].toscreen()
            return

        qtile.focus_screen(g.screen_affinity)
        qtile.groups_map[g.name].toscreen()

    return callback


for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.function(go_to_group(i)), desc="Switch to group {}".format(i.name)),
        # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False), desc="move focused window to group {}".format(i.name)),
    ])

dropdown_config = dict(
    on_focus_lost_hide=False,
    y=0.20,
    height=0.5,
)

groups.append(
    ScratchPad('scratchpad', [
        DropDown('terminal', terminal, **dropdown_config),
        DropDown('music', 'spotify', **dropdown_config),
        DropDown('mixer', 'pavucontrol', **dropdown_config),
        DropDown('pomodoro', 'pomatez', **dropdown_config),
        DropDown('system-monitor', 'gnome-system-monitor', **dropdown_config),
    ]))

keys.extend([
    ########## Scratch pads #########
    Key([mod], "Return", lazy.group["scratchpad"].dropdown_toggle('terminal'), desc="Launch scratchpad terminal"),
    Key([mod], "s", lazy.group["scratchpad"].dropdown_toggle('music'), desc="Launch scratchpad music player"),
    Key([mod], "v", lazy.group["scratchpad"].dropdown_toggle('mixer'), desc="Launch scratchpad pavucontrol"),
    Key([mod], "p", lazy.group["scratchpad"].dropdown_toggle('pomodoro'), desc="Launch scratchpad pomodoro clock"),
    Key(["control", "shift"], "escape", lazy.group["scratchpad"].dropdown_toggle('system-monitor'), desc="Launch scratchpad system monitor"),
])

# Fullscreen
groups.append(PinnedGroup('fullscreen', label='󰺵', layout='max', pinned_screen=0, persist=True))
keys.append(Key([mod], 'g', lazy.function(go_to_group(groups[-1]))))
keys.append(Key([mod, "shift"], 'g', lazy.function(enter_fullscreen)))
keys.append(Key([alt, "shift"], 'g', lazy.function(exit_fullscreen)))
#########################################
############# Window Layouts ###########
#########################################

layouts = [
    layout.Columns(num_columns=2, border_width=2, margin=4, wrap_focus_columns=False, wrap_focus_rows=False, border_focus=gruv_mat["grey"], border_normal=gruv_mat["dark"]),
    layout.Max(border_width=2, margin=6, border_focus=gruv_mat["grey"], border_normal=gruv_mat["dark"]),
]

########################################
######### FLOATING LAYOUT ##############
########################################
floating_layout = layout.Floating(
    border_width=2,
    border_focus=gruv_mat["grey"],
    border_normal=gruv_mat["dark"],
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="confirm"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="pavucontrol"),
        Match(wm_class="dialog"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="download"),
        Match(wm_class="steam", title=re.compile(r"^Steam.+$")),
        Match(wm_class="steam", title="Friends List"),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)

########################################
######### BAR AND WIDGETS ##############
########################################

########### MOUSE CALL BACKS ###########


def open_rofi():
    qtile.cmd_spawn(app_launcher)


######### DEFAULT WIDGET SETTINGS ######

widget_defaults = dict(font="FiraCode Nerd Font", fontsize=14, padding=3, foreground=gruv_mat["white"])
extension_defaults = widget_defaults.copy()

widgets = [
    #########################
    # Widget Configurations #
    #########################
    widget.Image(filename="~/.config/qtile/imgs/arch.png", mouse_callbacks={"Button1": open_rofi}, background=gruvbox["yellow"], margin=3),
    widget.Spacer(length=1, background=gruvbox["yellow"], **arrow_powerlineLeft),
    widget.GroupBox(font="FiraCode Nerd Font Mono",
                    fontsize=27,
                    padding_x=3,
                    padding_y=5,
                    rounded=False,
                    center_aligned=True,
                    disable_drag=True,
                    borderwidth=3,
                    highlight_method="line",
                    active=gruvbox["cream"],
                    inactive=gruvbox["blue-alt"],
                    highlight_color=gruvbox["dark-grey"],
                    this_current_screen_border=gruvbox["yellow"],
                    this_screen_border=gruv_mat["disabled"],
                    other_screen_border=gruv_mat["red"],
                    other_current_screen_border=gruv_mat["red"],
                    background=gruvbox["dark-grey"],
                    foreground=gruv_mat["disabled"],
                    use_mouse_wheel=False,
                    **arrow_powerlineLeft),
    widget.TaskList(margin=0,
                    padding=6,
                    icon_size=0,
                    fontsize=14,
                    borderwidth=1,
                    rounded=False,
                    highlight_method="block",
                    title_width_method="uniform",
                    urgent_alert_methond="border",
                    foreground=gruv_mat["black"],
                    background=gruvbox["cream"],
                    border=gruvbox["cream"],
                    urgent_border=gruv_mat["red-alt"],
                    txt_floating=" ",
                    txt_maximized=" ",
                    txt_minimized=" "),
    widget.Spacer(length=1, background=gruvbox["cream"], **rounded_powerlineRight),
    widget.CPU(padding=5, format="  {freq_current}GHz {load_percent}%", foreground=gruvbox["cream"], background=gruvbox["dark-grey"], **slash_powerlineRight),
    widget.ThermalSensor(padding=5,
                         update_interval=1,
                         format="󰔐 {temp:.0f}{unit}",
                         tag_sensor="Tctl",
                         foreground=gruvbox["cream"],
                         background=gruvbox["blue-alt"],
                         **slash_powerlineRight),
    widget.Memory(padding=5, format="󰈀 {MemUsed:.0f}{mm}", background=gruvbox["cream"], foreground=gruvbox["dark-grey"], **slash_powerlineRight),
    widget.Clock(padding=5, format="  %a %d %b %I:%M:%S", foreground=gruvbox["yellow"], background=gruvbox["dark-grey"], **slash_powerlineRight),
    widget.PulseVolume(fmt="󰕾 {}", foreground=gruvbox["dark"], background=gruvbox["yellow"], padding=10, **slash_powerlineRight),
    widget.Systray(padding=7, icon_size=15),
    widget.CurrentLayoutIcon(padding=5, scale=0.5),
]

widgets_2 = [
    #########################
    # Widget Configurations #
    #########################
    widget.Image(filename="~/.config/qtile/imgs/arch.png", mouse_callbacks={"Button1": open_rofi}, background=gruvbox["yellow"], margin=3),
    widget.Spacer(length=1, background=gruvbox["yellow"], **arrow_powerlineLeft),
    widget.GroupBox(font="FiraCode Nerd Font Mono",
                    fontsize=27,
                    padding_x=3,
                    padding_y=5,
                    rounded=False,
                    center_aligned=True,
                    disable_drag=True,
                    borderwidth=3,
                    highlight_method="line",
                    active=gruvbox["cream"],
                    inactive=gruvbox["blue-alt"],
                    highlight_color=gruvbox["dark-grey"],
                    this_current_screen_border=gruvbox["yellow"],
                    this_screen_border=gruv_mat["disabled"],
                    other_screen_border=gruv_mat["red"],
                    other_current_screen_border=gruv_mat["red"],
                    background=gruvbox["dark-grey"],
                    foreground=gruv_mat["disabled"],
                    use_mouse_wheel=False,
                    **arrow_powerlineLeft),
    widget.TaskList(margin=0,
                    padding=6,
                    icon_size=0,
                    fontsize=14,
                    borderwidth=1,
                    rounded=False,
                    highlight_method="block",
                    title_width_method="uniform",
                    urgent_alert_methond="border",
                    foreground=gruv_mat["black"],
                    background=gruvbox["cream"],
                    border=gruvbox["cream"],
                    urgent_border=gruv_mat["red-alt"],
                    txt_floating=" ",
                    txt_maximized=" ",
                    txt_minimized=" "),
    widget.Spacer(length=1, background=gruvbox["cream"], **rounded_powerlineRight),
    widget.CPU(padding=5, format="  {freq_current}GHz {load_percent}%", foreground=gruvbox["cream"], background=gruvbox["dark-grey"], **slash_powerlineRight),
    widget.ThermalSensor(padding=5,
                         update_interval=1,
                         format="󰔐 {temp:.0f}{unit}",
                         tag_sensor="Tctl",
                         foreground=gruvbox["cream"],
                         background=gruvbox["blue-alt"],
                         **slash_powerlineRight),
    widget.Memory(padding=5, format="󰈀 {MemUsed:.0f}{mm}", background=gruvbox["cream"], foreground=gruvbox["dark-grey"], **slash_powerlineRight),
    widget.Clock(padding=5, format="  %a %d %b %I:%M:%S", foreground=gruvbox["yellow"], background=gruvbox["dark-grey"], **slash_powerlineRight),
    widget.PulseVolume(fmt="󰕾 {}", foreground=gruvbox["dark"], background=gruvbox["yellow"], padding=10, **slash_powerlineRight),
    widget.Systray(padding=7, icon_size=15),
    widget.CurrentLayoutIcon(padding=5, scale=0.5),
]
size = 30

bar_configurations = dict(
    margin=[6, 10, 6, 10],
    border_width=[0, 0, 0, 0],
    background=gruv_mat["dark"],
)

screen_configurations = dict(
    wallpaper="~/Pictures/Wallpapers/dragon-ball-goku-gohan.png",
    wallpaper_mode="fill",
)

screens = [
    Screen(top=bar.Bar(widgets, size, **bar_configurations), **screen_configurations),
    Screen(top=bar.Bar(widgets_2, size, **bar_configurations), **screen_configurations),
]

#########################################
###### MOUSE SETTINGS / BINDINGS ########
#########################################
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
cursor_warp = True
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"
