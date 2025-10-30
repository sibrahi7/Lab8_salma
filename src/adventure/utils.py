from importlib import resources

def read_events_from_file(file_path: str) -> list[str]:
    """
    Reads adventure events from a text file, where each line is an event description.
    
    Args:
        file_path (str): The path to the text file containing the events.
    
    Returns:
        list[str]: A list of event strings, one per line (stripped of whitespace).
    """
    events = []
    try:
        with resources.files("adventure.data").joinpath("events.txt").open("r", encoding="utf-8") as file:
            # Read non-empty lines and strip whitespace/newlines
            events = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return events
