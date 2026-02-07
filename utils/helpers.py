"""
Helper utility functions
"""


def format_number(num, decimals=0):
    """Format number with thousand separators"""
    if decimals == 0:
        return f"{int(num):,}"
    else:
        return f"{num:,.{decimals}f}"


def calculate_percentage_change(current, previous):
    """Calculate percentage change between two values"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100


def get_trend_indicator(value):
    """Get emoji indicator for trend direction"""
    if value > 15:
        return "📈"
    elif value < -15:
        return "📉"
    else:
        return "➡️"


def get_badge_class(value, thresholds):
    """
    Get CSS badge class based on value and thresholds
    
    Args:
        value: The value to evaluate
        thresholds: Dict with 'danger', 'warning', 'success' keys
    """
    if value <= thresholds.get('danger', float('-inf')):
        return 'badge-danger'
    elif value <= thresholds.get('warning', float('-inf')):
        return 'badge-warning'
    else:
        return 'badge-success'
