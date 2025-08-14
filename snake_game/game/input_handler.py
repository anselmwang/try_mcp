"""
Cross-platform input handling for Snake Game
"""

import os
import sys
from typing import Optional

# Platform-specific imports
if os.name == "nt":
    try:
        import msvcrt
    except ImportError:
        msvcrt = None
else:
    try:
        import tty
        import termios
    except ImportError:
        tty = None
        termios = None


class InputHandler:
    """Handles cross-platform keyboard input"""

    def __init__(self):
        """Initialize input handler"""
        self.platform = os.name
        self._old_settings = None

    def __enter__(self):
        """Context manager entry"""
        if self.platform != "nt" and tty and termios:
            try:
                self._old_settings = termios.tcgetattr(sys.stdin.fileno())
                tty.cbreak(sys.stdin.fileno())
            except:
                pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.platform != "nt" and termios and self._old_settings:
            try:
                termios.tcsetattr(
                    sys.stdin.fileno(), termios.TCSADRAIN, self._old_settings
                )
            except:
                pass

    def get_key(self) -> Optional[str]:
        """
        Get a single key press without blocking
        Returns None if no key is pressed
        """
        if self.platform == "nt":
            # Windows
            return self._get_key_windows()
        else:
            # Unix/Linux/Mac
            return self._get_key_unix()

    def _get_key_windows(self) -> Optional[str]:
        """Get key press on Windows"""
        if msvcrt and msvcrt.kbhit():
            try:
                key = msvcrt.getch()
                if isinstance(key, bytes):
                    key = key.decode("utf-8", errors="ignore")

                # Handle special keys
                if key == "\x00" or key == "\xe0":  # Special key prefix
                    key2 = msvcrt.getch()
                    if isinstance(key2, bytes):
                        key2 = key2.decode("utf-8", errors="ignore")

                    # Arrow keys
                    if key2 == "H":  # Up arrow
                        return "w"
                    elif key2 == "P":  # Down arrow
                        return "s"
                    elif key2 == "K":  # Left arrow
                        return "a"
                    elif key2 == "M":  # Right arrow
                        return "d"

                return key.lower()
            except:
                return None
        return None

    def _get_key_unix(self) -> Optional[str]:
        """Get key press on Unix/Linux/Mac"""
        try:
            import select

            # Check if input is available
            if select.select([sys.stdin], [], [], 0.0)[0]:
                key = sys.stdin.read(1)

                # Handle escape sequences (arrow keys)
                if key == "\x1b":  # ESC
                    # Try to read the rest of the escape sequence
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        seq = sys.stdin.read(2)
                        if seq == "[A":  # Up arrow
                            return "w"
                        elif seq == "[B":  # Down arrow
                            return "s"
                        elif seq == "[D":  # Left arrow
                            return "a"
                        elif seq == "[C":  # Right arrow
                            return "d"

                return key.lower()
        except:
            return None

        return None

    def wait_for_key(self) -> str:
        """
        Wait for a key press and return it
        Blocking version of get_key()
        """
        if self.platform == "nt":
            return self._wait_for_key_windows()
        else:
            return self._wait_for_key_unix()

    def _wait_for_key_windows(self) -> str:
        """Wait for key press on Windows"""
        if msvcrt:
            try:
                key = msvcrt.getch()
                if isinstance(key, bytes):
                    key = key.decode("utf-8", errors="ignore")

                # Handle special keys
                if key == "\x00" or key == "\xe0":
                    key2 = msvcrt.getch()
                    if isinstance(key2, bytes):
                        key2 = key2.decode("utf-8", errors="ignore")

                    # Arrow keys
                    if key2 == "H":  # Up arrow
                        return "w"
                    elif key2 == "P":  # Down arrow
                        return "s"
                    elif key2 == "K":  # Left arrow
                        return "a"
                    elif key2 == "M":  # Right arrow
                        return "d"

                return key.lower()
            except:
                return input("Press Enter to continue: ").lower()
        else:
            return input("Enter command (w/a/s/d/q/p): ").lower()

    def _wait_for_key_unix(self) -> str:
        """Wait for key press on Unix/Linux/Mac"""
        if tty and termios:
            try:
                key = sys.stdin.read(1)

                # Handle escape sequences
                if key == "\x1b":
                    try:
                        seq = sys.stdin.read(2)
                        if seq == "[A":  # Up arrow
                            return "w"
                        elif seq == "[B":  # Down arrow
                            return "s"
                        elif seq == "[D":  # Left arrow
                            return "a"
                        elif seq == "[C":  # Right arrow
                            return "d"
                    except:
                        pass

                return key.lower()
            except:
                return input("Enter command (w/a/s/d/q/p): ").lower()
        else:
            return input("Enter command (w/a/s/d/q/p): ").lower()

    def flush_input(self):
        """Flush any pending input"""
        if self.platform == "nt" and msvcrt:
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            try:
                import select

                while select.select([sys.stdin], [], [], 0.0)[0]:
                    sys.stdin.read(1)
            except:
                pass
