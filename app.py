#***********************************************************************
#    Visulalization Project: Clean Renewable Energy in Switzerland     #
#                         Author: Sujay Ray                            #
#                        Date: 19th Nov 2025                           #
#***********************************************************************

import streamlit as st
import pandas as pd
from copy import deepcopy

import utils as utl
import plotting as pltg

#-------------------------------------------------------------------------
#------------------------------ load all data files ----------------------
energy_df_raw = utl.load_data(path='./data/swiss_clean_energy.csv')
energy_df_raw.rename(columns={'canton_name':'kan_name'})
energy_df = deepcopy(energy_df_raw)

geojsn_data_raw = utl.load_geojsn_data('./data/georef-switzerland-kanton.geojson')
geojsn_data = deepcopy(geojsn_data_raw)

geopd_raw = utl.load_geopanda_data('./data/georef-switzerland-kanton.geojson')
geopd_data = deepcopy(geopd_raw)
#------------------------------------------------------------------------------
#------------------------- Setting the page config ----------------------------
st.set_page_config(layout="wide")
st.markdown(
    f"""
    <p style='font-size:36px; font-weight:700; color:black; text-align:left'>
        Clean Renewable Energy in Switzerland <span style='font-size:36px'>(commissioned between 2004-2018)</span>
    </p>
    """,
    unsafe_allow_html=True
)
#------------------------------------------------------------------------------
#------------------------- Setting the tabs -----------------------------------
tab1, tab2, tab3 = st.tabs(["🌐 Overviewiew", "📍 Source location", "📊 Summary statistics"])
#-------------------------------------------------------------------------------------------------------------------------
#************************************************* Begin Tab1 ************************************************************
#-------------------------------------------------------------------------------------------------------------------------
with tab1:
    st.markdown(
        """
        <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
            Renewable energy is energy made from naturally replenished sources which produce little or no green house gases.
            Renewable energy systems have rapidly become more efficient and cheaper over the past 30 years.
            They play a crucial role in Switzerland's commitment to sustainability and reducing carbon emissions.
            This dashboard provides an interactive exploration of clean renewable energy sources commissioned between 2004 and
            2018 across various cantons in Switzerland. Users can analyze the distribution, capacity, and production of different
            energy types, gaining insights into the country's renewable energy landscape.
        </p>
        """,
        unsafe_allow_html=True
    )
    #------------------------- Setting the energy category ------------------------
    energy_catags = ['All'] + sorted(pd.unique(energy_df["energy_source_level_2"]))
    col1, col2 = st.columns([1, 4])
    with col1:
        energy_catg = st.selectbox('Select an Energy Categoy', energy_catags)
    #------------------------------------------------------------------------------
    if energy_catg=='All':
        sources_per_canton=energy_df.groupby('canton_name').size().reset_index(name='count')
        sources_per_canton['electrical_capacity']=energy_df.groupby('canton_name')['electrical_capacity'].sum().reset_index(name='electrical_capacity').electrical_capacity
        sources_per_canton['production']=energy_df.groupby('canton_name')['production'].sum().reset_index(name='production').production
    else:
        energy_df_tmp=energy_df[energy_df["energy_source_level_2"]==energy_catg]
        sources_per_canton=energy_df_tmp.groupby('canton_name').size().reset_index(name='count')
        sources_per_canton['electrical_capacity']=energy_df_tmp.groupby('canton_name')['electrical_capacity'].sum().reset_index(name='electrical_capacity').electrical_capacity
        sources_per_canton['production']=energy_df_tmp.groupby('canton_name')['production'].sum().reset_index(name='production').production

    custom_names = {
        "All": "Total Renewable",
        "Hydro": "Hydropower",
        "Solar": "Solar Power",
        "Wind": "Wind Power",
        "Bioenergy": "Bio"
    }
    # Replace only if found in the dictionary
    display_catg = custom_names.get(energy_catg, energy_catg)
    #------------------------------- Setting Maps for tab1 ----------------------------------------
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        fig=pltg.give_fig(sources_per_canton,geojsn_data,"count",display_catg)
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        fig=pltg.give_fig(sources_per_canton,geojsn_data,"electrical_capacity")
        st.plotly_chart(fig,use_container_width=True)
    with col3:
        fig=pltg.give_fig(sources_per_canton,geojsn_data,"production")
        st.plotly_chart(fig,use_container_width=True)

    st.write("")  #spacing
    st.write("")  #spacing
    st.write("")  #spacing

    st.markdown(
        """
        <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
            In the maps above, cantons are color-coded based on the number of energy sources, installed electrical capacity in Mega Watt (MW),
            and energy production per year in Mega-Watt-hour (MWh) for the selected energy category. Lightercolors indicate higher values,
            while darker colors represent lower values. This visual representation allows users to quickly identify cantons
            leading in renewable energy initiatives and those with potential for growth.
        </p>
        """,
        unsafe_allow_html=True
    )
    #------------------------- Highlight Top Cantons -----------------------------
    top_sources = sources_per_canton.loc[
        sources_per_canton["count"].idxmax(), "canton_name"
    ]
    top_sources_num = sources_per_canton.loc[
        sources_per_canton["count"].idxmax(), "count"
    ]
    top_capacity = sources_per_canton.loc[
        sources_per_canton["electrical_capacity"].idxmax(), "canton_name"
    ]
    top_capacity_number = round(sources_per_canton.loc[
        sources_per_canton["electrical_capacity"].idxmax(), "electrical_capacity"
    ], 2)
    top_production = sources_per_canton.loc[
        sources_per_canton["production"].idxmax(), "canton_name"
    ]
    top_production_number = round(sources_per_canton.loc[
        sources_per_canton["production"].idxmax(), "production"
    ], 2)
    st.write("")  #spacing
    st.write("")  #spacing
    st.markdown(
        f"""
        <p style='font-size:20px; font-weight:bold; color:black; text-align:left'>
            Top Canton(s) in {display_catg} Energy category
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <p style='font-size:16px; font-weight:normal; color:black; text-align:left'>
            Most Energy Sources: 
            <span style='color:#E74C3C'>{top_sources}</span> (Total number of energy sources: <span style='color:#E74C3C'>{top_sources_num})</span><br>
            Highest Electrical Capacity:
            <span style='color:#E74C3C'>{top_capacity}</span> (Total capacity: <span style='color:#E74C3C'>{top_capacity_number} MW)</span><br>
            Highest Production:
            <span style='color:#E74C3C'>{top_production}</span> (Total production: <span style='color:#E74C3C'>{top_production_number} MWh)</span>
        </p>
        """,
        unsafe_allow_html=True
    )
    #------------------------- Bar Plots for the Cantons -----------------------------
    sources_per_canton_sorted = sources_per_canton.sort_values(by='count', ascending=False)
    fig = pltg.give_bar_fig(sources_per_canton_sorted,'count','electrical_capacity','Number of Sources', "Electrical capacity<br>(in MW)")
    st.plotly_chart(fig,use_container_width=True)

    sources_per_canton_sorted = sources_per_canton.sort_values(by='electrical_capacity', ascending=False)
    fig = pltg.give_bar_fig(sources_per_canton_sorted,'electrical_capacity','production','Electrical Capacity (in MW)', "Production<br>(in MWh)")
    st.plotly_chart(fig,use_container_width=True)

    sources_per_canton_sorted = sources_per_canton.sort_values(by='production', ascending=False)
    fig = pltg.give_bar_fig(sources_per_canton_sorted,'production','count','Production (in MWh)', "Number of<br>Sources")
    st.plotly_chart(fig,use_container_width=True)

    st.markdown(
        """
        <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
            The bar charts above provide a detailed comparison of cantons based on the number of energy sources,
            installed electrical capacity, and annual energy production for the selected energy category.
            Users can identify leading cantons in each aspect of renewable energy, facilitating a deeper understanding
            of regional contributions to Switzerland's renewable energy goals. The color gradients in the bars help visualize
            the correlation between the number of sources, capacity, and production across cantons. In general, cantons with a
            higher greater electrical capacity tend to have greater production, but there are exceptions which can be spotted with
            the colormap. For instance, a canton may have a lower number of energy sources but higher overall production due to
            the engineering of energy sources, efficiency and demand (Valais ranks 9th in number of sources but 2nd in capacity
            and 1st in production).
        </p>
        """,
        unsafe_allow_html=True
    )
    st.write("Data Source: https://data.open-power-system-data.org/renewable_power_plants/2020-08-25")
#-------------------------------------------------------------------------------------------------------------------------
#************************************************* Begin Tab2 ************************************************************
#-------------------------------------------------------------------------------------------------------------------------
with tab2:
    st.markdown(
        """
        <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
            This tab provides an interactive map displaying the approximate locations of various renewable energy sources across Switzerland.
            Users can filter the data by selecting specific cantons and energy categories to visualize the distribution
            of energy sources.<span style='font-size:14px; font-style:italic; font-weight:400; color:gray'> (Remark: The locations are approximate and meant for visualization purposes only.
            And the pie charts represent the percentage of different energy types among only Renewable energies considered here while
            excluding other energy types like Nuclear, Fossil etc.)</span>
        </p>
        """,
        unsafe_allow_html=True
    )
    #------------------------- Set Canton and energy category -----------------------------
    canton_names = ['All'] + sorted(pd.unique(energy_df["canton_name"]))
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        canton_name = st.selectbox('Select a Canton', canton_names, key="select_canton")
    with col3:
        energy_catg = st.selectbox('Select an Energy Categoy', energy_catags, key="select_energy") 

    custom_names = {
        "All": "Total Renewable",
        "Hydro": "Hydropower",
        "Solar": "Solar Power",
        "Wind": "Wind Power"
        ,"Bioenergy": "Bio"
    }
    # Replace only if found in the dictionary
    display_catg = custom_names.get(energy_catg, energy_catg)
    #--------------------------------- set the data ---------------------------------------
    if energy_catg=='All':
        if canton_name=='All':
            df_temp=energy_df
            df_temp2=energy_df
        else:
            df_temp=energy_df[energy_df['canton_name']==canton_name]
            df_temp2=energy_df[energy_df['canton_name']==canton_name]
    else:
        if canton_name=='All':
            df_temp=energy_df[energy_df["energy_source_level_2"]==energy_catg]
            df_temp2=energy_df
        else:
            df_temp=energy_df[(energy_df['canton_name']==canton_name)&(energy_df["energy_source_level_2"]==energy_catg)]
            df_temp2=energy_df[energy_df['canton_name']==canton_name]
    #--------------------------------------------------------------------------------------
    col1, col2 = st.columns([1.2, 1])
    #---------------------------- Set the Map in Tab2 -------------------------------------
    with col1:
        st.write("")  #spacing
        if canton_name=='All':
            st.markdown(
                f"""
                <p style='font-size:24px; font-weight:600; color:black; text-align:left'>
                    {display_catg} Energy Sources in Switzerland</span>
                </p>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <p style='font-size:24px; font-weight:600; color:black; text-align:left'>
                    {display_catg} Energy Sources in the canton of {canton_name}</span>
                </p>
                """,
                unsafe_allow_html=True
            )
        #---------------------------- the map ----------------------------------
        if energy_catg=='All':
            if canton_name=='All':
                fig=pltg.give_swiss_fig(df_temp,geojsn_data,46.8,8.3,6.4)
                st.plotly_chart(fig)
            else:
                lat_cntr, lon_cntr, zoom = utl.give_cntr_zoom(geopd_data,'kan_name',canton_name)
                fig=pltg.give_canton_fig(df_temp,geojsn_data,lat_cntr,lon_cntr,zoom)
                st.plotly_chart(fig)
        else:
            if canton_name=='All':
                fig=pltg.give_swiss_fig(df_temp,geojsn_data,46.8,8.3,6.4)
                st.plotly_chart(fig)
            else:
                if len(df_temp)==0:
                    st.write(f"There are no energy sources available for {energy_catg} energy in the canton of {canton_name}.")
                else:
                    lat_cntr, lon_cntr, zoom = utl.give_cntr_zoom(geopd_data,'kan_name',canton_name)
                    fig=pltg.give_canton_fig(df_temp,geojsn_data,lat_cntr,lon_cntr,zoom)
                    st.plotly_chart(fig)

        st.markdown(
            """
            <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:88%;'>
                The map above displays the approximate locations of renewable energy sources based on the selected canton and
                energy category. The limitations in location accuracy are due to the available latitude and longitude data which
                 are only accurate upto 4th decimal place. Some of the locations overlap due to the limited accuracy.
            </p>
            """,
            unsafe_allow_html=True
        )
    #---------------------------- Set the stat and info in tab2 -------------------------------------
    with col2:
        total_sources = len(df_temp)
        total_capacity = round(df_temp['electrical_capacity'].sum(), 2)
        total_production = round(df_temp['production'].sum(), 2)
        st.write("")  #spacing
        st.markdown(
            f"""
            <p style='font-size:22px; font-weight:600; color:black; text-align:center'>
                Summary in {display_catg} Energy category</span>
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <p style='font-size:16px; font-weight:500; color:blue; text-align:center'>
                Total Number of Energy Sources: <span style='color:#E74C3C'>{total_sources}</span><br>
                Total Electrical Capacity (in MW): <span style='color:#E74C3C'>{total_capacity}</span><br>
                Total Production (in MWh): <span style='color:#E74C3C'>{total_production}</span>
            </p>
            """,
            unsafe_allow_html=True
        )
        #---------------------------- histogram and pie chart -------------------------------
        st.write("")  #spacing
        st.markdown(
            f"""
            <p style='font-size:22px; font-weight:600; color:black; text-align:center'>
                Overview in All Energy category</span>
            </p>
            """,
            unsafe_allow_html=True
        )
        #---------------------------- histogram -------------------------------
        df_sources = df_temp2.groupby('energy_source_level_2').size().reset_index(name='Number of Sources')
        fig = pltg.give_bar_fig2(df_temp2, 'Number of Sources')
        st.plotly_chart(fig,use_container_width=False)
        #---------------------------- Pie chart -------------------------------
        col2_2, col2_3 = st.columns([1, 1])
        with col2_2:
            st.markdown(
                f"""
                <p style='font-size:17px; font-weight:670; color:black; text-align:center'>
                    Electrical Capacity</span>
                </p>
                """,
                unsafe_allow_html=True
            )
            fig = pltg.give_pie_fig2(df_temp2,'electrical_capacity')
            st.plotly_chart(fig)
        with col2_3:
            st.markdown(
                f"""
                <p style='font-size:17px; font-weight:670; color:black; text-align:center'>
                    Electrical Production per year</span>
                </p>
                """,
                unsafe_allow_html=True
            )
            fig = pltg.give_pie_fig2(df_temp2,'production')
            st.plotly_chart(fig)
    st.write("Data Source: https://data.open-power-system-data.org/renewable_power_plants/2020-08-25")
#-------------------------------------------------------------------------------------------------------------------------
#************************************************* Begin Tab3 ************************************************************
#-------------------------------------------------------------------------------------------------------------------------
with tab3:
    st.markdown(
        """
        <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
            This tab provides summary statistics and visualizations for renewable energy sources across Switzerland.
            Users can view the distribution of capacities, and productions, along with breakdowns by energy type and
            different cantons.
        </p>
        """,
        unsafe_allow_html=True
    )
    #---------------------------------------- Violin Plot ----------------------------------------
    st.markdown(
        """
        <p style='font-size:22px; font-weight:600; color:black; text-align:justify; text-align-last:left; width:100%;'>
            Distribution of Renewable Energy Production and Electrical Capacity
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
            The violin plots below illustrate the distribution of energy production and electrical capacity across
            different renewable energy types and cantons. Users can select a specific canton and energy category to
            explore how these metrics vary among energy sources. Outliers can also be removed to provide clearer
            insights into the underlying distribution.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.write("")  #spacing
    #------------------------- Set Canton and energy category -----------------------------
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
    with col1:
        canton_name = st.selectbox('Select a Canton', canton_names, key="select_canton2")
    with col2:
        energy_catg = st.selectbox('Select an Energy Catagoy', energy_catags, key="select_energy2")
    with col3:    
        outlier_zoom = st.radio('Outliers removed:', ['No', 'Yes'], key='radio_view')
    #--------------------------------------------------------------------------------------
    custom_names = {
        "All": "Total Renewable",
        "Hydro": "Hydropower",
        "Solar": "Solar Power",
        "Wind": "Wind Power"
        ,"Bioenergy": "Bio"
    }
    # Replace only if found in the dictionary
    display_catg = custom_names.get(energy_catg, energy_catg)
    custom_names_cant = {
        "All": "Switzerland"
    }
    # Replace only if found in the dictionary
    display_catg_cant = custom_names_cant.get(canton_name, canton_name)
    energy_arr = [x for x in energy_catags if x != energy_catg]
    #----------------------------- set the data frame ----------------------------------------
    if energy_catg=='All':
        if canton_name=='All':
            df_temp=energy_df
            df_temp1=df_temp
        else:
            df_temp=energy_df[energy_df['canton_name']==canton_name]
            df_temp1=df_temp
    else:
        if canton_name=='All':
            df_temp=energy_df[energy_df["energy_source_level_2"]==energy_catg]
            df_temp1=energy_df
        else:
            df_temp=energy_df[(energy_df['canton_name']==canton_name)&(energy_df["energy_source_level_2"]==energy_catg)]
            df_temp1=energy_df[energy_df['canton_name']==canton_name]
    #----------------------------- production violin plot ---------------------------
    #----------------------------- main plot ----------------------------------------
    col1, col0, col2 = st.columns([1.1, 0.2, 1])
    with col1:
        st.write("")  #spacing
        st.write("")  #spacing
        st.markdown(
            f"""
            <p style='font-size:16px; font-weight:500; color:black; text-align:center;'>
                Distribution of {display_catg} Energy Production (in MWh) in {display_catg_cant}
            </p>
            """,
            unsafe_allow_html=True
        )
        if len(df_temp)==0:
            st.write(f"There are no energy sources available for {energy_catg} energy in the canton of {canton_name}.")
        else:
            fig=pltg.give_violin_fig(df_temp, 'production', 300, energy_catg, outlier_zoom)
            st.plotly_chart(fig)
            #fig=pltg.give_violin_fig(df_temp, 'production', 8, energy_catg, outlier_zoom)
            #st.pyplot(fig)
    #----------------------------- supplementary plot --------------------------------
    with col2:
        st.markdown(
            f"""
            <p style='font-size:16px; font-weight:500; color:black; text-align:center;'>
                Distribution of Energy Production (in MWh) in {display_catg_cant} for other Energy Types<br>
                (included to support comparative analysis)
            </p>
            """,
            unsafe_allow_html=True
        )
        col2_1, col2_2 = st.columns([1, 1])
        #-----------------------------------------------------
        with col2_1:
            if energy_arr[0]== 'All':
                df_temp21=df_temp1
            else:
                df_temp21=df_temp1[df_temp1["energy_source_level_2"]==energy_arr[0]]
            if len(df_temp21)==0:
                st.write(f"There are no energy sources available for {energy_arr[0]} energy in the canton of {canton_name}.")
            else:
                fig=pltg.give_violin_fig(df_temp21, 'production', 150, energy_arr[0], outlier_zoom)
                st.plotly_chart(fig)
                # fig=pltg.give_violin_fig(df_temp21, 'production', 8.1, energy_arr[0], outlier_zoom)
                # st.pyplot(fig)
        #-----------------------------------------------------
        with col2_2:
            df_temp22=df_temp1[df_temp1["energy_source_level_2"]==energy_arr[1]]
            if len(df_temp22)==0:
                st.write(f"There are no energy sources available for {energy_arr[1]} energy in the canton of {canton_name}.")
            else:
                fig=pltg.give_violin_fig(df_temp22, 'production', 150, energy_arr[1], outlier_zoom)
                st.plotly_chart(fig)
                # fig=pltg.give_violin_fig(df_temp22, 'production', 8.1, energy_arr[1], outlier_zoom)
                # st.pyplot(fig)
        #-----------------------------------------------------
        col2_1, col2_2 = st.columns([1, 1])
        #-----------------------------------------------------
        with col2_1:
            df_temp23=df_temp1[df_temp1["energy_source_level_2"]==energy_arr[2]]
            if len(df_temp23)==0:
                st.write(f"There are no energy sources available for {energy_arr[2]} energy in the canton of {canton_name}.")
            else:
                fig=pltg.give_violin_fig(df_temp23, 'production', 150, energy_arr[2], outlier_zoom)
                st.plotly_chart(fig)
                # fig=pltg.give_violin_fig(df_temp23, 'production', 8.1, energy_arr[2], outlier_zoom)
                # st.pyplot(fig)
        #-----------------------------------------------------
        with col2_2:
            df_temp24=df_temp1[df_temp1["energy_source_level_2"]==energy_arr[3]]
            if len(df_temp24)==0:
                st.write(f"There are no energy sources available for {energy_arr[3]} energy in the canton of {canton_name}.")
            else:
                fig=pltg.give_violin_fig(df_temp24, 'production', 150, energy_arr[3], outlier_zoom)
                st.plotly_chart(fig)
                # fig=pltg.give_violin_fig(df_temp24, 'production', 8.1, energy_arr[3], outlier_zoom)
                # st.pyplot(fig)
    #----------------------------- production violin plot ---------------------------
    #----------------------------- main plot ----------------------------------------
    st.write("")  #spacing
    col1, col0, col2 = st.columns([1.1, 0.2, 1])
    with col1:
        st.write("")  #spacing
        st.write("")  #spacing
        st.markdown(
            f"""
            <p style='font-size:16px; font-weight:500; color:black; text-align:center;'>
                Distribution of {display_catg} Energy Capacity (in MW)in {display_catg_cant}
            </p>
            """,
            unsafe_allow_html=True
        )
        if len(df_temp)==0:
            st.write(f"There are no energy sources available for {energy_catg} energy in the canton of {canton_name}.")
        else:
            fig=pltg.give_violin_fig(df_temp, 'electrical_capacity', 300, energy_catg, outlier_zoom)
            st.plotly_chart(fig)
            # fig=pltg.give_violin_fig(df_temp, 'electrical_capacity', 8, energy_catg, outlier_zoom)
            # st.pyplot(fig)
    #----------------------------- supplementary plot --------------------------------
    with col2:
        st.markdown(
            f"""
            <p style='font-size:16px; font-weight:500; color:black; text-align:center;'>
                Distribution of Energy Capacity (in MW) in {display_catg_cant} for other Energy Types<br>
                (included to support comparative analysis)
            </p>
            """,
            unsafe_allow_html=True
        )
        col2_1, col2_2 = st.columns([1, 1])
        #-----------------------------------------------------
        with col2_1:
            # if energy_arr[0]== 'All':
            #     df_temp21=df_temp1
            # else:
            #     df_temp21=df_temp1[df_temp1["energy_source_level_2"]==energy_arr[0]]
            if len(df_temp21)==0:
                st.write(f"There are no energy sources available for {energy_arr[0]} energy in the canton of {canton_name}.")
            else:
                fig=pltg.give_violin_fig(df_temp21, 'electrical_capacity', 150, energy_arr[0], outlier_zoom)
                st.plotly_chart(fig)
                # fig=pltg.give_violin_fig(df_temp21, 'electrical_capacity', 8.1, energy_arr[0], outlier_zoom)
                # st.pyplot(fig)
        #-----------------------------------------------------
        with col2_2:
            #df_temp22=df_temp1[df_temp1["energy_source_level_2"]==energy_arr[1]]
            if len(df_temp22)==0:
                st.write(f"There are no energy sources available for {energy_arr[1]} energy in the canton of {canton_name}.")
            else:
                fig=pltg.give_violin_fig(df_temp22, 'electrical_capacity', 150, energy_arr[1], outlier_zoom)
                st.plotly_chart(fig)
                # fig=pltg.give_violin_fig(df_temp22, 'electrical_capacity', 8.1, energy_arr[1], outlier_zoom)
                # st.pyplot(fig)
        #-----------------------------------------------------
        col2_1, col2_2 = st.columns([1, 1])
        #-----------------------------------------------------
        with col2_1:
            #df_temp23=df_temp1[df_temp1["energy_source_level_2"]==energy_arr[2]]
            if len(df_temp23)==0:
                st.write(f"There are no energy sources available for {energy_arr[2]} energy in the canton of {canton_name}.")
            else:
                fig=pltg.give_violin_fig(df_temp23, 'electrical_capacity', 150, energy_arr[2], outlier_zoom)
                st.plotly_chart(fig)
                # fig=pltg.give_violin_fig(df_temp23, 'electrical_capacity', 8.1, energy_arr[2], outlier_zoom)
                # st.pyplot(fig)
        #-----------------------------------------------------
        with col2_2:
            #df_temp24=df_temp1[df_temp1["energy_source_level_2"]==energy_arr[3]]
            if len(df_temp24)==0:
                st.write(f"There are no energy sources available for {energy_arr[3]} energy in the canton of {canton_name}.")
            else:
                fig=pltg.give_violin_fig(df_temp24, 'electrical_capacity', 150, energy_arr[3], outlier_zoom)
                st.plotly_chart(fig)
                # fig=pltg.give_violin_fig(df_temp24, 'electrical_capacity', 8.1, energy_arr[3], outlier_zoom)
                # st.pyplot(fig)

    st.write("")
    st.write("")
    #---------------------------------------- Scatter Plot and Histogram ----------------------------------------
    st.markdown(
        """
        <p style='font-size:22px; font-weight:600; color:black; text-align:justify; text-align-last:left; width:100%;'>
            Efficiency of Energy Production
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
            The efficiency of an energy source, relative to its installed electrical capacity, can be expressed
            using the ratio of production to capacity. A higher ratio indicates more efficient energy generation.
            However, this metric should be interpreted carefully, as efficiency also depends on external factors
            such as resource availability and the underlying technology. For example, wind power requires
            sufficiently high wind speeds, which may not be consistent throughout the year. Users can select an
            energy type and a canton to explore these efficiency patterns in more detail.
        </p>
        """,
        unsafe_allow_html=True
    )
    #------------------------- Set Canton and energy category -----------------------------
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
    with col1:
        canton_name = st.selectbox('Select a Canton', canton_names, key="select_canton3")
    with col2:
        energy_catg = st.selectbox('Select an Energy Catagoy', energy_catags, key="select_energy3")
    with col3:    
        outlier_zoom = st.radio('Outliers removed:', ['No', 'Yes'], key='radio_view3')
     #-------------------------------------- set the data -------------------------------------------
    df_temp = energy_df
    df_temp["ratio"] = df_temp.apply(lambda row: row["production"]/row["electrical_capacity"], axis=1)
    if energy_catg=='All':
        if canton_name=='All':
            df_temp1=df_temp
            #df_temp1=df_temp
        else:
            df_temp1=df_temp[df_temp['canton_name']==canton_name]
            #df_temp1=df_temp
    else:
        if canton_name=='All':
            df_temp1=df_temp[df_temp["energy_source_level_2"]==energy_catg]
            #df_temp1=energy_df
        else:
            df_temp1=df_temp[(df_temp['canton_name']==canton_name)&(df_temp["energy_source_level_2"]==energy_catg)]
            #df_temp1=energy_df[energy_df['canton_name']==canton_name]
    #-------------------------------------------------------------------------------------
    col1, col0, col2 = st.columns([1.0, 0.2, 0.9])
    #---------------------------------------- Scatter Plot ----------------------------------------
    with col1:
        st.write("")
        st.markdown(
            """
            <p style='text-indent:70px; font-size:16px; font-weight:500; color:black; text-align:center;'>
                Renewable Energy Efficiency Landscape
            </p>
            """,
            unsafe_allow_html=True
        )
        fig=pltg.give_scatter_fig(df_temp1,df_temp,energy_catg,outlier_zoom)
        st.pyplot(fig)
        st.markdown(
            """
            <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
                The straight lines in the scatter plot represent the average production-to-capacity ratio, computed
                from the median ratio within each energy type (see the right panel). Points above the line indicate higher production efficiency,
                while points below the line indicate lower efficiency relative to the average. Overall, the results
                suggest that Bioenergy and Hydropower tend to be more efficient, followed by Solar and Wind power.
            </p>
            """,
            unsafe_allow_html=True
        )
    #---------------------------------------- Histogram ----------------------------------------
    with col2:
        st.write("")
        st.write("")
        st.markdown(
            """
            <p style='text-indent:70px; font-size:16px; font-weight:500; color:black; text-align:center;'>
                Distribution of Energy Production Efficiency
            </p>
            """,
            unsafe_allow_html=True
        )
        fig=pltg.give_hist_fig(df_temp)
        #st.plotly_chart(fig)
        st.pyplot(fig)
        st.markdown(
            """
            <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
                Distribution of the production-to-capacity ratio for different energy types across Switzerland.
                The median ratio for each energy type is calculated to capture the central tendency of production efficiency.
                These median values are used in the left panel to draw the dashed reference lines that divide the
                scatter plot into higher- and lower-efficiency regions. The distribution plot shown here complements
                the scatter plot by providing additional insight into how the ratios are spread within each energy type.
            </p>
            """,
            unsafe_allow_html=True
        )
    #---------------------------------------- Yearly data ----------------------------------------
    st.write("")
    st.write("")
    st.markdown(
        """
        <p style='font-size:22px; font-weight:600; color:black; text-align:justify; text-align-last:left; width:100%;'>
            Increase in Renewable Energies over the years according to commissioning date
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
            """
            <p style='font-size:15px; font-weight:400; color:black; text-align:justify; text-align-last:left; width:100%;'>
                The plots below show the cumulative growth of renewable energy in Switzerland over the years, measured
                through the increasing number of installations, total production, and electrical capacity. Together,
                they highlight the steady expansion of renewable sources and their growing role in the country’s energy
                mix. Comparing these trends provides a clear snapshot of how rapidly renewable energy has developed and
                how different technologies have contributed to this progress. User can select a canton and an energy type
                to explore the data in details.
            </p>
            """,
            unsafe_allow_html=True
        )
    st.write("")
    #------------------------- Set Canton and energy category -----------------------------
    col1, col2, col3, col4 = st.columns([1, 0.2, 1, 3])
    with col1:
        canton_name = st.selectbox('Select a Canton', canton_names, key="select_canton4")
    with col3:
        energy_catg = st.selectbox('Select an Energy Catagoy', energy_catags, key="select_energy4")
    #------------------------------------ Set the data ------------------------------------
    df_temp = energy_df
    df_temp['count']=int(1)
    if energy_catg=='All':
        if canton_name=='All':
            df_temp1=df_temp
        else:
            df_temp1=df_temp[df_temp['canton_name']==canton_name]
    else:
        if canton_name=='All':
            df_temp1=df_temp[df_temp["energy_source_level_2"]==energy_catg]
        else:
            df_temp1=df_temp[(df_temp['canton_name']==canton_name)&(df_temp["energy_source_level_2"]==energy_catg)]
    #------------------------------------ plots ------------------------------------
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if len(df_temp1)==0:
                st.write(f"There are no energy sources available for {energy_catg} energy in the canton of {canton_name}.")
        else:
            fig=pltg.give_time_fig(df_temp1,'count',energy_catg)
            st.pyplot(fig)
    with col2:
        if len(df_temp1)==0:
                st.write(f"There are no energy sources available for {energy_catg} energy in the canton of {canton_name}.")
        else:
            fig=pltg.give_time_fig(df_temp1,'electrical_capacity',energy_catg)
            st.pyplot(fig)
    with col3:
        if len(df_temp1)==0:
                st.write(f"There are no energy sources available for {energy_catg} energy in the canton of {canton_name}.")
        else:
            fig=pltg.give_time_fig(df_temp1,'production',energy_catg)
            st.pyplot(fig)
    st.write("Data Source: https://data.open-power-system-data.org/renewable_power_plants/2020-08-25")
#------------------------------------------------------------------------------------------------------------------------------------------------
