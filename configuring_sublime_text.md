# Configuring Sublime Text 3 as a Python IDE

Personal settings for configuring Sublime Text 3 as a Python IDE.

1. Download [Sublime Text 3](https://www.sublimetext.com/3)

1. Install additional packages. 

  **Tools** -> **Command Palette...** -> type `Package Control: Install Package`. Click on the Package Control: Install Package.

  Install **Anaconda**.

  Install **SublimeREPL**

1. Configure user settings.

  **Preferences ** -> **Settings**

  Copy the following into *Preferences.sublime-settings - User*:
  ```{
	"auto_complete_commit_on_tab": true,
	"color_scheme": "Packages/Color Scheme - Default/IDLE.tmTheme",
	"font_size": 11,
	"ignored_packages":
	[
		"Vintage"
	]
}```

1. Configure Anaconda package settings.

   **Preferences** -> **Package Settings** -> **Anaconda**

