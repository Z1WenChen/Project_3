import plotly.express as px

def line_chart(data, title, y_axis_title = None, x_axis_title = None, x_ticks = None, y_ticks = None, marker_status = False):
    
    fig = px.line(
            data,
            title = title,
            markers = marker_status
            )
    
    if x_ticks is not None:
        fig = px.line(
            data,
            title = title,
            x = x_ticks,
            markers = marker_status
            )
    
    if y_ticks is not None:
        fig = px.line(
            data,
            title = title,
            y = y_ticks,
            markers = marker_status
            )
    
    
    if x_axis_title is not None:
        fig.update_xaxes(
            title_text = x_axis_title,
            title_standoff = 25
            )
    
    if y_axis_title is not None:
        fig.update_yaxes(
            title_text = y_axis_title,
            title_standoff = 25
            )
    
    return fig