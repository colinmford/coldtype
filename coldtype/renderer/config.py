from enum import Enum
from runpy import run_path
import argparse

def true_false_or_none(x):
    if x in ["0", "false", "False", "n", "no", "N"]:
        return False
    elif x in ["1", "true", "True", "y", "yes", "Y"]:
        return True
    else:
        return None


class ConfigOption(Enum):
    WindowPassthrough = ("window_passthrough", None, "wpass",
        true_false_or_none)
    WindowTransparent = ("window_transparent", None, "wt",
        true_false_or_none)
    WindowBackground = ("window_background", None, "wb",
        true_false_or_none)
    WindowFloat = ("window_float", None, "wf",
        true_false_or_none)
    WindowOpacity = ("window_opacity", 1, "wo",
        lambda x: float(x))
    WindowPin = ("window_pin", "NE", "wp")
    WindowPinInset = ("window_pin_inset", (0, 0), "wpi",
        lambda x: [int(n) for n in x.split(",")])
    WindowContentScale = ("window_content_scale", None, "wcs")
    MonitorName = ("monitor_name", None, "mn")
    EditorCommand = ("editor_command", None, "ec")
    ManyIncrement = ("many_increment", None, "minc")
    PreviewScale = ("preview_scale", 1, "ps",
        lambda x: float(x))
    FontDirs = ("font_dirs", [], "fd")
    Midi = ("midi", {}, None)
    Hotkeys = ("hotkeys", {}, None)
    ThreadCount = ("thread_count", 8, "tc")
    Multiplex = ("multiplex", None, "mp",
        true_false_or_none)
    DebounceTime = ("debounce_time", 0.25, "dt")
    RefreshDelay = ("refresh_delay", 0.025, "rd")
    InlineFiles = ("inline_files", [], "in",
        lambda x: x.split(","))
    BlenderWatch = ("blender_watch", None, "bw",
        true_false_or_none)

    @staticmethod
    def Help(e):
        if e == ConfigOption.WindowPassthrough:
            return "Should the window ignore all interaction?"
        elif e == ConfigOption.WindowTransparent:
            return "Should the window have no background?"
        elif e == ConfigOption.WindowBackground:
            return "Should the window open as a background process?"
        elif e == ConfigOption.WindowFloat:
            return "Should the window float above everything?"
        elif e == ConfigOption.WindowOpacity:
            return "A value for the transparency of the window"
        elif e == ConfigOption.WindowPin:
            return "Where should the window show up? Provide a compass direction N/S/E/W/NE/SE/SW/NW/C"
        elif e == ConfigOption.WindowPinInset:
            return "Experimental; offset window pin from edge"
        elif e == ConfigOption.WindowContentScale:
            return "Experimental; override auto-calculated window scale"
        elif e == ConfigOption.MonitorName:
            return "The name of the monitor to open the window in; pass 'list' to list all monitor names"
        elif e == ConfigOption.EditorCommand:
            return "If your text editor provides a command-line invocation, set it here for automated opening"
        elif e == ConfigOption.ManyIncrement:
            return "How many frames should the renderer jump forward when you hit cmd+arrow to move prev/next?"
        elif e == ConfigOption.PreviewScale:
            return "What preview scale should the window open at?"
        elif e == ConfigOption.FontDirs:
            return "What additional directories would you like to search for fonts?"
        elif e == ConfigOption.ThreadCount:
            return "How many threads when multiplexing?"
        elif e == ConfigOption.Multiplex:
            return "Should the renderer run multiple processes (determined by --thread-count)?"
        elif e == ConfigOption.DebounceTime:
            return "How long should the rendering loop wait before acting on a debounced action?"
        elif e == ConfigOption.RefreshDelay:
            return "How long should the renderer delay between rendering frames?"
        elif e == ConfigOption.BlenderWatch:
            return "Enable experimental blender live-coding integration?"

    @staticmethod
    def AddCommandLineArgs(pargs:dict,
        parser:argparse.ArgumentParser
        ):
        for co in ConfigOption:
            if co.value[2]:
                short = co.value[2]
                arg = co.value[0].replace("_", "-")
                type_spec = dict(default=None)
                #if co.value[1] is False:
                #    type_spec = dict(action="store_true", default=False)
                pargs[co.value[0]] = parser.add_argument(f"-{short}", f"--{arg}", help=ConfigOption.Help(co), **type_spec)


class ColdtypeConfig():
    def __init__(self,
        config,
        prev_config:"ColdtypeConfig"=None,
        args=None
        ):
        self.profile = None
        if args and hasattr(args, "profile") and args.profile:
            self.profile = args.profile
        
        for co in ConfigOption:
            if len(co.value) > 3:
                prop, default_value, _, cli_mod = co.value
            else:
                prop, default_value, _ = co.value
                cli_mod = lambda x: x
            
            setattr(self,
                prop,
                config.get(prop.upper(),
                    getattr(prev_config, prop) if prev_config else default_value))
            
            if self.profile and "PROFILES" in config and self.profile in config["PROFILES"]:
                v = config["PROFILES"][self.profile].get(prop.upper())
                if v:
                    #print("PROFILE", self.profile, prop, v)
                    setattr(self, prop, v)
            
            if args and hasattr(args, prop):
                value = getattr(args, prop)
                if value is not None:
                    #print("CLI", prop, value)
                    setattr(self, prop, cli_mod(value))
        
        #self.midi = config.get("MIDI")
        #self.hotkeys = config.get("HOTKEYS")
    
    def values(self):
        out = "<ColdtypeConfig:"
        if self.profile:
            out += f"({self.profile})"
        for co in ConfigOption:
            out += f"\n   {co.name}:{getattr(self, co.value[0])}"
        out += "/>"
        return out