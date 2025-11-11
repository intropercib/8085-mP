"""
Table module for 8085 Microprocessor Simulator
Provides a flexible Table class for displaying data in horizontal or vertical layouts
"""

from rich.table import Table as RichTable
from rich.console import Console
from typing import List, Dict, Any, Optional, Union
import yaml
from pathlib import Path


class Table:
    """
    A flexible table class for displaying data in the 8085 simulator.
    Supports both horizontal and vertical orientations with configurable styling.
    """
    
    def __init__(
        self,
        data: Optional[Union[List[List[Any]], List[Dict[str, Any]]]] = None,
        headers: Optional[List[str]] = None,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        orientation: str = "horizontal",
        color_scheme: str = "default",
        config_path: Optional[str] = None
    ):
        """
        Initialize the Table object.
        
        Args:
            data: The data to display. Can be:
                  - List of lists: [[row1_col1, row1_col2], [row2_col1, row2_col2], ...]
                  - List of dicts: [{"col1": val1, "col2": val2}, ...]
            headers: Column headers/names
            title: Table title
            caption: Table caption (displayed below table)
            orientation: "horizontal" or "vertical"
            color_scheme: Name of color scheme from config (e.g., "registers", "memory", "flags")
            config_path: Path to configuration file (defaults to conf.yml in same directory)
        """
        self.data = data or []
        self.headers = headers or []
        self.title = title
        self.caption = caption
        self.orientation = orientation.lower()
        self.color_scheme = color_scheme
        
        # Load configuration
        if config_path is None:
            config_path = Path(__file__).parent / "conf.yml"
        self.config = self._load_config(config_path)
        
        # Initialize console
        console_config = self.config.get("console", {})
        self.console = Console(
            width=console_config.get("width"),
            force_terminal=console_config.get("force_terminal", True),
            force_jupyter=console_config.get("force_jupyter", False),
            force_interactive=console_config.get("force_interactive", True)
        )
        
        # Build the table
        self.table = self._build_table()
    
    def _load_config(self, config_path: Union[str, Path]) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            return {}
    
    def _get_color_scheme_config(self) -> Dict:
        """Get the color scheme configuration."""
        schemes = self.config.get("table", {}).get("color_schemes", {})
        return schemes.get(self.color_scheme, schemes.get("default", {}))
    
    def _get_table_config(self) -> Dict:
        """Get the default table configuration."""
        return self.config.get("table", {}).get("default", {})
    
    def _get_styles_config(self) -> Dict:
        """Get the styles configuration."""
        return self.config.get("table", {}).get("styles", {})
    
    def _build_table(self) -> RichTable:
        """Build the Rich Table object based on configuration and data."""
        table_config = self._get_table_config()
        styles_config = self._get_styles_config()
        scheme_config = self._get_color_scheme_config()
        
        # Apply title styling
        styled_title = None
        if self.title:
            title_style = scheme_config.get("title", styles_config.get("title", {}).get("style", "bold"))
            styled_title = f"[{title_style}]{self.title}[/{title_style}]"
        
        # Apply caption styling
        styled_caption = None
        if self.caption:
            caption_style = styles_config.get("caption", {}).get("style", "italic")
            styled_caption = f"[{caption_style}]{self.caption}[/{caption_style}]"
        
        # Create Rich Table
        table = RichTable(
            title=styled_title,
            caption=styled_caption,
            show_header=table_config.get("show_header", True),
            show_lines=table_config.get("show_lines", False),
            show_edge=table_config.get("show_edge", True),
            show_footer=table_config.get("show_footer", False),
            padding=tuple(table_config.get("padding", [0, 1])),
            expand=table_config.get("expand", False),
            header_style=scheme_config.get("header", styles_config.get("header", {}).get("style", "bold")),
            border_style=styles_config.get("border", {}).get("style", "")
        )
        
        if self.orientation == "horizontal":
            self._build_horizontal_table(table, scheme_config, styles_config)
        elif self.orientation == "vertical":
            self._build_vertical_table(table, scheme_config, styles_config)
        else:
            raise ValueError(f"Invalid orientation: {self.orientation}. Use 'horizontal' or 'vertical'.")
        
        return table
    
    def _build_horizontal_table(self, table: RichTable, scheme_config: Dict, styles_config: Dict):
        column_config = styles_config.get("column", {})
        column_colors = scheme_config.get("columns", [column_config.get("default_style", "white")])
        
        # Extract headers if data is list of dicts
        if self.data and isinstance(self.data[0], dict) and not self.headers:
            self.headers = list(self.data[0].keys())
        
        # Add columns
        for i, header in enumerate(self.headers):
            color = column_colors[i % len(column_colors)]
            table.add_column(
                header,
                style=color,
                justify=column_config.get("justify", "left"),
                no_wrap=column_config.get("no_wrap", False),
                overflow=column_config.get("overflow", "fold")
            )
        
        # Add rows
        for row in self.data:
            if isinstance(row, dict):
                # Convert dict to list based on header order
                row_data = [str(row.get(header, "")) for header in self.headers]
            else:
                row_data = [str(cell) for cell in row]
            table.add_row(*row_data)
    
    def _build_vertical_table(self, table: RichTable, scheme_config: Dict, styles_config: Dict):
        """
        Build a vertical table (rows become columns).
        In vertical mode, each row from the data becomes a column in the display.
        """
        column_config = styles_config.get("column", {})
        column_colors = scheme_config.get("columns", [column_config.get("default_style", "white")])
        
        if not self.data:
            return
        
        # Extract headers if data is list of dicts
        if isinstance(self.data[0], dict) and not self.headers:
            self.headers = list(self.data[0].keys())
        
        # In vertical mode, headers become the first column
        # Add "Property" column (or similar) for the headers
        table.add_column(
            "Property",
            style=column_colors[0],
            justify="left",
            no_wrap=False
        )
        
        # Add a column for each data row
        num_data_rows = len(self.data)
        for i in range(num_data_rows):
            col_name = f"Value {i+1}" if num_data_rows > 1 else "Value"
            color = column_colors[(i + 1) % len(column_colors)]
            table.add_column(
                col_name,
                style=color,
                justify=column_config.get("justify", "left"),
                no_wrap=column_config.get("no_wrap", False)
            )
        
        # Add rows (each header becomes a row)
        for i, header in enumerate(self.headers):
            row_data = [header]
            for data_row in self.data:
                if isinstance(data_row, dict):
                    row_data.append(str(data_row.get(header, "")))
                else:
                    row_data.append(str(data_row[i] if i < len(data_row) else ""))
            table.add_row(*row_data)
    
    def render(self):
        self.console.print(self.table)
    
    def add_data(self, data: Union[List[List[Any]], List[Dict[str, Any]]]):
        """
        Add or update data and rebuild the table.
        
        Args:
            data: New data to display
        """
        self.data = data
        self.table = self._build_table()
    
    def set_headers(self, headers: List[str]):
        """
        Set or update headers and rebuild the table.
        
        Args:
            headers: New column headers
        """
        self.headers = headers
        self.table = self._build_table()
    
    def set_orientation(self, orientation: str):
        """
        Change table orientation and rebuild.
        
        Args:
            orientation: "horizontal" or "vertical"
        """
        self.orientation = orientation.lower()
        self.table = self._build_table()
    
    def set_color_scheme(self, color_scheme: str):
        """
        Change color scheme and rebuild the table.
        
        Args:
            color_scheme: Name of color scheme from config
        """
        self.color_scheme = color_scheme
        self.table = self._build_table()
    
    def get_table(self) -> RichTable:
        """
        Get the underlying Rich Table object for advanced customization.
        
        Returns:
            The Rich Table object
        """
        return self.table
    
    @classmethod
    def from_dict_list(
        cls,
        data: List[Dict[str, Any]],
        title: Optional[str] = None,
        caption: Optional[str] = None,
        orientation: str = "horizontal",
        color_scheme: str = "default"
    ) -> "Table":
        """
        Convenience method to create a table from a list of dictionaries.
        Headers are automatically extracted from dict keys.
        
        Args:
            data: List of dictionaries
            title: Table title
            caption: Table caption
            orientation: "horizontal" or "vertical"
            color_scheme: Name of color scheme from config
            
        Returns:
            Table instance
        """
        return cls(
            data=data,
            headers=None,  # Will be auto-extracted
            title=title,
            caption=caption,
            orientation=orientation,
            color_scheme=color_scheme
        )
    
    @classmethod
    def from_2d_list(
        cls,
        data: List[List[Any]],
        headers: List[str],
        title: Optional[str] = None,
        caption: Optional[str] = None,
        orientation: str = "horizontal",
        color_scheme: str = "default"
    ) -> "Table":
        """
        Convenience method to create a table from a 2D list.
        
        Args:
            data: 2D list of data
            headers: Column headers
            title: Table title
            caption: Table caption
            orientation: "horizontal" or "vertical"
            color_scheme: Name of color scheme from config
            
        Returns:
            Table instance
        """
        return cls(
            data=data,
            headers=headers,
            title=title,
            caption=caption,
            orientation=orientation,
            color_scheme=color_scheme
        )


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Horizontal table with list of lists
    print("\n=== Example 1: Registers (Horizontal) ===")
    registers_data = [
        ["A", "FFh", "255", "11111111b"],
        ["B", "00h", "0", "00000000b"],
        ["C", "5Ah", "90", "01011010b"],
        ["D", "12h", "18", "00010010b"],
    ]
    headers = ["Register", "Hex", "Decimal", "Binary"]
    
    table1 = Table(
        data=registers_data,
        headers=headers,
        title="8085 CPU Registers",
        orientation="horizontal",
        color_scheme="registers"
    )
    table1.render()
    
    # Example 2: Vertical table with same data
    print("\n=== Example 2: Registers (Vertical) ===")
    table2 = Table(
        data=registers_data,
        headers=headers,
        title="8085 CPU Registers - Vertical View",
        orientation="vertical",
        color_scheme="registers"
    )
    table2.render()
    
    # Example 3: Table from list of dictionaries
    print("\n=== Example 3: Flags (Horizontal) ===")
    flags_data = [
        {"Flag": "S (Sign)", "Status": "1", "Description": "Negative"},
        {"Flag": "Z (Zero)", "Status": "0", "Description": "Not Zero"},
        {"Flag": "AC (Aux Carry)", "Status": "1", "Description": "Set"},
        {"Flag": "P (Parity)", "Status": "0", "Description": "Odd"},
        {"Flag": "CY (Carry)", "Status": "1", "Description": "Set"},
    ]
    
    table3 = Table.from_dict_list(
        data=flags_data,
        title="8085 Flag Register",
        orientation="horizontal",
        color_scheme="flags"
    )
    table3.render()
    
    # Example 4: Memory view
    print("\n=== Example 4: Memory (Horizontal) ===")
    memory_data = [
        ["2000h", "3E"],
        ["2001h", "0A"],
        ["2002h", "06"],
        ["2003h", "05"],
    ]
    
    table4 = Table.from_2d_list(
        data=memory_data,
        headers=["Address", "Data"],
        title="Memory Contents",
        orientation="horizontal",
        color_scheme="memory",
        caption="Program Memory"
    )
    table4.render()
