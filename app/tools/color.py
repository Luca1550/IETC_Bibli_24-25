class Color:
    """A class to manage color constants and utilities for the application."""
    @staticmethod
    def primary_color():
        return "#1F6AA5" 
    @staticmethod
    def secondary_color():
        return "#e05822"
    @staticmethod
    def error_color():
        return "#e02822"
    @staticmethod
    def background_color():
        return "#2b2b2b"
    @staticmethod
    def status_available_color():
        return "#28a745"
    @staticmethod
    def status_borrowed_color():
        return "#dc3545"
    @staticmethod
    def status_reserved_color():
        return "#ff9800"
    
    @staticmethod
    def hover_color(hex_color : str, percent : int):
        """        
        Adjusts the brightness of a given hex color by a specified percentage.
        arguments:
        - hex_color: The hex color code to adjust (e.g., "#ff0000").
        - percent: The percentage to adjust the brightness (positive for lighter, negative for darker).
        returns:
        - A new hex color code with the adjusted brightness.
        """
        hex_color = hex_color.lstrip("#") 
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) 

        factor = 1 + (percent / 100) if percent > 0 else 1 - (abs(percent) / 100)
        adjusted_rgb = tuple(max(0, min(255, int(c * factor))) for c in rgb)

        return f"#{adjusted_rgb[0]:02x}{adjusted_rgb[1]:02x}{adjusted_rgb[2]:02x}"
    
    @staticmethod
    def status_color(status : int):
        """Returns the color associated with a given status."""
        match status:
            case 1:
                return Color.status_available_color()
            case 2:
                return Color.status_borrowed_color()
            case 3:
                return Color.status_reserved_color()
            case _:
                return Color.primary_color()