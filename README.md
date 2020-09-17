## Scream
 *Scre*enshots *A*uto*m*ated allows you to grab pictures of windows automatically by stimulating key press from keyboard.
 There would be a turning point in your life, where you think instead of manually pressing doing a key press and taking screenshot, you could have had an app to do it. Yes, here it is ! Scream makes it simple for you.

![Scream](/data/screenshot-capture.png)

## Requirements
 1. GNU Linux only
  Yea it means your Arch, Debian, Fedora, Linux Mint, Ubuntu etc.
 2. Supports one and only X Window System
  Wayland... huh...
  The libraries used by Scream work only with X.
 3. Requires Python 3
  As latest as possible. But please, no Python 2.
 4. Essential libraries :
  Without the following libraries, Scream just screams.
  - [GTK](www.gtk.org)
  - [Wnck](https://developer.gnome.org/libwnck/stable/index.html)
  - [Atspi](https://developer.gnome.org/libatspi/stable/)
  - [PyGObject](https://pygobject.readthedocs.io/en/latest/)

 They are from GNOME world and there is a very good chance that your system already has them installed. If not please install it.

## Installation
 Really, I never thought of making an install script, just like that. If you can make one, please do it.
 But that doesn't mean, you can't use Scream. Nah nah. Clone this repository (_Download_ it). Then open the downloaded repository.
 Launch a terminal in the directory. Then type `./scream` and boom.

 Assuming you downloaded the repository in your `Downloads`, the steps will be like this in a terminal.
 ```
 $ # If you have git...
 $ git clone https://github.com/j-arun-mani/Scream.git
 $ cd Downloads/Scream
 $ ./scream
 ```

## Usage
 Using Scream is not difficult at all. Every _control_ (like button) has a tool tip, so you can know what it is.

 ### In Capture tab
  1. Select the window you want to capture from combo box.
  2. If the window is new or not found, try clicking the _refresh_ icon beside it.
  3. Describe the area you want to grab. This mean, tell the top-left corner and bottom-right corner.
  4. Please use the _coordinates picker_ beside the entries if you don't know position. Using a ruler or measurement tape is fine too.

 ### In Actions tab
  1. Click the _plus_ button to add a row.
  2. Click the _minus_ button to remove selected row.
  3. Every row has three values : _keyval_, _repeat_, _delay_.
  4. Keyval is the code of the keyboard button you want to press. If you don't know the code, click _Don't know keyval ?_ button to find out.
  5. Repeat describes how many times you want to repeat the action. Remember it repeats the action, not just key press.
  6. Delay is the number of seconds the app will wait before pressing a key.

 ### In Options tab
  1. Choose the directory where you want to save the grabbed pictures. Always use an empty directory to avoid surprises.
  2. Select an image format. Only five types are supported for now. Just use _jpeg_ or _png_ if you are not a Picaso.
  3. Tick the check button if you want the app to close itself after grabbing pictures.

 Then click on the _execute_ icon and the app will start it's process.

 ### Notes
  1. Though the app will raise the _to be_ grabbed window, make sure that the window is not shadowed by other windows. Maximize the window for better results.
  2. Just sit idle when app the is grabbing pictures. If you want, count from 1 to _infinity_. After completion, the app will either bring back it's window or close itself. Interfering with the app's process leads to undefined behaviors.
  3. If you want to save all the settings (_session_) for a future use, click on the _save_ icon. It is just a plain JSON format, so use any filename or type.
  4. To open a saved _session_ click on the _open_ icon and select the saved file.
  5. Repeating an action means, the delay will also be included.
     For example, if you add a row to repeat _Enter_ press 2 times with 4 seconds delays.
     It means, the app will wait for 4 seconds, then press _Enter_. Then, again will wait for 4 seconds, then press _Enter_.
     Also repeat should be minimum 1 for an action to work.
  6. Almost all excepted errors will be handled by the app and will be reported to you _normally_, but have an eye on the terminal screen too.
     Some uncaught errors will be shown there, so you can inform me (by opening an issue).

## Command Line Usage
 If you have a saved session file, then you can pass it as an command line argument of `-f`.
 ```
 $ ./scream -f my_session.json
 ```
 To immediately start the execution of actions, use `-q`. This is same like launching the app, opening a session and then starting grabbing pictures.
 ```
 $ ./scream -q -f my_session.json
 ```

## Help or Bugs or Feedback
 Please open an issue. I will be really happy to help you in everyway possible. The brave hearts can also help in cleaning the bugs !

## Thanks to GNOME and Python.
