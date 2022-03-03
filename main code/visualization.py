import plotly.express as px

def line_chart(data, title, y_axis_title = None, x_axis_title = None, x_ticks = None, y_ticks = None, marker_status = False, height = None, width = None, legend_pos = None):
    
    fig = px.line(
            data,
            title = title,
            markers = marker_status
            )
    
    if height is not None or width is not None:
        fig = px.line(
            data,
            title = title,
            x = x_ticks,
            height = height,
            width = width
            
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
    
    if legend_pos is not None:
        fig.update_layout(
            legend=dict(
            yanchor=legend_pos[1],
            y=0.99,
            xanchor=legend_pos[0],
            x=0.01
            )
        )
    
    return fig


def scatter_chart(data, title, y_axis_title = None, x_axis_title = None, x_ticks = None, y_ticks = None, height = None, width = None, legend_pos = None):
    
    fig = px.scatter(
            data,
            title = title
            )
        
        
    if height is not None or width is not None:
        fig = px.scatter(
            data,
            title = title,
            x = x_ticks,
            height = height,
            width = width
            
            )
        
    
    if x_ticks is not None:
        fig = px.scatter(
            data,
            title = title,
            x = x_ticks
         
            )
    
    if y_ticks is not None:
        fig = px.scatter(
            data,
            title = title,
            y = y_ticks
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
        
    if legend_pos is not None:
        fig.update_layout(
            legend=dict(
            yanchor=legend_pos[1],
            y=0.01,
            xanchor=legend_pos[0],
            x=0.99
            )
        )
    
    return fig


# def circle_graph(data):
    
#     if len(data) == 0:
        