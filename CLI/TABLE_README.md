# Table Class Documentation

## Overview
The `Table` class provides a flexible, configurable way to display tabular data in your 8085 Microprocessor Simulator using the Rich library. It supports both horizontal and vertical table orientations with customizable color schemes defined in `conf.yml`.

## Features
- ✅ Insert all data at once (list of lists or list of dictionaries)
- ✅ Horizontal and vertical table orientations
- ✅ Configurable color schemes via `conf.yml`
- ✅ Support for titles and captions
- ✅ Dynamic updates (change data, headers, orientation on the fly)
- ✅ Pre-configured color schemes for common 8085 displays (registers, memory, flags, instructions)

---

## Quick Start

### Basic Usage - Horizontal Table

```python
from table import Table

# Method 1: Using list of lists
data = [
    ["A", "FFh", "255"],
    ["B", "00h", "0"],
    ["C", "5Ah", "90"]
]
headers = ["Register", "Hex", "Decimal"]

table = Table(
    data=data,
    headers=headers,
    title="8085 Registers",
    orientation="horizontal",
    color_scheme="registers"
)
table.render()

# Method 2: Using list of dictionaries
data = [
    {"Register": "A", "Hex": "FFh", "Decimal": "255"},
    {"Register": "B", "Hex": "00h", "Decimal": "0"}
]

table = Table.from_dict_list(
    data=data,
    title="8085 Registers",
    color_scheme="registers"
)
table.render()
```

### Vertical Table

```python
# Same data, different orientation
table = Table(
    data=data,
    headers=headers,
    title="8085 Registers",
    orientation="vertical",  # ← Key difference
    color_scheme="registers"
)
table.render()
```

---

## Class Methods

### Constructor: `Table()`

```python
Table(
    data=None,                    # List[List] or List[Dict]
    headers=None,                 # List[str]
    title=None,                   # str
    caption=None,                 # str
    orientation="horizontal",     # "horizontal" or "vertical"
    color_scheme="default",       # str (from conf.yml)
    config_path=None             # str (path to conf.yml)
)
```

### Class Methods

```python
# Create from list of dictionaries (headers auto-extracted)
Table.from_dict_list(data, title=None, caption=None, orientation="horizontal", color_scheme="default")

# Create from 2D list with explicit headers
Table.from_2d_list(data, headers, title=None, caption=None, orientation="horizontal", color_scheme="default")
```

### Instance Methods

```python
table.render()                      # Display the table
table.add_data(new_data)           # Update data and rebuild
table.set_headers(new_headers)     # Update headers and rebuild
table.set_orientation("vertical")  # Change orientation
table.set_color_scheme("memory")   # Change color scheme
table.get_table()                  # Get underlying Rich Table object
```

---

## Color Schemes (conf.yml)

Pre-configured color schemes:

- **`registers`** - Cyan, green, yellow, blue columns with magenta headers
- **`memory`** - Bright white and bright green columns with yellow headers
- **`flags`** - Bright cyan and bright magenta columns with red headers
- **`instructions`** - Cyan, yellow, green columns with green headers
- **`default`** - Simple white theme

### Using Color Schemes

```python
# For register displays
table = Table(data=reg_data, headers=headers, color_scheme="registers")

# For memory contents
table = Table(data=mem_data, headers=headers, color_scheme="memory")

# For flag status
table = Table(data=flag_data, headers=headers, color_scheme="flags")

# For instruction set
table = Table(data=inst_data, headers=headers, color_scheme="instructions")
```

---

## Configuration File (conf.yml)

You can customize all styling in `conf.yml`:

```yaml
table:
  color_schemes:
    my_custom_scheme:
      header: "bold cyan"
      title: "bold magenta"
      columns:
        - "red"
        - "green"
        - "blue"
```

Then use it:
```python
table = Table(data=data, headers=headers, color_scheme="my_custom_scheme")
```

---

## Examples

### Example 1: Register Display

```python
registers = [
    ["A", "FFh", "255", "11111111b"],
    ["B", "00h", "0", "00000000b"],
    ["PC", "2005h", "8197", "0010000000000101b"]
]

table = Table(
    data=registers,
    headers=["Register", "Hex", "Decimal", "Binary"],
    title="8085 CPU Registers",
    color_scheme="registers"
)
table.render()
```

### Example 2: Memory Contents

```python
memory = [
    {"Address": "2000h", "Data": "3E", "Instruction": "MVI A, 0Ah"},
    {"Address": "2001h", "Data": "0A", "Instruction": "Data"},
    {"Address": "2002h", "Data": "76", "Instruction": "HLT"}
]

table = Table.from_dict_list(
    data=memory,
    title="Program Memory",
    caption="Sample Program",
    color_scheme="memory"
)
table.render()
```

### Example 3: Dynamic Updates

```python
# Create table with initial data
table = Table(
    data=[["A", "00h"]],
    headers=["Register", "Value"],
    title="Registers"
)
table.render()

# Update with new data
table.add_data([
    ["A", "FFh"],
    ["B", "5Ah"],
    ["C", "12h"]
])
table.render()

# Switch to vertical
table.set_orientation("vertical")
table.render()
```

### Example 4: Vertical Register Comparison

```python
# Compare two register states side-by-side
comparison = [
    ["A", "FFh", "255"],  # Before
    ["A", "5Ah", "90"]    # After
]

table = Table(
    data=comparison,
    headers=["Register", "Hex", "Decimal"],
    title="Register Before/After",
    orientation="vertical",
    color_scheme="registers"
)
table.render()
```

---

## Tips

1. **Horizontal vs Vertical**:
   - Use **horizontal** for traditional row-based data (most common)
   - Use **vertical** to compare multiple entries side-by-side

2. **Data Formats**:
   - Use **list of dicts** when you want automatic header extraction
   - Use **list of lists** when you want full control over headers

3. **Color Schemes**:
   - Stick to pre-defined schemes for consistency
   - Create custom schemes in `conf.yml` for special displays

4. **Performance**:
   - The table rebuilds on every update (add_data, set_orientation, etc.)
   - For frequent updates, batch your changes

---

## Integration with Main Program

```python
# In your main.py
from table import Table

def display_cpu_state(cpu):
    """Display current CPU state"""
    registers = [
        ["A", f"{cpu.A:02X}h", str(cpu.A)],
        ["B", f"{cpu.B:02X}h", str(cpu.B)],
        ["C", f"{cpu.C:02X}h", str(cpu.C)],
        # ... more registers
    ]
    
    table = Table(
        data=registers,
        headers=["Register", "Hex", "Decimal"],
        title="Current CPU State",
        color_scheme="registers"
    )
    table.render()

def display_memory_range(memory, start, end):
    """Display memory contents"""
    mem_data = []
    for addr in range(start, end + 1):
        mem_data.append([
            f"{addr:04X}h",
            f"{memory[addr]:02X}h"
        ])
    
    table = Table(
        data=mem_data,
        headers=["Address", "Data"],
        title=f"Memory: {start:04X}h - {end:04X}h",
        color_scheme="memory"
    )
    table.render()
```

---

## API Reference

| Method | Description |
|--------|-------------|
| `__init__(...)` | Create a new table with data |
| `render()` | Display the table to console |
| `add_data(data)` | Update table data |
| `set_headers(headers)` | Update column headers |
| `set_orientation(orientation)` | Change to "horizontal" or "vertical" |
| `set_color_scheme(scheme)` | Apply a different color scheme |
| `get_table()` | Get underlying Rich Table for advanced use |
| `from_dict_list(...)` | Create from list of dictionaries |
| `from_2d_list(...)` | Create from 2D list with headers |

---

## Notes

- All colors and styles are configured in `conf.yml`
- The table automatically handles string conversion for all data types
- Headers are auto-extracted from dict keys if not provided
- Caption appears below the table (useful for additional context)
- Title appears above the table (bold and centered)
