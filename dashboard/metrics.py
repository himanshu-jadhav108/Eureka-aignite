"""
Metric card generation module
"""


def create_metric_card(label, value, delta=None, icon="📊"):
    """
    Create a styled metric card with optional delta indicator
    
    Args:
        label: Metric label/name
        value: Metric value (formatted)
        delta: Optional percentage change
        icon: Emoji icon
        
    Returns:
        HTML string for metric card
    """
    delta_html = ""
    if delta:
        delta_color = "#10b981" if delta > 0 else "#ef4444"
        delta_symbol = "▲" if delta > 0 else "▼"
        delta_html = f'<div class="metric-delta" style="color: {delta_color};">{delta_symbol} {abs(delta):.1f}%</div>'
    
    return f"""
    <div class="metric-card slide-in">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
