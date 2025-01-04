# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, layout, widget
from libqtile.backend.wayland.inputs import Keyboard
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook
from libqtile.backend.wayland import InputConfig

mod = "mod4"
terminal = "kitty"

wl_input_rules = {
    "type:keyboard": InputConfig(
        kb_repeat_rate=50,
        kb_repeat_delay=300,
        kb_layout="fr",
    ),
    "type:touchpad": InputConfig(drag=True, tap=True, natural_scroll=True),
}

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/autostart.sh')
    subprocess.Popen([home])

lock_command = "sh -c ~/.config/qtile/lock"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 5+ unmute"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 5- unmute"), desc='volume down'),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle"), desc='Volume Mute'),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([mod], "l", lazy.spawn(lock_command), desc="Lock the computa"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show combi -combi-modi \"window,drun\" -modi combi -window-format \"{c} {t}\""), desc="Spawn a command using a prompt widget"),
]

#groups = [Group(i) for i in "123456789"]

groups = [
        Group('1', label=""),
        Group('2', spawn="kitty", label=""),
        Group('3', spawn="firefox", label="󰈹"),
        Group('4', spawn="discord", label="󰙯"),
        Group('5', spawn="ncmpcpp", label="󰌳")
]

# Key substitues for the french keyboard with "&é"'(-è_çà)='
fr_groups = {
    '1': 'ampersand',
    '2': 'eacute',
    '3': 'quotedbl',
    '4': 'apostrophe',
    '5': 'parenleft',
    '6': 'minus',
    '7': 'egrave',
    '8': 'underscore',
    '9': 'ccedilla',
    '0': 'agrave'
}

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                fr_groups[i.name],
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                fr_groups[i.name],
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


#for i in groups:
#    keys.extend([
#        # mod1 + letter of group = switch to group
#        Key([mod], i.name, lazy.group[i.name].toscreen()),
#
#       # mod1 + shift + letter of group = switch to & move focused window to group
#        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
#    ])

colors = [
    ["#2e3440", "#2e3440"],  # 0 background
    ["#d8dee9", "#d8dee9"],  # 1 foreground
    ["#3b4252", "#3b4252"],  # 2 background lighter
    ["#bf616a", "#bf616a"],  # 3 red
    ["#a3be8c", "#a3be8c"],  # 4 green
    ["#ebcb8b", "#ebcb8b"],  # 5 yellow
    ["#81a1c1", "#81a1c1"],  # 6 blue
    ["#b48ead", "#b48ead"],  # 7 magenta
    ["#88c0d0", "#88c0d0"],  # 8 cyan
    ["#e5e9f0", "#e5e9f0"],  # 9 white
    ["#4c566a", "#4c566a"],  # 10 grey
    ["#d08770", "#d08770"],  # 11 orange
    ["#8fbcbb", "#8fbcbb"],  # 12 super cyan
    ["#5e81ac", "#5e81ac"],  # 13 super blue
    ["#242831", "#242831"],  # 14 super dark background
]

layout_theme = {
    "border_width": 3,
    "margin": 4,
    "border_focus": "3b4252",
    "border_normal": "3b4252",
    "font": "JetBrainsMono Nerd Font",
    "grow_amount": 2,
}

group_box_settings = {
    "padding": 7,
    "fontsize": 18,
    "borderwidth": 4,
    "active": colors[9],
    "inactive": colors[10],
    "disable_drag": True,
    "rounded": True,
    "highlight_color": colors[2],
    "block_highlight_text_color": colors[6],
    "highlight_method": "block",
    "this_current_screen_border": colors[14],
    "this_screen_border": colors[7],
    "other_current_screen_border": colors[14],
    "other_screen_border": colors[14],
    "foreground": colors[1],
    "background": colors[14],
    "urgent_border": colors[3],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    layout.RatioTile(**layout_theme),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    text="󰣇",
                    foreground=colors[13],
                    background=colors[0],
                    font="JetBrainsMono Nerd Font",
                    fontsize=28,
                    padding=20,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.GroupBox(
                    font="JetBrainsMono Nerd Font",
                    **group_box_settings,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.TextBox(
                    text=" ",
                    foreground=colors[12],
                    background=colors[14],
                    # fontsize=38,
                    font="Font Awesome 6 Free Solid",
                ),
                widget.WindowName(
                    background=colors[14],
                    foreground=colors[12],
                    width=bar.CALCULATED,
                    empty_group_string="Desktop",
                    max_chars=130,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.Spacer(),
                widget.Systray(
                    icon_size=26,
                    background=colors[0],
                    padding=7,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.TextBox(
                    text="󱚻 ",
                    font="Font Awesome 6 Free Solid",
                    foreground=colors[3],  # fontsize=38
                    background=colors[14],
                ),
                widget.Wlan(
                    foreground=colors[3],  # fontsize=3
                    background=colors[14],
                    font="JetBrainsMono Nerd Font",
                    format='{essid} {percent:2.0%}',
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    foreground=colors[5],  # fontsize=38
                    background=colors[14],
                ),
                widget.Clock(
                    format="%a, %b %d",
                    background=colors[14],
                    foreground=colors[5],
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    foreground=colors[4],  # fontsize=38
                    background=colors[14],
                ),
                widget.Clock(
                    format="%I:%M %p",
                    foreground=colors[4],
                    background=colors[14],
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
                widget.Battery(
                    charge_char=' ',
                    discharge_char=' ',
                    update_interval=10,
                    foreground=colors[7],
                    background=colors[14],
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=28,
                    padding=0,
                ),
            ],
            35,
            background=colors[0],
            margin=[0, 0, 10, 0],
            border_width=[0, 0, 3, 0],
            border_color="#3b4252",
        ),
        bottom=bar.Gap(5),
        left=bar.Gap(5),
        right=bar.Gap(5),
        wallpaper="~/Pictures/wallpaper.png",
        wallpaper_mode="fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
#
wl_input_rules = {
       "type:keyboard": InputConfig(kb_layout="fr"),
}

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
