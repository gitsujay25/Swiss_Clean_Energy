import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#---------------------------- give_fig ------------------------------
# This function returns the plotly figure with cantons color coded
# by the variable in the category of energy_catg
def give_fig(df, geo_data, variable, energy_catg=None):
    # Map variable names to figure titles
    figure_titles = {
        "count": f"Number of {energy_catg} Energy Sources",
        "electrical_capacity": "Electrical Capacity in MW",
        "production": "Energy Production per year in MWh"
    }
    # Map variable names to colorbar titles
    colorbar_titles = {
        "count": "Number of Sources",
        "electrical_capacity": "MW",
        "production": "MWh"
    }
    # Pick titles based on the variable
    figure_title = figure_titles.get(variable, variable.title())
    colorbar_title = colorbar_titles.get(variable, variable.title())
    # Create the choropleth map
    fig = px.choropleth_map(
        df,
        color=variable,
        geojson=geo_data,
        locations="canton_name",
        featureidkey="properties.kan_name",
        center={"lat": 46.8, "lon": 8.3},
        map_style="open-street-map",
        zoom=5.6,
        opacity=0.5,
        width=900,
        height=400,
        labels={"canton_name": "Canton",
                "count": "Number of Sources",
                "electrical_capacity": "Electrical Capacity (MW)",
                "production": "Energy Production (MWh)"},
        title=figure_title,
        color_continuous_scale="viridis"
    )
    # Update layout: colorbar title and fonts
    fig.update_layout(
        margin={"r":0,"t":140,"l":0,"b":0},
        #font={"family":"Sans", "color":"maroon"},
        title={"font_size":22, "xanchor":"center", "x":0.5, "yanchor":"top"},
        hoverlabel={"bgcolor":"white", "font_size":12, "font_family":"Sans"},
        coloraxis_colorbar=dict(
            title=dict(
                text=colorbar_title,
                side="top",
                font=dict(size=15, family="Arial"),
            ),
            orientation="h",
            x=0.5,            # center horizontally (0=left, 1=right)
            y=1.0,           # place below plot
            xanchor="center",
            yanchor="bottom",
            tickfont=dict(size=15, family="Arial"),
            ticklen=5,
            thickness=15,
            len=1.0,
            bgcolor="rgba(0,0,0,0)",
            outlinewidth=0
        )
    )
    return fig

#---------------------------- give_swiss_fig ------------------------------
# This function returns the plotly figure with switzerland shaded and the
# location of the of the sources in scatter plot
def give_swiss_fig(df,geo_data,lat_cntr,lon_cntr,zoom):
    custom_colors = ["#FF0000", "#218BEF", "#07FF03", "#FFF200"]
    fig_ = px.choropleth_map(
        data_frame=df,
        geojson=geo_data,
        locations="canton_name",
        featureidkey="properties.kan_name",
        center={"lat": lat_cntr, "lon": lon_cntr},
        map_style="open-street-map", 
        zoom=zoom,
        opacity=0.15,
        color_discrete_sequence=["#B101FC"],
    )

    fig_scatr = px.scatter_map(df,
                        lat='lat',
                        lon='lon',
                        color='energy_source_level_2',
                        map_style="open-street-map",
                        hover_name='municipality',
                        labels={'energy_source_level_2': 'Energy Type',
                            'company': 'Company',
                            'address': 'Address',
                            "electrical_capacity": "Electrical Capacity (MW)",
                            "production": "Energy Production (MWh)"},
                        hover_data={
                            'energy_source_level_2': True,
                            'lat': False,      # hide lat
                            'lon': False,      # hide lon
                            'technology': False,
                            'company': True,
                            'address': True,
                            'electrical_capacity': ':.2f',  # format number
                            'production': ':.2f'    # format number
                        },
                        #zoom=1.5,
                        color_discrete_sequence=custom_colors,
                        category_orders={"energy_source_level_2": ["Solar", "Hydro", "Bioenergy", "Wind"]},
                        opacity=1,
                        size_max=0.1)

    fig_.update_layout(
                        title=dict(
                            text=f"",
                            font=dict(size=1),
                            xanchor="left",
                            x=0.0,
                            yanchor="top"
                        ),
                        hoverlabel={"bgcolor":"white", "font_size":12, "font_family":"Sans"},
                        title_font=dict(size=24, color='Black', family='Arial, sans-serif'),
                        height=600,
                        width=600,
                        coloraxis_showscale=False,
                        hovermode='closest',
                        # map=dict(
                        #     style='carto-positron'
                        # ),
                        legend_title_text='Energy Type'
    )
    fig_.add_traces(list(fig_scatr.select_traces()))
    fig_.data[0].showlegend = False
    return fig_

#---------------------------- give_canton_fig ------------------------------
# This function returns the plotly figure with canton shaded and the
# location of the of the sources in scatter plot
def give_canton_fig(df,geo_data,lat_cntr,lon_cntr,zoom):
    custom_colors = ["#FF0000", "#218BEF", "#07FF03", "#FFF200"]
    fig_ = px.choropleth_map(
        data_frame=df,
        color="canton_name",
        geojson=geo_data,
        locations="canton_name",
        featureidkey="properties.kan_name",
        center={"lat": lat_cntr, "lon": lon_cntr},
        map_style="open-street-map", 
        zoom=zoom,
        opacity=0.15,
        color_discrete_sequence=["#B101FC"],
    )

    fig_scatr = px.scatter_map(df,
                        lat='lat',
                        lon='lon',
                        color='energy_source_level_2',
                        map_style="open-street-map",
                        hover_name='municipality',
                        labels={'energy_source_level_2': 'Energy Type',
                            'company': 'Company',
                            'address': 'Address',
                            "electrical_capacity": "Electrical Capacity (MW)",
                            "production": "Energy Production (MWh)"},
                        hover_data={
                            'energy_source_level_2': True,
                            'lat': False,      # hide lat
                            'lon': False,      # hide lon
                            'technology': False,
                            'company': True,
                            'address': True,
                            'electrical_capacity': ':.2f',  # format number
                            'production': ':.2f'    # format number
                        },
                        #zoom=1.5,
                        color_discrete_sequence=custom_colors,
                        category_orders={"energy_source_level_2": ["Solar", "Hydro", "Bioenergy", "Wind"]},
                        opacity=1,
                        size_max=0.1)
    #variable = df["canton_name"].iloc[0]
    fig_.update_layout(
                        title=dict(
                            text=f"",
                            font=dict(size=1),
                            xanchor="left",
                            x=0.0,
                            yanchor="top"
                        ),
                        hoverlabel={"bgcolor":"white", "font_size":12, "font_family":"Sans"},
                        title_font=dict(size=24, color='Black', family='Arial, sans-serif'),
                        height=600,
                        width=600,
                        coloraxis_showscale=False,
                        hovermode='closest',
                        # map=dict(
                        #     style='carto-positron'
                        # ),
                        legend_title_text='Energy Type'
    )
    fig_.add_traces(list(fig_scatr.select_traces()))
    fig_.data[0].showlegend = False
    return fig_

#---------------------------- give_bar_fig ------------------------------
# This function returns the plotly figure with a colorcoded barplot 
def give_bar_fig(sources_per_canton_sorted, yvar, cvar, yax, cax):
    fig = px.bar(
        sources_per_canton_sorted,
        x='canton_name',
        y=yvar,
        color=cvar,
        color_continuous_scale='Viridis',
        hover_data={
            "canton_name": True,    # show this
            "production": ':.2f',   # format to 1 decimal
            "electrical_capacity": ':.2f',  # 2 decimals
            "count": True          # hide from hover
        },
        labels={
            "canton_name": "Canton",
            "count": "Number of Sources",
            "electrical_capacity": "Electrical Capacity (MW)",
            "production": "Production (MWh)"
        },
        #labels={'electrical_capacity':'Electrical capacity<br>(in MWh)'}
        #color_discrete_sequence=['#1E90FF']  # <-- set bar color (blue here)
    )
    fig.update_layout(
        title=dict(
            text=yax + " per Canton",  # Title text
            font=dict(
                family="Arial",   # Font family
                size=18,          # Font size
                color="black"  # Font color
        ),
            # x=0,  # Horizontal alignment (0=left, 0.5=center, 1=right)
            # xanchor='center',  # Anchor point
            # yanchor='top'      # Vertical anchor
        ),
        #xaxis_title='Canton',
        #yaxis_title='Count',
        xaxis=dict(
            title=dict(
                text='', 
                font=dict(size=1, color='black', family='Arial')
            ),
            tickfont=dict(size=15, color='dimgray', family='Arial')
        ),
        yaxis=dict(
            title=dict(
                text=yax,
                font=dict(size=16, color='black', family='Arial')
            ),
            gridcolor='white',
            tickfont=dict(size=15, color='dimgray', family='Arial')
        ),
        plot_bgcolor='#E3EEFA',
        coloraxis_colorbar=dict(
            title=dict(
                text=cax,  # title text
                font=dict(size=16)              # title font size
            ),
            tickfont=dict(size=15),             # tick label font
            len=1.0,                            # colorbar length (0–1 fraction)
            thickness=20,                       # colorbar width (pixels)
            yanchor="middle",
            y=0.5
        )
    )
    return fig

#---------------------------- give_pie_fig ------------------------------
# This function returns the plotly figure for piechart 
def give_pie_fig(df, variable):
    figure_titles = {
        "electrical_capacity": "Electrical Capacity",
        "production": "Energy Production per year"
    }
    figure_title = figure_titles.get(variable, variable.title())
    fig_ = px.pie(
        df,
        names="energy_source_level_2",
        values=variable,
        color="energy_source_level_2",
        color_discrete_map={
            "Solar": "#FF0000",
            "Hydro": "#218BEF",
            "Bioenergy": "#07FF03",
            "Wind": "#FFF200"
        }
    )

    fig_.update_traces(
        textposition='outside',
        textinfo='percent+label',
        # textfont=dict(
        #     family="Arial",         # font family
        #     size=18,                # font size
        #     color="black"           # font color
        # )
    )

    fig_.update_layout(
        title=dict(
            text=figure_title,  # your title
            x=0.5,      # horizontal center (0=left, 0.5=center, 1=right)
            xanchor='center',
            yanchor='top',
            y=0.95,
            font=dict(size=16, color='black', family="Arial")
        ),
        height=310,
        width=310,
        showlegend=False
    )
    return fig_

#---------------------------- give_pie_fig ------------------------------
# This function returns the plotly figure for piechart with doughnut shape
def give_pie_fig2(df, variable):
    figure_titles = {
    "electrical_capacity": "Electrical Capacity",
        "production": "Energy Production per year"
    }
    figure_title = figure_titles.get(variable, variable.title())

    df_plot = df.groupby("energy_source_level_2")[variable].sum().reset_index()
    # Desired order (important!)
    #desired_order = ["Solar", "Hydro", "Bioenergy", "Wind"]
    # Custom colors
    custom_color = ["#FF0000", "#218BEF", "#07FF03", "#FFF200"]
    color_map={
        "Solar": "#FF0000",
        "Hydro": "#218BEF",
        "Bioenergy": "#07FF03",
        "Wind": "#FFF200"
    }
    # Reorder df according to desired order
    #df_plot = df_new#.set_index("energy_source_level_2").loc[desired_order].reset_index()
    colors = df_plot["energy_source_level_2"].map(color_map)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df_plot["energy_source_level_2"],
                values=df_plot[variable],
                hole=0.6,
                marker=dict(colors=colors),
                textinfo="percent+label",
                textfont=dict(size=14),
                hovertemplate="<b>%{label}</b><br> %{value}<extra></extra>"
            )
        ]
    )
    if variable == 'electrical_capacity':
        text_t=f"<b>Total<br>{df[variable].sum():,.0f}</b><br>MW"
    else:
        text_t=f"<b>Total<br>{df[variable].sum():,.0f}</b><br>MWh"
    
    # Add center text
    fig.update_layout(
        annotations=[
            dict(
                text=text_t,
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=15)
            )
        ],
        #margin=dict(t=45, b=15, l=10, r=10),
        title=dict(
            text="",
            x=0.5,      # horizontal center (0=left, 0.5=center, 1=right)
            xanchor='center',
            yanchor='top',
            y=0.99,
            font=dict(size=1, color='black', family="Arial")
        ),
        height=340,
        width=300,
        showlegend=False
    )
    return fig

#---------------------------- give_bar_fig ------------------------------
# This function returns the plotly figure for bar plot
def give_bar_fig2(df_org, variable):
    if variable == 'Number of Sources':
        df = df_org.groupby('energy_source_level_2').size().reset_index(name='Number of Sources')
    else:
        df = df_org.groupby('energy_source_level_2')[variable].sum.reset_index(name=variable)
    ymaximum = df[variable].max()
    ymaximum = ymaximum + (0.25 * ymaximum)
    fig_ = px.bar(
        df,
        x=variable,
        y="energy_source_level_2",
        text='Number of Sources',  # show value on top
        color="energy_source_level_2",
        color_discrete_map={
            "Solar": "#FF0000",
            "Hydro": "#218BEF",
            "Bioenergy": "#07FF03",
            "Wind": "#FFF200"
        },
    )

    # Automatically place text on top of bars
    fig_.update_traces(textposition='outside', texttemplate="%{text}", textfont_size=14)
    fig_.update_xaxes(tickfont=dict(size=14))
    fig_.update_yaxes(tickfont=dict(size=14))
    fig_.update_xaxes(range=[0, ymaximum])

    # Axis labels
    fig_.update_layout(
        title=dict(
            text="Number of Sources",  # your title
            x=0.5,      # horizontal center (0=left, 0.5=center, 1=right)
            xanchor='center',
            yanchor='top',
            y=0.95,
            font=dict(size=16, color='black', family="Arial")
        ),
        yaxis_title="",
        xaxis_title="",
        
        height=220,
        width=600,
        #autosize=True,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False
    )
    return fig_

#---------------------------- give_violin_fig ------------------------------
# This function returns the plotly figure for violin plot
def give_violin_fig(cl_en, variable, height, titl, zoom):
    if zoom == 'Yes':
        Q1 = cl_en[variable].quantile(0.25)
        Q3 = cl_en[variable].quantile(0.75)
        IQR = Q3 - Q1
        UF = Q3 + 1.5 * IQR
        LF = Q1 - 1.5 * IQR
        df_clean = cl_en[(cl_en[variable] >= LF)&(cl_en[variable] <= UF)]
        box_var = False
    else:
        df_clean = cl_en
        box_var = True
 
    fig = px.violin(
        df_clean,
        x=variable,       # the distribution you want to visualize
        color_discrete_sequence=["#fc7c7c"],
        box=box_var,             # show mini boxplot inside
        points="all", #False #"all"          # show all data points
        )

    fig.update_traces(marker=dict(size=4))
    fig.update_xaxes(
        tickfont=dict(size=14, color="black", family="Arial")
    )

    fig.update_xaxes(showgrid=True)
    fig.update_xaxes(gridcolor="white")
    fig.update_layout(
        title=dict(
            text=titl,  # your title
            x=0.9,      # horizontal center (0=left, 0.5=center, 1=right)
            xanchor='right',
            yanchor='top',
            y=0.95,
            font=dict(size=16, color='black', family="Arial")
        ),
        #xaxis_title="Production",
        plot_bgcolor= "#dce7f4",
        height=height,
        xaxis_title=None,
        margin=dict(b=0, t=0)
        #width=400,
    )
    return fig

#---------------------------- give_sns ------------------------------
# This function returns seaborn histogram axes
def give_sns(df,ax,col,bin_size,lab):
    sns.histplot(data=df,
                 x="ratio",
                 color=col,
                 alpha=0.35,
                 edgecolor=None,
                 stat="density",
                 kde= True,
                 bins=bin_size,
                 label=lab,
                 ax=ax)

#---------------------------- give_hist_fig ------------------------------
# This function returns histogram plots with seaborn and matplotlib
def give_hist_fig(df):
    df_clean = df.dropna(subset=["ratio"])
    df_plot1=df_clean[df_clean['energy_source_level_2']=='Solar']
    df_plot2=df_clean[df_clean['energy_source_level_2']=='Hydro']
    df_plot3=df_clean[df_clean['energy_source_level_2']=='Bioenergy']
    df_plot4=df_clean[df_clean['energy_source_level_2']=='Wind']
    median_solar = df_plot1["ratio"].median()
    median_hydro = df_plot2["ratio"].median()
    median_bio = df_plot3["ratio"].median()
    median_wind = df_plot4["ratio"].median()
    sns.set_style("darkgrid", {"axes.facecolor": "0.9"})
    plt.rcParams['axes.facecolor'] = "#dce7f4ff"

    fig, ax = plt.subplots(figsize=(5, 4))
    give_sns(df_plot1,ax,"#E20202",30,'Solar')
    give_sns(df_plot2,ax,"#1F75C6",50, 'Hydro')
    give_sns(df_plot3,ax,"#07BA04",55,'Bioenergy')
    give_sns(df_plot4,ax,"#E7AB06",13,'Wind')
    plt.axvline(median_solar, color="#E20202", linestyle='--', linewidth=1, label=f"Median Solar: {median_solar:.2f}")
    plt.axvline(median_hydro, color="#1F75C6", linestyle='--', linewidth=1, label=f"Median Hydo: {median_hydro:.2f}")
    plt.axvline(median_bio, color="#07BA04", linestyle='--', linewidth=1, label=f"Median Bioenergy: {median_bio:.2f}")
    plt.axvline(median_wind, color="#E7AB06", linestyle='--', linewidth=1, label=f"Median Wind: {median_wind:.2f}")

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlabel("Ratio of production and capacity (h)",
            fontsize=10,
            fontfamily='Arial')

    plt.ylabel("Count",
            fontsize=10,
            fontfamily='Arial')
    
    ax.legend()
    leg = ax.legend()
    for text in leg.get_texts():
        text.set_fontsize(9)
        text.set_family("Arial")
    #plt.setp(ax.legend(), fontsize=1, family="Arial", fontweight="bold")
    #plt.setp(leg.get_title(), fontsize=16, family="Arial", fontweight="bold")
    return fig

#---------------------------- give_scatter_fig ------------------------------
# This function returns scatter plots with seaborn and matplotlib
def give_scatter_fig(df,df1,en_cat,zoom):
    df_ = df.dropna(subset=["ratio"])
    df_clean1 = df1.dropna(subset=["ratio"])

    if zoom == 'Yes':
        Q1 = df_["production"].quantile(0.25)
        Q3 = df_["production"].quantile(0.75)
        IQR = Q3 - Q1
        UF = Q3 + 1.5 * IQR
        LF = Q1 - 1.5 * IQR
        EQ1 = df_["electrical_capacity"].quantile(0.25)
        EQ3 = df_["electrical_capacity"].quantile(0.75)
        EIQR = EQ3 - EQ1
        EUF = EQ3 + 1.5 * EIQR
        ELF = EQ1 - 1.5 * EIQR
        df_clean = df_[(df_["production"] >= LF)&(df_["production"] <= UF)&(df_["electrical_capacity"] >= ELF)&(df_["electrical_capacity"] <= EUF)]
    else:
        df_clean = df_
    
    df_plot1=df_clean[df_clean['energy_source_level_2']=='Solar']
    df_plot2=df_clean[df_clean['energy_source_level_2']=='Hydro']
    df_plot3=df_clean[df_clean['energy_source_level_2']=='Bioenergy']
    df_plot4=df_clean[df_clean['energy_source_level_2']=='Wind']
    median_solar = df_clean1[df_clean1['energy_source_level_2']=='Solar']["ratio"].median()
    median_hydro = df_clean1[df_clean1['energy_source_level_2']=='Hydro']["ratio"].median()
    median_bio = df_clean1[df_clean1['energy_source_level_2']=='Bioenergy']["ratio"].median()
    median_wind = df_clean1[df_clean1['energy_source_level_2']=='Wind']["ratio"].median()
    sns.set_style("darkgrid", {"axes.facecolor": "0.9"})
    plt.rcParams['axes.facecolor'] = "#dce7f4ff"

    fig, ax = plt.subplots(figsize=(5, 5))
    if (en_cat=="All")or(en_cat=="Solar"):
        sns.scatterplot(data=df_plot1,
                        x="electrical_capacity", 
                        y="production",
                        alpha=0.5,
                        size=10,
                        color="#E20202",
                        legend='auto')
        ax.axline((0, 0), slope=median_solar, color="#F6A3A3", alpha=1.0, linestyle='--', linewidth=1.2)
    if (en_cat=="All")or(en_cat=="Hydro"):
        sns.scatterplot(data=df_plot2,
                        x="electrical_capacity", 
                        y="production",
                        alpha=0.7,
                        size=10,
                        color="#1F75C6")
        ax.axline((0, 0), slope=median_hydro, color="#80A8CD", alpha=1.0, linestyle='--', linewidth=1.2)
    if (en_cat=="All")or(en_cat=="Bioenergy"):
        sns.scatterplot(data=df_plot3,
                        x="electrical_capacity", 
                        y="production",
                        alpha=0.7,
                        size=10,
                        color="#07BA04")
        ax.axline((0, 0), slope=median_bio, color="#85C384", alpha=1.0, linestyle='--', linewidth=1.2)
    if (en_cat=="All")or(en_cat=="Wind"):
        sns.scatterplot(data=df_plot4,
                        x="electrical_capacity", 
                        y="production",
                        alpha=0.7,
                        size=10,
                        color="#E7AB06")
        ax.axline((0, 0), slope=median_wind, color="#E4C87B", alpha=1.0, linestyle='--', linewidth=1.2)
    
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.xlabel("Electrical capacity (MW)",
            fontsize=9,
            fontfamily='Arial')

    plt.ylabel("Production (MWh)",
            fontsize=9,
            fontfamily='Arial')
    
    ax.legend()
    handles, labels  =  ax.get_legend_handles_labels()
    if en_cat=="All":
        ax.legend(handles, ['Solar', 'Hydro', 'Bioenergy', 'Wind'], prop = {"size": 8}, loc='upper left')
    elif en_cat=="Solar":
        ax.legend(handles, ['Solar'], prop = {"size": 8}, loc='upper left')
    elif en_cat=="Hydro":
        ax.legend(handles, ['Hydro'], prop = {"size": 8}, loc='upper left')
    elif en_cat=="Bioenergy":
        ax.legend(handles, ['Bioenergy'], prop = {"size": 8}, loc='upper left')
    elif en_cat=="Wind":
        ax.legend(handles, ['Wind'], prop = {"size": 8}, loc='upper left')
    # for text in ax.legend().get_texts():
    #     text.set_fontsize(7)
    #     text.set_family("Arial")
    #plt.setp(ax.legend(), fontsize=1, family="Arial", fontweight="bold")
    #plt.setp(leg.get_title(), fontsize=16, family="Arial", fontweight="bold")
    return fig

#---------------------------- give_scatter_fig ------------------------------
# This function returns line plots with matplotlib
def give_time_fig(df,variable,en_cat):
    time_ = pd.to_datetime(df.commissioning_date)
    df['commissioning_date']=time_.sort_values(ascending=True)
    df1=df[df['energy_source_level_2']=='Solar']
    df2=df[df['energy_source_level_2']=='Hydro']
    df3=df[df['energy_source_level_2']=='Bioenergy']
    df4=df[df['energy_source_level_2']=='Wind']

    df['cumsum']=df[variable].cumsum(axis=0, skipna=True)
    df1['cumsum']=df1[variable].cumsum(axis=0, skipna=True)
    df2['cumsum']=df2[variable].cumsum(axis=0, skipna=True)
    df3['cumsum']=df3[variable].cumsum(axis=0, skipna=True)
    df4['cumsum']=df4[variable].cumsum(axis=0, skipna=True)

    fig, ax = plt.subplots(figsize=(5, 4))
    if en_cat=='All':
        #sns.lineplot(data=df, x='commissioning_date', y='cumsum',ax=ax)
        ax.plot(df['commissioning_date'],df['cumsum'],color="#000000", alpha=1.0, linestyle='-', linewidth=1.5)
    if (en_cat=="All")or(en_cat=="Solar"):
        ax.plot(df1['commissioning_date'],df1['cumsum'],color="#E20202", alpha=1.0, linestyle='-', linewidth=1.5)
    if (en_cat=="All")or(en_cat=="Hydro"):
        ax.plot(df2['commissioning_date'],df2['cumsum'],color="#1F75C6", alpha=1.0, linestyle='-', linewidth=1.5)
    if (en_cat=="All")or(en_cat=="Bioenergy"):
        ax.plot(df3['commissioning_date'],df3['cumsum'],color="#07BA04", alpha=1.0, linestyle='-', linewidth=1.5)
    if (en_cat=="All")or(en_cat=="Wind"):
        ax.plot(df4['commissioning_date'],df4['cumsum'],color="#E7AB06", alpha=1.0, linestyle='-', linewidth=1.5)
    
    plt.xlabel("Year",
            fontsize=12,
            fontfamily='Arial')
    if variable=='production':
        plt.ylabel("Total Production (MWh)",
                fontsize=12,
                fontfamily='Arial')
    if variable=='electrical_capacity':
        plt.ylabel("Total Electrical Capacity (MW)",
                fontsize=12,
                fontfamily='Arial')
    if variable=='count':
        plt.ylabel("Total Number of Sources",
                fontsize=12,
                fontfamily='Arial')
    #ax.legend()
    #handles, labels  =  ax.get_legend_handles_labels()
    if en_cat=="All":
        plt.legend(['All', 'Solar', 'Hydro', 'Bioenergy', 'Wind'], prop = {"size": 10}, loc='upper left')
    elif en_cat=="Solar":
        ax.legend(['Solar'], prop = {"size": 10}, loc='upper left')
    elif en_cat=="Hydro":
        ax.legend(['Hydro'], prop = {"size": 10}, loc='upper left')
    elif en_cat=="Bioenergy":
        ax.legend(['Bioenergy'], prop = {"size": 10}, loc='upper left')
    elif en_cat=="Wind":
        ax.legend(['Wind'], prop = {"size": 10}, loc='upper left')
    return fig
#------------------------------------------------------------------------------------------------------------------------------------------


# def give_kde_fig(df):
#     fig = ff.create_distplot(
#         [df["ratio"].dropna()],
#         ['r1'],  # your labels
#         show_hist=True,
#         bin_size=[110],
#         show_rug=False,
#     )
#     fig.update_yaxes(
#         tickfont=dict(size=14, color="black", family="Arial")
#     )
#     fig.update_layout(
#         title=dict(
#             text="xxx",  # your title
#             x=0.9,      # horizontal center (0=left, 0.5=center, 1=right)
#             xanchor='right',
#             yanchor='top',
#             y=0.95,
#             font=dict(size=16, color='black', family="Arial")
#         ),
#         yaxis_title="Production",
#         plot_bgcolor='#E3EEFA',
#         height=400,
#         width=400,
#         #xaxis_title=None,
#         #margin=dict(b=10, t=10, l=10, r=10)
#         #width=400,
#     )
#     fig.update_yaxes(automargin=True)
#     #fig.data[1].visible = False
#     # fig.data[0].opacity = 0.3
#     # fig.data[1].opacity = 0.3
#     # fig.data[2].opacity = 0.3
#     # fig.data[3].opacity = 0.3
    
#     return fig
# ------------ sns violin plot -----------------
 # fig, ax = plt.subplots(figsize=(height, 4))
    # if zoom=='No':
    #     sns.violinplot(data=df_clean,
    #                 x=variable,
    #                 inner_kws=dict(box_width=15, whis_width=2, color="0.3"),
    #                 color="#FE9C9C",
    #                 ax=ax)
    # else:
    #     sns.violinplot(data=df_clean,
    #                x=variable,
    #                inner="point",
    #                color="#FE9C9C",
    #                ax=ax)
    # # plt.xlabel("Electrical capacity (MW)",
    # #         fontsize=10,
    # #         fontfamily='Arial')
    # if height==8:
    #     plt.xticks(fontsize=12)
    #     if variable=='production':
    #         plt.xlabel("Production (MWh)",
    #                 fontsize=12,
    #                 fontfamily='Arial')
    #     else:
    #         plt.xlabel("Electrical Capacity (MW)",
    #                 fontsize=12,
    #                 fontfamily='Arial')
    #     ax.text(.9,.9,titl,
    #     horizontalalignment='center',
    #     transform=ax.transAxes,
    #     fontsize=13)
    # else:
    #     if df_clean[variable].max() > 45000:
    #         plt.xticks(range(0,int(df_clean[variable].max()),15000))
    #     plt.xticks(fontsize=24)
    #     plt.xlabel("",
    #             fontsize=1,
    #             fontfamily='Arial')
    #     ax.text(.85,.85,titl,
    #         horizontalalignment='center',
    #         transform=ax.transAxes,
    #         fontsize=27)