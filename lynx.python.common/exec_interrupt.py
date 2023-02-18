class MapExit(Exception):
    """
    Is raised when `exec` execution should be stopped.
    For example, when player enters next `Scene`
    """
