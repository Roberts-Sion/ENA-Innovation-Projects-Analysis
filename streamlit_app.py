import streamlit as st
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

st.title("Analysis of Ofgem Innovation Projects")
st.write("This analysis provides insight into previous and current Innovation Projects funded by Ofgem.\
         Data regarding these projects, accessed using Energy Networks Association's Smarter Networks Portal,\
         is accessible through a series of different visual and graphical means, and adjustable to the users demand.\
         Information regarding the analyses conducted and methods used can be found with each plot.")

#Import the datafile
data = pd.read_excel('snp_dataset_useful.xlsx')
#Extract the required data from the datafile
#Time
start_date = data['Project Start Date']
end_date = data['Project End Date']
status = data['Project Status']
#Funding & Association
budget = data['Project Budget']
owners = data['Owner Network']
collaborators = data['Collaborating Networks']
funding_mechanism = data['Funding Mechanism']
#Area of research
titles = data['Project Title']
strategy = data['Strategy Theme']
research = data['Research Areas']
technology = data['Technology Areas']
sector = data['Lead Sector']
secondary_sectors = data['Other Related Sectors']

#Determine the time difference between the start and end dates
start_dt = pd.to_datetime(start_date, format="%d/%m/%Y", errors='coerce')
end_dt = pd.to_datetime(end_date, format="%d/%m/%Y", errors='coerce')
time_difference = end_dt - start_dt
durations = time_difference.dt.days

#For the projects involved in multiple sectors, make sure they are included in each sector list
sector_types = sector.unique()
sector_types = sector_types[:4]
sector_types_idx = [sector[sector.str.contains(st, na=False)].index.tolist() for st in sector_types]

#Do the same for owners as well
owner_types = owners.unique()
owner_types = [ot for ot in owner_types if pd.notna(ot)]
owner_types_idx = [owners[owners.str.contains(ot, na=False)].index.tolist() for ot in owner_types]

#Do the same for technology as well
technology_types = ['Active Network Management','Asset Management', 'Biomethane', 'Carbon Emission Reduction Technologies', 'Commercial', 'Comms and IT',\
                    'Community Schemes', 'Condition Monitoring', 'Conductors', 'Control Systems', 'Cyber Security', 'Demand Response', 'Demand Side Management',\
                    'Digital Network', 'Distributed Generation', 'Electric Vehicles', 'Electricity Transmission Networks', 'Energy Storage', 'Energy Storage and Demand Response',\
                    'Environmental', 'Fault Current', 'Fault Level', 'Fault Management', 'Gas Distribution Networks', 'Gas Transmission Networks', 'Gas Vehicles',\
                    'Green Gas', 'HVDC', 'Harmonics', 'Health and Safety', 'Heat Pumps', 'High Voltage Technology', 'Hydrogen', 'LV & 11kV Networks', 'Low Carbon Generation',\
                    'Maintenance & Inspections', 'Measurement', 'Meshed Networks', 'Modelling', 'Network Automation', 'Network Monitoring', 'Offshore Transmission',\
                    'Overhead Lines', 'Photovoltaics', 'Poverty', 'Pre-Heat', 'Protection', 'Resilience', 'Stakeholder Engagement', 'Storage', 'Substation Monitoring',\
                    'Substations', 'System Security', 'Transformers', 'Voltage Control']
technology_types = [tt for tt in technology_types if pd.notna(tt)]
technology_types_idx = [technology[technology.str.contains(tt, na=False)].index.tolist() for tt in technology_types]

st.subheader("Plot of Total Project Budgets vs Sector (use as test)")
st.write("(Description of plot to be included here)")
total_sector_budget = np.zeros(len(sector_types))
for i in range(len(sector_types)):
  for j in range(len(sector_types_idx[i])):
    total_sector_budget[i] += budget[sector_types_idx[i][j]]
bts_total_sector_budget_idx = np.argsort(total_sector_budget)[::-1]
bts_total_sector_budget = total_sector_budget[bts_total_sector_budget_idx]
bts_sector_types = np.array(sector_types)[bts_total_sector_budget_idx]
fig = px.bar(x=bts_sector_types, y=bts_total_sector_budget, labels={'x':'Sector', 'y':'Total Funding (£)'})
st.write(fig)
sector_names = ["Electricity Distribution", "Electricity Transmission", "Gas Distribution", "Gas Transmission"]
sector_indices = {"Electricity Distribution": sector_types_idx[0], "Electricity Transmission": sector_types_idx[1],\
                  "Gas Distribution": sector_types_idx[2], "Gas Transmission": sector_types_idx[3]}
tables = {}
for sect in sector_names:
  indices = sector_indices[sect]
  tables[sect] = pd.DataFrame({"Project Title": titles.iloc[indices].values,\
                                 "Technology Areas": technology.iloc[indices].values,\
                                 "Project Budget": budget.iloc[indices].values,\
                                 "Funding Mechanism": funding_mechanism.iloc[indices].values})
if "selected_sector" not in st.session_state:
  st.session_state.selected_sector = None
for sect in sector_names:
  if st.button(f"Show Table ({sect})", key=f"button_{sect}"):
    st.session_state.selected_sector = sect
if st.session_state.selected_sector is not None:
  selected_sector = st.session_state.selected_sector
  st.subheader(selected_sector)
  st.dataframe(tables[selected_sector], use_container_width=True, hide_index=True)
  if st.button("Hide Table", key="hide_table"):
    st.session_state.selected_sector = None
    st.rerun()

st.subheader("Plot of Count vs Technology Area (for each sector - use as test)")
st.write("(Description of plot to be included here)")
#Create plots that display the technologies funded in each sector
tech_4_sect = []
for i in range(len(sector_types)):
  filtered_tech = technology[sector_types_idx[i]].dropna()
  filtered_tech = filtered_tech.str.split(', ').explode().str.strip()
  tech_4_sect.append(filtered_tech)

tech_4_sect_type = []
for i in range(len(sector_types)):
  counts = tech_4_sect[i].value_counts()
  counts = counts.reindex(technology_types, fill_value=0)
  tech_4_sect_type.append(counts)

bts_tech_4_sect_type = []
bts_technology_types = []
for i in range(len(sector_types)):
  counts = tech_4_sect_type[i].sort_values(ascending=False)
  non_zero_counts = counts[counts > 0]
  bts_technology_types.append(non_zero_counts.index)
  bts_tech_4_sect_type.append(non_zero_counts)

fig1 = make_subplots(rows=len(sector_types), cols=1, subplot_titles=sector_types)
for i in range(len(sector_types)):
  fig1.add_trace(go.Bar(x=bts_technology_types[i], y=bts_tech_4_sect_type[i].values), row=i+1, col=1)
fig1.update_layout(height=1000, width=1350, showlegend=False)
fig1.update_xaxes(tickmode='linear', tickangle=30, tickfont=dict(size=8))
st.write(fig1)

st.subheader("Plot of Total Project Budgets vs Owner (use as test)")
st.write("(Description of plot to be included here)")
total_owner_budget = np.zeros(len(owner_types))
for i in range(len(owner_types)):
  for j in range(len(owner_types_idx[i])):
    total_owner_budget[i] += budget[owner_types_idx[i][j]]
bts_total_owner_budget_idx = np.argsort(total_owner_budget)[::-1]
bts_total_owner_budget = total_owner_budget[bts_total_owner_budget_idx]
bts_owner_types = np.array(owner_types)[bts_total_owner_budget_idx]
fig2 = px.bar(x=bts_owner_types, y=bts_total_owner_budget, labels={'x':'Owner', 'y':'Total Funding (£)'})
st.write(fig2)

#Create a plot to see when each technology has been invested in
tech_4_owner = []
tech_4_owner_start_dt = []
for i in range(len(owner_types)):
  current_owner_idx = owner_types_idx[i]
  current_owner_tech = technology[current_owner_idx].dropna()
  current_owner_tech = current_owner_tech.str.split(', ').explode().str.strip()
  current_owner_tech = current_owner_tech[current_owner_tech.isin(technology_types)]
  current_owner_start_dt = start_dt.loc[current_owner_tech.index]
  tech_4_owner.append(current_owner_tech)
  tech_4_owner_start_dt.append(current_owner_start_dt)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=tech_4_owner_start_dt[0], y=tech_4_owner[0], mode='markers', name=f'{owner_types[0]}'))
for i in range(len(owner_types)-1):
  fig3.add_trace(go.Scatter(x=tech_4_owner_start_dt[i+1], y=tech_4_owner[i+1], mode='markers', name=f'{owner_types[i+1]}', visible=False))

buttons = []
buttons.append(dict(label=f'{owner_types[0]}', method='update', args=[{'visible': [True] + [False]*(len(owner_types) - 1)}, {'title': f'Technology Area funded by date ({owner_types[0]})'}]))
for i in range(1, len(owner_types)):
  visible = [False] * (len(owner_types))
  visible[i] = True
  buttons.append(dict(label=f'{owner_types[i]}', method='update', args=[{'visible': visible}, {'title': f'Technology Area funded by date ({owner_types[i]})'}]))

technology_order = technology_types
fig3.update_layout(updatemenus=[dict(buttons=buttons, direction='down', showactive=True, x=0, xanchor='left', y=1.12, yanchor='top')],\
                  xaxis_title='Date (DD-MM-YY)', yaxis_title='Technology Area', title=f'Technology Area funded by date ({owner_types[0]})', hovermode='x unified',\
                  yaxis=dict(categoryorder='array', categoryarray=technology_order))
st.write(fig3)

st.subheader("Plot of Total Project Budgets vs Technology (use as test)")
st.write("(Description of plot to be included here)")
#Plot of total project budgets vs technology
total_technology_budget = np.zeros(len(technology_types))
for i in range(len(technology_types)):
  for j in range(len(technology_types_idx[i])):
    total_technology_budget[i] += budget[technology_types_idx[i][j]]
bts_total_technology_budget_idx = np.argsort(total_technology_budget)[::-1]
bts_total_technology_budget = total_technology_budget[bts_total_technology_budget_idx]
bts_technology_types = np.array(technology_types)[bts_total_technology_budget_idx]

fig4 = px.bar(x=bts_technology_types, y=bts_total_technology_budget, labels={'x':'Technology', 'y':'Total Funding (£)'})
fig4.update_layout(width=1500, height=600)
fig4.update_xaxes(tickmode='linear', tickangle=30, tickfont=dict(size=8))
st.write(fig4)

st.subheader('(Other test plot)')
st.write("(Description of plot to be included here)")
start_dt_sort = np.sort(start_dt)
total_cumul = [np.sum(start_dt_sort <= date) for date in start_dt_sort]
end = 0
while end == 0:
  remove = total_cumul.pop()
  end = remove
  if end == 0:
    continue
  else:  
    total_cumul.append(remove)
sector_cumul = {}
for sc in sector_types:
  sector_idx = sector[sector.str.contains(sc, na=False)].index
  sector_dates = start_dt.loc[sector_idx]
  sector_cumul[sc] = [np.sum(sector_dates.values <= date) for date in start_dt_sort]
  end = 0
  while end == 0:
    remove = sector_cumul[sc].pop()
    end = remove
    if end == 0:
      continue
    else:  
      sector_cumul[sc].append(remove)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=start_dt_sort, y=total_cumul, mode='lines+markers', name='Total'))
for sc in sector_types:
  fig5.add_trace(go.Scatter(x=start_dt_sort, y=sector_cumul[sc], mode='lines+markers', name=sc, visible=False))

buttons = []
buttons.append(dict(label='Total', method='update', args=[{'visible': [True] + [False]*len(sector_types)}, {'title': 'Cumulative Number of All Projects'}]))
for i, sc in enumerate(sector_types):
  visible = [False] * (len(sector_types) + 1)
  visible[i+1] = True
  buttons.append(dict(label=sc, method='update', args=[{'visible': visible}, {'title': f'Cumulative Number of {sc} Projects'}]))

fig5.update_layout(updatemenus=[dict(buttons=buttons, direction='down', showactive=True, x=0, xanchor='left', y=1.12, yanchor='top')],\
                  xaxis_title='Date (DD-MM-YY)', yaxis_title='Number of Projects', title='Cumulative Number of Projects', hovermode='x unified')
st.plotly_chart(fig5, use_container_width=True)

st.write("Last updated 15:02, 01/10/2026")